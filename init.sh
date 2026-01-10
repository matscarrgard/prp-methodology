#!/bin/bash
# PRP Methodology - Project Initializer
#
# Usage:
#   mkdir my-project && cd my-project
#   curl -O https://raw.githubusercontent.com/matscarrgard/prp-methodology/main/init.sh
#   chmod +x init.sh && ./init.sh

set -e

echo "=== PRP Methodology - Project Initializer ==="
echo ""

# Check if already initialized
if [ -d ".prp" ]; then
  echo "Error: .prp directory already exists. Project already initialized."
  exit 1
fi

# Get project name
DEFAULT_NAME=$(basename "$(pwd)")
read -p "Project name [$DEFAULT_NAME]: " PROJECT_NAME
PROJECT_NAME=${PROJECT_NAME:-$DEFAULT_NAME}

echo ""
echo "Initializing project: $PROJECT_NAME"
echo ""

# Step 1: Initialize git
if [ ! -d ".git" ]; then
  echo "→ Initializing git..."
  git init
else
  echo "→ Git already initialized"
fi

# Step 2: Create initial commit if needed
if ! git rev-parse HEAD >/dev/null 2>&1; then
  echo "→ Creating initial commit..."
  git commit --allow-empty -m "Initial commit for $PROJECT_NAME"
else
  echo "→ Initial commit exists"
fi

# Step 3: Add methodology subtree
echo "→ Adding PRP methodology..."
git remote add prp-method https://github.com/matscarrgard/prp-methodology.git 2>/dev/null || true
git subtree add --prefix=.prp prp-method main --squash

# Step 4: Bootstrap
echo "→ Running bootstrap..."
.prp/scripts/bootstrap.sh

# Step 5: Clean up init script
echo "→ Cleaning up..."
rm -f init.sh

# Done
echo ""
echo "=== Project Initialized! ==="
echo ""
echo "Next steps:"
echo "  1. Start Claude Code:  claude"
echo "  2. Create your PRD:    /prd"
echo "  3. Add boilerplate:    /init-project"
echo "  4. Scaffold project:   /scaffold"
echo ""
echo "Or if you have input files:"
echo "  /prd inputs/           # Create PRD from notes"
echo ""
