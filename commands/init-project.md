# Initialize Project with PRP Methodology

Wire the PRP methodology into the current project.

> **Note**: This command sets up methodology only. For language-specific scaffolding, use your template's `/scaffold` command.

## What This Does

1. Creates `.claude/` directory with symlinks to methodology
2. Creates `features/` directory for progress tracking
3. Sets up hooks in `.claude/settings.json`
4. Creates `CLAUDE.md` from template (if not exists)

## Prerequisites

- Project has `.prp/` directory (methodology subtree)
- Git repository initialized

## Process

### Phase 1: Verify Methodology Present

```bash
ls .prp/commands/ .prp/skills/ .prp/hooks/
```

If `.prp/` doesn't exist, inform user:
```
Methodology not found. Add it with:
  git remote add prp-method https://github.com/matscarrgard/prp-methodology.git
  git subtree add --prefix=.prp prp-method main --squash
```

### Phase 2: Wire Claude Code

1. **Create .claude directory**
   ```bash
   mkdir -p .claude/skills
   ```

2. **Create command symlinks** (if not exists)
   ```bash
   # If .claude/commands doesn't exist or is empty
   ln -s ../.prp/commands .claude/commands
   ```

   Or for selective symlinks (if template has local commands):
   ```bash
   for cmd in .prp/commands/*.md; do
     name=$(basename "$cmd")
     [ ! -e ".claude/commands/$name" ] && ln -s "../../.prp/commands/$name" ".claude/commands/$name"
   done
   ```

3. **Create agent symlinks**
   ```bash
   ln -s ../.prp/agents .claude/agents
   ```

4. **Create skill symlinks**
   ```bash
   ln -s ../../.prp/skills/prp-methodology .claude/skills/prp-methodology
   ln -s ../../.prp/skills/error-handling .claude/skills/error-handling
   ```

### Phase 3: Setup Features Directory

```bash
mkdir -p features/archive
cp .prp/templates/progress.template.txt features/progress.txt
```

### Phase 4: Configure Hooks

Create or update `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.prp/hooks/validate-bash.py\""
          }
        ]
      }
    ]
  }
}
```

If settings.json exists, merge the hooks configuration.

### Phase 5: Create CLAUDE.md (if not exists)

If `CLAUDE.md` doesn't exist:
```bash
cp .prp/templates/CLAUDE.template.md CLAUDE.md
```

Then prompt user:
```
Created CLAUDE.md from template. Please update it with:
- Project name and overview
- Your tech stack
- Project-specific commands (Install, Test, Lint, Run)
- Pattern guide locations
```

### Phase 6: Verify Setup

Run verification checks:
```bash
# Check symlinks
ls -la .claude/commands
ls -la .claude/agents
ls -la .claude/skills/

# Check features
ls features/

# Check CLAUDE.md
head -20 CLAUDE.md
```

## Output

Report setup status:

```markdown
## PRP Methodology Initialized

### Components Wired
- [x] .claude/commands -> .prp/commands
- [x] .claude/agents -> .prp/agents
- [x] .claude/skills/ (prp-methodology, error-handling)
- [x] .claude/settings.json (hooks configured)

### Features Directory
- [x] features/progress.txt created

### CLAUDE.md
- [x] Created from template (EDIT THIS FILE!)

### Next Steps
1. Edit CLAUDE.md with your project details
2. Run `/scaffold` for language-specific setup (if available)
3. Run `/prime` to verify everything works
```

## If Already Initialized

If methodology is already wired, report current state and offer to:
- Refresh symlinks
- Update hooks
- Re-copy templates (with confirmation)
