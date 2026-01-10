# Initialize Project with PRP Methodology

Wire the PRP methodology and add language-specific boilerplate or patterns.

Handles both **new projects** (full setup) and **existing projects** (selective pattern adoption).

## Process

### Phase 0: Detect Project Type

Check for existing project indicators:

```bash
# Existing project if ANY of these exist:
[ -f "CLAUDE.md" ] || [ -d "src" ] || [ -f "pyproject.toml" ] || [ -f "package.json" ]
```

**New project**: No existing code structure
**Existing project**: Has CLAUDE.md, src/, or project config files

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
  .prp/scripts/bootstrap-existing.sh  # For existing projects
  # OR
  .prp/scripts/bootstrap-new.sh       # For new projects

Then run /init-project again.
```

### Phase 2: Wire Claude Code

**For new projects** (no .claude/ directory):

1. **Create .claude directory structure**
   ```bash
   mkdir -p .claude/commands .claude/skills
   ```

2. **Create command symlinks** (link to methodology)
   ```bash
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

5. **Configure hooks** in `.claude/settings.json`

**For existing projects** (already has .claude/):

Skip this phase - assume bootstrap-existing.sh was run.
Verify commands are linked:
```bash
ls -la .claude/commands/*.md | head -3
```

### Phase 3: Setup Features Directory

```bash
mkdir -p features/archive
[ -f features/progress.txt ] || cp .prp/templates/progress.template.txt features/progress.txt
```

---

## Phase 4: Add Boilerplate

### For NEW Projects

**Ask the user using AskUserQuestion:**

"Do you want to add a language-specific boilerplate?"

| Option | Repository | Description |
|--------|------------|-------------|
| **Python** | `matscarrgard/python-boilerplate` | FastAPI, FastHTML, SQLAlchemy patterns |
| **None** | - | Start with minimal CLAUDE.md template |

#### If Python selected (new project):

1. **Add boilerplate as subtree**
   ```bash
   git remote add py-boilerplate https://github.com/matscarrgard/python-boilerplate.git
   git subtree add --prefix=.boilerplate py-boilerplate main --squash
   ```

