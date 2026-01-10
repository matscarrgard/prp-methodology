# Ralph Iteration Prompt

Execute a SINGLE task from the current plan. One task per iteration, fresh context each time.

## Context Loading (IN THIS ORDER)

1. **Read `features/progress.txt`** - Codebase Patterns section FIRST
   - These are learnings from previous iterations
   - Apply them to avoid repeating mistakes

2. **Read `TODO.md`** - Find current plan file path

3. **Read the plan file** - Find next pending task
   - Look for first unchecked task `- [ ]`
   - If all tasks done → output `FEATURE_COMPLETE`

4. **Read `CLAUDE.md`** - Project conventions and patterns

## Execution Process

### 1. Select Task
- Find first incomplete task in plan
- If ALL tasks complete → output `FEATURE_COMPLETE`
- If ALL remaining tasks blocked → output `ALL_BLOCKED`

### 2. Implement
- Follow patterns from CLAUDE.md
- Apply learnings from progress.txt Codebase Patterns
- Keep changes focused on JUST this task

### 3. Verify
- Run lint/test commands from plan's Validation section
- Fix any failures (up to 3 attempts)

### 4. On SUCCESS
- Mark task complete in plan file `- [x]`
- Commit: `git add -A && git commit -m "feat(scope): task description"`
- Update progress.txt with learnings
- Output `STORY_COMPLETE`

### 5. On FAILURE (3 attempts)
- Do NOT commit broken code
- Document blocker in progress.txt
- Output `STORY_BLOCKED`

## Memory Updates (REQUIRED)

After EVERY task, append to `features/progress.txt`:

```markdown
### Iteration N - YYYY-MM-DD HH:MM
**Task**: [task number] - [task title]
**Status**: complete | blocked
**Learnings**:
- [what was discovered that helps future iterations]
**Files Changed**:
- [list of files]
**Commit**: [hash] (if complete)
```

If you discover a REUSABLE pattern, add it to the "Codebase Patterns" section at the TOP of progress.txt.

## Completion Markers

Output EXACTLY ONE at the end:

| Marker | When |
|--------|------|
| `STORY_COMPLETE` | Task done, ready for next iteration |
| `STORY_BLOCKED` | Cannot complete after 3 attempts |
| `FEATURE_COMPLETE` | ALL tasks in plan are done |
| `ALL_BLOCKED` | All remaining tasks are blocked |

## Rules

- ONE task per iteration (fresh context next time)
- ALWAYS read progress.txt Codebase Patterns FIRST
- ALWAYS update progress.txt after task
- NEVER commit broken code
- NEVER skip tasks
- STAY FOCUSED on the single task
