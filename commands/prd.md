# PRD (Product Requirements Document)

Create or update the project PRD with key decisions for scaffolding.

## Input

$ARGUMENTS - Optional: specific section to update (e.g., "technical", "scope")

## Process

### Phase 1: Check Current State

1. **Read existing PRD** (if exists)
   - Check for PRD in docs directory
   - Summarize current state: what's filled in, what's missing

2. **Gather context** (if PRD is blank/new)
   - Read `README.md` for project description
   - Read any existing documentation
   - Check project config for project name

### Phase 2: Collect Project Information

3. **Core identity** (ask if not defined)
   - Project name
   - One-liner description
   - Problem statement (what problem does this solve?)

4. **Technical decisions** (ask user)
   - Architecture pattern
   - Database choice
   - External services/integrations
   - Key technical constraints

5. **MVP scope** (ask if not defined)
   - 2-3 must-have features for v1
   - What's explicitly out of scope?

### Phase 3: Write PRD

6. **Create/Update PRD file**

   Structure:
   ```markdown
   # [Project Name] PRD

   ## Executive Summary
   [One-paragraph description of what this project does]

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

   ### In Scope
   - Feature 1
   - Feature 2
   - Feature 3

   ### Out of Scope
   - Thing 1
   - Thing 2

   ---

   ## Non-Functional Requirements

   ### Performance
   - [expectations]

   ### Security
   - [requirements]

   ---

   ## Open Questions

   - [questions to resolve]
   ```

### Phase 4: Validate

7. **Verify PRD completeness**
   - Has Executive Summary
   - Has Technical Decisions
   - Has MVP Scope

8. **Show next step**
   - "Run `/plan-feature` to plan your first feature"

## Output

- [ ] PRD created/updated
- [ ] Executive Summary filled in
- [ ] Technical Decisions present
- [ ] MVP Scope defined
- [ ] Ready for feature planning
