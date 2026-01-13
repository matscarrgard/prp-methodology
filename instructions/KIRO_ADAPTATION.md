# Adapting PRP for Amazon Kiro

Guide for running PRP methodology in Kiro IDE and Kiro CLI.

> **Last Updated**: January 2026
> **Kiro Version**: v0.8.x (IDE), v1.23.0+ (CLI)

## Overview

[Kiro](https://kiro.dev/) is Amazon's spec-driven agentic IDE that shares philosophical alignment with PRP:
- Structured specifications before implementation
- Plan-then-execute workflow
- Memory via steering files

This guide documents how to adapt PRP's methodology for Kiro while maintaining compatibility with Claude Code.

## Conceptual Mapping

| PRP Component | Kiro Equivalent | Notes |
|---------------|-----------------|-------|
| `CLAUDE.md` | `.kiro/steering/tech.md` + `product.md` | Long-term project context |
| `AGENTS.md` | Native support | Kiro reads AGENTS.md automatically[^1] |
| `F####-spec.md` | `.kiro/specs/*/requirements.md` | Feature requirements (EARS notation) |
| `F####-plan.md` | `.kiro/specs/*/design.md` + `tasks.md` | Technical design + tasks split |
| `F####-tracking.yaml` | Task checkboxes in `tasks.md` | Story progress |
| `features/progress.txt` | No equivalent | Medium-term memory (manual) |
| `.prp/agents/*.md` | `.kiro/agents/*.json` | Custom agent configs |
| `/plan-feature` | Plan Agent (`/plan`) | Requirements → Plan → Handoff |
| Ralph loop | Subagents | Parallel task execution |

## Directory Structure

### PRP Structure
```
.prp/
├── commands/           # Slash commands
├── instructions/       # Methodology docs
├── templates/          # Starter files
├── agents/             # Agent prompts (markdown)
└── hooks/              # Safety hooks

features/
├── F0014-name/
│   ├── F0014-spec.md
│   ├── F0014-plan.md
│   └── F0014-tracking.yaml
└── progress.txt
```

### Kiro Structure
```
.kiro/
├── steering/           # Project context
│   ├── product.md      # Product vision, features
│   ├── tech.md         # Tech stack, tools
│   └── structure.md    # Directory organization
├── agents/             # Custom agents (JSON)
│   ├── code-reviewer.json
│   ├── plan-executor.json
│   └── test-writer.json
├── specs/              # Feature specifications
│   └── feature-name/
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
├── hooks/              # Event-driven automations
└── settings/
    └── mcp.json        # MCP server configs
```

## Kiro Features (December 2025)

### Subagents[^2]

Subagents enable parallel task execution with independent contexts:

```
Use the backend agent to refactor the payment module
```

Key capabilities:
- Each subagent has its own context window
- Live progress tracking during execution
- Access to core tools: read, write, shell, MCP tools
- Custom subagents via your agent configurations

This replaces Ralph's external bash loop with internal delegation.

### Plan Agent[^3]

Access via `Shift + Tab` or `/plan` command. Workflow:

1. **Requirements gathering** — Structured questions with multiple-choice options
2. **Research & analysis** — Explores codebase using grep/glob tools
3. **Implementation plan** — Detailed task breakdowns
4. **Handoff** — Transfers plan to execution agent

The Plan Agent operates read-only (no file modifications during planning).

### Contextual Hooks[^4]

Hooks fire at key moments in the agent workflow:

| Trigger | Purpose |
|---------|---------|
| `agentSpawn` | Agent initialization |
| `userPromptSubmit` | Before processing user message |
| `preToolUse` | Before tool execution (can block) |
| `postToolUse` | After tool execution |
| `stop` | After assistant response |

Actions:
- **Agent Prompt**: Natural language instructions
- **Shell Command**: Local commands (no credit cost)

### AGENTS.md Support[^1]

> "Kiro supports providing steering directives via the AGENTS.md standard. AGENTS.md files are in markdown format, similar to Kiro steering files; however, AGENTS.md files do not support inclusion modes and are always included."

Place `AGENTS.md` in:
- `~/.kiro/steering/` (global)
- Project root (workspace-specific)

## Agent Configuration

### Format Reference[^5]

Kiro agents use JSON configuration in `.kiro/agents/`:

```json
{
  "name": "agent-name",
  "description": "Human-readable purpose",
  "prompt": "file://./prompts/agent.md",
  "model": "claude-sonnet-4",
  "tools": ["read", "write", "shell"],
  "allowedTools": ["read"],
  "toolsSettings": {
    "write": {
      "allowedPaths": ["src/**", "tests/**"]
    },
    "shell": {
      "allowedCommands": ["git diff", "pytest", "ruff check"]
    }
  },
  "resources": [
    "file://CLAUDE.md",
    "file://docs/**/*.md"
  ],
  "hooks": {
    "agentSpawn": [{
      "command": "git status --porcelain",
      "timeout_ms": 5000
    }]
  }
}
```

### Key Fields

| Field | Type | Purpose |
|-------|------|---------|
| `prompt` | string | System prompt (inline or `file://` URI) |
| `tools` | array | Available tools (`read`, `write`, `shell`, `@mcp-server`) |
| `allowedTools` | array | Tools that run without permission prompts |
| `toolsSettings` | object | Per-tool configuration (paths, commands) |
| `resources` | array | Files to include in context (`file://` URIs) |
| `hooks` | object | Lifecycle triggers |
| `mcpServers` | object | MCP server definitions |

### Converting PRP Agents

**PRP agent** (`.prp/agents/code-reviewer.md`):
```markdown
# Code Reviewer Agent
Reviews code for CLAUDE.md compliance, bugs, security issues...
```

**Kiro agent** (`.kiro/agents/code-reviewer.json`):
```json
{
  "name": "code-reviewer",
  "description": "Reviews code for CLAUDE.md compliance, bugs, security issues",
  "prompt": "file://.prp/agents/code-reviewer.md",
  "tools": ["read", "shell"],
  "allowedTools": ["read"],
  "toolsSettings": {
    "shell": {
      "allowedCommands": ["git diff", "git status", "ruff check", "pytest"]
    }
  },
  "resources": [
    "file://CLAUDE.md",
    "file://AGENTS.md",
    "file://.prp/instructions/*.md"
  ]
}
```

## Workflow Comparison

### Planning

| PRP | Kiro |
|-----|------|
| `/plan-feature "Add auth"` | `/plan` or `Shift + Tab` |
| Creates `F####-spec.md`, `F####-plan.md` | Creates `requirements.md`, `design.md`, `tasks.md` |
| Human approves plan file | Human approves in UI |

### Execution

| PRP (Ralph) | Kiro (Subagents) |
|-------------|------------------|
| External bash loop | Internal agent delegation |
| `ralph.sh 15` | Prompt with subagent instruction |
| YAML status tracking | Task checkboxes |
| Fresh context per iteration | Subagent has own context |
| Git commits between stories | Checkpointing for rollback |

**Ralph-style prompt in Kiro:**
```
Execute stories F0014-01 through F0014-05 from features/F0014-vector-chunking/F0014-tracking.yaml.
Use subagents for each story. Run validation (ruff check, pytest) after each story.
Update the tracking file status as you complete each story.
```

### Validation

| PRP | Kiro |
|-----|------|
| `/validate` command | Hooks on `postToolUse` |
| Manual lint/test | Automated via hooks |

**Validation hook:**
```json
{
  "hooks": {
    "postToolUse": [{
      "matcher": "write",
      "command": "uv run ruff check src/ --fix && uv run pytest tests/ -x"
    }]
  }
}
```

## Implementation Guide

### Step 1: Enable AGENTS.md

Copy or symlink to project root:
```bash
cp .boilerplate/AGENTS.md ./AGENTS.md
# or
ln -s .boilerplate/AGENTS.md ./AGENTS.md
```

Kiro will read this automatically.

### Step 2: Create Steering Files

Generate `.kiro/steering/` from existing docs:

```bash
mkdir -p .kiro/steering

# Extract product info from CLAUDE.md
cat > .kiro/steering/product.md << 'EOF'
# AI Reader

AI-assisted reading app for EPUBs with contextual AI chat.
Key differentiator: retention features (quizzes, spaced repetition) and cross-platform sync.

## Core Features
- EPUB parsing and rendering
- Contextual AI chat ("highlight → explain")
- Entity extraction (X-Ray)
- Vector search across library
EOF

# Extract tech stack
cat > .kiro/steering/tech.md << 'EOF'
# Technology Stack

- **Runtime**: Python 3.13+
- **Validation**: Pydantic v2
- **Logging**: loguru
- **Web**: FastHTML, MonsterUI, fastlite
- **EPUB**: ebooklib, beautifulsoup4, lxml
- **AI**: litellm
- **Database**: SQLAlchemy 2.0, pgvector
- **Dev**: ruff, pytest

## Commands
- Install: `uv sync --extra web`
- Test: `uv run pytest tests/ -x`
- Lint: `uv run ruff check src/ --fix`
- Run: `uv run python -m app`
EOF
```

### Step 3: Convert Agents

Create `.kiro/agents/` with JSON configs:

```bash
mkdir -p .kiro/agents

# Plan executor (Ralph equivalent)
cat > .kiro/agents/plan-executor.json << 'EOF'
{
  "name": "plan-executor",
  "description": "Executes stories from feature tracking files with memory updates",
  "prompt": "file://.prp/agents/plan-executor.md",
  "tools": ["read", "write", "shell", "subagent"],
  "allowedTools": ["read"],
  "toolsSettings": {
    "write": {
      "allowedPaths": ["src/**", "tests/**", "features/**"]
    },
    "shell": {
      "allowedCommands": [
        "uv run ruff check src/ --fix",
        "uv run pytest tests/ -x",
        "git status",
        "git diff",
        "git add",
        "git commit"
      ]
    }
  },
  "resources": [
    "file://CLAUDE.md",
    "file://features/progress.txt",
    "file://features/**/*.yaml",
    "file://features/**/*.md"
  ],
  "hooks": {
    "agentSpawn": [{
      "command": ".prp/scripts/feature-status.py status",
      "timeout_ms": 5000
    }]
  }
}
EOF
```

### Step 4: Configure Hooks

For validation after writes:

```bash
mkdir -p .kiro/hooks

cat > .kiro/hooks/validation.json << 'EOF'
{
  "postToolUse": [{
    "matcher": "write",
    "command": "uv run ruff check src/ --fix",
    "timeout_ms": 30000
  }]
}
EOF
```

## Specs Format (EARS Notation)

Kiro uses EARS (Easy Approach to Requirements Syntax)[^6] for acceptance criteria:

| Pattern | Example |
|---------|---------|
| Ubiquitous | "The system shall [action]" |
| Event-driven | "When [trigger], the system shall [action]" |
| State-driven | "While [state], the system shall [action]" |
| Optional | "Where [feature enabled], the system shall [action]" |
| Complex | "If [condition], then the system shall [action]" |

**PRP style:**
```markdown
## Acceptance Criteria
- [ ] Chunks align with section boundaries
- [ ] Each chunk includes hierarchy context
```

**Kiro EARS style:**
```markdown
## Acceptance Criteria
- When chunking document content, the system shall align chunks with section boundaries
- When generating chunks, the system shall include hierarchy context (chapter/section titles)
```

## Gaps and Limitations

### What Kiro Lacks

1. **progress.txt equivalent** — No built-in iteration memory. Maintain manually or use steering files.

2. **Story attempts/notes** — Task checkboxes lack metadata. Use comments in tasks.md.

3. **External loop control** — Can't wrap Kiro in bash script like Ralph. Use subagent prompting instead.

### What PRP Lacks (Kiro advantages)

1. **Parallel execution** — Kiro subagents run concurrently; Ralph is sequential.

2. **Persistent context** — Kiro autonomous agent learns from code reviews.

3. **Native IDE integration** — Kiro has per-file review, checkpointing.

## Dual-Agent Strategy

Run both Claude Code and Kiro for complementary strengths:

| Task | Agent |
|------|-------|
| Planning | Kiro Plan Agent or Claude `/plan-feature` |
| Spec generation | Kiro (EARS format) |
| Ralph loops | Claude Code (external control) |
| Code review | Either (Kiro has per-file review) |
| Large context analysis | Kiro (better context management) |

Update `AGENTS.md`:
```markdown
| Agent | Config File | Role |
|-------|-------------|------|
| Claude Code | CLAUDE.md | Ralph loops, execution |
| Kiro | .kiro/steering/ | Planning, code review |
| Gemini CLI | GEMINI.md | Large context review |
```

## Quick Reference

### Kiro Commands

| Command | Purpose |
|---------|---------|
| `/plan` | Start Plan Agent |
| `Shift + Tab` | Quick access to Plan Agent |
| `@agent-name` | Invoke custom agent |
| `/mcp` | Manage MCP connections |

### File Locations

| Purpose | Location |
|---------|----------|
| Global agents | `~/.kiro/agents/` |
| Project agents | `.kiro/agents/` |
| Global steering | `~/.kiro/steering/` |
| Project steering | `.kiro/steering/` |
| MCP config | `.kiro/settings/mcp.json` |

## References

[^1]: [Kiro Steering Documentation](https://kiro.dev/docs/cli/steering/) — AGENTS.md support
[^2]: [Subagents, Plan Agent Changelog](https://kiro.dev/changelog/subagents-plan-agent-grep-glob-tools-and-mcp-registry/) — December 2025 release
[^3]: [Kiro Plan Agent](https://kiro.dev/changelog/subagents-plan-agent-grep-glob-tools-and-mcp-registry/) — /plan command details
[^4]: [Contextual Hooks Changelog](https://kiro.dev/changelog/web-tools-subagents-contextual-hooks-and-per-file-code-review/) — Hook triggers
[^5]: [Agent Configuration Reference](https://kiro.dev/docs/cli/custom-agents/configuration-reference/) — JSON schema
[^6]: [Introducing Kiro Blog](https://kiro.dev/blog/introducing-kiro/) — EARS notation

## See Also

- [Kiro Official Documentation](https://kiro.dev/docs/)
- [Kiro Changelog](https://kiro.dev/changelog/)
- [Kiro GitHub](https://github.com/kirodotdev/Kiro)
- [Kiro Agent Examples](https://kiro.dev/docs/cli/custom-agents/examples/)
- [AWS re:Invent 2025 Announcements](https://caylent.com/blog/aws-reinvent-2025-every-ai-announcement-including-amazon-nova-2-and-kiro)
