#!/usr/bin/env python3
"""
cindy_worker.py — Worker da Cindy: coordenação, triagem e roteamento

Responsabilidades:
  - Recebe tarefas indiferenciadas do PO via Telegram/Hermes
  - Tria e roteia para o especialista correto via capability registry
  - Consolida resultados e escala ao PO quando necessário
  - Gerencia po_gate (escalações)
"""

import logging
from workers.base_worker import BaseWorker, EscalateToHuman
from acp.task_lifecycle import Task

log = logging.getLogger("workers.cindy")


class CindyWorker(BaseWorker):
    """Orquestradora do time AIOps."""

    agent_id = "cindy"

    # Ações que a Cindy processa diretamente (sem rotear)
    LOCAL_ACTIONS = {"status", "dashboard", "po_gate", "coordinate", "sprint"}

    def handle(self, task: Task) -> dict:
        if task.action in self.LOCAL_ACTIONS:
            return self._handle_local(task)
        return self._route_to_specialist(task)

    # ─── Handlers locais ────────────────────────────────────────────

    def _handle_local(self, task: Task) -> dict:
        if task.action == "status":
            return self._get_status()
        if task.action == "dashboard":
            return self._get_dashboard()
        if task.action == "po_gate":
            return self._handle_escalation(task)
        if task.action == "sprint":
            return self._handle_sprint(task)
        return {"summary": f"Ação local '{task.action}' processada pela Cindy"}

    def _get_status(self) -> dict:
        dash = self.mesh.dashboard()
        summary = (
            f"Status do time AIOps:\n"
            f"  Agentes: {', '.join(dash['agents'])}\n"
            f"  Tarefas: queued={dash['queued']} running={dash['running']} "
            f"blocked={dash['blocked']} done={dash['done']} failed={dash['failed']} "
            f"escalated={dash['escalated']}"
        )
        return {"summary": summary, "artifact_ref": None}

    def _get_dashboard(self) -> dict:
        dash = self.mesh.dashboard()
        return {"summary": str(dash), "artifact_ref": None}

    def _handle_escalation(self, task: Task) -> dict:
        """Recebe escalação de outros agentes e notifica o PO."""
        payload = task.payload
        original_task_id = payload.get("original_task_id", "N/A")
        reason           = payload.get("reason", "Sem motivo especificado")
        log.warning("[CINDY] ESCALAÇÃO recebida — task_id=%s reason=%s", original_task_id, reason)
        # Em produção: envia mensagem ao PO via Telegram/Hermes
        return {
            "summary":      f"ESCALAÇÃO encaminhada ao PO: task={original_task_id} — {reason}",
            "artifact_ref": None,
        }

    def _handle_sprint(self, task: Task) -> dict:
        """Tarefas de sprint sempre sobem ao PO."""
        raise EscalateToHuman(
            f"Sprint management requer aprovação do PO: {task.payload.get('description', task.action)}"
        )

    # ─── Roteamento ─────────────────────────────────────────────────

    def _route_to_specialist(self, task: Task) -> dict:
        """Roteia tarefa ao agente mais adequado pelo capability registry."""
        candidates = self.mesh.registry.route(task.action)

        if not candidates:
            log.warning("[CINDY] Nenhum especialista encontrado para action=%s", task.action)
            raise EscalateToHuman(
                f"Não encontrei um especialista para '{task.action}'. Preciso da orientação do PO."
            )

        target = candidates[0]
        log.info("[CINDY] Roteando action=%s para agent=%s", task.action, target.agent)

        new_task = self.mesh.handoff(
            task_id          = task.task_id,
            from_agent       = self.agent_id,
            to_agent         = target.agent,
            action           = task.action,
            payload          = task.payload,
            context          = task.context,
            artifact_ref     = task.artifact_ref,
            expected_response= task.expected_response,
        )

        return {
            "summary":      f"Tarefa roteada para {target.agent} (task_id={new_task.task_id})",
            "artifact_ref": None,
        }


if __name__ == "__main__":
    import sys
    worker = CindyWorker()
    if "--once" in sys.argv:
        n = worker.run_once()
        print(f"[cindy] Processadas {n} tarefa(s)")
    else:
        worker.run()
