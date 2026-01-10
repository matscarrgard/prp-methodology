#!/bin/bash
# Bootstrap PRP methodology - copy .claude/ and features/ directories
# Run after adding the .prp subtree:
#   .prp/scripts/bootstrap.sh

set -e

# Check we're in project root with methodology
if [ ! -d ".prp" ]; then
  echo "Error: .prp directory not found."
  echo "Run this from your project root after adding the methodology subtree."
  exit 1
fi

echo "=== Bootstrapping PRP Methodology ==="

# Copy .claude template (preserves symlinks)
echo "Setting up .claude/..."
cp -PR .prp/.claude-template .claude

# Copy features template
echo "Setting up features/..."
cp -R .prp/features-template features

echo ""
echo "=== Bootstrap Complete ==="
echo ""
echo "You can now start Claude Code:"
echo "  claude"
echo ""
echo "Then run:"
echo "  /init-project  - Add language boilerplate (optional)"
echo "  /prime         - Verify setup"