2. **Copy all boilerplate files to root**
   ```bash
   cp .boilerplate/CLAUDE.md .
   cp .boilerplate/pyproject.toml .
   cp .boilerplate/.gitignore . 2>/dev/null || true
   cp .boilerplate/.env.example . 2>/dev/null || true
   cp -r .boilerplate/src .
   cp -r .boilerplate/tests .
   mkdir -p docs/agents/guides
   cp -r .boilerplate/docs/agents/guides/* docs/agents/guides/
   cp .boilerplate/.claude/commands/scaffold.md .claude/commands/
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

4. **Inform user**:
   ```
   Python boilerplate added!

   Next steps:
   1. Edit CLAUDE.md with your project name/description
   2. Run /scaffold to create project structure (api-only, web-only, etc.)
   3. Run /prime to verify setup
   ```

#### If None selected (new project):

1. **Create minimal CLAUDE.md from template**
   ```bash
   cp .prp/templates/CLAUDE.template.md CLAUDE.md
   ```

2. **Inform user** to fill in CLAUDE.md

---

### For EXISTING Projects

**Ask the user using AskUserQuestion:**

"Do you want to add the Python boilerplate as a reference for patterns and guides?"

| Option | Description |
|--------|-------------|
| **Yes, add reference** | Add .boilerplate/ subtree, then choose what to adopt |
| **No, skip** | Continue without boilerplate reference |

#### If Yes selected (existing project):

1. **Add boilerplate as subtree** (reference only)
   ```bash
   git remote add py-boilerplate https://github.com/matscarrgard/python-boilerplate.git
   git subtree add --prefix=.boilerplate py-boilerplate main --squash
   ```

2. **Show available assets using AskUserQuestion** (multiSelect: true):

   "What would you like to adopt from the boilerplate?"

   | Option | Path | Description |
   |--------|------|-------------|
   | **Pattern guides** | `docs/agents/guides/` | FastAPI, SQLAlchemy, testing, error handling patterns |
   | **Testing structure** | `tests/` | Unit/integration test layout with conftest.py |
   | **Scaffold command** | `.claude/commands/scaffold.md` | Project scaffolding for adding new features |
   | **Example configs** | `.env.example`, `.gitignore` | Environment and git configuration |
   | **None** | - | Just keep .boilerplate/ as reference |

3. **Copy selected assets** (merge, don't overwrite):

   **Pattern guides** (if selected):
   ```bash
   mkdir -p docs/agents/guides
   # Copy guides that don't exist locally
   for guide in .boilerplate/docs/agents/guides/*.md; do
     name=$(basename "$guide")
     [ -f "docs/agents/guides/$name" ] || cp "$guide" "docs/agents/guides/"
   done
   echo "Copied guides. Review and customize for your project."
   ```

   **Testing structure** (if selected):
   ```bash
   mkdir -p tests/unit tests/integration
   [ -f tests/conftest.py ] || cp .boilerplate/tests/conftest.py tests/
   [ -f tests/__init__.py ] || cp .boilerplate/tests/__init__.py tests/
   echo "Created test structure. Existing tests preserved."
   ```

   **Scaffold command** (if selected):
   ```bash
   cp .boilerplate/.claude/commands/scaffold.md .claude/commands/
   echo "Added /scaffold command. Run it to add new components."
   ```

   **Example configs** (if selected):
   ```bash
   [ -f .env.example ] || cp .boilerplate/.env.example .
   # For .gitignore, append rather than overwrite
   if [ -f .gitignore ]; then
     echo "# Check .boilerplate/.gitignore for additional patterns" >> .gitignore
   else
     cp .boilerplate/.gitignore .
   fi
   ```

4. **Inform user**:
   ```
   Boilerplate reference added at .boilerplate/

   Selected assets copied to your project.
   The .boilerplate/ directory is kept as a reference - browse it for:
   - Additional patterns and examples
   - Template code to adapt

   To update boilerplate later:
   - Pull: git subtree pull --prefix=.boilerplate py-boilerplate main --squash

   Next: Run /prd to create a PRD for your existing project.
   ```

#### If No selected (existing project):

```
Skipping boilerplate. You can add it later by running /init-project again.

Next: Run /prd to create a PRD for your existing project.
```

---

### Phase 5: Verify Setup

Run verification:
```bash
echo "=== Verifying setup ==="
ls -la .claude/commands/ | head -5
ls -la .claude/skills/
ls features/
[ -d .boilerplate ] && echo ".boilerplate/ present (reference)"
head -5 CLAUDE.md 2>/dev/null || echo "CLAUDE.md: update needed"
```

## Output Summary

### For New Projects
```markdown
## PRP Methodology Initialized (New Project)

- [x] .claude/ configured with methodology commands
- [x] features/progress.txt created
- [x] Boilerplate: {Python | None}

Next steps:
1. Edit CLAUDE.md with your project details
2. Run /scaffold to create project structure
3. Run /plan-feature to start building!
```

### For Existing Projects
```markdown
## PRP Methodology Initialized (Existing Project)

- [x] Methodology commands available
- [x] features/progress.txt created
- [x] Boilerplate reference: {Added | Skipped}
- [x] Adopted: {list of selected assets}

Next steps:
1. Update CLAUDE.md with workflow section (if needed)
2. Run /prd to document your existing project
3. Run /prime to verify setup
```

---

## Available Boilerplates

| Language | Repository | Status |
|----------|------------|--------|
| Python | `matscarrgard/python-boilerplate` | Available |
| React | `matscarrgard/react-boilerplate` | Coming soon |
| Go | `matscarrgard/go-boilerplate` | Coming soon |

## Re-running Init

Running `/init-project` again will:
- Detect current state (new vs existing, boilerplate present)
- Offer to add missing components
- For existing boilerplate: offer to adopt additional assets

## Updating Templates

Both `.prp/` and `.boilerplate/` are git subtrees.

```bash
# Pull latest
git subtree pull --prefix=.prp prp-method main --squash
git subtree pull --prefix=.boilerplate py-boilerplate main --squash

# Push improvements
git subtree push --prefix=.prp prp-method main
git subtree push --prefix=.boilerplate py-boilerplate main
```

**Always pull before making changes** to avoid conflicts.
