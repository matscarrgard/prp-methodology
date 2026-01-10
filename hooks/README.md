# PRP Methodology Hooks

Claude Code hooks for safety and automation.

## Available Hooks

### validate-bash.py

**Type**: PreToolUse (Bash)
**Purpose**: Block dangerous commands, prompt for risky ones

Patterns:
- **BLOCKED**: `rm -rf /`, disk writes, fork bombs
- **ASK**: `rm -rf`, force push, DROP TABLE, hard reset
- **WARN**: curl|bash, eval (logged but allowed)

### Installation

Add to `.claude/settings.json`:

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

## Hook Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Allow the tool call |
| 2 | Block the tool call |
| JSON output | Special behavior (e.g., ask user) |

## JSON Output Format

For "ask" behavior:

```json
{
  "decision": "ask",
  "reason": "Confirm: Force push will overwrite remote history"
}
```

## Creating New Hooks

1. Create Python script in `hooks/`
2. Read input from stdin (JSON with tool info)
3. Exit with appropriate code
4. Add to settings.json

Template:

```python
#!/usr/bin/env python3
import json
import sys

data = json.load(sys.stdin)
tool_input = data.get("tool_input", {})

# Your validation logic here

sys.exit(0)  # 0=allow, 2=block
```
