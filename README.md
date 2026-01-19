# PRP Methodology

Language-agnostic AI coding methodology for Claude Code.

## Quick Start (New Project)

```bash
# Option A: One-command setup
mkdir my-project && cd my-project
curl -O https://raw.githubusercontent.com/matscarrgard/prp-methodology/main/init.sh
chmod +x init.sh && ./init.sh

# Option B: Manual setup
mkdir my-project && cd my-project
git init && git commit --allow-empty -m "Initial commit"
git remote add prp-method https://github.com/matscarrgard/prp-methodology.git
git subtree add --prefix=.prp prp-method main --squash
.prp/scripts/bootstrap-new.sh
```

Then in Claude:
```
/prd              # Create PRD from inputs or conversation
/init-project     # Add language boilerplate (optional)
/scaffold         # Create project structure (if boilerplate added)
```

## Adding to Existing Project

```bash
# 1. Add methodology subtree
cd existing-project
git remote add prp-method https://github.com/matscarrgard/prp-methodology.git
git subtree add --prefix=.prp prp-method main --squash

# 2. Bootstrap (preserves existing .claude/)
.prp/scripts/bootstrap-existing.sh
```

Then in Claude:
```
/prd              # Create PRD documenting existing project
/prime            # Verify setup
```

## Workflow

### New Project
```
/prd [inputs/]    → Create PRD from notes/requirements
/scaffold         → Create project structure (language-specific)
/plan-feature     → Plan first feature from PRD
/execute          → Implement
/validate         → Test
/commit           → Ship
```

### Adding Features
```
/prime            → Load context (checks PRD, progress.txt)
/plan-feature     → Plan feature (from PRD or description)
/execute          → Implement
/validate         → Test
/commit           → Ship
```

## Commands

| Command | Purpose |
|---------|---------|
| `/prd` | Create/update PRD from inputs or conversation |
| `/init-project` | Wire methodology + add language boilerplate |
| `/scaffold` | Create project structure (language-specific) |
| `/prime` | Load project context |
| `/plan-feature` | Plan a feature |
| `/execute` | Execute implementation plan |
| `/validate` | Run tests and lint |
| `/commit` | Create git commit |
| `/debug` | Debug issues |
| `/code-review` | Review recent changes |

## Structure

```
.prp/
├── commands/           # Slash commands
├── skills/             # Auto-applied knowledge
│   ├── prp-methodology/
│   └── error-handling/
├── agents/             # Specialized sub-agents
├── hooks/              # Safety hooks (bash validation)
├── instructions/       # Methodology docs
├── templates/          # Starter files
├── scripts/
│   ├── bootstrap-new.sh      # For new projects
│   └── bootstrap-existing.sh # For existing projects
├── .claude-template/   # Pre-configured .claude/ for bootstrap
└── features-template/  # Pre-configured features/ for bootstrap
```

## Memory System

| Tier | File | Purpose |
|------|------|---------|
| Long-term | `CLAUDE.md` | Project conventions, commands |
| Medium-term | `features/progress.txt` | Feature learnings, patterns |
| Short-term | Plan file | Current task status |

## Available Boilerplates

| Language | Repository | Status |
|----------|------------|--------|
| Python | `matscarrgard/python-boilerplate` | Available |
| Flutter | `matscarrgard/boilerplate-flutter` | Available |
| React | - | Coming soon |
| Go | - | Coming soon |

Boilerplates are added as subtrees (`.boilerplate-python/`, `.boilerplate-flutter/`) and files are copied to root.
This keeps your project decoupled while allowing template updates.

## Updating Templates

Methodology (`.prp/`) and boilerplates are git subtrees.

```bash
# Pull latest methodology
git subtree pull --prefix=.prp prp-method main --squash

# Pull latest Python boilerplate (if present)
git subtree pull --prefix=.boilerplate-python py-boilerplate main --squash

# Pull latest Flutter boilerplate (if present)
git subtree pull --prefix=.boilerplate-flutter flutter-boilerplate main --squash
```

To push improvements back:

```bash
# Push methodology improvements
git subtree push --prefix=.prp prp-method main

# Push Python boilerplate improvements
git subtree push --prefix=.boilerplate-python py-boilerplate main

# Push Flutter boilerplate improvements
git subtree push --prefix=.boilerplate-flutter flutter-boilerplate main
```

**Note**: Always pull before making changes to avoid conflicts.

## Key Files

- **PRD**: `docs/agents/prd.md` - Project scope and feature list
- **Progress**: `features/progress.txt` - Iteration memory
- **Features**: `features/F####-name/` - Per-feature folders containing:
  - `F####-spec.md` - Feature specification
  - `F####-plan.md` - Implementation plan
  - `F####-tracking.yaml` - Story tracking for Ralph
- **CLAUDE.md**: Project-specific config and commands
