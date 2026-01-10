# Code Review Fix

Address issues from a code review systematically.

## Input

$ARGUMENTS - Optional: path to review file or specific issues to address

## Process

### 1. Load Review

If review was saved to a file, read it.
Otherwise, ask user to paste or describe the review findings.

### 2. Categorize Issues

Group issues by:
- **Critical**: Must fix (security, bugs)
- **Warnings**: Should fix (quality issues)
- **Suggestions**: Nice to have

### 3. Plan Fixes

For each issue:
1. Understand the problem
2. Identify the fix location
3. Determine if fix affects other code

### 4. Fix Issues

Address issues in priority order:

1. **Critical issues first**
   - Fix each critical issue
   - Verify fix is correct
   - Run relevant tests

2. **Warning issues**
   - Fix each warning
   - Verify fix is correct

3. **Suggestions** (if time allows)
   - Apply reasonable suggestions
   - Skip if too invasive

### 5. Validate

After all fixes:
- Run project lint/format
- Run tests
- Verify no regressions

### 6. Report

```markdown
## Review Fixes Applied

### Critical Issues
- [x] `[file:line]` Issue - Fixed by: [description]
- [x] `[file:line]` Issue - Fixed by: [description]

### Warnings
- [x] `[file:line]` Issue - Fixed by: [description]
- [ ] `[file:line]` Issue - Skipped: [reason]

### Suggestions
- [x] Applied: [description]
- [ ] Skipped: [reason]

### Validation
- Lint: PASS/FAIL
- Tests: PASS/FAIL

### Files Changed
- [list]
```

## Output

- All critical issues addressed
- Warning issues addressed (or justified skips)
- Validation passing
- Ready for re-review or merge
