#!/usr/bin/env python3
"""
builder_worker.py — Worker do Builder: execução técnica via OpenCode

Responsabilidades:
  - implement: escrever ou completar código
  - fix: corrigir bugs
  - refactor: refatorar com segurança
  - automate: criar scripts e automações
  - build: pipelines, builds, CI
"""

import logging
import subprocess
import os
import sys
from workers.base_worker import BaseWorker, EscalateToHuman, BlockedByDependency
from acp.task_lifecycle import Task

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from opencode.opencode_executor import OpenCodeExecutor

log = logging.getLogger("workers.builder")


class BuilderWorker(BaseWorker):
    """Especialista em engenharia e execução técnica."""

    agent_id = "builder"

    # Ações que requerem aprovação do PO antes de executar
    ALWAYS_ESCALATE = {"deploy_production", "architecture", "breaking_change", "security_patch"}

    def handle(self, task: Task) -> dict:
        action = task.action.lower()

        if action in self.ALWAYS_ESCALATE:
            raise EscalateToHuman(f"Ação '{action}' requer aprovação do PO antes de executar")

        dispatch = {
            "implement": self._implement,
            "fix":       self._fix,
            "refactor":  self._refactor,
            "automate":  self._automate,
            "build":     self._build,
            "code":      self._implement,
        }

        handler = dispatch.get(action, self._generic)
        return handler(task)

    # ─── Handlers por ação ──────────────────────────────────────────

    def _implement(self, task: Task) -> dict:
        """Implementa uma feature ou função via OpenCode coder."""
        spec  = task.payload.get("spec", task.payload.get("description", ""))
        files = task.payload.get("files", [])
        context = task.context or ""

        executor = OpenCodeExecutor(profile="coder")
        result = executor.run(
            instruction = spec,
            context     = context,
            files       = files,
        )
        return {
            "summary":      result.get("summary", "Implementação concluída"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": True,  # Toda implementação vai para review
        }

    def _fix(self, task: Task) -> dict:
        """Corrige um bug."""
        bug_description = task.payload.get("description", "")
        file_path       = task.payload.get("file")
        line            = task.payload.get("line")
        context         = task.context or ""

        instruction = f"Fix the following bug: {bug_description}"
        if file_path:
            instruction += f"\nFile: {file_path}"
        if line:
            instruction += f"\nLine: {line}"

        executor = OpenCodeExecutor(profile="coder")
        result = executor.run(instruction=instruction, context=context)
        return {
            "summary":      result.get("summary", f"Bug corrigido: {bug_description[:80]}"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": True,
        }

    def _refactor(self, task: Task) -> dict:
        """Refatora código com segurança."""
        target   = task.payload.get("target", "")
        scope    = task.payload.get("scope", "")
        rationale= task.payload.get("rationale", "")

        instruction = (
            f"Refactor the following: {target}\n"
            f"Scope: {scope}\n"
            f"Rationale: {rationale}\n"
            "Ensure no breaking changes. Add tests if missing."
        )
        executor = OpenCodeExecutor(profile="coder")
        result = executor.run(instruction=instruction, context=task.context or "")
        return {
            "summary":      result.get("summary", f"Refatoração de {target} concluída"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": True,
        }

    def _automate(self, task: Task) -> dict:
        """Cria scripts e automações."""
        description = task.payload.get("description", "")
        output_path = task.payload.get("output_path", "")
        executor = OpenCodeExecutor(profile="coder")
        result = executor.run(
            instruction = f"Create an automation script: {description}\nOutput to: {output_path}",
            context     = task.context or "",
        )
        return {
            "summary":      result.get("summary", "Automação criada"),
            "artifact_ref": output_path or result.get("artifact_ref"),
            "needs_review": False,  # Automações simples sem review obrigatório
        }

    def _build(self, task: Task) -> dict:
        """Executa ou configura pipeline/build."""
        command = task.payload.get("command", "")
        cwd     = task.payload.get("cwd", "/mnt/c/CindyAgent")

        if not command:
            raise BlockedByDependency("Comando de build não especificado no payload")

        try:
            proc = subprocess.run(
                command, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=120
            )
            success = proc.returncode == 0
            return {
                "summary":      f"Build {'OK' if success else 'FALHOU'}: {command}\n{proc.stdout[-500:] if proc.stdout else ''}{proc.stderr[-300:] if proc.stderr else ''}",
                "artifact_ref": None,
                "needs_review": not success,
            }
        except subprocess.TimeoutExpired:
            raise BlockedByDependency("Build excedeu timeout de 120s")

    def _generic(self, task: Task) -> dict:
        """Handler genérico para ações não mapeadas."""
        executor = OpenCodeExecutor(profile="coder")
        result = executor.run(
            instruction = str(task.payload.get("description", task.action)),
            context     = task.context or "",
        )
        return {
            "summary":      result.get("summary", f"Ação '{task.action}' processada"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": True,
        }


if __name__ == "__main__":
    import sys
    worker = BuilderWorker()
    if "--once" in sys.argv:
        n = worker.run_once()
        print(f"[builder] Processadas {n} tarefa(s)")
    else:
        worker.run()
