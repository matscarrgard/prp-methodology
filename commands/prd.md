# PRD (Product Requirements Document)

Create a structured PRD from inputs (notes, ideas, requirements) or conversation.

## Input

$ARGUMENTS - Optional: path to input files or folder with requirements/notes

## Process

### Phase 1: Gather Inputs

1. **Check for input files** (if $ARGUMENTS provided)
   - Read specified files or folder
   - Look for: requirements, notes, ideas, meeting notes, user stories
   - Summarize what was found

2. **Check existing PRD**
   - Look for PRD in `docs/agents/prd.md` or `docs/prd.md`
   - If exists, summarize current state

3. **If no inputs provided**
   - Ask user to describe the project/feature
   - "What are you building? What problem does it solve?"

### Phase 2: Process & Structure

4. **Extract from inputs** (if messy notes provided)
   - Identify project goals
   - Extract features and requirements
   - Note technical constraints mentioned
   - Flag open questions or ambiguities

5. **Clarify with user**
   - Confirm understanding of core purpose
   - Ask about unclear requirements
   - Resolve ambiguities before documenting

### Phase 3: Collect Missing Information

6. **Core identity** (ask if not in inputs)
   - Project name
   - One-liner description
   - Problem statement (what problem does this solve?)

7. **Technical decisions** (ask user)
   - Architecture pattern (api-only, web-only, etc.)
   - Database choice
   - External services/integrations
   - Key technical constraints

8. **MVP scope** (prioritize from inputs)
   - 3-5 must-have features for v1
   - What's explicitly out of scope?

### Phase 4: Write PRD

9. **Create/Update PRD file** at `docs/agents/prd.md`

   ```markdown
   # [Project Name] PRD

   ## Executive Summary
   [One-paragraph description of what this project does and why]

   ---

   ## Problem Statement
   [What problem does this solve? Who has this problem?]

   ---

   ## Technical Decisions

   > These decisions guide project scaffolding.

   ### Architecture Pattern
   - [x] {selected_pattern}

   ### Database
   - [x] {selected_database}

   ### External Services
   - {list of services or "None"}

   ---

   ## MVP Scope

   ### In Scope (v1)
   1. [Feature] - [brief description]
   2. [Feature] - [brief description]
   3. [Feature] - [brief description]

   ### Out of Scope (later versions)
   - [Thing 1]
   - [Thing 2]

   ---

   ## Feature Details

   ### Feature 1: [Name]
   **User Story**: As a [user], I want to [action] so that [benefit]
   **Acceptance Criteria**:
   - [ ] Criterion 1
   - [ ] Criterion 2

   ### Feature 2: [Name]
   ...

   ---

   ## Non-Functional Requirements

   ### Performance
   - [expectations]

   ### Security
   - [requirements]

   ---

   ## Open Questions
   - [questions to resolve before implementation]

   ---

   ## Source Materials
   - [list of input files processed, if any]
   ```

### Phase 5: Next Steps

10. **Show workflow**
    ```
    PRD created! Next steps:

    1. Review and refine the PRD
    2. Run /scaffold to create project structure (if not done)
    3. Run /plan-feature to plan your first feature
    ```

## Usage Examples

```bash
# From conversation (interactive)
/prd

# From a folder of notes
/prd inputs/

# From specific files
/prd requirements.md notes.txt

# Update existing PRD
/prd --update
```

## Output

- [ ] PRD created at `docs/agents/prd.md`
- [ ] Executive Summary filled in
- [ ] Problem Statement clear
- [ ] Technical Decisions present
- [ ] MVP Scope defined (3-5 features)
- [ ] Ready for feature planning with `/plan-feature`
