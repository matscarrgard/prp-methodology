# Ralph Iteration Prompt

Execute a SINGLE story from the current feature. One story per iteration, fresh context each time.

## Context Loading (IN THIS ORDER)

1. **Read `features/progress.txt`** - Codebase Patterns section FIRST
   - These are learnings from previous iterations
   - Apply them to avoid repeating mistakes

2. **Read the feature tracking YAML** - Find at `features/F####-*/F####-tracking.yaml`
   - Find the first story with `status: pending`
   - Read its `criteria` for acceptance requirements
   - Check `notes` field for any context from previous attempts

3. **Read the plan file** - Path is in the feature YAML's `plan` field
   - Find the detailed task breakdown for the current story
   - Follow the implementation guidance

4. **Read `CLAUDE.md`** - Project conventions and patterns

## Execution Process

### 1. Select Story
- Find first story in feature YAML with `status: pending`
- If ALL stories have `status: complete` → output `FEATURE_COMPLETE`
- If ALL remaining stories have `status: blocked` → output `ALL_BLOCKED`

### 2. Implement + Test
- Follow patterns from CLAUDE.md
- Apply learnings from progress.txt Codebase Patterns
- Keep changes focused on JUST this story
- **Write tests for this story** - each story should have its own tests
- Check the story's `criteria` - each must be satisfied

**Testing Guidelines (avoid over-testing):**
- Test the **contract**, not the implementation
- Happy path + key error cases only (validation errors, not found, edge cases)
- 1-2 tests per simple class (e.g., exceptions, dataclasses)
- Use **parameterized tests** for similar cases (e.g., multiple aspect ratios = 1 test, not 7)
- Skip integration tests if unit tests already cover the logic
- Internal code needs less testing than system boundaries
- Aim for ~10-15 tests per story, not 25+

### 3. Verify
- Run **story-specific tests first** (from criteria, e.g., `pytest tests/ -k "test_story_name"`)
- Run validation commands from the feature YAML's `validation` section (lint, full test suite)
- Fix any failures (up to 3 attempts)

**Testing Rule**: Don't defer tests to a later story. Each story is verified independently.

### 4. On SUCCESS
Update the feature YAML:
```yaml
- id: F0001-03
  status: complete          # Change from pending
  attempts: 1               # Number of attempts taken
  notes: "Used X pattern, discovered Y"  # What you learned
```

Then:
- Commit: `git add -A && git commit -m "feat(F0001-03): story title"`
- Update progress.txt with learnings
- Output `STORY_COMPLETE`

### 5. On FAILURE (after 3 attempts)
Update the feature YAML:
```yaml
- id: F0001-03
  status: blocked           # Change from pending
  attempts: 3
  notes: "Blocked because X. Tried Y and Z."
```

Then:
- Do NOT commit broken code
- Document blocker in progress.txt
- Output `STORY_BLOCKED`

## Memory Updates (REQUIRED)

After EVERY story, append to `features/progress.txt`:

```markdown
### Iteration N - YYYY-MM-DD HH:MM
**Story**: F0001-03 - Story title
**Status**: complete | blocked
**Learnings**:
- [what was discovered that helps future iterations]
**Files Changed**:
- [list of files]
**Commit**: [hash] (if complete)
```

If you discover a REUSABLE pattern, add it to the "Codebase Patterns" section at the TOP of progress.txt.

## Feature YAML Updates

Always update the story in the feature YAML file:
- `status`: pending → complete | blocked
- `attempts`: increment on each attempt
- `notes`: add learnings specific to this story

Example:
```yaml
stories:
  - id: F0001-01
    title: Add user model
    status: complete
    attempts: 1
    notes: "Used existing Base class pattern from core/db.py"
```

## Completion Markers

Output EXACTLY ONE at the end of your work:

| Marker | When |
|--------|------|
| `STORY_COMPLETE` | Story done, ready for next iteration |
| `STORY_BLOCKED` | Cannot complete after 3 attempts |
| `FEATURE_COMPLETE` | ALL stories in feature YAML are complete |
| `ALL_BLOCKED` | All remaining stories are blocked |

## Rules

- ONE story per iteration (fresh context next time)
- ALWAYS read progress.txt Codebase Patterns FIRST
- ALWAYS update both feature YAML and progress.txt after story
- NEVER commit broken code
- NEVER skip stories (do them in priority order)
- STAY FOCUSED on the single story
- INCREMENT attempts count on each try
- MARK blocked after 3 failed attempts

## On Feature Completion

When outputting `FEATURE_COMPLETE` or `ALL_BLOCKED`:
1. **Archive the Ralph log** to the feature folder:
   ```bash
   cp ralph.log features/F####-*/F####-ralph.log
   ```
2. Output the marker and a brief summary
3. Do NOT attempt to plan or start the next feature
4. Do NOT ask questions or request input
5. Stop immediately - the outer loop will handle next steps

## E2E Validation (After Feature Completion)

After the outer loop receives `FEATURE_COMPLETE`, it should trigger E2E validation:

1. **Run automated E2E tests** (if any exist for the feature):
   ```bash
   uv run pytest tests/e2e/ --e2e -x
   ```

2. **Run interactive UI validation** using `/validate-ui`:
   - Tests functional flows with Playwright MCP
   - Critically evaluates design quality
   - Generates report with screenshots

3. **If issues found**: Create follow-up feature (e.g., F0004b) for fixes

See `.prp/commands/validate-ui.md` for the interactive validation process.
