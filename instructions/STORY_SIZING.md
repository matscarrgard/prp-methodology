# Story Sizing Guide

How to break features into right-sized stories for AI execution.

## The Golden Rule

> A story should be completable in ONE context window.

If you can't describe it in 2-3 sentences with clear acceptance criteria, it's too big.

## Good Story Size

### Characteristics

- **Describable**: 2-3 sentences max
- **Completable**: One focused session (1-3 iterations)
- **Verifiable**: Clear acceptance criteria ("tests pass", not "looks good")
- **Independent**: Can be committed separately
- **Valuable**: Delivers something useful on its own

### Examples

**Good stories:**
- "Add User model with email, password_hash, created_at fields"
- "Add POST /api/users endpoint that creates user"
- "Add login endpoint that returns JWT token"
- "Add middleware that validates JWT and sets current_user"

**Bad stories (too big):**
- "Add user authentication" (multiple components)
- "Build the API" (entire subsystem)
- "Make it secure" (vague, unbounded)

## Splitting Strategies

### Horizontal Slicing (by layer)

Split by technical layer:

```
Original: "Add user authentication"

Split into:
1. Add User model and migration
2. Add user creation endpoint
3. Add password hashing utility
4. Add login endpoint with JWT
5. Add JWT validation middleware
6. Add protected endpoint example
```

### Vertical Slicing (by feature)

Split by user-facing capability:

```
Original: "Add user profile management"

Split into:
1. View own profile (GET /profile)
2. Update own profile (PATCH /profile)
3. Upload profile picture (POST /profile/picture)
4. Delete account (DELETE /profile)
```

### Workflow Slicing

Split by workflow step:

```
Original: "Add checkout flow"

Split into:
1. Add cart summary view
2. Add shipping address form
3. Add payment method selection
4. Add order confirmation
5. Add order submission
```

## Size Estimation

### Iteration Estimate

| Size | Iterations | Description |
|------|------------|-------------|
| XS | 1 | Single file change, obvious implementation |
| S | 1-2 | Single component, clear pattern exists |
| M | 2-3 | Multiple files, some exploration needed |
| L | 3-5 | Multiple components, might need to split |
| XL | 5+ | TOO BIG - must split |

### When to Split

Split if story has:
- More than 3 new files
- More than 2 acceptance criteria
- Dependencies on other uncommitted work
- Multiple integration points
- "and" in the description

## Story Template

```yaml
- id: FEAT-001
  title: Add User model
  description: Create SQLAlchemy User model with email and password_hash
  criteria:
    - User model in src/app/models/user.py
    - "Fields: id, email (unique), password_hash, created_at"
    - Migration created and runs successfully
    - "Tests: test_user_model_* pass"  # IMPORTANT: Include tests in EVERY story
    - Lint passes
  priority: 1
  status: pending
```

**Critical**: Each story includes its own tests as criteria. Don't batch tests at the end of a feature.

## Acceptance Criteria Rules

### Good Criteria

- **Specific**: "Endpoint returns 201 with user ID"
- **Testable**: "pytest tests/unit/test_x.py passes"
- **Binary**: Either passes or fails, no "mostly done"

### Bad Criteria

- **Vague**: "Works correctly" (what does that mean?)
- **Subjective**: "Looks good" (to whom?)
- **Unbounded**: "Handle all errors" (which ones?)

## Priority Guidelines

Prioritize stories by:

1. **Dependencies**: If B needs A, do A first
2. **Risk**: Do risky/uncertain stories early
3. **Value**: Core functionality before nice-to-have
4. **Learning**: Do exploratory stories early to inform later ones

## Anti-Patterns

### The Megastory
```
Story: Build the backend
```
Split into: Models, endpoints, services, tests (maybe 20+ stories)

### The Invisible Story
```
Story: Improve performance
```
Fix by: Define specific metric and target ("Reduce API latency to <100ms")

### The Assumption Story
```
Story: Add feature X (assuming Y works)
```
Fix by: Make dependency explicit or verify first

### The Endless Story
```
Story: Keep improving until perfect
```
Fix by: Define "done" criteria upfront

## Practical Test

Before starting a story, answer:

1. Can I describe what "done" looks like in one sentence?
2. Can I verify completion with a command?
3. Can I commit the result independently?
4. Will this take 1-3 iterations max?

If any answer is "no", split the story.
