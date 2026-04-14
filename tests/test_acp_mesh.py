#!/usr/bin/env python3
"""
test_acp_mesh.py — Smoke tests e validação de handoffs na infra do ACP usando Pytest.
ST-S3-12: Playwright Validation Suite / Básico de Comportamento.
Esse teste exercita via Python/Redis o pipeline semântico de lifecycle.
(Parte do portfólio de testes mantido pelo papel 'Reviewer').
"""

import pytest
import sys
import os
from pathlib import Path

# Injeta a raiz do script no sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / '.agents' / 'scripts'))

from acp.task_lifecycle import TaskStore, Task, TaskState
from acp.acp_mesh import ACPMesh
import logging

logging.basicConfig(level=logging.INFO)

@pytest.fixture
def test_mesh():
    mesh = ACPMesh(host='localhost', port=6379)
    mesh._r.flushdb() # Clean state
    return mesh

def test_task_lifecycle_queuing(test_mesh):
    """Smoke test: validação estrutural do ciclo básico: queued -> done e tracking no Redis"""
    
    # 1. Enviar task
    task = test_mesh.send_task(
        to_agent="builder",
        action="Criar fixture dummy",
        payload={},
        from_agent="cindy"
    )
    task_id = task.task_id
    
    task_data = test_mesh.store.get(task_id)
    assert task_data.state == TaskState.QUEUED
    
    # 2. Worker Consome
    task_list = test_mesh.consume("builder", count=1)
    assert len(task_list) == 1
    
    task_data = test_mesh.store.get(task_id)
    assert task_data.state == TaskState.CLAIMED
    
    # 3. Simulate Worker processing state transitions
    test_mesh.start(task_id, agent="builder")
    assert test_mesh.store.get(task_id).state == TaskState.RUNNING

    test_mesh.complete(task_id, agent="builder", result_summary="Processed Fixture Dummy")
    assert test_mesh.store.get(task_id).state == TaskState.DONE


def test_handoff_rework_validation(test_mesh):
    """Simula um handoff do worker de volta para aprovação e posterior escalação ao PO."""
    
    # Cindy envia -> Reviewer
    task = test_mesh.send_task("reviewer", "Validar Playwright", payload={}, from_agent="cindy")
    task_id = task.task_id
    
    # Reviewer consome
    task_list = test_mesh.consume("reviewer", count=1)
    test_mesh.start(task_id, agent="reviewer")
    
    # Reviewer acha erro complexo, escalate (PO Gate)
    test_mesh.escalate(task_id, agent="reviewer", reason="PO: Precisamos de credenciais do BrowserStack.")
    
    task_data = test_mesh.store.get(task_id)
    assert task_data.state == TaskState.ESCALATED

    logs = test_mesh._r.lrange(f"acp:log:{task_id}", 0, -1)
    assert len(logs) > 0
    assert "escalated" in str(logs)

