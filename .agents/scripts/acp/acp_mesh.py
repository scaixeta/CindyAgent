#!/usr/bin/env python3
"""
acp_mesh.py — ACP Mesh governado (evolução do acp_redis.py)

Protocolo completo com:
  - task lifecycle formal
  - capability registry
  - handoffs rastreáveis (trace_id)
  - logging estruturado de tarefas
  - retry e dead-letter

Uso:
    from acp.acp_mesh import ACPMesh
    mesh = ACPMesh()
    task = mesh.send_task("builder", "implement", {"spec": "..."}, from_agent="cindy")
"""

import json
import uuid
import logging
from datetime import datetime, timezone
from typing import Optional, Callable
import redis

from acp.task_lifecycle import Task, TaskState, TaskStore
from acp.capability_registry import CapabilityRegistry

log = logging.getLogger("acp.mesh")


class ACPMesh:
    """
    Mesh governado de comunicação entre agentes.

    Namespaces Redis:
      acp:task:<id>               — task store
      acp:log:<id>                — task event log
      acp:stream:<agent>          — stream de tarefas por agente
      acp:registry:<agent>        — agent card
      acp:dlq:<agent>             — dead-letter queue
      acp:handoff:<trace_id>      — histórico de handoffs do trace
    """

    STREAM_PREFIX  = "acp:stream"
    DLQ_PREFIX     = "acp:dlq"
    HANDOFF_PREFIX = "acp:handoff"
    MAX_RETRIES    = 3

    def __init__(self, host: str = "localhost", port: int = 6379):
        self._r        = redis.Redis(host=host, port=port, decode_responses=True)
        self.store     = TaskStore(host, port)
        self.registry  = CapabilityRegistry(host, port)

    # ─── Envio de tarefa ────────────────────────────────────────────

    def send_task(
        self,
        to_agent:       str,
        action:         str,
        payload:        dict,
        from_agent:     str,
        trace_id:       Optional[str] = None,
        context:        Optional[str] = None,
        deadline:       Optional[str] = None,
        artifact_ref:   Optional[str] = None,
        expected_response: Optional[str] = None,
    ) -> Task:
        """
        Cria uma tarefa, persiste no store e publica no stream do agente destino.
        Retorna a Task criada com task_id e trace_id gerados.
        """
        task = Task(
            action           = action,
            payload          = payload,
            from_agent       = from_agent,
            to_agent         = to_agent,
            trace_id         = trace_id,
            context          = context,
            deadline         = deadline,
            artifact_ref     = artifact_ref,
            expected_response= expected_response,
        )
        self.store.save(task)
        self._publish_to_stream(to_agent, task)
        self._record_handoff(task)
        self.store.log_event(task.task_id, task.trace_id, "task_sent", from_agent,
                             f"action={action} to={to_agent}")
        log.info("[MESH] task_sent task_id=%s trace_id=%s action=%s from=%s to=%s",
                 task.task_id, task.trace_id, action, from_agent, to_agent)
        return task

    def route_task(
        self,
        action:     str,
        payload:    dict,
        from_agent: str,
        context:    Optional[str] = None,
    ) -> Optional[Task]:
        """
        Roteia tarefa automaticamente pelo capability registry.
        Usa o agente mais especializado disponível.
        """
        candidates = self.registry.route(action)
        if not candidates:
            log.warning("[MESH] Nenhum agente encontrado para action=%s", action)
            return None
        best = candidates[0]
        log.info("[MESH] Roteando action=%s para agent=%s (score primeiro)", action, best.agent)
        return self.send_task(
            to_agent   = best.agent,
            action     = action,
            payload    = payload,
            from_agent = from_agent,
            context    = context,
        )

    # ─── Consumo de tarefas ─────────────────────────────────────────

    def consume(
        self,
        agent_id:  str,
        group:     Optional[str] = None,
        count:     int = 10,
    ) -> list[Task]:
        """
        Consome tarefas do stream do agente e transiciona para CLAIMED.
        """
        group = group or f"workers:{agent_id}"
        stream_key = f"{self.STREAM_PREFIX}:{agent_id}"
        consumer   = f"{agent_id}-worker"

        try:
            self._r.xgroup_create(stream_key, group, id="0", mkstream=True)
        except redis.ResponseError:
            pass

        entries = self._r.xreadgroup(group, consumer, {stream_key: ">"}, count=count)
        tasks = []
        for _, msgs in (entries or []):
            for entry_id, fields in msgs:
                task_id = fields.get("task_id")
                task = self.store.get(task_id) if task_id else None
                if task:
                    try:
                        self.store.transition(task_id, TaskState.CLAIMED, agent_id, "consumed from stream")
                        self.store.log_event(task_id, task.trace_id, "task_claimed", agent_id)
                        tasks.append(task)
                    except ValueError as e:
                        log.warning("[MESH] Transição inválida para task %s: %s", task_id, e)
                self._r.xack(stream_key, group, entry_id)
        return tasks

    # ─── Ciclo de vida via mesh ─────────────────────────────────────

    def start(self, task_id: str, agent: str) -> Task:
        task = self.store.transition(task_id, TaskState.RUNNING, agent, "worker started")
        self.store.log_event(task_id, task.trace_id, "task_running", agent)
        log.info("[MESH] task_running task_id=%s agent=%s", task_id, agent)
        return task

    def complete(self, task_id: str, agent: str, artifact_ref: Optional[str] = None, result_summary: str = "") -> Task:
        task = self.store.get(task_id)
        if artifact_ref:
            task.artifact_ref = artifact_ref
            self.store.save(task)
        task = self.store.transition(task_id, TaskState.DONE, agent, result_summary or "completed")
        self.store.log_event(task_id, task.trace_id, "task_done", agent,
                             f"artifact={artifact_ref} result={result_summary}")
        log.info("[MESH] task_done task_id=%s agent=%s artifact=%s", task_id, agent, artifact_ref)
        return task

    def fail(self, task_id: str, agent: str, reason: str, retry: bool = True) -> Task:
        task = self.store.get(task_id)
        retries = sum(1 for h in task.history if h.get("to") == "failed")
        if retry and retries < self.MAX_RETRIES:
            # Requeue
            task = self.store.transition(task_id, TaskState.FAILED, agent, reason)
            self.store.transition(task_id, TaskState.QUEUED, "system", f"retry #{retries+1}")
            self._publish_to_stream(task.to_agent, task)
            self.store.log_event(task_id, task.trace_id, "task_retry", agent,
                                 f"reason={reason} attempt={retries+1}")
            log.warning("[MESH] task_retry task_id=%s attempt=%d reason=%s", task_id, retries+1, reason)
        else:
            task = self.store.transition(task_id, TaskState.FAILED, agent, reason)
            self._send_to_dlq(task, reason)
            self.store.log_event(task_id, task.trace_id, "task_failed_final", agent,
                                 f"reason={reason} sent_to_dlq=true")
            log.error("[MESH] task_failed_final task_id=%s agent=%s reason=%s", task_id, agent, reason)
        return task

    def block(self, task_id: str, agent: str, reason: str) -> Task:
        task = self.store.transition(task_id, TaskState.BLOCKED, agent, reason)
        self.store.log_event(task_id, task.trace_id, "task_blocked", agent, reason)
        log.warning("[MESH] task_blocked task_id=%s agent=%s reason=%s", task_id, agent, reason)
        return task

    def escalate(self, task_id: str, agent: str, reason: str) -> Task:
        task = self.store.transition(task_id, TaskState.ESCALATED, agent, reason)
        self.store.log_event(task_id, task.trace_id, "task_escalated", agent, reason)
        # Notifica Cindy via stream
        escalation_task = Task(
            action     = "po_gate",
            payload    = {"original_task_id": task_id, "reason": reason},
            from_agent = agent,
            to_agent   = "cindy",
            trace_id   = task.trace_id,
            context    = f"ESCALATION from {agent}: {reason}",
        )
        self.store.save(escalation_task)
        self._publish_to_stream("cindy", escalation_task)
        log.warning("[MESH] task_escalated task_id=%s agent=%s reason=%s", task_id, agent, reason)
        return task

    def request_review(self, task_id: str, agent: str, artifact_ref: str) -> Task:
        task = self.store.get(task_id)
        task.artifact_ref = artifact_ref
        self.store.save(task)
        task = self.store.transition(task_id, TaskState.REVIEW, agent, f"artifact={artifact_ref}")
        # Notifica reviewer via stream
        review_task = Task(
            action     = "review",
            payload    = {"original_task_id": task_id, "artifact_ref": artifact_ref},
            from_agent = agent,
            to_agent   = "reviewer",
            trace_id   = task.trace_id,
        )
        self.store.save(review_task)
        self._publish_to_stream("reviewer", review_task)
        self.store.log_event(task_id, task.trace_id, "review_requested", agent, f"artifact={artifact_ref}")
        return task

    # ─── Handoff ────────────────────────────────────────────────────

    def handoff(
        self,
        task_id:          str,
        from_agent:       str,
        to_agent:         str,
        action:           str,
        payload:          dict,
        context:          Optional[str] = None,
        artifact_ref:     Optional[str] = None,
        expected_response: Optional[str] = None,
    ) -> Task:
        """Passagem formal de tarefa entre agentes, preservando trace_id."""
        original = self.store.get(task_id)
        if not original:
            raise KeyError(f"Task original não encontrada: {task_id}")
        new_task = self.send_task(
            to_agent          = to_agent,
            action            = action,
            payload           = payload,
            from_agent        = from_agent,
            trace_id          = original.trace_id,
            context           = context,
            artifact_ref      = artifact_ref,
            expected_response = expected_response,
        )
        self.store.log_event(task_id, original.trace_id, "handoff_sent", from_agent,
                             f"to={to_agent} new_task={new_task.task_id}")
        return new_task

    # ─── Internos ───────────────────────────────────────────────────

    def _publish_to_stream(self, agent_id: str, task: Task) -> str:
        stream_key = f"{self.STREAM_PREFIX}:{agent_id}"
        entry = {
            "task_id":   task.task_id,
            "trace_id":  task.trace_id,
            "action":    task.action,
            "from":      task.from_agent,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        return self._r.xadd(stream_key, entry, maxlen=5000)

    def _record_handoff(self, task: Task) -> None:
        key = f"{self.HANDOFF_PREFIX}:{task.trace_id}"
        entry = json.dumps({
            "task_id":   task.task_id,
            "action":    task.action,
            "from":      task.from_agent,
            "to":        task.to_agent,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._r.rpush(key, entry)
        self._r.expire(key, 86400 * 7)

    def _send_to_dlq(self, task: Task, reason: str) -> None:
        key = f"{self.DLQ_PREFIX}:{task.to_agent}"
        entry = json.dumps({**task.to_dict(), "dlq_reason": reason,
                            "dlq_at": datetime.now(timezone.utc).isoformat()})
        self._r.rpush(key, entry)

    # ─── Observabilidade ─────────────────────────────────────────────

    def get_trace(self, trace_id: str) -> list[dict]:
        """Retorna o histórico completo de handoffs de um trace."""
        key = f"{self.HANDOFF_PREFIX}:{trace_id}"
        return [json.loads(e) for e in self._r.lrange(key, 0, -1)]

    def get_task_log(self, task_id: str) -> list[dict]:
        return self.store.get_log(task_id)

    def dashboard(self) -> dict:
        """Snapshot de saúde do mesh."""
        return {
            "agents":       self.registry.all_agents(),
            "queued":       len(self.store.list_by_state(TaskState.QUEUED)),
            "running":      len(self.store.list_by_state(TaskState.RUNNING)),
            "blocked":      len(self.store.list_by_state(TaskState.BLOCKED)),
            "review":       len(self.store.list_by_state(TaskState.REVIEW)),
            "done":         len(self.store.list_by_state(TaskState.DONE)),
            "failed":       len(self.store.list_by_state(TaskState.FAILED)),
            "escalated":    len(self.store.list_by_state(TaskState.ESCALATED)),
            "timestamp":    datetime.now(timezone.utc).isoformat(),
        }
