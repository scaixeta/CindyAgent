#!/bin/bash
set -e

echo "=== Hermes Agent Installation Script ==="

GIT_BIN="$(command -v git.exe 2>/dev/null || command -v git)"
export GIT_TERMINAL_PROMPT=1

echo "[1/5] Creating ~/.hermes/ directory structure..."
mkdir -p ~/.hermes/{logs,sessions,cron,skills,memories}
mkdir -p ~/.local/bin
echo "    Done."

echo "[2/5] Cloning/Updating hermes-agent repository..."
if [ -d "$HOME/.hermes/hermes-agent/.git" ]; then
    echo "    Repository exists, pulling latest changes..."
    cd ~/.hermes/hermes-agent
    "$GIT_BIN" pull
else
    echo "    Cloning repository to ~/.hermes/hermes-agent..."
    "$GIT_BIN" clone https://github.com/scaixeta/hermes-agent.git ~/.hermes/hermes-agent
fi
echo "    Done."

echo "[3/5] Creating Python 3.11 virtual environment..."
cd ~/.hermes/hermes-agent
PYTHON_BIN=""
for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        if "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
            PYTHON_BIN="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON_BIN" ]; then
    echo "    ERROR: Python 3.11+ is required."
    exit 1
fi

"$PYTHON_BIN" -m venv venv
echo "    Done."

echo "[4/5] Installing dependencies with uv sync --all-extras..."
source venv/bin/activate
if ! command -v uv >/dev/null 2>&1; then
    echo "    uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi
uv sync --all-extras
echo "    Done."

echo "[5/5] Linking hermes to PATH..."
ln -sf ~/.hermes/hermes-agent/venv/bin/hermes ~/.local/bin/hermes 2>/dev/null || \
ln -sf ~/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes 2>/dev/null || \
echo "    Warning: Could not link to ~/.local/bin or /usr/local/bin"
echo "    You may need to add ~/.local/bin to your PATH"
echo "    Done."

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next step: Run 'hermes setup' to complete configuration"
echo ""
