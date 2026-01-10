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

2. **Copy boilerplate files to root** (decoupled from template)
   ```bash
   # Copy project files
   cp .boilerplate/CLAUDE.md .
   cp .boilerplate/pyproject.toml .
   cp .boilerplate/.gitignore . 2>/dev/null || true
   cp .boilerplate/.env.example . 2>/dev/null || true
   cp -r .boilerplate/src .
   cp -r .boilerplate/tests .

   # Copy docs/guides
   mkdir -p docs/agents/guides
   cp -r .boilerplate/docs/agents/guides/* docs/agents/guides/

   # Copy the scaffold command (not symlinked - project-specific)
   cp .boilerplate/.claude/commands/scaffold.md .claude/commands/
   ```

3. **Keep .boilerplate/** - DO NOT remove it. It stays as a subtree for:
   - Pulling template updates: `git subtree pull --prefix=.boilerplate py-boilerplate main --squash`
   - Pushing improvements back: `git subtree push --prefix=.boilerplate py-boilerplate main`

4. **Add .boilerplate to .gitignore considerations**
   - The directory IS tracked (it's a subtree)
   - Files copied to root are independent of the template
   - Updates to guides should be made in `.boilerplate/` then copied out

5. **Install dependencies**
   ```bash
   uv sync
   ```

6. **Inform user**:
   ```
   Python boilerplate added!

   Files copied to project root (independent of template).
   Template kept at .boilerplate/ for future updates.

   Next steps:
   1. Edit CLAUDE.md with your project name/description
   2. Run /scaffold to create project structure (api-only, web-only, etc.)
   3. Run /prime to verify setup

   To update template later:
   - Pull: git subtree pull --prefix=.boilerplate py-boilerplate main --squash
   - Push: git subtree push --prefix=.boilerplate py-boilerplate main
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

## Updating Templates

Both `.prp/` (methodology) and `.boilerplate/` (language-specific) are git subtrees.

### Pull Latest Updates

**Always pull before making changes** to avoid conflicts:

```bash
# Update methodology
git subtree pull --prefix=.prp prp-method main --squash

# Update boilerplate (if using Python)
git subtree pull --prefix=.boilerplate py-boilerplate main --squash
```

### Push Improvements Back

If you improve guides, patterns, or templates:

```bash
# Push methodology improvements
git subtree push --prefix=.prp prp-method main

# Push boilerplate improvements
git subtree push --prefix=.boilerplate py-boilerplate main
```

### Workflow for Template Updates

1. **Pull latest** from upstream
2. **Make changes** in `.prp/` or `.boilerplate/`
3. **Test changes** in your project
4. **Commit** your changes locally
5. **Push back** to upstream repo

Note: Changes in `.boilerplate/` don't automatically update files at root.
If you improve a guide, manually copy it: `cp .boilerplate/docs/agents/guides/x.md docs/agents/guides/`
