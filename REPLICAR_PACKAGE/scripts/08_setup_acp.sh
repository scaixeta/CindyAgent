#!/bin/bash
# ============================================================
# 08_setup_acp.sh — ACP (Agent Communication Protocol)
# ============================================================
set -e

echo "=== 08: ACP ==="

# Redis keys para ACP
redis-cli SET acp:namespace:sentivis "sentivis-oc" 2>/dev/null || echo "Redis não disponível"
redis-cli SET acp:agent:hermes:id "hermes-01" 2>/dev/null || true
redis-cli SET acp:agent:hermes:role "orchestrator" 2>/dev/null || true
redis-cli SET acp:agent:hermes:status "active" 2>/dev/null || true

# Python deps
pip install redis asyncio 2>/dev/null || pip3 install redis asyncio 2>/dev/null || true

# Copiar ACP lib
mkdir -p ~/.agents/scripts ~/.hermes/acp
cp /mnt/c/CindyAgent/REPLICAR_PACKAGE/scripts/acp_redis.py ~/.agents/scripts/ 2>/dev/null || true
cp /mnt/c/CindyAgent/REPLICAR_PACKAGE/scripts/test_acp_multi_agent.py ~/.agents/scripts/ 2>/dev/null || true
cp /mnt/c/CindyAgent/REPLICAR_PACKAGE/scripts/acp_redis.py ~/.hermes/acp/ 2>/dev/null || true
cp /mnt/c/CindyAgent/REPLICAR_PACKAGE/scripts/test_acp_multi_agent.py ~/.hermes/acp/ 2>/dev/null || true

echo "ACP configurado. Keys Redis:"
redis-cli KEYS "acp:*" 2>/dev/null || echo "Redis não disponível"

echo "=== 08 completo ==="
