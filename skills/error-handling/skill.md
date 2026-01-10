---
name: error-handling
description: Error handling patterns for robust applications. Use when implementing error handling, exception classes, or error responses.
---

# Error Handling Patterns

## Philosophy

- **Fail fast**: Validate early, raise exceptions immediately
- **Be specific**: Use typed exceptions, not generic errors
- **Be informative**: Include context in error messages
- **Don't swallow**: Never catch and ignore silently

## Exception Hierarchy

Create a project-specific exception hierarchy:

```python
# core/exceptions.py

class AppError(Exception):
    """Base exception for application errors."""
    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(message)

class ValidationError(AppError):
    """Invalid input data."""
    pass

class NotFoundError(AppError):
    """Resource not found."""
    pass

class ConflictError(AppError):
    """Resource conflict (duplicate, etc.)."""
    pass

class AuthenticationError(AppError):
    """Authentication failed."""
    pass

class AuthorizationError(AppError):
    """Permission denied."""
    pass
```

## Where to Handle Errors

| Layer | What to Handle | How |
|-------|----------------|-----|
| **Boundary** (API routes, CLI) | All exceptions | Convert to response |
| **Service** | Business logic errors | Raise specific exceptions |
| **Repository** | DB errors | Wrap in domain exceptions |

## API Error Responses

Return consistent error format:

```python
# HTTP response format
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Email format is invalid",
        "details": {"field": "email", "value": "not-an-email"}
    }
}
```

Map exceptions to HTTP status codes:

| Exception | HTTP Status |
|-----------|-------------|
| ValidationError | 400 Bad Request |
| AuthenticationError | 401 Unauthorized |
| AuthorizationError | 403 Forbidden |
| NotFoundError | 404 Not Found |
| ConflictError | 409 Conflict |
| AppError (generic) | 500 Internal Server Error |

## Anti-Patterns to Avoid

### Don't catch and ignore

```python
# BAD - swallowing errors
try:
    do_something()
except Exception:
    pass  # Silent failure

# GOOD - handle or re-raise
try:
    do_something()
except SpecificError as e:
    logger.warning("Expected error", error=str(e))
    return default_value
```

### Don't use bare except

```python
# BAD - catches everything including KeyboardInterrupt
try:
    do_something()
except:
    handle_error()

# GOOD - be specific
try:
    do_something()
except (ValueError, TypeError) as e:
    handle_error(e)
```

### Don't re-raise without context

```python
# BAD - loses stack trace
try:
    do_something()
except SomeError:
    raise DifferentError("Something went wrong")

# GOOD - chain exceptions
try:
    do_something()
except SomeError as e:
    raise DifferentError("Context about what failed") from e
```

## Logging Errors

Log errors with context:

```python
from loguru import logger

try:
    result = process_user(user_id)
except NotFoundError:
    logger.warning("user_not_found", user_id=user_id)
    raise
except Exception as e:
    logger.error("user_processing_failed", user_id=user_id, error=str(e))
    raise
```

## Validation Patterns

Validate at boundaries, trust internally:

```python
# At API boundary - validate
@router.post("/users")
async def create_user(data: UserCreate):  # Pydantic validates
    return await service.create(data)

# In service - trust the input (already validated)
class UserService:
    async def create(self, data: UserCreate) -> User:
        # Don't re-validate email format here
        user = User(**data.model_dump())
        ...
```

## Return vs Raise

| Situation | Pattern |
|-----------|---------|
| Expected absence | Return `None` or empty |
| Unexpected absence | Raise `NotFoundError` |
| Invalid input | Raise `ValidationError` |
| Business rule violation | Raise specific exception |
| Optional operation failed | Return `Result` type |
