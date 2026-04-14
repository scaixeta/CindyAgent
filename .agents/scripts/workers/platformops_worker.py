#!/usr/bin/env python3
"""
platformops_worker.py — Worker do PlatformOps: infra, IoT, runtime e n8n

Responsabilidades:
  - monitor: monitorar serviços e runtime
  - debug: depurar problemas de runtime/infra
  - deploy: deploy de serviços (com gate PO obrigatório)
  - iot: operações ThingsBoard / telemetria
  - n8n: atividades no n8n
  - runtime: operações no Hermes e gateway
"""

import logging
import subprocess
import json
import os
import sys
from datetime import datetime, timezone
from workers.base_worker import BaseWorker, EscalateToHuman, BlockedByDependency
from acp.task_lifecycle import Task

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from opencode.opencode_executor import OpenCodeExecutor

log = logging.getLogger("workers.platformops")


class PlatformOpsWorker(BaseWorker):
    """Especialista em infraestrutura, runtime e plataforma IoT."""

    agent_id = "platformops"

    ALWAYS_ESCALATE = {"production_deploy", "data_migration", "security_patch", "schema_change"}

    def handle(self, task: Task) -> dict:
        action = task.action.lower()

        if action in self.ALWAYS_ESCALATE:
            raise EscalateToHuman(f"'{action}' requer aprovação explícita do PO")

        dispatch = {
            "monitor":  self._monitor,
            "debug":    self._debug,
            "deploy":   self._deploy_safe,
            "iot":      self._iot_ops,
            "n8n":      self._n8n_ops,
            "runtime":  self._runtime_ops,
            "infra":    self._monitor,
            "restart":  self._restart_service,
            "health":   self._health_check,
        }

        handler = dispatch.get(action, self._generic_ops)
        return handler(task)

    # ─── Handlers ───────────────────────────────────────────────────

    def _monitor(self, task: Task) -> dict:
        """Coleta status de serviços e runtime."""
        checks = {
            "hermes_gateway": "wsl -d Ubuntu -u root -- bash -c 'systemctl is-active hermes-gateway.service'",
            "hermes_health":  "wsl -d Ubuntu -u root -- bash -c 'curl -s http://127.0.0.1:8642/health'",
            "redis":          "wsl -d Ubuntu -u root -- bash -c 'redis-cli ping'",
            "redis_streams":  "wsl -d Ubuntu -u root -- bash -c 'redis-cli xlen acp:stream:cindy 2>/dev/null || echo 0'",
        }
        results = {}
        for name, cmd in checks.items():
            try:
                proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                results[name] = proc.stdout.strip() or proc.stderr.strip() or "no output"
            except subprocess.TimeoutExpired:
                results[name] = "TIMEOUT"
            except Exception as e:
                results[name] = f"ERROR: {e}"

        summary = "Monitor resultado:\n" + "\n".join(f"  {k}: {v}" for k, v in results.items())
        all_ok = all(
            v in ("active", "PONG", '{"status": "ok", "platform": "hermes-agent"}') or v.isdigit()
            for v in results.values()
        )
        return {
            "summary":      summary,
            "artifact_ref": None,
            "needs_review": not all_ok,
        }

    def _debug(self, task: Task) -> dict:
        """Depura problema de runtime com análise de logs."""
        service        = task.payload.get("service", "hermes-gateway.service")
        lines          = task.payload.get("log_lines", 50)
        error_pattern  = task.payload.get("error_pattern", "ERROR|CRITICAL|ImportError|Traceback")

        cmd = (
            f"wsl -d Ubuntu -u root -- bash -c "
            f"\"journalctl -u {service} -n {lines} --no-pager 2>&1 | "
            f"grep -E '{error_pattern}'\""
        )
        try:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            log_output = proc.stdout or "Nenhum erro encontrado nos logs."
        except subprocess.TimeoutExpired:
            log_output = "TIMEOUT ao coletar logs"

        executor = OpenCodeExecutor(profile="sre-debugger")
        analysis = executor.run(
            instruction = f"Analyze these service logs and identify root cause:\n{log_output}",
            context     = f"Service: {service}",
        )
        return {
            "summary":      f"Debug de {service}:\n{analysis.get('summary', log_output[:500])}",
            "artifact_ref": None,
            "needs_review": "critical" in log_output.lower() or "error" in log_output.lower(),
        }

    def _deploy_safe(self, task: Task) -> dict:
        """Deploy seguro — apenas serviços staging permitidos sem gate PO."""
        service  = task.payload.get("service", "")
        env      = task.payload.get("environment", "staging")

        if env == "production":
            raise EscalateToHuman(f"Deploy em produção requer aprovação explícita do PO: {service}")

        cmd = task.payload.get("deploy_command", "")
        if not cmd:
            raise BlockedByDependency("deploy_command não especificado no payload")

        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        success = proc.returncode == 0
        return {
            "summary":      f"Deploy {'OK' if success else 'FALHOU'}: {service} [{env}]\n{proc.stdout[-600:]}",
            "artifact_ref": None,
            "needs_review": not success,
        }

    def _restart_service(self, task: Task) -> dict:
        """Reinicia um serviço systemd no WSL2."""
        service = task.payload.get("service", "hermes-gateway.service")
        cmd = f"wsl -d Ubuntu -u root -- bash -c 'systemctl restart {service} && sleep 3 && systemctl is-active {service}'"
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        ok = "active" in proc.stdout
        return {
            "summary":      f"Restart de {service}: {'OK' if ok else 'FALHOU'}\n{proc.stdout.strip()}",
            "artifact_ref": None,
            "needs_review": not ok,
        }

    def _health_check(self, task: Task) -> dict:
        """Healthcheck completo do ambiente."""
        return self._monitor(task)

    def _iot_ops(self, task: Task) -> dict:
        """Operações ThingsBoard / IoT."""
        operation   = task.payload.get("operation", "")
        device_id   = task.payload.get("device_id", "")
        telemetry   = task.payload.get("telemetry", {})

        executor = OpenCodeExecutor(profile="sre-debugger")
        result = executor.run(
            instruction = f"Perform IoT operation '{operation}' for device '{device_id}' with telemetry: {json.dumps(telemetry)}",
            context     = task.context or "ThingsBoard CE integration",
        )
        return {
            "summary":      result.get("summary", f"IoT op '{operation}' em device '{device_id}' executada"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": False,
        }

    def _n8n_ops(self, task: Task) -> dict:
        """Operações no n8n: ativar, criar ou depurar workflows."""
        operation   = task.payload.get("operation", "list_workflows")
        workflow_id = task.payload.get("workflow_id", "")

        executor = OpenCodeExecutor(profile="sre-debugger")
        result = executor.run(
            instruction = f"Perform n8n operation '{operation}' on workflow '{workflow_id}'",
            context     = task.context or "n8n self-hosted",
        )
        return {
            "summary":      result.get("summary", f"n8n op '{operation}' executada"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": False,
        }

    def _runtime_ops(self, task: Task) -> dict:
        """Operações no runtime Hermes."""
        operation = task.payload.get("operation", "status")

        cmds = {
            "status": "wsl -d Ubuntu -u root -- bash -c 'systemctl status hermes-gateway.service --no-pager | head -20'",
            "logs":   "wsl -d Ubuntu -u root -- bash -c 'journalctl -u hermes-gateway.service -n 30 --no-pager'",
            "version":"wsl -d Ubuntu -u root -- bash -c 'hermes --version 2>&1'",
        }
        cmd = cmds.get(operation, cmds["status"])
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        return {
            "summary":      f"Runtime op '{operation}':\n{proc.stdout.strip() or proc.stderr.strip()}",
            "artifact_ref": None,
            "needs_review": "error" in (proc.stdout + proc.stderr).lower(),
        }

    def _generic_ops(self, task: Task) -> dict:
        executor = OpenCodeExecutor(profile="sre-debugger")
        result = executor.run(
            instruction = str(task.payload.get("description", task.action)),
            context     = task.context or "",
        )
        return {
            "summary":      result.get("summary", f"Op '{task.action}' executada"),
            "artifact_ref": result.get("artifact_ref"),
            "needs_review": result.get("failed", False),
        }


if __name__ == "__main__":
    import sys
    worker = PlatformOpsWorker()
    if "--once" in sys.argv:
        n = worker.run_once()
        print(f"[platformops] Processadas {n} tarefa(s)")
    else:
        worker.run()
