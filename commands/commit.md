# Create Commit

Create a well-structured git commit for the current changes.

## Process

### 1. Review Current State

```bash
git status
git diff --stat
```

### 2. Validate Before Commit

Run the project's validation commands (lint, tests).

If any checks fail, report and stop.

### 3. Stage Changes

Stage all relevant changes (excluding generated files):
```bash
git add -A
git status
```

### 4. Generate Commit Message

Analyze the changes and create a commit message following Conventional Commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `docs`: Documentation only
- `test`: Adding or updating tests
- `chore`: Maintenance (deps, config, etc.)

**Examples:**
```
feat(users): add user registration endpoint

- Add POST /api/users/register endpoint
- Add UserCreate and UserResponse schemas
- Add unit tests for registration flow
```

```
fix(auth): handle expired JWT tokens gracefully

Return 401 with clear error message instead of 500.
```

### 5. Create Commit

Present the proposed commit message for approval, then:

```bash
git commit -m "<message>"
```

### 6. Confirm

```bash
git log -1 --oneline
```

## Output

Confirmation of the commit with:
- Commit hash
- Files changed
- Commit message
