# PRP Methodology

Language-agnostic AI coding methodology for Claude Code.

## Quick Start

```bash
# Add to existing project
git remote add prp-method git@github.com:yourorg/prp-methodology.git
git subtree add --prefix=.prp prp-method main --squash

# Wire Claude Code
ln -s ../.prp/commands .claude/commands
ln -s ../.prp/agents .claude/agents
ln -s ../.prp/skills .claude/skills

# Initialize features
mkdir -p features
cp .prp/templates/progress.template.txt features/progress.txt
```

## Components

```
prp-methodology/
├── commands/           # Claude Code slash commands
│   ├── prime.md        # Load project context
│   ├── plan-feature.md # Create implementation plan
│   └── execute.md      # Execute plan with memory
│
├── skills/             # Auto-applied knowledge
│   ├── prp-methodology/
│   └── error-handling/
│
├── agents/             # Specialized sub-agents
│   ├── code-reviewer.md
│   ├── test-writer.md
│   ├── debugger.md
│   └── plan-executor.md
│
├── hooks/              # Claude Code hooks
│   └── validate-bash.py
│
├── instructions/       # Methodology docs
│   ├── WORKFLOW.md     # PIV loop
│   ├── STORY_SIZING.md # How to size stories
│   └── RALPH.md        # Autonomous loops
│
├── templates/          # Starter files
│   ├── CLAUDE.template.md
│   ├── progress.template.txt
│   ├── plan.template.md
│   └── feature.template.json
│
└── scripts/            # Automation
    ├── ralph.sh        # Bash Ralph loop
    └── prp-sync        # Subtree management
```

## Core Workflow (PIV Loop)

```
Plan → Implement → Validate → Commit
```

1. `/prime` - Load project context
2. `/plan-feature "description"` - Create plan
3. `/execute` - Implement plan (after context reset)
4. `/validate` - Run tests and lint
5. `/commit` - Create commit

## Memory System

| Tier | File | Purpose |
|------|------|---------|
| Long-term | CLAUDE.md | Project conventions |
| Medium-term | features/progress.txt | Feature learnings |
| Short-term | Plan file | Current task status |

## Ralph Loops

For autonomous execution:

```bash
./ralph.sh 15  # Run up to 15 iterations
```

See `instructions/RALPH.md` for details.

## Managing Updates

```bash
# Helper script
./prp-sync status   # Check current state
./prp-sync pull     # Pull updates
./prp-sync push     # Push improvements
```

Or manually:
```bash
git subtree pull --prefix=.prp prp-method main --squash
```
