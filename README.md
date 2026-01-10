# PRP Methodology

Language-agnostic AI coding methodology for Claude Code.

## Quick Start

```bash
# 1. Create project and add methodology
mkdir my-project && cd my-project
git init
git commit --allow-empty -m "Initial commit"
git remote add prp-method https://github.com/matscarrgard/prp-methodology.git
git subtree add --prefix=.prp prp-method main --squash

# 2. Bootstrap (copies .claude/ and features/)
.prp/scripts/bootstrap.sh

# 3. Start Claude Code
claude

# 4. Create PRD and scaffold (optional: add language boilerplate)
/prd              # Create PRD from inputs or conversation
/init-project     # Wire methodology + optionally add boilerplate
/scaffold         # Create project structure (if boilerplate added)
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
├── scripts/            # Bootstrap, sync helpers
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
| React | - | Coming soon |
| Go | - | Coming soon |

## Updating Methodology

```bash
# Pull latest changes
git subtree pull --prefix=.prp prp-method main --squash

# Push improvements back
git subtree push --prefix=.prp prp-method main
```

## Key Files

- **PRD**: `docs/agents/prd.md` - Project scope and feature list
- **Progress**: `features/progress.txt` - Iteration memory
- **Plans**: `docs/agents/plans/` - Implementation plans
- **CLAUDE.md**: Project-specific config and commands
