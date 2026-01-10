# Debug Issue

Diagnose and fix a bug or unexpected behavior.

## Input

$ARGUMENTS - Description of the issue, error message, or failing test

## Process

### 1. Capture Error Context

Gather all relevant information:
- Error message and stack trace
- Steps to reproduce
- Expected vs actual behavior
- Recent changes (`git diff HEAD~5`)

### 2. Reproduce the Issue

If possible, create a minimal reproduction:
- Run failing test
- Execute command that fails
- Trigger the error condition

### 3. Analyze

Form hypotheses about root cause.

Common causes by error type:

| Error Type | Common Causes |
|------------|---------------|
| Type errors | Wrong types, null values |
| Not found | Missing resources, wrong paths |
| Connection | Service down, wrong config |
| Validation | Invalid input, schema mismatch |
| Permission | Auth issues, missing access |

### 4. Investigate

Gather evidence to support/refute hypotheses:
- Read relevant code
- Add logging/print statements
- Check config values
- Examine data state

### 5. Fix

Once root cause is identified:
1. Make minimal fix
2. Remove debug statements
3. Run tests

### 6. Verify

- Original issue is resolved
- No regressions introduced
- Tests pass

### 7. Report

```markdown
## Debug Report

### Issue
[Original error/problem]

### Root Cause
[What caused the issue]

### Evidence
[How this was determined]

### Fix
```
[code change]
```

### Verification
- [x] Original issue resolved
- [x] Tests pass
- [x] No regressions

### Prevention
[How to prevent similar issues]
```

## Output

- Root cause identified
- Fix implemented
- Verification passed
- Prevention suggestion (optional)
