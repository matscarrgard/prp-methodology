# Code Review

Review recent code changes for quality, security, and project conventions.

## Input

$ARGUMENTS - Optional: specific files or commit range (defaults to uncommitted changes)

## Process

### 1. Get Changes to Review

```bash
# Uncommitted changes
git diff HEAD

# Or specific commit range
git diff <commit-range>
```

### 2. Read Project Context

- Read CLAUDE.md for project conventions
- Check any referenced pattern guides

### 3. Review Changes

For each changed file:

#### Code Quality
- [ ] Functions reasonably sized
- [ ] Clear naming
- [ ] No duplicate code
- [ ] Proper error handling

#### Security
- [ ] No hardcoded secrets
- [ ] Input validation on boundaries
- [ ] No injection vulnerabilities

#### Project Conventions
- [ ] Follows CLAUDE.md patterns
- [ ] Correct file locations
- [ ] Proper naming conventions

#### Tests
- [ ] New code has tests
- [ ] Tests cover edge cases

### 4. Generate Review

Output findings by priority:

```markdown
## Code Review Results

### Critical (must fix before merge)
- `[file:line]` Issue description
  - **Why**: Risk/impact
  - **Fix**: Suggested solution

### Warnings (should fix)
- `[file:line]` Issue description
  - **Fix**: Suggested solution

### Suggestions (consider)
- `[file:line]` Improvement idea

### Positive Notes
- Good patterns observed

## Summary
- Files reviewed: N
- Critical issues: N
- Warnings: N
- **Verdict**: APPROVE / REQUEST_CHANGES / NEEDS_DISCUSSION
```

## Output

A structured code review with:
- Findings categorized by priority
- Specific file:line references
- Actionable fix suggestions
- Overall verdict
