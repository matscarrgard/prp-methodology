#!/bin/bash
# Bootstrap PRP methodology - wire .claude/ directory
# Run this after adding the .prp subtree:
#   .prp/scripts/bootstrap.sh

set -e

echo "=== Bootstrapping PRP Methodology ==="

# Check we're in project root
if [ ! -d ".prp" ]; then
  echo "Error: .prp directory not found."
  echo "Run this from your project root after adding the methodology subtree."
  exit 1
fi

# Create .claude directory structure
echo "Creating .claude/ directory..."
mkdir -p .claude/commands .claude/skills

# Symlink commands
echo "Linking commands..."
for cmd in .prp/commands/*.md; do
  name=$(basename "$cmd")
  ln -sf "../../.prp/commands/$name" ".claude/commands/$name"
done

# Symlink agents
echo "Linking agents..."
ln -sf ../.prp/agents .claude/agents

# Symlink skills
echo "Linking skills..."
ln -sf ../../.prp/skills/prp-methodology .claude/skills/prp-methodology
ln -sf ../../.prp/skills/error-handling .claude/skills/error-handling

# Create settings.json with hooks
echo "Configuring hooks..."
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.prp/hooks/validate-bash.py\""
          }
        ]
      }
    ]
  }
}
EOF

# Create features directory
echo "Creating features/ directory..."
mkdir -p features/archive
cp .prp/templates/progress.template.txt features/progress.txt

# Verify
echo ""
echo "=== Bootstrap Complete ==="
echo ""
echo "Wired:"
ls -la .claude/commands/ | head -5
echo "..."
echo ""
echo "Next steps:"
echo "  1. Start Claude Code: claude"
echo "  2. Run /init-project to add language boilerplate (optional)"
echo "  3. Run /prime to verify setup"
