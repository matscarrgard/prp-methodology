# Feature: F0000 - [NAME]

> Feature Spec: `features/F0000-name/F0000-spec.md`
> Story Tracking: `features/F0000-name/F0000-tracking.yaml`

## Problem Statement

[What problem does this solve? Why is it needed?]

## Solution Overview

[High-level approach in 2-3 sentences]

## Success Criteria

- [ ] [Specific, testable criterion]
- [ ] [Specific, testable criterion]
- [ ] All tests pass
- [ ] No lint errors

## Context & References

- Pattern to follow: [link to similar feature or example]
- Documentation: [relevant docs URLs]
- Gotchas: [known issues to avoid]

## Patterns Reference

> Code snippets from guides - use these exact APIs during implementation.

### [Category] (from [guide])
```
[relevant code patterns]
```

## Files to Create/Modify

| File | Action | Purpose |
|------|--------|---------|
| `path/to/file` | Create | [purpose] |
| `path/to/other` | Modify | [what changes] |

## Implementation Stories

> Each story maps to an entry in the feature YAML.
> Stories should be completable in 1-3 iterations.

### F0000-01: [Story Title]

**Criteria:**
- [ ] Specific acceptance criterion
- [ ] Another criterion
- [ ] Validation passes

**Tasks:**
- [ ] Implementation step 1
- [ ] Implementation step 2

---

### F0000-02: [Story Title]

**Criteria:**
- [ ] Specific acceptance criterion
- [ ] Validation passes

**Tasks:**
- [ ] Implementation step 1
- [ ] Implementation step 2

---

### F0000-03: [Story Title]

**Criteria:**
- [ ] Specific acceptance criterion
- [ ] Validation passes

**Tasks:**
- [ ] Implementation step 1
- [ ] Implementation step 2

## Testing Strategy

- **Unit tests**: [what to test, where]
- **Integration tests**: [what to test, where]
- **Manual verification**: [how to verify manually]

## Validation Commands

```bash
# Lint
uv run ruff check src/ --fix

# Tests
uv run pytest tests/ -x

# Type check (if applicable)
# uv run mypy src/
```

## Implementation Confidence

**Score: X/10**

Confidence factors:
- Similar pattern exists: Yes/No
- Clear requirements: Yes/No
- External dependencies understood: Yes/No
- Testing approach clear: Yes/No

Risks:
- [Risk 1]
- [Risk 2]

Mitigations:
- [Mitigation 1]
- [Mitigation 2]
