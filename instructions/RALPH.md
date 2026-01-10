# Ralph Wiggum Loop Guide

Autonomous execution loops for completing features.

## What is Ralph?

Ralph is a pattern for autonomous AI coding:
1. Feed prompt to Claude
2. Claude works until it stops
3. Check for completion
4. If not complete, feed same prompt again
5. Repeat until done or max iterations

Named after the Simpsons character who keeps trying until he succeeds.

## Why Ralph?

### Context Window Management

Each iteration gets fresh context. Instead of one long context that degrades:

```
Without Ralph:
[Plan][Impl1][Debug1][Impl2][Debug2][Impl3]...[DUMB ZONE]

With Ralph:
Iteration 1: [Plan][Story1][Commit] → fresh
Iteration 2: [Plan][Story2][Commit] → fresh
Iteration 3: [Plan][Story3][Commit] → fresh
```

### Memory via Files (Three-Tier System)

State persists through files, not context. Based on Carson's pattern:

| Tier | File | Scope | Contains |
|------|------|-------|----------|
| **1** | `CLAUDE.md` | Project-wide | Conventions, patterns, tech stack |
| **2** | `features/progress.txt` | Feature-wide | Codebase patterns, iteration history |
| **3** | Plan file | Task-wide | Story status, acceptance criteria |

Reading order matters: Tier 2 Codebase Patterns → Plan file → CLAUDE.md

Git commits provide atomic rollback points for each completed story.

## Implementation Options

### Option 1: Custom Bash Script (Recommended)

```bash
#!/bin/bash
# ralph.sh - Basic implementation

MAX_ITERATIONS=${1:-15}
ITERATION=0

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    echo "=== Iteration $ITERATION of $MAX_ITERATIONS ==="

    # Run Claude with execute prompt
    claude -p "$(cat ralph-prompt.md)" --print

    # Check for completion markers
    if grep -q "FEATURE_COMPLETE" features/progress.txt; then
        echo "Feature complete!"
        exit 0
    fi

    if grep -q "ALL_BLOCKED" features/progress.txt; then
        echo "All stories blocked."
        exit 1
    fi

    sleep 2
done

echo "Max iterations reached."
exit 2
```

### Option 2: Official Plugin

```bash
/ralph-wiggum:ralph-loop "<prompt>" --max-iterations 15 --completion-promise "COMPLETE"
```

Plugin limitations:
- Uses compaction (loses some context)
- Less control over iteration behavior
- Harder to customize

## Ralph Prompt Template

```markdown
# Ralph Iteration

## Context (Read First)
1. Read `features/progress.txt` - Codebase Patterns section FIRST
2. Read current plan file for next pending task
3. Read `CLAUDE.md` for project conventions

## Task
Execute the SINGLE next pending story. Do not skip ahead.

## Process
1. Find first story with status "pending"
2. Implement following project patterns
3. Run verification commands
4. If pass: Mark complete, commit, update progress.txt
5. If fail (3 attempts): Mark blocked, update progress.txt

## Memory Updates
After EVERY story, append to progress.txt:

```
### Iteration N - [timestamp]
**Story**: [ID] - [title]
**Status**: complete|blocked
**Learnings**: [discoveries]
**Files**: [changed files]
```

## Completion
- Output FEATURE_COMPLETE when all stories done
- Output ALL_BLOCKED when stuck and no pending stories
- Otherwise, stop naturally (loop will restart you)
```

## Safety Controls

### Max Iterations
Always set a limit:
```bash
./ralph.sh 15  # Stop after 15 iterations
```

### Cost Monitoring
Watch API costs. Rough estimates per iteration:

| Task Type | Input Tokens | Output Tokens | Estimated Cost |
|-----------|--------------|---------------|----------------|
| Simple story | ~10K | ~2K | $0.50-1.50 |
| Medium story | ~20K | ~5K | $1.50-3.00 |
| Complex story | ~40K | ~10K | $3.00-6.00 |
| Debug/retry | ~30K | ~8K | $2.00-5.00 |

Full feature estimates (5-10 stories): $15-40

### Checkpoint Commits
Each successful story creates a commit. Rollback is easy:
```bash
git reset --hard HEAD~3  # Rollback last 3 stories
```

### Blocked Detection
Stories mark themselves blocked after 3 attempts. Monitor:
```bash
watch -n 5 cat features/progress.txt
```

## Best Practices

### Story Sizing
Keep stories SMALL for Ralph:
- 1-3 iterations per story
- Clear verification criteria
- Independent (can commit separately)

### Memory Discipline
- Progress.txt Codebase Patterns read FIRST
- Learnings appended IMMEDIATELY after story
- Patterns that help future iterations promoted

### Monitoring
Watch progress in real-time:
```bash
# Terminal 1: Run Ralph
./ralph.sh 20

# Terminal 2: Watch progress
tail -f features/progress.txt

# Terminal 3: Watch git
watch -n 10 'git log --oneline -5'
```

### Human on the Loop
You can be AFK, but:
- Set appropriate max iterations
- Have cost alerts configured
- Check results periodically
- Be ready to `git reset` if needed

## Troubleshooting

### Loop Never Completes
- Check completion marker detection
- Verify marker is written to expected file
- Check for typos in marker string

### Same Error Every Iteration
- Progress.txt not being read first?
- Learnings not being captured?
- Story too big? Split it.

### High Cost, Low Progress
- Stories too big
- Verification criteria unclear
- Too much exploration per iteration

### Thrashing Between States
- Task dependencies unclear
- Acceptance criteria ambiguous
- Split into smaller stories

## Cost Optimization

### Reduce Iterations
- Better story sizing
- Clearer acceptance criteria
- More patterns in progress.txt

### Use Appropriate Model
- Sonnet for simple stories
- Opus for complex logic
- Haiku for validation-only tasks

### Cache Learnings
Good progress.txt reduces repeated mistakes:
```markdown
## Codebase Patterns
- API uses Annotated[T, Depends()] pattern
- All models inherit from Base in core/db.py
- Tests use async fixtures from conftest.py
```

## Example Session

```bash
# 1. Plan the feature
/plan-feature "Add user registration"

# 2. Review and approve plan
# (human reviews docs/plans/0001-user-registration.md)

# 3. Prepare Ralph prompt
cat > ralph-prompt.md << 'EOF'
# Ralph Iteration
[... prompt content ...]
EOF

# 4. Run Ralph
./ralph.sh 20

# 5. Monitor
tail -f features/progress.txt

# 6. Review results
git log --oneline -10
/validate

# 7. If needed, rollback and retry
git reset --hard HEAD~N
```
