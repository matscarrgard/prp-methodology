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
   ln -sf ../../.prp/skills/brainstorm .claude/skills/brainstorm
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
| **Flutter** | `matscarrgard/boilerplate-flutter` | Riverpod, GoRouter, Dio, Hive patterns |
| **Next.js/Sanity** | `matscarrgard/boilerplate-nextjs-sanity` | Next.js 16, Sanity CMS, Tailwind v4 |
| **None** | - | Start with minimal CLAUDE.md template |

#### If Python selected (new project):

1. **Add boilerplate as subtree**
   ```bash
   git remote add py-boilerplate https://github.com/matscarrgard/python-boilerplate.git
   git subtree add --prefix=.boilerplate-python py-boilerplate main --squash
   ```

2. **Copy all boilerplate files to root**
   ```bash
   cp .boilerplate-python/CLAUDE.md .
   cp \.boilerplate-python/pyproject.toml .
   cp \.boilerplate-python/.gitignore . 2>/dev/null || true
   cp \.boilerplate-python/.env.example . 2>/dev/null || true
   cp -r \.boilerplate-python/src .
   cp -r \.boilerplate-python/tests .
   mkdir -p docs/agents/guides
   cp -r \.boilerplate-python/docs/agents/guides/* docs/agents/guides/
   cp \.boilerplate-python/.claude/commands/scaffold.md .claude/commands/
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

#### If Flutter selected (new project):

1. **Add boilerplate as subtree**
   ```bash
   git remote add flutter-boilerplate https://github.com/matscarrgard/boilerplate-flutter.git
   git subtree add --prefix=.boilerplate-flutter flutter-boilerplate main --squash
   ```

2. **Create Flutter project and copy boilerplate files**
   ```bash
   # Create Flutter project (use appropriate name)
   flutter create --org com.example my_app
   cd my_app

   # Copy boilerplate files
   cp ../.boilerplate-flutter/CLAUDE.md .
   cp ../.boilerplate-flutter/templates/analysis_options.yaml .
   cp ../.boilerplate-flutter/templates/pubspec.yaml.template pubspec.yaml

   # Create directory structure
   mkdir -p lib/config lib/services lib/providers lib/router lib/screens lib/widgets lib/models

   # Copy templates
   cp ../.boilerplate-flutter/templates/main.dart lib/
   cp ../.boilerplate-flutter/templates/app.dart lib/
   cp ../.boilerplate-flutter/templates/config/*.dart lib/config/
   cp ../.boilerplate-flutter/templates/services/*.dart lib/services/
   cp ../.boilerplate-flutter/templates/providers/*.dart lib/providers/
   cp ../.boilerplate-flutter/templates/router/*.dart lib/router/
   cp ../.boilerplate-flutter/templates/screens/*.dart lib/screens/

   # Copy test templates
   mkdir -p test/unit test/widget test/integration
   cp ../.boilerplate-flutter/templates/tests/*.dart test/

   # Copy guides
   mkdir -p docs/guides
   cp ../.boilerplate-flutter/docs/guides/*.md docs/guides/

   # Copy scaffold command
   mkdir -p .claude/commands
   cp ../.boilerplate-flutter/.claude/commands/scaffold.md .claude/commands/
   ```

3. **Install dependencies**
   ```bash
   flutter pub get
   ```

4. **Inform user**:
   ```
   Flutter boilerplate added!

   Next steps:
   1. Edit CLAUDE.md with your project name/description
   2. Edit pubspec.yaml with your app name and dependencies
   3. Run /scaffold to customize (app-only, app-api, app-offline, full)
   4. Run flutter test to verify setup
   ```

#### If Next.js/Sanity selected (new project):

1. **Add boilerplate as subtree**
   ```bash
   git remote add nextjs-boilerplate https://github.com/matscarrgard/boilerplate-nextjs-sanity.git
   git subtree add --prefix=.boilerplate-nextjs-sanity nextjs-boilerplate main --squash
   ```

2. **Copy boilerplate files to root**
   ```bash
   cp .boilerplate-nextjs-sanity/CLAUDE.md .
   cp .boilerplate-nextjs-sanity/package.json .
   cp .boilerplate-nextjs-sanity/next.config.ts .
   cp .boilerplate-nextjs-sanity/tsconfig.json .
   cp .boilerplate-nextjs-sanity/sanity.config.ts .
   cp .boilerplate-nextjs-sanity/postcss.config.mjs .
   cp .boilerplate-nextjs-sanity/.gitignore . 2>/dev/null || true
   cp .boilerplate-nextjs-sanity/.env.example . 2>/dev/null || true
   cp -r .boilerplate-nextjs-sanity/src .
   mkdir -p docs/agents/guides
   cp -r .boilerplate-nextjs-sanity/docs/agents/guides/* docs/agents/guides/
   cp .boilerplate-nextjs-sanity/.claude/commands/scaffold.md .claude/commands/
   ```

3. **Install dependencies**
   ```bash
   bun install
   ```

4. **Inform user**:
   ```
   Next.js/Sanity boilerplate added!

   Next steps:
   1. Edit CLAUDE.md with your project name/description
   2. Create Sanity project at sanity.io/manage
   3. Copy Project ID to .env.local
   4. Run `bun dev` and open /studio
   5. Run /scaffold to add features (blog, authors, etc.)
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

"Do you want to add a boilerplate as a reference for patterns and guides?"

| Option | Repository | Description |
|--------|------------|-------------|
| **Python** | `matscarrgard/python-boilerplate` | FastAPI, SQLAlchemy, testing patterns |
| **Flutter** | `matscarrgard/boilerplate-flutter` | Riverpod, GoRouter, Dio, Hive patterns |
| **Next.js/Sanity** | `matscarrgard/boilerplate-nextjs-sanity` | Next.js 16, Sanity CMS, Tailwind v4 patterns |
| **No, skip** | - | Continue without boilerplate reference |

#### If Python selected (existing project):

1. **Add boilerplate as subtree** (reference only)
   ```bash
   git remote add py-boilerplate https://github.com/matscarrgard/python-boilerplate.git
   git subtree add --prefix=.boilerplate-python py-boilerplate main --squash
   ```

2. **Show available assets using AskUserQuestion** (multiSelect: true):

   "What would you like to adopt from the boilerplate?"

   | Option | Path | Description |
   |--------|------|-------------|
   | **Pattern guides** | `docs/agents/guides/` | FastAPI, SQLAlchemy, testing, error handling patterns |
   | **Testing structure** | `tests/` | Unit/integration test layout with conftest.py |
   | **Scaffold command** | `.claude/commands/scaffold.md` | Project scaffolding for adding new features |
   | **Example configs** | `.env.example`, `.gitignore` | Environment and git configuration |
   | **None** | - | Just keep \.boilerplate-python/ as reference |

3. **Copy selected assets** (merge, don't overwrite):

   **Pattern guides** (if selected):
   ```bash
   mkdir -p docs/agents/guides
   # Copy guides that don't exist locally
   for guide in \.boilerplate-python/docs/agents/guides/*.md; do
     name=$(basename "$guide")
     [ -f "docs/agents/guides/$name" ] || cp "$guide" "docs/agents/guides/"
   done
   echo "Copied guides. Review and customize for your project."
   ```

   **Testing structure** (if selected):
   ```bash
   mkdir -p tests/unit tests/integration
   [ -f tests/conftest.py ] || cp \.boilerplate-python/tests/conftest.py tests/
   [ -f tests/__init__.py ] || cp \.boilerplate-python/tests/__init__.py tests/
   echo "Created test structure. Existing tests preserved."
   ```

   **Scaffold command** (if selected):
   ```bash
   cp \.boilerplate-python/.claude/commands/scaffold.md .claude/commands/
   echo "Added /scaffold command. Run it to add new components."
   ```

   **Example configs** (if selected):
   ```bash
   [ -f .env.example ] || cp \.boilerplate-python/.env.example .
   # For .gitignore, append rather than overwrite
   if [ -f .gitignore ]; then
     echo "# Check \.boilerplate-python/.gitignore for additional patterns" >> .gitignore
   else
     cp \.boilerplate-python/.gitignore .
   fi
   ```

4. **Inform user**:
   ```
   Boilerplate reference added at \.boilerplate-python/

   Selected assets copied to your project.
   The \.boilerplate-python/ directory is kept as a reference - browse it for:
   - Additional patterns and examples
   - Template code to adapt

   To update boilerplate later:
   - Pull: git subtree pull --prefix=.boilerplate-python py-boilerplate main --squash

   Next: Run /prd to create a PRD for your existing project.
   ```

#### If Flutter selected (existing project):

1. **Add boilerplate as subtree** (reference only)
   ```bash
   git remote add flutter-boilerplate https://github.com/matscarrgard/boilerplate-flutter.git
   git subtree add --prefix=.boilerplate-flutter flutter-boilerplate main --squash
   ```

2. **Show available assets using AskUserQuestion** (multiSelect: true):

   "What would you like to adopt from the Flutter boilerplate?"

   | Option | Path | Description |
   |--------|------|-------------|
   | **Pattern guides** | `docs/guides/` | Flutter, Riverpod, testing patterns |
   | **Scaffold command** | `.claude/commands/scaffold.md` | Project scaffolding (app-only, app-api, etc.) |
   | **Analysis options** | `templates/analysis_options.yaml` | Strict Dart linting rules |
   | **None** | - | Just keep .boilerplate-flutter/ as reference |

3. **Copy selected assets** (merge, don't overwrite):

   **Pattern guides** (if selected):
   ```bash
   mkdir -p docs/guides
   for guide in .boilerplate-flutter/docs/guides/*.md; do
     name=$(basename "$guide")
     [ -f "docs/guides/$name" ] || cp "$guide" "docs/guides/"
   done
   echo "Copied guides. Review and customize for your project."
   ```

   **Scaffold command** (if selected):
   ```bash
   mkdir -p .claude/commands
   cp .boilerplate-flutter/.claude/commands/scaffold.md .claude/commands/
   echo "Added /scaffold command. Run it to add new components."
   ```

   **Analysis options** (if selected):
   ```bash
   [ -f analysis_options.yaml ] || cp .boilerplate-flutter/templates/analysis_options.yaml .
   echo "Copied analysis_options.yaml. Existing file preserved if present."
   ```

4. **Inform user**:
   ```
   Flutter boilerplate reference added at .boilerplate-flutter/

   Selected assets copied to your project.
   The .boilerplate-flutter/ directory is kept as a reference - browse it for:
   - Template code (services, providers, screens)
   - Flutter version gotchas (flutter-learnings.md)

   To update boilerplate later:
   - Pull: git subtree pull --prefix=.boilerplate-flutter flutter-boilerplate main --squash

   Next: Run /prd to create a PRD for your existing project.
   ```

#### If Next.js/Sanity selected (existing project):

1. **Add boilerplate as subtree** (reference only)
   ```bash
   git remote add nextjs-boilerplate https://github.com/matscarrgard/boilerplate-nextjs-sanity.git
   git subtree add --prefix=.boilerplate-nextjs-sanity nextjs-boilerplate main --squash
   ```

2. **Show available assets using AskUserQuestion** (multiSelect: true):

   "What would you like to adopt from the Next.js/Sanity boilerplate?"

   | Option | Path | Description |
   |--------|------|-------------|
   | **Pattern guides** | `docs/agents/guides/` | Next.js, Sanity, Tailwind patterns |
   | **Scaffold command** | `.claude/commands/scaffold.md` | Add blog, authors, etc. |
   | **Example configs** | `.env.example`, `.gitignore` | Environment and git configuration |
   | **None** | - | Just keep .boilerplate-nextjs-sanity/ as reference |

3. **Copy selected assets** (merge, don't overwrite):

   **Pattern guides** (if selected):
   ```bash
   mkdir -p docs/agents/guides
   for guide in .boilerplate-nextjs-sanity/docs/agents/guides/*.md; do
     name=$(basename "$guide")
     [ -f "docs/agents/guides/$name" ] || cp "$guide" "docs/agents/guides/"
   done
   echo "Copied guides. Review and customize for your project."
   ```

   **Scaffold command** (if selected):
   ```bash
   mkdir -p .claude/commands
   cp .boilerplate-nextjs-sanity/.claude/commands/scaffold.md .claude/commands/
   echo "Added /scaffold command. Run it to add blog, authors, etc."
   ```

   **Example configs** (if selected):
   ```bash
   [ -f .env.example ] || cp .boilerplate-nextjs-sanity/.env.example .
   ```

4. **Inform user**:
   ```
   Next.js/Sanity boilerplate reference added at .boilerplate-nextjs-sanity/

   Selected assets copied to your project.
   The .boilerplate-nextjs-sanity/ directory is kept as a reference - browse it for:
   - Component patterns (Hero, Container, Layout)
   - Sanity schema examples
   - Design system tokens

   To update boilerplate later:
   - Pull: git subtree pull --prefix=.boilerplate-nextjs-sanity nextjs-boilerplate main --squash

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
[ -d .boilerplate-python ] && echo ".boilerplate-python/ present (Python reference)"
[ -d .boilerplate-flutter ] && echo ".boilerplate-flutter/ present (Flutter reference)"
[ -d .boilerplate-nextjs-sanity ] && echo ".boilerplate-nextjs-sanity/ present (Next.js reference)"
head -5 CLAUDE.md 2>/dev/null || echo "CLAUDE.md: update needed"
```

## Output Summary

### For New Projects
```markdown
## PRP Methodology Initialized (New Project)

- [x] .claude/ configured with methodology commands
- [x] features/progress.txt created
- [x] Boilerplate: {Python | Flutter | None}

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
| Flutter | `matscarrgard/boilerplate-flutter` | Available |
| Next.js/Sanity | `matscarrgard/boilerplate-nextjs-sanity` | Available |
| React | `matscarrgard/react-boilerplate` | Coming soon |
| Go | `matscarrgard/go-boilerplate` | Coming soon |

## Re-running Init

Running `/init-project` again will:
- Detect current state (new vs existing, boilerplate present)
- Offer to add missing components
- For existing boilerplate: offer to adopt additional assets

## Updating Templates

`.prp/` and boilerplate directories are git subtrees.

```bash
# Pull latest methodology
git subtree pull --prefix=.prp prp-method main --squash

# Pull latest Python boilerplate (if present)
git subtree pull --prefix=.boilerplate-python py-boilerplate main --squash

# Pull latest Flutter boilerplate (if present)
git subtree pull --prefix=.boilerplate-flutter flutter-boilerplate main --squash

# Pull latest Next.js/Sanity boilerplate (if present)
git subtree pull --prefix=.boilerplate-nextjs-sanity nextjs-boilerplate main --squash

# Push improvements
git subtree push --prefix=.prp prp-method main
git subtree push --prefix=.boilerplate-python py-boilerplate main
git subtree push --prefix=.boilerplate-flutter flutter-boilerplate main
git subtree push --prefix=.boilerplate-nextjs-sanity nextjs-boilerplate main
```

**Always pull before making changes** to avoid conflicts.
