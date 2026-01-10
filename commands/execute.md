# Execute Implementation Plan

Execute the current implementation plan task by task until complete.

## Critical Instruction

**Start with a fresh conversation** - Clear context from planning to avoid confusion.

**DO NOT STOP until the entire plan is fulfilled and all validation passes.**

You must:
- Complete ALL tasks in the plan, not just some of them
- Fix any validation failures before moving on
- Run the full validation suite at the end
- Only stop when everything passes or you hit an unresolvable blocker

## Input

$ARGUMENTS - Optional: path to plan file (defaults to most recent plan)

## Process

### Phase 1: Load Plan

1. **Read the plan file**
   - Load the specified plan or find most recent
   - Read the ENTIRE plan before starting
   - Understand all tasks, their dependencies, and validation criteria

2. **Create rollback point**
   ```bash
   git add -A && git commit -m "chore: pre-execute checkpoint" --allow-empty
   ```
   - If execution fails badly, user can rollback with: `git reset --hard HEAD~1`

3. **Verify prerequisites**
   - Check dependencies are installed
   - Check starting state: `git status`
   - Read any referenced documentation from the plan

4. **Configuration checkpoint** (AI often gets this wrong!)
   - Review any environment variable changes in the plan
   - Verify config file updates match actual requirements
   - Check package versions are correct

### Phase 2: Think Before Acting

5. **Plan your approach**
   - Break complex tasks into manageable steps
   - Identify existing code patterns to follow
   - Note potential gotchas from the plan
   - Consider the order of implementation

### Phase 3: Execute

For each task in the plan:

6. **Navigate to task**
   - Read the task requirements carefully
   - Identify files to create/modify
   - Check for existing patterns in similar features

7. **Reference documentation before implementing**
   - Check the "Patterns Reference" section in the plan
   - Read relevant pattern guides
   - Use exact APIs from guides, don't guess

8. **Implement the task**
   - Write code following patterns in CLAUDE.md
   - Follow existing patterns in similar features
   - Keep files under recommended limits

9. **Verify the task**
   - Run linting
   - Run relevant tests
   - Fix any failures before proceeding

10. **Mark task complete**
    - Update the plan file to mark task as done
    - Move to next task
    - **DO NOT STOP** - continue to next task

### Phase 4: Validate

11. **Final verification**
    - Run full test suite
    - Run full lint check
    - If any failures, fix them and re-run

12. **Re-read plan**
    - Verify all checklist items are complete
    - Confirm all success criteria are met

### Phase 5: Complete

13. **Archive the plan**
    - Move the completed plan to completed plans directory
    - Rename with date: `{feature-name}-{YYYY-MM-DD}.md`

14. **Summary report**
    Report the following:
    - Tasks completed (X/Y)
    - Files created/modified (list them)
    - Validation results (all passing?)
    - Any deviations from the plan
    - Follow-up tasks needed (if any)

## Configuration

| Situation | Action |
|-----------|--------|
| Test failure | Fix the issue, re-run tests, continue |
| Lint error | Auto-fix if possible, continue |
| Unresolvable blocker | Stop and report clearly |

## Error Recovery

If execution goes badly wrong:

```bash
# Rollback to pre-execute checkpoint
git reset --hard HEAD~1
```

## Thoroughness Checklist

Before reporting completion, verify:
- [ ] All plan tasks marked complete
- [ ] All tests passing
- [ ] No lint errors
- [ ] Configuration correct
- [ ] All success criteria from plan met
- [ ] Plan archived
- [ ] Summary includes all files changed

## Output

A completion report with:
- Final status (SUCCESS / BLOCKED)
- Tasks: X/Y completed
- Files changed: [list]
- Validation: All passing / Issues remaining
- Deviations: [any changes from plan]
- Follow-up: [any new tasks identified]
