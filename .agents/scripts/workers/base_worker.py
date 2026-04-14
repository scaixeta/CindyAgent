#!/usr/bin/env python3
"""
base_worker.py — Classe base para todos os workers do time AIOps

Cada worker especialista herda desta classe e implementa:
  - handle(task) -> resultado

O loop de consumo, logging, retry e escalação são gerenciados na base.

Uso:
    class BuilderWorker(BaseWorker):
        agent_id = "builder"
        def handle(self, task: Task) -> dict:
            ...
"""

import logging
import signal
import time
from abc import ABC, abstractmethod
from typing import Optional
import sys
import os

# Adiciona o diretório raiz dos scripts ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from acp.acp_mesh import ACPMesh
from acp.task_lifecycle import Task, TaskState
from acp.capability_registry import CapabilityRegistry, load_default_cards

log = logging.getLogger("workers.base")


class BaseWorker(ABC):
    """Classe base para workers de agentes do time AIOps."""

    agent_id:      str = "base"
    poll_interval: int = 2   # segundos entre polls do stream
    group:         str = ""  # consumer group (default: workers:<agent_id>)

    def __init__(self, host: str = "localhost", port: int = 6379):
        self.mesh      = ACPMesh(host, port)
        self._running  = False
        self.group     = self.group or f"workers:{self.agent_id}"
        self._register()
        logging.basicConfig(
            level   = logging.INFO,
            format  = "%(asctime)s [%(name)s] %(levelname)s %(message)s",
        )

    def _register(self) -> None:
        """Registra o agent card no capability registry ao iniciar."""
        cards = {c.agent: c for c in load_default_cards()}
        card = cards.get(self.agent_id)
        if card:
            self.mesh.registry.register(card)
            log.info("[%s] Agent card registrado no registry", self.agent_id)
        else:
            log.warning("[%s] Nenhum agent card encontrado para registro", self.agent_id)

    # ─── Interface pública ───────────────────────────────────────────

    def run(self) -> None:
        """Loop principal de consumo de tarefas."""
        self._running = True
        signal.signal(signal.SIGTERM, self._shutdown)
        signal.signal(signal.SIGINT, self._shutdown)
        log.info("[%s] Worker iniciado. Aguardando tarefas...", self.agent_id)

        while self._running:
            try:
                tasks = self.mesh.consume(self.agent_id, self.group)
                for task in tasks:
                    self._execute(task)
            except Exception as e:
                log.error("[%s] Erro no loop de consumo: %s", self.agent_id, e, exc_info=True)
            time.sleep(self.poll_interval)

        log.info("[%s] Worker encerrado.", self.agent_id)

    def run_once(self) -> int:
        """Processa tarefas disponíveis agora (sem loop). Retorna quantidade processada."""
        tasks = self.mesh.consume(self.agent_id, self.group)
        for task in tasks:
            self._execute(task)
        return len(tasks)

    # ─── Execução interna ───────────────────────────────────────────

    def _execute(self, task: Task) -> None:
        log.info("[%s] Processando task_id=%s action=%s", self.agent_id, task.task_id, task.action)
        try:
            self.mesh.start(task.task_id, self.agent_id)
            result = self.handle(task)

            artifact_ref    = result.get("artifact_ref") if isinstance(result, dict) else None
            result_summary  = result.get("summary", str(result)) if isinstance(result, dict) else str(result)
            needs_review    = result.get("needs_review", False) if isinstance(result, dict) else False

            if needs_review and artifact_ref:
                self.mesh.request_review(task.task_id, self.agent_id, artifact_ref)
            else:
                self.mesh.complete(task.task_id, self.agent_id, artifact_ref, result_summary)

        except EscalateToHuman as e:
            self.mesh.escalate(task.task_id, self.agent_id, str(e))
        except BlockedByDependency as e:
            self.mesh.block(task.task_id, self.agent_id, str(e))
        except Exception as e:
            log.error("[%s] Falha ao processar task_id=%s: %s", self.agent_id, task.task_id, e, exc_info=True)
            self.mesh.fail(task.task_id, self.agent_id, str(e), retry=True)

    @abstractmethod
    def handle(self, task: Task) -> dict:
        """
        Processa a tarefa e retorna resultado.

        O dict de retorno pode conter:
          {
            "summary":      str,          # resumo do resultado
            "artifact_ref": str | None,   # caminho ou referência do artefato gerado
            "needs_review": bool,         # True se precisa validação do Reviewer
          }
        """

    def _shutdown(self, *_):
        log.info("[%s] Sinal de encerramento recebido.", self.agent_id)
        self._running = False


# ─── Exceções semânticas ──────────────────────────────────────────────────────

class EscalateToHuman(Exception):
    """Levanta quando a tarefa excede os limites de autonomia do agente."""

class BlockedByDependency(Exception):
    """Levanta quando a tarefa não pode prosseguir por dependência externa."""
