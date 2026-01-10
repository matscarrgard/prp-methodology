# Plan Feature Implementation

Create a structured implementation plan for a feature.

> **Tip**: For complex features, use `"think hard"` or `"ultrathink"` for deeper architectural analysis.

## Input

$ARGUMENTS - Either:
- A feature ID (e.g., `F0001`) or multiple IDs (e.g., `F0001,F0002`) to read from feature specs
- A description of the feature to implement

## Context Loading

Load available pattern documentation for the project's tech stack.

## Process

### Phase 1: Understand the Request

1. **Load feature spec(s)** (if feature ID provided)
   - Look for `features/F{ID}-*.md` matching each ID
   - Support multiple IDs: `F0001,F0002` creates combined plan
   - Read requirements, acceptance criteria from each spec
   - Use specs as the primary source of truth
   - **Update feature status to "In Progress"** in both the spec file and `features/BACKLOG.md`

2. **Clarify the feature** (if description provided)
   - What exactly should this feature do?
   - What are the inputs and outputs?
   - What are the edge cases?
   - Consider using `/create-features` first to create a proper spec

3. **Check the PRD** (if exists)
   - Verify this feature aligns with project scope
   - Note any relevant constraints

4. **Check dependencies**
   - If feature depends on others (from spec), verify they are Complete
   - Warn if dependencies are not met

### Phase 2: Codebase Intelligence

4. **Analyze existing codebase**
   - Find similar features in the codebase
   - Identify patterns to follow
   - Check examples directory for reference implementations
   - Note shared utilities

5. **Identify dependencies**
   - New packages needed?
   - Database migrations required?
   - New shared utilities needed?

### Phase 3: External Research (if needed)

6. **Research external requirements**
   - Check library documentation if using new libraries
   - Note any API quirks or gotchas
   - Document relevant URLs for reference

### Phase 4: Design

7. **Present 2-3 implementation options**
   - Option A: [approach] - Pros/Cons
   - Option B: [approach] - Pros/Cons
   - Option C (if applicable): [approach] - Pros/Cons
   - **Recommend one** and explain why
   - Wait for human to confirm approach before detailed planning

8. **Determine feature structure** (after approach is confirmed)
   - Which files need to be created?
   - Which files need to be modified?
   - What's the data flow?
   - What are the API contracts?

### Phase 5: Create Structured Plan

9. **Extract relevant patterns from guides**
   Read and extract specific code patterns from project's pattern documentation.
   **Include a "Patterns Reference" section in the plan** with actual code snippets.

10. **Write the implementation plan**

    Save to `docs/agents/plans/{NNNN}-{feature-name}.md`:

    ```markdown
    # Feature: [Name]

    > Feature Spec: `features/F{NNNN}-{name}.md` (or multiple if combined)

    ## Problem Statement
    [What problem does this solve?]

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

    ## Files to Create/Modify
    | File | Action | Purpose |
    |------|--------|---------|
    | `path/to/file` | Create | [purpose] |
    | `path/to/other` | Modify | [what changes] |

    ## Implementation Tasks

    ### Task 1: [Description]
    - [ ] Subtask 1.1
    - [ ] Subtask 1.2

    ### Task 2: [Description]
    - [ ] Subtask 2.1
    - [ ] Subtask 2.2

    ## Testing Strategy
    - Unit tests: [what to test]
    - Integration tests: [what to test]
    - Manual verification: [how to verify]

    ## Validation Checklist
    - [ ] Run validation command
    - [ ] Run tests
    - [ ] Manual smoke test
    ```

### Phase 6: Confidence Assessment

11. **Score the plan**

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
    ```

## Output

1. A structured plan saved to `docs/agents/plans/{NNNN}-{feature-name}.md`
2. Feature spec(s) updated to "In Progress" status
3. Backlog updated
4. TODO.md updated:
   - Current: `/execute {plan-file}`
   - Completed: `- [x] Planned F{NNNN}: {title}`
5. **Commit the plan**:
   ```bash
   git add -A && git commit -m "plan({NNNN}): {feature-name}"
   ```
6. A summary for human review including:
   - Feature overview
   - Number of tasks
   - Files to be created/modified
   - Confidence score
   - Any questions or clarifications needed

**Wait for human approval before proceeding to execution.**

## Plan Quality Guidelines

- **Target length**: 500-700 lines (under 1000 is acceptable)
- **Task granularity**: 5-15 tasks total
- **Each task**: Should be completable in one focused session
- **Validation**: Must be runnable commands, not vague descriptions
