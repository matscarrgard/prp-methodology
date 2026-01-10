# Execution Report

Generate a detailed report of what was accomplished during execution.

## Input

$ARGUMENTS - Optional: path to completed plan or "recent" for last session

## Process

### 1. Gather Execution Data

Read:
- Completed plan file (if specified)
- Recent git commits
- features/progress.txt (if exists)

### 2. Analyze Changes

```bash
# Recent commits
git log --oneline -10

# Files changed
git diff HEAD~N --stat

# Detailed changes (if needed)
git diff HEAD~N
```

### 3. Compile Statistics

- Commits created
- Files created/modified/deleted
- Lines added/removed
- Tests added/modified

### 4. Generate Report

```markdown
## Execution Report

**Date**: [date]
**Feature/Plan**: [name or description]

---

### Summary

[Brief description of what was accomplished]

### Commits

| Hash | Message |
|------|---------|
| abc123 | feat: description |
| def456 | fix: description |

### Files Changed

**Created:**
- path/to/new/file.py

**Modified:**
- path/to/modified/file.py

**Deleted:**
- path/to/old/file.py

### Statistics

- Files: +N created, ~N modified, -N deleted
- Lines: +N added, -N removed
- Tests: +N added

### Validation Results

- Lint: PASS/FAIL
- Tests: PASS/FAIL (X passed, Y failed)

### Learnings

[Key discoveries from features/progress.txt]

### Follow-up Items

- [ ] [Any remaining work]
- [ ] [Future improvements identified]

---

### Appendix: Detailed Changes

[Optional: Include detailed diff summary]
```

## Output

A comprehensive execution report suitable for:
- Team communication
- Documentation
- Future reference
