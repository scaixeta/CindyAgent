#!/usr/bin/env python3
"""
reviewer_worker.py — Worker do Reviewer: validação, QA e compliance

Responsabilidades:
  - review: revisão semântica e de código
  - validate: validação de artefatos
  - test: execução de testes
  - audit: auditoria de compliance DOC2.5
  - qa: verificação de qualidade geral
"""

import logging
import subprocess
import os
import sys
from workers.base_worker import BaseWorker, EscalateToHuman
from acp.task_lifecycle import Task

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from opencode.opencode_executor import OpenCodeExecutor

log = logging.getLogger("workers.reviewer")

WORKSPACE_WIN = "C:\\CindyAgent"
WORKSPACE_WSL = "/mnt/c/CindyAgent"


class ReviewerWorker(BaseWorker):
    """Especialista em validação, testes e compliance."""

    agent_id = "reviewer"

    ALWAYS_ESCALATE = {"security_finding", "critical_bug", "compliance_failure"}

    def handle(self, task: Task) -> dict:
        action = task.action.lower()

        dispatch = {
            "review":   self._review_code,
            "validate": self._validate,
            "test":     self._run_tests,
            "audit":    self._audit_doc25,
            "qa":       self._qa_check,
            "smoke":    self._smoke_test,
        }

        handler = dispatch.get(action, self._generic_review)
        return handler(task)

    # ─── Handlers ───────────────────────────────────────────────────

    def _review_code(self, task: Task) -> dict:
        """Revisão semântica de código via OpenCode reviewer."""
        artifact_ref = task.payload.get("artifact_ref") or task.artifact_ref
        code_snippet = task.payload.get("code", "")
        file_path    = task.payload.get("file_path", "")

        instruction = "Perform a thorough code review. Check for:\n"
        instruction += "1. Logic errors and edge cases\n"
        instruction += "2. Security vulnerabilities\n"
        instruction += "3. Performance issues\n"
        instruction += "4. DOC2.5 compliance (comments, traceability)\n"
        instruction += "5. Test coverage adequacy\n"

        if file_path:
            instruction += f"\nFile to review: {file_path}"
        if code_snippet:
            instruction += f"\nCode:\n{code_snippet}"

        executor = OpenCodeExecutor(profile="reviewer")
        result  = executor.run(instruction=instruction, context=task.context or "")

        has_critical = result.get("has_critical_issue", False)
        if has_critical:
            raise EscalateToHuman(f"Review encontrou problema crítico: {result.get('summary', '')}")

        return {
            "summary":      result.get("summary", "Review concluído sem problemas críticos"),
            "artifact_ref": result.get("artifact_ref", artifact_ref),
            "needs_review": False,
        }

    def _validate(self, task: Task) -> dict:
        """Valida artefato contra critério de pronto."""
        artifact_ref   = task.payload.get("artifact_ref", "")
        criteria       = task.payload.get("criteria", "")

        instruction = (
            f"Validate the artifact at '{artifact_ref}' against the following criteria:\n"
            f"{criteria}\n"
            "Return: PASS or FAIL with justification for each criterion."
        )
        executor = OpenCodeExecutor(profile="reviewer")
        result = executor.run(instruction=instruction, context=task.context or "")
        return {
            "summary":      result.get("summary", f"Validação de {artifact_ref} concluída"),
            "artifact_ref": artifact_ref,
            "needs_review": False,
        }

    def _run_tests(self, task: Task) -> dict:
        """Executa suite de testes via CLI."""
        test_cmd = task.payload.get("command", "python -m pytest tests/ -v --tb=short")
        cwd      = task.payload.get("cwd", WORKSPACE_WSL)

        try:
            proc = subprocess.run(
                test_cmd, shell=True, cwd=cwd,
                capture_output=True, text=True, timeout=180
            )
            passed  = proc.returncode == 0
            output  = (proc.stdout or "")[-1500:] + (proc.stderr or "")[-500:]
            summary = f"Tests {'PASSARAM' if passed else 'FALHARAM'}\n{output}"

            if not passed and "CRITICAL" in output.upper():
                raise EscalateToHuman(f"Falha crítica nos testes: {output[:300]}")

            return {
                "summary":      summary,
                "artifact_ref": None,
                "needs_review": not passed,
            }
        except subprocess.TimeoutExpired:
            return {
                "summary":      "Timeout nos testes (>180s) — possível travamento",
                "artifact_ref": None,
                "needs_review": True,
            }

    def _audit_doc25(self, task: Task) -> dict:
        """Audita conformidade DOC2.5."""
        target_path = task.payload.get("path", WORKSPACE_WIN)

        checks = [
            f"Verify Dev_Tracking_S3.md exists and has active sprint entries at {target_path}",
            "Verify tests/bugs_log.md has structured entries",
            "Verify KB/aiops/S3_EXECUTION_PLAN.md is present",
            "Verify .clinerules/WORKSPACE_RULES_GLOBAL.md exists",
            "Verify docs/ contains ARCHITECTURE.md, SETUP.md, OPERATIONS.md, DEVELOPMENT.md",
        ]

        executor = OpenCodeExecutor(profile="reviewer")
        results = []
        for check in checks:
            r = executor.run(instruction=check, context=target_path)
            results.append(f"✓ {check[:60]}" if not r.get("failed") else f"✗ {check[:60]}")

        summary = "DOC2.5 Audit:\n" + "\n".join(results)
        failed = any("✗" in r for r in results)

        if failed:
            raise EscalateToHuman(f"Falha na auditoria DOC2.5:\n{summary}")

        return {"summary": summary, "artifact_ref": None, "needs_review": False}

    def _smoke_test(self, task: Task) -> dict:
        """Executa smoke tests via Playwright."""
        test_file = task.payload.get("test_file", "tests/smoke/")
        executor = OpenCodeExecutor(profile="tester")
        result = executor.run(
            instruction = f"Run Playwright smoke tests at {test_file}",
            context     = task.context or "",
        )
        return {
            "summary":      result.get("summary", "Smoke tests concluídos"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": result.get("failed", False),
        }

    def _qa_check(self, task: Task) -> dict:
        """QA geral de um artefato."""
        return self._review_code(task)

    def _generic_review(self, task: Task) -> dict:
        executor = OpenCodeExecutor(profile="reviewer")
        result = executor.run(
            instruction = str(task.payload.get("description", task.action)),
            context     = task.context or "",
        )
        return {
            "summary":      result.get("summary", f"Review de '{task.action}' concluído"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": False,
        }


if __name__ == "__main__":
    import sys
    worker = ReviewerWorker()
    if "--once" in sys.argv:
        n = worker.run_once()
        print(f"[reviewer] Processadas {n} tarefa(s)")
    else:
        worker.run()
