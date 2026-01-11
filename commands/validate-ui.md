# Validate UI

Run end-of-feature UI validation using Playwright. Checks both functionality AND design quality.

## Purpose

This skill runs after feature implementation to catch:
1. **Functional issues**: Broken interactions, missing elements, JS errors
2. **Design issues**: Misalignment, spacing problems, visual inconsistencies

## CRITICAL: Design Validation Mindset

**You MUST be critical, not validating.**

Models tend to say "looks good" when there are obvious issues. Fight this tendency:

- **Assume there ARE problems** - your job is to find them
- **List EVERY issue**, no matter how small
- **Never say "looks good overall"** - be specific about what works AND what doesn't
- **Rate issues by severity** - don't downplay problems
- **Compare against standards** - not just "does it work"

### Design Checklist (CHECK EVERY ITEM)

For each screen, explicitly evaluate:

| Category | What to Check |
|----------|---------------|
| **Alignment** | Are elements aligned to a grid? Inconsistent margins? |
| **Spacing** | Is spacing consistent? Too cramped? Too sparse? |
| **Typography** | Font sizes appropriate? Hierarchy clear? Line height readable? |
| **Color/Contrast** | Sufficient contrast? Consistent color usage? Dark mode? |
| **Responsiveness** | Does it work at different widths? Mobile-friendly? |
| **Consistency** | Does it match other pages in the app? Same patterns? |
| **Polish** | Hover states? Focus indicators? Loading states? |
| **Accessibility** | Keyboard navigation? Screen reader labels? |

### Severity Ratings

- **P0 Critical**: Blocks usage, looks broken
- **P1 Major**: Significant UX degradation, looks unprofessional
- **P2 Minor**: Noticeable but not blocking, polish issues
- **P3 Nitpick**: Perfectionist concerns, low priority

## Process

### 1. Start the App

```bash
# Start app in background
uv run python -m app &
APP_PID=$!
sleep 3  # Wait for startup
```

### 2. Run Functional Checks

For each key flow in the feature:

1. **Navigate** to the page using `mcp__playwright__browser_navigate`
2. **Snapshot** the page using `mcp__playwright__browser_snapshot`
3. **Check for errors** using `mcp__playwright__browser_console_messages`
4. **Interact** with elements (click, type, etc.)
5. **Verify** expected state changes

### 3. Run Design Checks

For each screen:

1. **Take screenshot** using `mcp__playwright__browser_take_screenshot`
2. **Analyze the screenshot visually** - look at it critically
3. **Check the design checklist** item by item
4. **Document ALL issues found** with severity rating
5. **Test at multiple viewport sizes** (desktop, tablet, mobile)

### 4. Generate Report

Output a structured report:

```markdown
## UI Validation Report: [Feature Name]

### Summary
- **Functional Issues**: X found
- **Design Issues**: X found
- **Overall Status**: PASS / FAIL / NEEDS_WORK

### Functional Checks

| Flow | Status | Issues |
|------|--------|--------|
| [Flow 1] | PASS/FAIL | [description] |

### Design Issues

| Screen | Severity | Category | Issue | Screenshot |
|--------|----------|----------|-------|------------|
| Library | P1 | Alignment | Card titles not aligned | library-1.png |
| Reader | P2 | Spacing | Chapter nav too cramped on mobile | reader-mobile.png |

### Screenshots
[Attach all screenshots taken]

### Recommendations
1. [Prioritized list of fixes]
```

### 5. Cleanup

```bash
kill $APP_PID
```

## Integration with Ralph

At the end of each feature (after all stories complete), add to tracking YAML:

```yaml
e2e_validation:
  flows:
    - name: "Upload book flow"
      steps:
        - Navigate to /library
        - Click upload button
        - Upload test EPUB
        - Verify preview appears
        - Confirm upload
        - Verify book in library
    - name: "Read book flow"
      steps:
        - Click book card
        - Verify reader opens
        - Navigate chapters
        - Verify position saves
  design_screens:
    - /library (empty state)
    - /library (with books)
    - /read/{id} (chapter 1)
    - /read/{id} (navigation)
```

## Example Usage

```
/validate-ui

# Or with specific feature
/validate-ui F0004
```

## Output

1. Console report with all issues
2. Screenshots saved to `screenshots/` directory
3. **Verdict**: PASS, FAIL, or NEEDS_WORK with specific issues listed

**Remember: Your job is to FIND problems, not confirm everything works.**
