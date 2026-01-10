#!/bin/bash
# Bootstrap PRP methodology for EXISTING projects
# Adds methodology commands without overwriting existing .claude/ setup
#
# Usage (existing project with .claude/ already present):
#   .prp/scripts/bootstrap-existing.sh
#
# For new projects:
#   .prp/scripts/bootstrap-new.sh

set -e

# Check we're in project root with methodology
if [ ! -d ".prp" ]; then
  echo "Error: .prp directory not found."
  echo "Run this from your project root after adding the methodology subtree."
  exit 1
fi

echo "=== Bootstrapping PRP Methodology (Existing Project) ==="

# Check if .claude exists
if [ ! -d ".claude" ]; then
  echo "Error: .claude directory not found."
  echo "Use bootstrap-new.sh for new projects without existing .claude/ setup."
  exit 1
fi

# Create commands directory if missing
mkdir -p .claude/commands

# Symlink methodology commands (skip existing)
echo "Adding methodology commands..."
for cmd in .prp/commands/*.md; do
  name=$(basename "$cmd")
  if [ -f ".claude/commands/$name" ] || [ -L ".claude/commands/$name" ]; then
    echo "  Skipping $name (already exists)"
  else
    ln -s "../../.prp/commands/$name" ".claude/commands/$name"
    echo "  Added $name"
  fi
done

# Symlink agents (if not already present)
echo "Setting up agents..."
if [ -L ".claude/agents" ] || [ -d ".claude/agents" ]; then
  echo "  Skipping agents (already exists)"
else
  ln -s ../.prp/agents .claude/agents
  echo "  Added agents symlink"
fi

# Symlink skills (if not already present)
echo "Setting up skills..."
mkdir -p .claude/skills
if [ -L ".claude/skills/prp-methodology" ]; then
  echo "  Skipping prp-methodology (already exists)"
else
  ln -s ../../.prp/skills/prp-methodology .claude/skills/prp-methodology
  echo "  Added prp-methodology skill"
fi

if [ -L ".claude/skills/error-handling" ]; then
  echo "  Skipping error-handling (already exists)"
else
  ln -s ../../.prp/skills/error-handling .claude/skills/error-handling
  echo "  Added error-handling skill"
fi

# Create features directory if missing
echo "Setting up features..."
mkdir -p features/archive
if [ -f "features/progress.txt" ]; then
  echo "  Skipping progress.txt (already exists)"
else
  cp .prp/templates/progress.template.txt features/progress.txt
  echo "  Created progress.txt"
fi

echo ""
echo "=== Bootstrap Complete ==="
echo ""
echo "Methodology commands added to your existing .claude/ setup."
echo ""
echo "You may want to update your CLAUDE.md to add:"
echo "  ## Workflow"
echo "  See \`.prp/instructions/WORKFLOW.md\` for methodology."
echo "  Commands: /prime -> /plan-feature -> /execute -> /validate -> /commit"
echo ""
echo "Then start Claude Code and run:"
echo "  /prd              - Create PRD for existing project"
echo "  /prime            - Verify setup"
echo ""
