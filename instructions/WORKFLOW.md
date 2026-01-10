# PRP Workflow Guide

The Plan-Implement-Validate (PIV) loop for AI-assisted development.

## Core Philosophy

> "One context window, one goal."

Each context window should focus on a single objective:
- **Planning context**: Explore, design, create plan
- **Execution context**: Implement plan, fresh start
- **Review context**: Analyze changes, suggest improvements

Don't mix planning and execution in the same context - it leads to confusion.

## The PIV Loop

```
┌─────────────────────────────────────────────────────────┐
│                                                          │
│   ┌──────────┐    ┌─────────────┐    ┌──────────────┐   │
│   │   PLAN   │───>│  IMPLEMENT  │───>│   VALIDATE   │   │
│   └──────────┘    └─────────────┘    └──────────────┘   │
│        │                                    │            │
│        │         ┌──────────────┐          │            │
│        └────────>│    COMMIT    │<─────────┘            │
│                  └──────────────┘                        │
│                        │                                 │
│                        ▼                                 │
│                  [Next Feature]                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Standard Workflow

### 1. Start Session

```bash
/prime  # Load project context
```

Check `features/progress.txt` and `features/current.json` for active work.

### 2. Plan Feature

```bash
/plan-feature "Add user authentication with JWT"
```

This creates:
- Implementation plan at `docs/plans/NNNN-feature-name.md`
- Breaks feature into sized stories
- Identifies patterns to follow

**Wait for human approval before proceeding.**

### 3. Context Reset

Before execution, clear your context:
- Use `/clear` command
- Or start a new conversation

Why? Planning fills context with exploration. Execution needs clean space.

### 4. Execute Plan

```bash
/execute docs/plans/0001-user-auth.md
```

This:
- Creates rollback checkpoint
- Works through each task
- Updates plan with progress
- Commits working increments

### 5. Validate

```bash
/validate
```

Runs:
- Tests
- Linting
- Type checking (if applicable)

### 6. Commit

```bash
/commit
```

Creates well-formatted commit message following conventions.

## Memory System

### Three Tiers

```
┌────────────────────────────────────────────────────┐
│  TIER 1: Long-Term (CLAUDE.md)                     │
│  ─────────────────────────────                     │
│  • Project conventions                              │
│  • Tech stack                                       │
│  • Patterns that benefit ALL work                   │
│  • Updated rarely                                   │
├────────────────────────────────────────────────────┤
│  TIER 2: Medium-Term (features/progress.txt)       │
│  ────────────────────────────────────────          │
│  • Codebase patterns for current feature            │
│  • Iteration history with learnings                 │
│  • READ FIRST each iteration                        │
│  • Updated after each story                         │
├────────────────────────────────────────────────────┤
│  TIER 3: Short-Term (Plan file)                    │
│  ─────────────────────────────                     │
│  • Current tasks with status                        │
│  • Story notes and blockers                         │
│  • Updated during execution                         │
└────────────────────────────────────────────────────┘
```

### When to Update Each Tier

| Event | Update |
|-------|--------|
| Discover pattern useful for THIS feature | progress.txt Codebase Patterns |
| Discover pattern useful for ALL features | CLAUDE.md |
| Complete a story | progress.txt Iteration Log |
| Hit a blocker | Plan file + progress.txt |

## Autonomous Execution (Ralph)

For autonomous loops, use the plan-executor agent:

```bash
# Start Ralph loop
./ralph.sh 15  # max 15 iterations
```

Each iteration:
1. Reads progress.txt (Codebase Patterns FIRST)
2. Reads plan for next pending task
3. Executes single story
4. Updates memory
5. Commits if successful
6. Checks for completion

## Error Recovery

### Rollback Execution

```bash
git reset --hard HEAD~1  # Rollback to pre-execute checkpoint
```

### Review Failed Iteration

Check `features/progress.txt` for failure notes.

### Resume After Fix

```bash
/execute  # Continues from where it left off
```

## Best Practices

### Do
- Clear context between planning and execution
- Read progress.txt FIRST each iteration
- Commit working increments
- Document learnings immediately
- Keep stories small (1-3 iterations)

### Don't
- Mix planning and execution in same context
- Skip reading memory files
- Commit broken code
- Make unrelated changes
- Forget to update memory

## Command Reference

| Command | Purpose |
|---------|---------|
| `/prime` | Load project context |
| `/prd` | Create PRD from conversation |
| `/plan-feature` | Create implementation plan |
| `/execute` | Execute plan with memory |
| `/validate` | Run validation suite |
| `/commit` | Git commit workflow |
| `/code-review` | Review recent changes |
| `/debug` | Debug issues |
