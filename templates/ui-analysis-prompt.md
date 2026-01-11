# UI Screenshot Analysis

Analyze the following screenshots for visual issues and design quality.

## Context

**Story**: {{story_id}} - {{story_title}}
**Expected Changes**: {{acceptance_criteria}}
**Viewports Captured**: {{viewports}}

## Screenshots

{{screenshot_list}}

## Analysis Checklist

### 1. Layout Issues
- [ ] No overlapping elements
- [ ] Content properly aligned
- [ ] Grid/flex layouts intact
- [ ] No content outside viewport
- [ ] Proper spacing/margins

### 2. Visual Bugs
- [ ] All images/icons loading
- [ ] Correct colors applied
- [ ] Text readable (no overflow/truncation issues)
- [ ] Buttons/links visible and styled
- [ ] No broken styling

### 3. Responsive Behavior (compare viewports)
- [ ] Content readable at all sizes
- [ ] Navigation accessible on mobile
- [ ] Touch targets adequate (44px+) on mobile
- [ ] No horizontal scroll on mobile
- [ ] Appropriate content reflow

### 4. Accessibility Basics
- [ ] Sufficient color contrast
- [ ] Readable font sizes (16px+ base)
- [ ] Clear visual hierarchy
- [ ] Focus states visible (if interactive)

### 5. Story-Specific Validation
Based on the acceptance criteria, verify:
{{criteria_checklist}}

## Output Format

```
UI_ANALYSIS_RESULT: PASS | FAIL | NEEDS_REVIEW

ISSUES_FOUND:
- [severity: critical|major|minor] Description of issue
- ...

RECOMMENDATIONS:
- Suggested fix or improvement
- ...

NOTES:
Additional observations about the UI quality.
```

If FAIL or NEEDS_REVIEW, the story should be marked as needing fixes before commit.
