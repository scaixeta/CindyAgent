#!/usr/bin/env python3
"""
capability_registry.py — Registro de capacidades por agente no ACP mesh

Cada agente anuncia sua missão, domínio, ferramentas e limites.
O registry permite roteamento por capacidade, não só por nome.

Uso:
    from acp.capability_registry import CapabilityRegistry, AgentCard
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional
import redis


@dataclass
class AgentCard:
    """Contrato operacional de um agente."""
    agent:               str
    mission:             str
    domain:              str
    tools_allowed:       list[str]
    tools_forbidden:     list[str]
    skills:              list[str]
    workflows:           list[str]
    input_types:         list[str]            # tipos de tarefa que aceita
    output_format:       str                   # formato do resultado
    max_autonomy:        list[str]             # pode decidir sem escalar
    always_escalate:     list[str]             # sempre escala ao PO
    preferred_model:     str
    fallback_model:      str
    cost_policy:         str                   # low / medium / high
    tags:                list[str] = field(default_factory=list)
    version:             str = "1.0"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AgentCard":
        return cls(**data)

    def can_handle(self, action: str) -> bool:
        """Verifica se o agente pode lidar com a ação pela lista de tags e domínio."""
        return (
            action in self.input_types
            or any(tag in action.lower() for tag in self.tags)
        )


class CapabilityRegistry:
    """
    Registry de capacidades dos agentes no Redis.
    
    Chaves:
      acp:registry:<agent>  -> AgentCard serializado (JSON)
      acp:registry:index    -> Set com nomes de todos os agentes registrados
    """

    KEY_PREFIX  = "acp:registry"
    INDEX_KEY   = "acp:registry:index"
    TAG_PREFIX  = "acp:registry:tag"

    def __init__(self, host: str = "localhost", port: int = 6379):
        self._r = redis.Redis(host=host, port=port, decode_responses=True)

    def register(self, card: AgentCard) -> None:
        """Registra ou atualiza o agent card no registry."""
        key = f"{self.KEY_PREFIX}:{card.agent}"
        self._r.set(key, json.dumps(card.to_dict()))
        self._r.sadd(self.INDEX_KEY, card.agent)
        # Índice por tag para roteamento
        for tag in card.tags:
            self._r.sadd(f"{self.TAG_PREFIX}:{tag}", card.agent)

    def get(self, agent: str) -> Optional[AgentCard]:
        """Recupera o agent card pelo nome."""
        raw = self._r.get(f"{self.KEY_PREFIX}:{agent}")
        if not raw:
            return None
        return AgentCard.from_dict(json.loads(raw))

    def all_agents(self) -> list[str]:
        """Lista todos os agentes registrados."""
        return list(self._r.smembers(self.INDEX_KEY))

    def all_cards(self) -> list[AgentCard]:
        """Retorna todos os agent cards."""
        cards = []
        for agent in self.all_agents():
            card = self.get(agent)
            if card:
                cards.append(card)
        return cards

    def route(self, action: str) -> list[AgentCard]:
        """
        Retorna lista de agentes capazes de lidar com a ação.
        Ordena por especificidade: correspondência exata de input_type primeiro.
        """
        candidates = []
        for card in self.all_cards():
            if card.can_handle(action):
                score = 2 if action in card.input_types else 1
                candidates.append((score, card))
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in candidates]

    def route_by_tag(self, tag: str) -> list[str]:
        """Retorna agentes indexados pelo tag."""
        return list(self._r.smembers(f"{self.TAG_PREFIX}:{tag}"))

    def unregister(self, agent: str) -> None:
        """Remove o agente do registry."""
        card = self.get(agent)
        if card:
            for tag in card.tags:
                self._r.srem(f"{self.TAG_PREFIX}:{tag}", agent)
        self._r.delete(f"{self.KEY_PREFIX}:{agent}")
        self._r.srem(self.INDEX_KEY, agent)

    def dump(self) -> list[dict]:
        """Retorna todos os cards como lista de dicts. Útil para debug."""
        return [c.to_dict() for c in self.all_cards()]


def load_default_cards() -> list[AgentCard]:
    """Retorna os agent cards padrão do time AIOps."""
    return [
        AgentCard(
            agent           = "cindy",
            mission         = "Coordenação operacional do time: triagem, roteamento, consolidação e escala ao PO",
            domain          = "orchestration",
            tools_allowed   = ["hermes", "acp", "redis", "task_store", "capability_registry"],
            tools_forbidden = ["git_commit", "deploy", "production_changes"],
            skills          = ["triage", "routing", "handoff", "sprint_management"],
            workflows       = ["route_task", "consolidate_results", "escalate_to_po"],
            input_types     = ["route", "triage", "status", "sprint", "escalate", "coordinate"],
            output_format   = "task_routed | status_report | escalation",
            max_autonomy    = ["routing", "status_check", "handoff", "clarification"],
            always_escalate = ["sprint_creation", "architecture_change", "cost_decision", "scope_change"],
            preferred_model = "MiniMax-M2.7",
            fallback_model  = "gpt-5.3-codex",
            cost_policy     = "low",
            tags            = ["coordinator", "router", "orchestrator"],
        ),
        AgentCard(
            agent           = "builder",
            mission         = "Execução técnica: código, automações, refatoração e pipelines",
            domain          = "engineering",
            tools_allowed   = ["opencode", "git", "terminal", "file", "browser"],
            tools_forbidden = ["deploy_production", "database_drop"],
            skills          = ["coder", "tester", "refactoring", "pipeline"],
            workflows       = ["implement_feature", "fix_bug", "refactor", "create_pipeline"],
            input_types     = ["code", "implement", "fix", "refactor", "automate", "build"],
            output_format   = "code_artifact | diff | test_result",
            max_autonomy    = ["implementation", "refactoring", "unit_tests", "local_fix"],
            always_escalate = ["architecture", "breaking_change", "security", "production_deploy"],
            preferred_model = "MiniMax-M2.7",
            fallback_model  = "gpt-5.3-codex",
            cost_policy     = "medium",
            tags            = ["code", "engineering", "automation", "build"],
        ),
        AgentCard(
            agent           = "reviewer",
            mission         = "Validação semântica, QA, revisão de código e compliance",
            domain          = "quality",
            tools_allowed   = ["playwright", "sonarcloud", "grep", "file", "terminal"],
            tools_forbidden = ["git_push", "deploy"],
            skills          = ["reviewer", "tester", "auditor"],
            workflows       = ["review_code", "run_tests", "audit_compliance", "smoke_test"],
            input_types     = ["review", "validate", "test", "audit", "qa", "compliance"],
            output_format   = "review_report | test_result | compliance_status",
            max_autonomy    = ["code_review", "test_execution", "lint_check"],
            always_escalate = ["security_finding", "critical_bug", "compliance_failure"],
            preferred_model = "gpt-5.3-codex",
            fallback_model  = "MiniMax-M2.7",
            cost_policy     = "medium",
            tags            = ["qa", "review", "validation", "testing", "compliance"],
        ),
        AgentCard(
            agent           = "documenter",
            mission         = "Documentação técnica, contratos, KB e material operacional",
            domain          = "documentation",
            tools_allowed   = ["file", "markdown", "kb_write", "memory"],
            tools_forbidden = ["terminal_exec", "code_deploy"],
            skills          = ["docs-writer", "kb_updater", "contract_writer"],
            workflows       = ["write_doc", "update_kb", "create_contract", "write_runbook"],
            input_types     = ["document", "write", "update_kb", "contract", "runbook", "adr"],
            output_format   = "markdown_document | kb_entry",
            max_autonomy    = ["doc_update", "kb_entry", "runbook"],
            always_escalate = ["architectural_decision", "breaking_change_doc", "external_publication"],
            preferred_model = "MiniMax-M2.7",
            fallback_model  = "gpt-5.3-codex",
            cost_policy     = "low",
            tags            = ["documentation", "kb", "contract", "runbook"],
        ),
        AgentCard(
            agent           = "platformops",
            mission         = "Infraestrutura, runtime, telemetria, IoT, n8n e ThingsBoard",
            domain          = "platform",
            tools_allowed   = ["docker", "redis_cli", "terminal", "n8n", "thingsboard", "ssh"],
            tools_forbidden = ["production_schema_drop", "bulk_delete"],
            skills          = ["sre-debugger", "infra_ops", "iot_ops"],
            workflows       = ["monitor_infra", "deploy_service", "configure_n8n", "debug_runtime"],
            input_types     = ["infra", "deploy", "monitor", "iot", "n8n", "thingsboard", "runtime", "debug"],
            output_format   = "infra_status | deployment_result | telemetry_report",
            max_autonomy    = ["monitoring", "restart_service", "config_update", "log_analysis"],
            always_escalate = ["production_deploy", "data_migration", "security_patch"],
            preferred_model = "MiniMax-M2.7",
            fallback_model  = "gpt-5.3-codex",
            cost_policy     = "low",
            tags            = ["infra", "iot", "n8n", "thingsboard", "runtime", "platform"],
        ),
    ]
