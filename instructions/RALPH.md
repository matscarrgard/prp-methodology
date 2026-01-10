# Ralph Wiggum Loop Guide

Autonomous execution loops for completing features.

## What is Ralph?

Ralph is a pattern for autonomous AI coding:
1. Feed prompt to Claude
2. Claude works on ONE story until it stops
3. Check feature YAML for completion status
4. If not complete, feed same prompt again
5. Repeat until done or max iterations

Named after the Simpsons character who keeps trying until he succeeds.

## Why Ralph?

### Context Window Management

Each iteration gets fresh context. Instead of one long context that degrades:

```
Without Ralph:
[Plan][Story1][Debug1][Story2][Debug2][Story3]...[DUMB ZONE]

With Ralph:
Iteration 1: [Read][Story1][Commit] → fresh
Iteration 2: [Read][Story2][Commit] → fresh
Iteration 3: [Read][Story3][Commit] → fresh
```

### Memory via Files (Three-Tier System)

State persists through files, not context:

| Tier | File | Scope | Contains |
|------|------|-------|----------|
| **1** | `CLAUDE.md` | Project-wide | Conventions, patterns, tech stack |
| **2** | `features/progress.txt` | Feature-wide | Codebase patterns, iteration history |
| **3** | `features/F####-name.yaml` | Story-level | Status, criteria, per-story notes |

Reading order matters: Tier 2 Codebase Patterns → Feature YAML → Plan file → CLAUDE.md

## File Structure

```
features/
├── F0001-epub-parsing.yaml    # Story tracking (status, notes)
├── progress.txt               # Iteration memory
└── specs/                     # Optional feature specs
    └── F0001-epub-parsing.md

docs/agents/plans/
└── F0001-epub-parsing.md      # Detailed implementation plan
```

## Feature YAML Format

```yaml
id: F0001
name: EPUB Parsing Service
branch: feature/epub-parsing
plan: docs/agents/plans/F0001-epub-parsing.md
created: 2025-01-10

validation:
  lint: uv run ruff check src/ --fix
  test: uv run pytest tests/ -x

stories:
  - id: F0001-01
    title: Add EPUB exceptions
    criteria:
      - EPUBError base class exists
      - Lint passes
    priority: 1
    status: complete           # pending | complete | blocked
    attempts: 1
    notes: "Used AppError pattern from core/"

  - id: F0001-02
    title: Create data models
    criteria:
      - BookMetadata dataclass
      - Chapter dataclass
    priority: 2
    status: pending
    attempts: 0
    notes: ""
```

## Running Ralph

```bash
# Basic usage (auto-detects feature file)
.prp/scripts/ralph.sh

# With max iterations
.prp/scripts/ralph.sh 20

# With specific feature file
.prp/scripts/ralph.sh 15 features/F0001-epub-parsing.yaml
```

### Prerequisites

1. Feature YAML at `features/F####-*.yaml`
2. Plan file referenced in YAML
3. `ralph-prompt.md` in project root (copy from `.prp/templates/ralph-prompt.template.md`)
4. Git repository initialized

## Story Status Flow

```
pending → in_progress → complete
                    ↘ blocked (after 3 attempts)
```

Ralph checks status via `.prp/scripts/feature-status.py`:
- `all-done`: All stories complete → exit loop
- `all-blocked`: All remaining blocked → exit with error
- `next`: Get next pending story ID

## Safety Controls

### Max Iterations
Always set a limit:
```bash
./ralph.sh 15  # Stop after 15 iterations
```

### Cost Monitoring
Rough estimates per iteration:

| Story Size | Input Tokens | Output Tokens | Cost |
|------------|--------------|---------------|------|
| Simple | ~10K | ~2K | $0.50-1.50 |
| Medium | ~20K | ~5K | $1.50-3.00 |
| Complex | ~40K | ~10K | $3.00-6.00 |

Full feature (5-10 stories): $15-40

### Checkpoint Commits
Each successful story creates a commit. Rollback is easy:
```bash
git reset --hard HEAD~3  # Rollback last 3 stories
```

### Blocked Detection
Stories mark themselves blocked after 3 attempts:
```yaml
- id: F0001-05
  status: blocked
  attempts: 3
  notes: "Cannot resolve circular import. Tried X, Y, Z."
```

## Best Practices

### Story Sizing
Keep stories SMALL for Ralph:
- 1-3 iterations per story
- Clear acceptance criteria
- Independent (can commit separately)
- 2-3 sentence description max

### Memory Discipline
- Progress.txt Codebase Patterns read FIRST
- Learnings appended IMMEDIATELY after story
- Story notes updated in YAML
- Reusable patterns promoted to progress.txt top

### Monitoring
Watch progress in real-time:
```bash
# Terminal 1: Run Ralph
.prp/scripts/ralph.sh 20

# Terminal 2: Watch progress
tail -f features/progress.txt

# Terminal 3: Check status
.prp/scripts/feature-status.py status
```

### Human on the Loop
You can be AFK, but:
- Set appropriate max iterations
- Have cost alerts configured
- Check results periodically
- Be ready to `git reset` if needed

## Troubleshooting

### Loop Never Completes
- Check feature YAML status updates
- Verify criteria are checkable
- Story might be too big → split it

### Same Error Every Iteration
- Progress.txt not being read first?
- Learnings not being captured in notes?
- Story too big? Split it.

### High Cost, Low Progress
- Stories too big
- Criteria unclear or untestable
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
Good Codebase Patterns reduce repeated mistakes:
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

# 2. Review and approve plan (human reviews)
# Plan created at: docs/agents/plans/F0002-user-registration.md
# YAML created at: features/F0002-user-registration.yaml

# 3. Copy Ralph prompt template
cp .prp/templates/ralph-prompt.template.md ralph-prompt.md

# 4. Run Ralph
.prp/scripts/ralph.sh 20

# 5. Monitor
.prp/scripts/feature-status.py status
tail -f features/progress.txt

# 6. Review results
git log --oneline -10
/validate

# 7. If needed, rollback and retry
git reset --hard HEAD~N
```

## Helper Commands

```bash
# Check feature status
.prp/scripts/feature-status.py status

# Get next pending story
.prp/scripts/feature-status.py next

# Count by status
.prp/scripts/feature-status.py pending
.prp/scripts/feature-status.py complete
.prp/scripts/feature-status.py blocked

# Check if done
.prp/scripts/feature-status.py all-done && echo "Complete!"
```
