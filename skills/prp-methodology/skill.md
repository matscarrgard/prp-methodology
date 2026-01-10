---
name: prp-methodology
description: PRP (Plan-Review-Progress) methodology for feature development. Use when planning features, executing stories, tracking progress, or running Ralph loops.
---

# PRP Methodology

## Core Workflow (PIV Loop)

```
Plan → Implement → Validate → (repeat or commit)
```

**Commands:**
- `/prime` - Load project context
- `/plan-feature <desc>` - Create implementation plan
- `/execute [plan]` - Execute plan with memory
- `/validate` - Run tests and lint
- `/commit` - Create git commit

## Story Sizing (Critical)

Stories MUST be:
- Describable in 2-3 sentences
- Completable in ONE context window
- Have checkable acceptance criteria ("tests pass", not "looks good")

**If a story feels big, SPLIT IT.**

Good story sizes:
- Add single endpoint with tests
- Add single model with migration
- Add single UI component
- Fix specific bug with test

Bad story sizes:
- "Add user authentication" (too broad)
- "Refactor the database layer" (too vague)
- "Make it faster" (no clear criteria)

## Three-Tier Memory System

### Tier 1: Long-Term (CLAUDE.md)
- Project conventions
- Tech stack
- Reusable patterns discovered
- **Updated rarely** - only for patterns that benefit ALL future work

### Tier 2: Medium-Term (features/progress.txt)
- Codebase patterns discovered during feature
- Iteration log with learnings
- **READ THIS FIRST** each iteration
- **Updated after each story** - capture learnings immediately

### Tier 3: Short-Term (Plan file)
- Current tasks with status
- Story notes and blockers
- **Updated during execution**

## Progress File Structure

```markdown
## Codebase Patterns
<!-- Read FIRST - learnings from iterations -->
- Pattern 1 discovered
- Pattern 2 discovered

---

## Current: [feature-name]
Branch: feature/xyz
Started: [date]

---

## Iteration Log

### Iteration 1 - [timestamp]
**Task**: [description]
**Status**: complete
**Learnings**: [what was discovered]
**Files**: [list of files changed]
```

## Task Status Values

- `pending` - Not started
- `in_progress` - Currently working
- `complete` - Done and verified
- `blocked` - Cannot proceed (add notes explaining why)

## Context Reset Pattern

**Between planning and execution:**
1. Complete planning phase with `/plan-feature`
2. Clear context (`/clear` or new conversation)
3. Start execution with `/execute` - reads plan fresh

**Why:** Planning fills context with exploration. Execution needs clean context for implementation.

## Ralph Loop Process

For autonomous execution:

1. **Read state** (every iteration):
   - `features/progress.txt` (Codebase Patterns FIRST)
   - Current plan for next pending task
   - `CLAUDE.md` for project conventions

2. **Execute single story:**
   - Implement per acceptance criteria
   - Run verification (tests, lint)
   - Handle failures (fix or mark blocked)

3. **Update memory:**
   - Update task status in plan
   - Append learnings to progress.txt
   - Commit if complete

4. **Check completion:**
   - All tasks done? → `FEATURE_COMPLETE`
   - Blocked with no pending? → `BLOCKED`
   - Max iterations? → `MAX_ITERATIONS`
   - Otherwise → Continue

**Safety:** Always set max iterations (default: 15)

## One Context Window = One Goal

> "If you ask it to do too much in the working context, some results are going to be dumb."

- One feature per context window
- One story per Ralph iteration
- Clear context between major phases

## System Evolution

After each feature:
1. Review what went wrong
2. Identify: Missing pattern? Bad process?
3. Update: CLAUDE.md, commands, or guides
4. Prevent: Same issue can't happen again

**Don't just fix bugs. Fix the system that allowed the bug.**
