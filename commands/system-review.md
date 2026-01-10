# System Review

Review the overall system architecture and identify improvements.

## Input

$ARGUMENTS - Optional: specific area to focus on (e.g., "security", "performance", "architecture")

## Process

### 1. Gather System Context

Read:
- CLAUDE.md for project conventions
- README.md for project overview
- Main entry points
- Core configuration

### 2. Map Architecture

Identify:
- Main components/modules
- Data flow paths
- External dependencies
- Entry points (API, CLI, etc.)

### 3. Review Areas

#### Architecture
- [ ] Clear separation of concerns
- [ ] Appropriate layering
- [ ] No circular dependencies
- [ ] Consistent patterns throughout

#### Security
- [ ] Authentication in place
- [ ] Authorization checks
- [ ] Input validation
- [ ] Secrets management
- [ ] No sensitive data in logs

#### Performance
- [ ] No obvious bottlenecks
- [ ] Appropriate caching
- [ ] Efficient queries
- [ ] Resource cleanup

#### Reliability
- [ ] Error handling
- [ ] Logging
- [ ] Graceful degradation
- [ ] Recovery mechanisms

#### Maintainability
- [ ] Code organization
- [ ] Documentation
- [ ] Test coverage
- [ ] Clear naming

### 4. Generate Report

```markdown
## System Review Report

### Architecture Overview
[Brief description of current architecture]

### Strengths
- [What's working well]

### Areas for Improvement

#### Critical
- [Must address - security/reliability issues]

#### Important
- [Should address - quality/maintainability]

#### Nice to Have
- [Could improve - optimization/polish]

### Recommendations

1. **[Area]**: [Specific recommendation]
   - Impact: High/Medium/Low
   - Effort: High/Medium/Low

2. **[Area]**: [Specific recommendation]
   - Impact: High/Medium/Low
   - Effort: High/Medium/Low

### Quick Wins
[Easy improvements with good impact]

### Technical Debt
[Debt to address before it grows]
```

## Output

A comprehensive system review with:
- Architecture understanding
- Prioritized improvements
- Actionable recommendations
