---
name: brainstorm
description: >-
  Refine rough ideas into clear requirements through Socratic dialogue before
  creating PRDs or features. Use when starting a new project, exploring a feature
  idea, or when requirements are vague. Outputs a summary ready for /prd or /create-features.
disable-model-invocation: true
user-invocable: true
argument-hint: "[idea or topic]"
---

# Brainstorm: Ideas Into Requirements

Transform rough ideas into well-defined requirements through collaborative dialogue.
Output feeds directly into `/prd` or `/create-features`.

## When to Use

| Trigger | Action |
|---------|--------|
| `/brainstorm` | Full brainstorm session |
| `/brainstorm [idea]` | Start with specific idea |
| Before `/prd` | Clarify project vision |
| Before `/create-features` | Explore feature scope |

## Core Principles

| Principle | Why |
|-----------|-----|
| **One question at a time** | Don't overwhelm - let ideas develop naturally |
| **Multiple choice preferred** | Easier to answer, surfaces options user hadn't considered |
| **YAGNI ruthlessly** | Remove unnecessary complexity from all designs |
| **Explore alternatives** | Always present 2-3 approaches before settling |
| **Validate incrementally** | Confirm understanding before moving forward |
| **No jargon** | Keep questions accessible, explain technical terms |

## Process

### Phase 1: Understand the Core (2-4 questions)

Start by understanding what they're building:

1. **The idea** - "What are you thinking of building?" (if not provided)
2. **The problem** - "What problem does this solve? Who has this problem?"
3. **Success criteria** - "How will you know when it's working?"
4. **Existing context** - Check if project has existing PRD, features, or codebase

Example question format:
```
What problem does this solve?

A) Users can't easily [specific pain point]
B) There's no good way to [task]
C) Current solutions are [limitation]
D) Other: [let me describe]
```

### Phase 2: Explore the Solution Space (3-5 questions)

Dig into the approach based on what they're building:

**For new projects:**
- Target users (who specifically?)
- Core workflow (what's the main thing users do?)
- Must-have vs nice-to-have (MVP scope)

**For features:**
- How it fits with existing functionality
- User journey (where does this appear? what triggers it?)
- Edge cases (what happens when X?)

**For all:**
- Present 2-3 alternative approaches with trade-offs
- Lead with recommended option and explain why

Example approach comparison:
```
I see two main approaches:

**A) [Approach name]**
- Pro: [benefit]
- Con: [drawback]
- Best for: [scenario]

**B) [Approach name]**
- Pro: [benefit]
- Con: [drawback]
- Best for: [scenario]

Which feels right for your situation?
```

### Phase 3: Define Boundaries (2-3 questions)

Clarify scope and constraints:

1. **Out of scope** - "What should this explicitly NOT do?"
2. **Constraints** - "Any technical constraints or requirements?" (auth, mobile, etc.)
3. **Dependencies** - "Does this depend on anything else being built first?"

### Phase 4: Synthesize & Confirm

Present a structured summary for validation:

```markdown
## Brainstorm Summary: [Topic]

### The Idea
[One paragraph description]

### Problem Statement
[Who has what problem]

### Proposed Approach
[Selected approach with brief rationale]

### Key Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Out of Scope
- [Explicitly excluded item]

### Open Questions
- [Any unresolved questions]

### Next Steps
- [ ] `/prd` - Create full PRD (for new projects)
- [ ] `/create-features [description]` - Create feature spec (for features)
```

Ask: "Does this capture your thinking? Anything to add or change?"

### Phase 5: Save & Handoff

After user confirms:

1. **Save the summary** to `docs/brainstorms/YYYY-MM-DD-{topic}.md`
   - Create directory if it doesn't exist
   - Use kebab-case for topic

2. **Suggest next command**:
   - New project → "Run `/prd docs/brainstorms/YYYY-MM-DD-{topic}.md` to create your PRD"
   - Feature idea → "Run `/create-features [summary]` to create the feature spec"

## Anti-Patterns to Avoid

- **Don't ask multiple questions at once** - One question, wait for answer
- **Don't assume technical knowledge** - Explain options in plain terms
- **Don't skip to solutions** - Understand the problem first
- **Don't over-engineer** - Simplest solution that could work
- **Don't go in circles** - If stuck, summarize and move forward

## Example Session

```
User: /brainstorm authentication