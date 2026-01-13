#!/bin/bash
# Install nmrxiv skill for Claude Code

SKILL_DIR="$HOME/.claude/skills/nmrxiv"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "Installing nmrxiv skill for Claude Code..."

# Create skill directory
mkdir -p "$SKILL_DIR"

# Copy skill file
cp "$REPO_DIR/skills/SKILL.md" "$SKILL_DIR/SKILL.md"

if [ -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✓ Skill installed to $SKILL_DIR"
    echo ""
    echo "Usage: In Claude Code, the skill will be automatically invoked when"
    echo "       you ask about NMR data or nmrxiv. You can also use /nmrxiv."
else
    echo "✗ Installation failed"
    exit 1
fi
