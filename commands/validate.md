# Validate Implementation

Run the full validation pyramid on the current codebase.

## Validation Pyramid

| Level | Check | Purpose |
|-------|-------|---------|
| 1 | Lint & Format | Syntax and style |
| 2 | Unit Tests | Logic correctness |
| 3 | Integration Tests | System correctness |
| 4 | Human Review | Final approval |

## Process

### Level 1: Lint & Format

Run the project's lint command (defined in CLAUDE.md or project config).

Report any issues found.

### Level 2: Unit Tests

Run unit tests with verbose output.

Report test results, focusing on any failures.

### Level 3: Integration Tests

Run integration tests (if they exist).

Report integration test results.

### Level 4: Human Review Preparation

**Get changes since last commit:**
```bash
git diff --stat
git diff --name-only
```

Provide a structured summary:

```markdown
## Validation Results

### Lint & Format
- Status: PASS/FAIL
- Issues: [count]

### Unit Tests
- Status: PASS/FAIL
- Passed: X, Failed: Y, Skipped: Z

### Integration Tests
- Status: PASS/FAIL (or SKIPPED if none)
- Passed: X, Failed: Y, Skipped: Z

### Files Changed (for human review)
[List from git diff --name-only]

### Changes Summary
[Brief description of what changed - based on git diff]

### Recommended Next Steps
- [ ] Review the diff in detail
- [ ] Manual smoke test
- [ ] Approve or request changes
```

## Error Recovery

If validation reveals problems that require rollback:
```bash
# See what would be undone
git diff HEAD~1

# Rollback to pre-execute checkpoint
git reset --hard HEAD~1
```

## Output

A validation report with pass/fail status for each level and recommendations for human review.
