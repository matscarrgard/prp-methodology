# Create Feature Specifications

Create one or more feature specification files from PRD, conversation, or provided documentation.

## Input

$ARGUMENTS - Optional: specific PRD section, feature description, or document references

## Process

### Phase 1: Gather Context

1. **Identify input sources**
   - Check if PRD exists at `docs/agents/prd.md`
   - Check conversation context for feature descriptions
   - Check for any document references in arguments

2. **Load PRD** (if exists)
   - Read the PRD to understand project scope
   - Identify feature sections or user stories
   - Note any prioritization or phasing

3. **Scan existing features**
   - List `features/F*.md` to find highest feature number
   - Next feature will be F{max + 1}
   - Note any dependencies between existing features

### Phase 2: Extract Features

4. **Identify distinct features**
   From the input sources, extract features that are:
   - **Cohesive**: Single responsibility
   - **Valuable**: Delivers user value independently
   - **Sized appropriately**: Can be planned and executed as a unit

5. **For each feature, gather**:
   - Clear title and one-liner description
   - Primary user story (As a... I want... So that...)
   - Problem being solved
   - High-level solution approach
   - Functional requirements
   - Acceptance criteria
   - Dependencies on other features

### Phase 3: User Review

6. **Present feature list for confirmation**

   Before creating files, show:
   ```
   ## Proposed Features

   | ID | Title | Size | Depends On |
   |----|-------|------|------------|
   | F0001 | [title] | M | None |
   | F0002 | [title] | S | F0001 |
   ```

   Ask user to confirm or modify before proceeding.

### Phase 4: Create Feature Files

7. **For each confirmed feature**:

   - Load template from `.prp/templates/feature-spec.template.md`
   - Fill in all sections
   - Save to `features/F{NNNN}-{kebab-case-title}.md`
   - Mark status as "Draft"

8. **Estimate size**:

   | Size | Guideline |
   |------|-----------|
   | S | 1-2 stories, single component |
   | M | 3-5 stories, multiple components |
   | L | 6-10 stories, significant complexity |
   | XL | Split into smaller features |

### Phase 5: Finalize

9. **Update the backlog**

   Update `features/BACKLOG.md`:
   - Add new features to appropriate phase section
   - Update the summary counts
   - If backlog doesn't exist, create from `.prp/templates/backlog.template.md`

   ```markdown
   ### Phase 1: MVP

   | ID | Title | Status | Size | Depends On |
   |----|-------|--------|------|------------|
   | F0001 | [title] | Draft | M | - |
   | F0002 | [title] | Draft | S | F0001 |
   ```

10. **Ask user for phase placement**
    - Which phase should each feature go in? (MVP, Enhancement, Future)
    - Confirm priority ordering within phase

11. **Commit the features**
    ```bash
    git add features/
    git commit -m "feat(specs): add feature specs F{start}-F{end}"
    ```

## Output

1. Feature spec files created in `features/`
2. Backlog updated with new features
3. Summary:
   - Features created: [list with IDs]
   - Total features: X
   - Ready for `/plan-feature F{NNNN}` or `/plan-feature F{NNNN},F{NNNN}` to create implementation plan

## Examples

### From PRD
```
/create-features
```
Extracts all features from `docs/agents/prd.md`

### From conversation
```
/create-features "User authentication with email/password and OAuth"
```
Creates feature spec(s) from the description

### Specific PRD section
```
/create-features "Phase 1 features from PRD"
```
Creates features from a specific PRD section

### Multiple related features
```
/create-features "EPUB parsing, library management, and book reader"
```
Creates multiple related feature specs

## Feature Quality Guidelines

Good features are:
- **Independent**: Can be developed without waiting for others (except explicit dependencies)
- **Negotiable**: Details can be discussed, not locked in
- **Valuable**: Delivers clear user value
- **Estimable**: Can be sized (S/M/L)
- **Small enough**: Can be planned in one `/plan-feature` session
- **Testable**: Has clear acceptance criteria

## Next Steps

After creating features:
1. Review and refine each feature spec
2. Mark features as "Ready" when spec is complete
3. Use `/plan-feature F{NNNN}` to create implementation plan
4. Use `/execute` to implement the plan
