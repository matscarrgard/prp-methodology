# Initialize Project with PRP Methodology

Wire the PRP methodology and optionally add language-specific boilerplate.

## Process

### Phase 1: Verify Methodology Present

Check that `.prp/` exists (methodology subtree):

```bash
ls .prp/commands/ .prp/skills/ .prp/hooks/
```

If `.prp/` doesn't exist, show instructions:
```
Methodology not found. Add it first:

  git remote add prp-method https://github.com/matscarrgard/prp-methodology.git
  git subtree add --prefix=.prp prp-method main --squash

Then run /init-project again.
```

### Phase 2: Wire Claude Code

1. **Create .claude directory structure**
   ```bash
   mkdir -p .claude/commands .claude/skills
   ```

2. **Create command symlinks** (link to methodology)
   ```bash
   # Symlink all methodology commands
   for cmd in .prp/commands/*.md; do
     name=$(basename "$cmd")
     ln -sf "../../.prp/commands/$name" ".claude/commands/$name"
   done
   ```

3. **Create agent symlinks**
   ```bash
   ln -sf ../.prp/agents .claude/agents
   ```

4. **Create skill symlinks**
   ```bash
   ln -sf ../../.prp/skills/prp-methodology .claude/skills/prp-methodology
   ln -sf ../../.prp/skills/error-handling .claude/skills/error-handling
   ```

5. **Configure hooks** in `.claude/settings.json`:
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

### Phase 3: Setup Features Directory

```bash
mkdir -p features/archive
cp .prp/templates/progress.template.txt features/progress.txt
```

### Phase 4: Add Language Boilerplate (Optional)

**Ask the user using AskUserQuestion:**

"Do you want to add a language-specific boilerplate?"

Options:
| Option | Repository | Description |
|--------|------------|-------------|
| **Python** | `matscarrgard/python-boilerplate` | FastAPI, FastHTML, SQLAlchemy patterns |
| **None** | - | Start with minimal CLAUDE.md template |

*(Future: React, Go, Rust boilerplates)*

#### If Python selected:

1. **Add boilerplate as subtree**
   ```bash
   git remote add py-boilerplate https://github.com/matscarrgard/python-boilerplate.git
   git subtree add --prefix=.boilerplate py-boilerplate main --squash
   ```

2. **Copy boilerplate files to root**
   ```bash
   # Copy all boilerplate files (except .git)
   cp -r .boilerplate/* .
   cp .boilerplate/.* . 2>/dev/null || true

   # Copy the local /scaffold command (not symlinked)
   cp .boilerplate/.claude/commands/scaffold.md .claude/commands/
   ```

3. **Clean up**
   ```bash
   rm -rf .boilerplate
   git remote remove py-boilerplate
   ```

4. **Install dependencies**
   ```bash
   uv sync
   ```

5. **Inform user**:
   ```
   Python boilerplate added!

   Next steps:
   1. Edit CLAUDE.md with your project name/description
   2. Run /scaffold to create project structure (api-only, web-only, etc.)
   3. Run /prime to verify setup
   ```

#### If None selected:

1. **Create minimal CLAUDE.md from template**
   ```bash
   cp .prp/templates/CLAUDE.template.md CLAUDE.md
   ```

2. **Inform user**:
   ```
   Minimal setup complete!

   CLAUDE.md created from template. Please update it with:
   - Project name and overview
   - Your tech stack
   - Project commands (Install, Test, Lint, Run)
   - Pattern guide locations (if any)

   Run /prime to verify setup.
   ```

### Phase 5: Verify Setup

Run verification:
```bash
echo "=== Verifying setup ==="
ls -la .claude/commands/ | head -5
ls -la .claude/skills/
ls features/
head -10 CLAUDE.md 2>/dev/null || echo "CLAUDE.md not found"
```

## Output

```markdown
## PRP Methodology Initialized

### Methodology Wired
- [x] .claude/commands → .prp/commands (symlinks)
- [x] .claude/agents → .prp/agents (symlink)
- [x] .claude/skills/ (prp-methodology, error-handling)
- [x] .claude/settings.json (hooks configured)
- [x] features/progress.txt created

### Boilerplate
- [x] Python boilerplate added (or "Minimal setup - no boilerplate")

### Next Steps
1. Edit CLAUDE.md with your project details
2. Run /scaffold to create project structure (if Python boilerplate)
3. Run /prime to verify everything works
4. Run /plan-feature to start building!
```

## Available Boilerplates

| Language | Repository | Status |
|----------|------------|--------|
| Python | `matscarrgard/python-boilerplate` | Available |
| React | `matscarrgard/react-boilerplate` | Coming soon |
| Go | `matscarrgard/go-boilerplate` | Coming soon |

## Re-running Init

If already initialized, `/init-project` will:
- Check current state
- Offer to refresh symlinks
- Offer to re-pull boilerplate (with confirmation)
