#!/bin/bash
# 99_activate.sh - Final activation and validation

set -e

echo "============================================================"
echo "       CINDY AGENT - Final Validation"
echo "============================================================"

HERMES_DIR="$HOME/.hermes"

echo ""
echo "Checking Hermes..."
if command -v hermes >/dev/null 2>&1; then
    echo "  hermes: OK ($(hermes --version 2>/dev/null || echo installed))"
elif [ -f "$HERMES_DIR/hermes-agent/venv/bin/hermes" ]; then
    echo "  hermes: OK (venv)"
else
    echo "  hermes: FAIL - not found"
fi

echo ""
echo "Checking Python..."
if command -v python3 >/dev/null 2>&1; then
    echo "  python3: $(python3 --version)"
else
    echo "  python3: FAIL"
fi

echo ""
echo "Checking Redis..."
if redis-cli PING >/dev/null 2>&1; then
    echo "  Redis: OK ($(redis-cli INFO server | grep redis_version | cut -d: -f2 | tr -d '[:space:]'))"
else
    echo "  Redis: FAIL - run redis-server --daemonize yes"
fi

echo ""
echo "Checking OpenCode..."
if command -v opencode >/dev/null 2>&1; then
    echo "  opencode: OK"
else
    echo "  opencode: not found (optional)"
fi

echo ""
echo "Checking canonical KB..."
for f in SOUL.md; do
    if [ -f "$HERMES_DIR/$f" ]; then
        echo "  $f: OK"
    else
        echo "  $f: FAIL"
    fi
done

for f in USER.md MEMORY.md; do
    if [ -f "$HERMES_DIR/memories/$f" ]; then
        echo "  memories/$f: OK"
    else
        echo "  memories/$f: FAIL"
    fi
done

echo ""
echo "Checking ACP scripts..."
if [ -f "$HOME/.agents/scripts/acp_redis.py" ]; then
    echo "  acp_redis.py: OK"
    python3 -c "import sys; sys.path.insert(0,'$HOME/.agents/scripts'); from acp_redis import ACPRedis; print('  ACP import: OK')" 2>/dev/null || echo "  ACP import: FAIL"
else
    echo "  acp_redis.py: FAIL"
fi

echo ""
echo "Checking routing gate..."
if [ -f "$HOME/.agents/skills/dual-model-orchestrator/scripts/dual_model_gate.py" ]; then
    RESULT=$(python3 "$HOME/.agents/skills/dual-model-orchestrator/scripts/dual_model_gate.py" "monitorar thingsboard" 2>/dev/null)
    echo "  dual_model_gate.py: OK (test -> $RESULT)"
else
    echo "  dual_model_gate.py: FAIL"
fi

echo ""
echo "Checking project files..."
if [ -d "/mnt/c/CindyAgent" ]; then
    echo "  /mnt/c/CindyAgent: OK"
    echo "  Docs: $(ls /mnt/c/CindyAgent/docs/*.md 2>/dev/null | wc -l) files"
elif [ -d "$HOME/CindyAgent" ]; then
    echo "  $HOME/CindyAgent: OK"
    echo "  Docs: $(ls "$HOME"/CindyAgent/docs/*.md 2>/dev/null | wc -l) files"
else
    echo "  CindyAgent: NOT FOUND - clone the repo first"
fi

echo ""
echo "============================================================"
echo "       SUMMARY"
echo "============================================================"
echo ""
echo "To start Cindy in the terminal:"
echo ""
echo "  cd /mnt/c/CindyAgent"
echo "  source ~/.hermes/hermes-agent/venv/bin/activate"
echo "  hermes chat"
echo ""
echo "To activate Telegram:"
echo ""
echo "  hermes gateway start"
echo ""
echo "To test ACP:"
echo ""
echo "  python3 ~/.agents/scripts/test_acp_multi_agent.py"
echo ""
echo "============================================================"
echo "  Cindy Agent ready."
echo "============================================================"
