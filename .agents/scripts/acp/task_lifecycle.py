#!/usr/bin/env python3
"""
task_lifecycle.py — Ciclo de vida formal de tarefas no ACP mesh

Estados:
  queued -> claimed -> running -> review -> done
                               -> blocked
                               -> failed
                               -> escalated

Uso:
    from acp.task_lifecycle import Task, TaskState, TaskStore
"""

import uuid
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
import redis


class TaskState(str, Enum):
    QUEUED    = "queued"
    CLAIMED   = "claimed"
    RUNNING   = "running"
    BLOCKED   = "blocked"
    REVIEW    = "review"
    DONE      = "done"
    FAILED    = "failed"
    ESCALATED = "escalated"


# Transições válidas por estado
VALID_TRANSITIONS: dict[TaskState, list[TaskState]] = {
    TaskState.QUEUED:    [TaskState.CLAIMED, TaskState.ESCALATED],
    TaskState.CLAIMED:   [TaskState.RUNNING, TaskState.FAILED],
    TaskState.RUNNING:   [TaskState.REVIEW, TaskState.BLOCKED, TaskState.DONE, TaskState.FAILED, TaskState.ESCALATED],
    TaskState.BLOCKED:   [TaskState.RUNNING, TaskState.FAILED, TaskState.ESCALATED],
    TaskState.REVIEW:    [TaskState.DONE, TaskState.RUNNING, TaskState.FAILED],
    TaskState.DONE:      [],
    TaskState.FAILED:    [TaskState.QUEUED],     # retry permitido
    TaskState.ESCALATED: [TaskState.QUEUED, TaskState.DONE],
}


class Task:
    """Representa uma tarefa no mesh ACP."""

    def __init__(
        self,
        action: str,
        payload: dict,
        from_agent: str,
        to_agent: str,
        task_id: Optional[str] = None,
        trace_id: Optional[str] = None,
        deadline: Optional[str] = None,
        artifact_ref: Optional[str] = None,
        context: Optional[str] = None,
        expected_response: Optional[str] = None,
        escalation_reason: Optional[str] = None,
    ):
        self.task_id       = task_id or str(uuid.uuid4())
        self.trace_id      = trace_id or str(uuid.uuid4())
        self.action        = action
        self.payload       = payload
        self.from_agent    = from_agent
        self.to_agent      = to_agent
        self.state         = TaskState.QUEUED
        self.deadline      = deadline
        self.artifact_ref  = artifact_ref
        self.context       = context
        self.expected_response = expected_response
        self.escalation_reason = escalation_reason
        self.created_at    = datetime.now(timezone.utc).isoformat()
        self.updated_at    = self.created_at
        self.history: list[dict] = []
        self._record_transition(None, TaskState.QUEUED, "system", "task created")

    def transition(self, new_state: TaskState, agent: str, reason: str = "") -> None:
        """Realiza transição de estado com validação."""
        if new_state not in VALID_TRANSITIONS.get(self.state, []):
            raise ValueError(
                f"Transição inválida: {self.state} -> {new_state} "
                f"(permitidas: {[s.value for s in VALID_TRANSITIONS.get(self.state, [])]})"
            )
        old_state = self.state
        self.state = new_state
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self._record_transition(old_state, new_state, agent, reason)

    def _record_transition(self, from_state: Optional[TaskState], to_state: TaskState, agent: str, reason: str):
        self.history.append({
            "from":      from_state.value if from_state else None,
            "to":        to_state.value,
            "agent":     agent,
            "reason":    reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def to_dict(self) -> dict:
        return {
            "task_id":           self.task_id,
            "trace_id":          self.trace_id,
            "action":            self.action,
            "payload":           self.payload,
            "from_agent":        self.from_agent,
            "to_agent":          self.to_agent,
            "state":             self.state.value,
            "deadline":          self.deadline,
            "artifact_ref":      self.artifact_ref,
            "context":           self.context,
            "expected_response": self.expected_response,
            "escalation_reason": self.escalation_reason,
            "created_at":        self.created_at,
            "updated_at":        self.updated_at,
            "history":           self.history,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        t = cls(
            action           = data["action"],
            payload          = data["payload"],
            from_agent       = data["from_agent"],
            to_agent         = data["to_agent"],
            task_id          = data["task_id"],
            trace_id         = data["trace_id"],
            deadline         = data.get("deadline"),
            artifact_ref     = data.get("artifact_ref"),
            context          = data.get("context"),
            expected_response= data.get("expected_response"),
            escalation_reason= data.get("escalation_reason"),
        )
        t.state      = TaskState(data["state"])
        t.created_at = data["created_at"]
        t.updated_at = data["updated_at"]
        t.history    = data.get("history", [])
        return t

    def __repr__(self):
        return f"<Task {self.task_id[:8]} action={self.action} state={self.state.value} agent={self.to_agent}>"


class TaskStore:
    """Persiste e recupera tarefas no Redis."""

    KEY_PREFIX = "acp:task"
    LOG_PREFIX = "acp:log"

    def __init__(self, host: str = "localhost", port: int = 6379):
        self._r = redis.Redis(host=host, port=port, decode_responses=True)

    def save(self, task: Task) -> None:
        key = f"{self.KEY_PREFIX}:{task.task_id}"
        self._r.set(key, json.dumps(task.to_dict()), ex=86400 * 7)  # TTL: 7 dias
        # Índice por estado
        self._r.sadd(f"{self.KEY_PREFIX}:state:{task.state.value}", task.task_id)

    def get(self, task_id: str) -> Optional[Task]:
        key = f"{self.KEY_PREFIX}:{task_id}"
        raw = self._r.get(key)
        if not raw:
            return None
        return Task.from_dict(json.loads(raw))

    def transition(self, task_id: str, new_state: TaskState, agent: str, reason: str = "") -> Task:
        """Carrega, transiciona e salva a tarefa atomicamente."""
        task = self.get(task_id)
        if not task:
            raise KeyError(f"Task não encontrada: {task_id}")
        old_state = task.state
        task.transition(new_state, agent, reason)
        # Atualiza índice de estados
        self._r.srem(f"{self.KEY_PREFIX}:state:{old_state.value}", task_id)
        self._r.sadd(f"{self.KEY_PREFIX}:state:{new_state.value}", task_id)
        self.save(task)
        return task

    def list_by_state(self, state: TaskState) -> list[Task]:
        ids = self._r.smembers(f"{self.KEY_PREFIX}:state:{state.value}")
        return [t for tid in ids if (t := self.get(tid)) is not None]

    def log_event(self, task_id: str, trace_id: str, event: str, agent: str, detail: str = "") -> None:
        """Grava evento de auditoria no log do trace."""
        entry = json.dumps({
            "task_id":   task_id,
            "trace_id":  trace_id,
            "event":     event,
            "agent":     agent,
            "detail":    detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self._r.rpush(f"{self.LOG_PREFIX}:{task_id}", entry)
        self._r.expire(f"{self.LOG_PREFIX}:{task_id}", 86400 * 7)

    def get_log(self, task_id: str) -> list[dict]:
        entries = self._r.lrange(f"{self.LOG_PREFIX}:{task_id}", 0, -1)
        return [json.loads(e) for e in entries]
