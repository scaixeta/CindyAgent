#!/bin/bash
set -e

echo "=== Hermes Agent Installation Script ==="

GIT_BIN="$(command -v git.exe 2>/dev/null || command -v git)"
export GIT_TERMINAL_PROMPT=1
HERMES_DIR="$HOME/.hermes"
HERMES_REPO_DIR="$HERMES_DIR/hermes-agent"
HERMES_SOURCE_DIR="${HERMES_AGENT_SOURCE_DIR:-}"
HERMES_SOURCE_URL="${HERMES_AGENT_REPO_URL:-https://github.com/nousresearch/hermes-agent.git}"
HERMES_SOURCE_ARCHIVE="${HERMES_AGENT_ARCHIVE:-}"

echo "[1/5] Creating ~/.hermes/ directory structure..."
mkdir -p "$HERMES_DIR"/{logs,sessions,cron,skills,memories}
mkdir -p ~/.local/bin
echo "    Done."

install_from_local_source() {
    local source_dir="$1"
    echo "    Installing from local source: $source_dir"
    rm -rf "$HERMES_REPO_DIR"
    mkdir -p "$HERMES_REPO_DIR"
    cp -a "$source_dir"/. "$HERMES_REPO_DIR"/
    rm -rf "$HERMES_REPO_DIR/.git" "$HERMES_REPO_DIR/venv"
}

install_from_archive() {
    local archive_path="$1"
    local tmp_dir
    tmp_dir="$(mktemp -d)"
    echo "    Extracting archive: $archive_path"
    case "$archive_path" in
        *.tar.gz|*.tgz) tar -xzf "$archive_path" -C "$tmp_dir" ;;
        *.tar) tar -xf "$archive_path" -C "$tmp_dir" ;;
        *.zip) unzip -q "$archive_path" -d "$tmp_dir" ;;
        *)
            echo "    ERROR: Unsupported archive format: $archive_path"
            rm -rf "$tmp_dir"
            return 1
            ;;
    esac
    local extracted
    extracted="$(find "$tmp_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
    if [ -z "$extracted" ]; then
        extracted="$tmp_dir"
    fi
    install_from_local_source "$extracted"
    rm -rf "$tmp_dir"
}

echo "[2/5] Acquiring hermes-agent source..."
if [ -x "$HERMES_REPO_DIR/venv/bin/hermes" ]; then
    echo "    Existing Hermes installation detected, skipping source acquisition."
elif [ -d "$HERMES_REPO_DIR/.git" ]; then
    echo "    Repository exists, pulling latest changes..."
    cd "$HERMES_REPO_DIR"
    "$GIT_BIN" pull
elif [ -n "$HERMES_SOURCE_DIR" ] && [ -d "$HERMES_SOURCE_DIR" ]; then
    install_from_local_source "$HERMES_SOURCE_DIR"
elif [ -n "$HERMES_SOURCE_ARCHIVE" ] && [ -f "$HERMES_SOURCE_ARCHIVE" ]; then
    install_from_archive "$HERMES_SOURCE_ARCHIVE"
elif [ -n "$HERMES_SOURCE_URL" ]; then
    echo "    Cloning repository from configured URL..."
    "$GIT_BIN" clone --recurse-submodules "$HERMES_SOURCE_URL" "$HERMES_REPO_DIR"
else
    echo "    ERROR: No hermes-agent source available."
    echo "    Set one of:"
    echo "      HERMES_AGENT_SOURCE_DIR=/path/to/project-hermes-checkout"
    echo "      HERMES_AGENT_ARCHIVE=/path/to/hermes-agent.tar.gz"
    echo "      HERMES_AGENT_REPO_URL=https://.../hermes-agent.git"
    exit 1
fi
echo "    Done."

echo "[3/5] Creating Python 3.11 virtual environment..."
cd "$HERMES_REPO_DIR"
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
ln -sf "$HERMES_REPO_DIR/venv/bin/hermes" ~/.local/bin/hermes 2>/dev/null || \
ln -sf "$HERMES_REPO_DIR/venv/bin/hermes" /usr/local/bin/hermes 2>/dev/null || \
echo "    Warning: Could not link to ~/.local/bin or /usr/local/bin"
echo "    You may need to add ~/.local/bin to your PATH"
echo "    Done."

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Next step: Run 'hermes setup' to complete configuration"
echo ""
