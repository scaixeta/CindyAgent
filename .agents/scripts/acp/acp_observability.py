#!/usr/bin/env python3
"""
acp_observability.py — Ferramenta de Observabilidade do ACP Mesh (Fase 5)
Permite extrair métricas de throughput, tracking de handoffs e intervenção humana/falhas.
Uso: `python -m acp.acp_observability summary`
"""

import redis
import json
from collections import defaultdict
from typing import Dict, List, Any

class ACPObservability:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        keys = self.r.keys("acp:task:*")
        tasks = []
        for key in keys:
            data = self.r.get(key)
            if data:
                try:
                    tasks.append(json.loads(data))
                except json.JSONDecodeError:
                    pass
        return tasks

    def get_all_logs(self) -> Dict[str, List[Dict[str, Any]]]:
        """Obtém as timelines de log agrupadas por task_id"""
        keys = self.r.keys("acp:log:*")
        logs = defaultdict(list)
        for key in keys:
            task_id = key.split(":")[-1]
            entries = self.r.lrange(key, 0, -1)
            for entry in entries:
                try:
                    logs[task_id].append(json.loads(entry))
                except json.JSONDecodeError:
                    pass
        return logs

    def generate_metrics(self) -> Dict[str, Any]:
        """Gera as métricas chave (throughput, falhas, retrabalho)"""
        tasks = self.get_all_tasks()
        logs = self.get_all_logs()

        total_tasks = len(tasks)
        states = defaultdict(int)
        human_escalations = 0
        handoffs = 0

        for task in tasks:
            states[task.get("state", "unknown")] += 1

        for task_id, timeline in logs.items():
            for event in timeline:
                if event.get("to_state") == "escalated":
                    human_escalations += 1
                if event.get("event") == "handoff":
                    handoffs += 1

        rework = 0 
        for task_id, timeline in logs.items():
            # Conta se uma task pulou de um Worker para Reviewer, e então Reviewer rejeitou.
            # Simulação simples: se o número de handoffs > 2
            if len([e for e in timeline if e.get("event") == "handoff"]) >= 2:
                rework += 1

        success_rate = states.get("done", 0) / total_tasks * 100 if total_tasks > 0 else 0

        return {
            "total_tasks": total_tasks,
            "states": dict(states),
            "human_interventions": human_escalations,
            "handoffs_count": handoffs,
            "rework_count": rework,
            "success_rate_percentage": round(success_rate, 2)
        }

    def print_summary(self):
        print("======== ACP Mesh Observability Summary ========")
        metrics = self.generate_metrics()
        print(f"Total de Tarefas Criadas: {metrics['total_tasks']}")
        print(f"Taxa de Sucesso (Done): {metrics['success_rate_percentage']}%")
        print("\n=== Distribuição de Status ===")
        for state, count in metrics['states'].items():
            print(f"- {state.upper()}: {count}")
        print(f"\n=== Governança ===")
        print(f"Gatilhos de Escalação Semântica (PO Gates Acionados): {metrics['human_interventions']}")
        print(f"Total de Handoffs Executados: {metrics['handoffs_count']}")
        print(f"Tarefas com Retrabalho / Bate-volta (>2 handoffs): {metrics['rework_count']}")
        print("=================================================")

if __name__ == "__main__":
    obs = ACPObservability()
    obs.print_summary()
