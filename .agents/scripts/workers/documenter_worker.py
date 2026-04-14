#!/usr/bin/env python3
"""
documenter_worker.py — Worker do Documenter: documentação técnica e KB

Responsabilidades:
  - document: escrever ou atualizar documentação
  - update_kb: adicionar/atualizar entradas na KB
  - contract: escrever contratos e especificações
  - runbook: criar runbooks operacionais
  - adr: registrar decisões arquiteturais (Architecture Decision Records)
"""

import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from workers.base_worker import BaseWorker, EscalateToHuman
from acp.task_lifecycle import Task

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from opencode.opencode_executor import OpenCodeExecutor

log = logging.getLogger("workers.documenter")

WORKSPACE_WIN = "C:\\CindyAgent"
DOCS_PATH     = os.path.join(WORKSPACE_WIN, "docs")
KB_PATH       = os.path.join(WORKSPACE_WIN, "KB")


class DocumenterWorker(BaseWorker):
    """Especialista em documentação técnica e gestão da KB."""

    agent_id = "documenter"

    ALWAYS_ESCALATE = {"architectural_decision", "external_publication", "breaking_change_doc"}

    def handle(self, task: Task) -> dict:
        action = task.action.lower()

        if action in self.ALWAYS_ESCALATE:
            raise EscalateToHuman(f"'{action}' requer aprovação do PO antes de publicar")

        dispatch = {
            "document":   self._write_doc,
            "update_kb":  self._update_kb,
            "contract":   self._write_contract,
            "runbook":    self._write_runbook,
            "adr":        self._write_adr,
            "write":      self._write_doc,
        }

        handler = dispatch.get(action, self._generic_doc)
        return handler(task)

    # ─── Handlers ───────────────────────────────────────────────────

    def _write_doc(self, task: Task) -> dict:
        """Escreve ou atualiza um documento técnico."""
        topic       = task.payload.get("topic", "")
        output_file = task.payload.get("output_file", "")
        existing    = task.payload.get("existing_content", "")
        context     = task.context or ""

        instruction = (
            f"Write technical documentation about: {topic}\n"
            "Use Markdown. Follow DOC2.5 standards:\n"
            "- Clear headings hierarchy\n"
            "- Concrete examples\n"
            "- No vague statements\n"
            "- Include timestamp and status\n"
        )
        if existing:
            instruction += f"\nUpdate this existing document:\n{existing[:2000]}"
        if output_file:
            instruction += f"\nSave to: {output_file}"

        executor = OpenCodeExecutor(profile="docs-writer")
        result = executor.run(instruction=instruction, context=context)

        artifact = output_file or result.get("artifact_ref", "")
        return {
            "summary":      f"Documentação '{topic}' produzida em {artifact}",
            "artifact_ref": artifact,
            "needs_review": False,
        }

    def _update_kb(self, task: Task) -> dict:
        """Atualiza ou cria entrada na KB."""
        kb_file   = task.payload.get("kb_file", "")
        content   = task.payload.get("content", "")
        section   = task.payload.get("section", "")
        kb_domain = task.payload.get("domain", "aiops")  # aiops | hermes | meta

        target_dir = os.path.join(KB_PATH, kb_domain)
        os.makedirs(target_dir, exist_ok=True)

        if not kb_file:
            slug = section.lower().replace(" ", "_") if section else "entry"
            ts   = datetime.now(timezone.utc).strftime("%Y%m%d")
            kb_file = os.path.join(target_dir, f"{slug}_{ts}.md")

        instruction = (
            f"Write or update the KB entry for section '{section}':\n"
            f"{content}\n\n"
            f"Target: {kb_file}\n"
            "Format: Markdown, factual, concise, with status and date."
        )
        executor = OpenCodeExecutor(profile="docs-writer")
        result = executor.run(instruction=instruction, context=task.context or "")
        return {
            "summary":      f"KB atualizada: {kb_file}",
            "artifact_ref": kb_file,
            "needs_review": False,
        }

    def _write_contract(self, task: Task) -> dict:
        """Escreve contratos operacionais como agent_cards."""
        contract_type = task.payload.get("type", "agent_card")
        subject       = task.payload.get("subject", "")
        output_file   = task.payload.get("output_file", "")
        context       = task.context or ""

        instruction = (
            f"Write a formal operational contract of type '{contract_type}' for: {subject}\n"
            "Include: mission, domain, tools, limits, escalation policy, model strategy.\n"
            "Format: YAML with clear sections. Follow the agent_card schema."
        )
        if output_file:
            instruction += f"\nSave to: {output_file}"

        executor = OpenCodeExecutor(profile="docs-writer")
        result = executor.run(instruction=instruction, context=context)
        return {
            "summary":      f"Contrato '{contract_type}' para '{subject}' produzido",
            "artifact_ref": output_file or result.get("artifact_ref"),
            "needs_review": True,  # Contratos sempre vão para review
        }

    def _write_runbook(self, task: Task) -> dict:
        """Cria runbook operacional."""
        process   = task.payload.get("process", "")
        steps     = task.payload.get("steps", [])
        output    = task.payload.get("output_file", "")

        instruction = (
            f"Write an operational runbook for: {process}\n"
            "Include: trigger conditions, step-by-step procedure, "
            "verification steps, rollback plan, and owner.\n"
        )
        if steps:
            instruction += f"Known steps:\n" + "\n".join(f"- {s}" for s in steps)
        if output:
            instruction += f"\nSave to: {output}"

        executor = OpenCodeExecutor(profile="docs-writer")
        result = executor.run(instruction=instruction, context=task.context or "")
        return {
            "summary":      f"Runbook para '{process}' produzido",
            "artifact_ref": output or result.get("artifact_ref"),
            "needs_review": False,
        }

    def _write_adr(self, task: Task) -> dict:
        """Registra uma Architecture Decision Record."""
        title      = task.payload.get("title", "")
        context    = task.payload.get("context", "")
        decision   = task.payload.get("decision", "")
        rationale  = task.payload.get("rationale", "")

        adr_num = self._next_adr_number()
        output = os.path.join(DOCS_PATH, "adr", f"ADR-{adr_num:04d}-{title.lower().replace(' ', '-')}.md")
        os.makedirs(os.path.dirname(output), exist_ok=True)

        instruction = (
            f"Write an Architecture Decision Record (ADR):\n"
            f"Title: {title}\n"
            f"Context: {context}\n"
            f"Decision: {decision}\n"
            f"Rationale: {rationale}\n"
            f"Save to: {output}\n"
            "Use standard ADR format: Status, Context, Decision, Consequences."
        )
        executor = OpenCodeExecutor(profile="docs-writer")
        result = executor.run(instruction=instruction, context=self.mesh.dashboard().__str__())
        return {
            "summary":      f"ADR-{adr_num} '{title}' registado",
            "artifact_ref": output,
            "needs_review": True,  # ADRs sempre sobem para revisão
        }

    def _next_adr_number(self) -> int:
        adr_dir = Path(DOCS_PATH) / "adr"
        if not adr_dir.exists():
            return 1
        existing = list(adr_dir.glob("ADR-*.md"))
        return len(existing) + 1

    def _generic_doc(self, task: Task) -> dict:
        executor = OpenCodeExecutor(profile="docs-writer")
        result = executor.run(
            instruction = str(task.payload.get("description", task.action)),
            context     = task.context or "",
        )
        return {
            "summary":      result.get("summary", f"Documento '{task.action}' produzido"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": False,
        }


if __name__ == "__main__":
    import sys
    worker = DocumenterWorker()
    if "--once" in sys.argv:
        n = worker.run_once()
        print(f"[documenter] Processadas {n} tarefa(s)")
    else:
        worker.run()
