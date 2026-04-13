#!/bin/bash
# 06_sync_kb.sh - Sync canonical KB to ~/.hermes/

set -e

SOURCE_KB="/mnt/c/CindyAgent/KB/hermes"
TARGET_DIR="$HOME/.hermes"
MEMORIES_DIR="$TARGET_DIR/memories"
ACTIVATE_SCRIPT="$SOURCE_KB/activate_cindy_runtime.py"

echo "=== Sync KB Canonical ==="
echo "Source: $SOURCE_KB"
echo "Target: $TARGET_DIR"

mkdir -p "$TARGET_DIR" "$MEMORIES_DIR"

echo "Copying KB files..."
cp "$SOURCE_KB/SOUL.md" "$TARGET_DIR/" 2>/dev/null || true
cp "$SOURCE_KB/USER.md" "$MEMORIES_DIR/" 2>/dev/null || true
cp "$SOURCE_KB/MEMORY.md" "$MEMORIES_DIR/" 2>/dev/null || true

if [ -f "$ACTIVATE_SCRIPT" ]; then
    cp "$ACTIVATE_SCRIPT" "$TARGET_DIR/"
    echo "Copied activate_cindy_runtime.py"
else
    echo "WARNING: $ACTIVATE_SCRIPT not found"
fi

echo ""
echo "=== Verification ==="
if [ -d "$TARGET_DIR" ]; then
    echo "OK Target directory exists: $TARGET_DIR"
else
    echo "ERROR Target directory missing"
    exit 1
fi

for file in SOUL.md activate_cindy_runtime.py; do
    if [ -f "$TARGET_DIR/$file" ]; then
        echo "OK Found: $file"
    else
        echo "ERROR Missing: $file"
    fi
done

for file in USER.md MEMORY.md; do
    if [ -f "$MEMORIES_DIR/$file" ]; then
        echo "OK Found: memories/$file"
    else
        echo "ERROR Missing: memories/$file"
    fi
done

echo ""
echo "=== KB Sync Complete ==="
