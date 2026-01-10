#!/usr/bin/env python3
"""Validate bash commands for dangerous patterns.

This hook blocks or prompts for confirmation on potentially dangerous commands.
Used as a PreToolUse hook for the Bash tool.

Exit codes:
- 0: Allow command
- 2: Block command
- JSON with {"decision": "ask"}: Prompt user for confirmation
"""

import json
import re
import sys

# Commands that are ALWAYS blocked - catastrophic risk
BLOCKED_PATTERNS = [
    (r"rm\s+-rf\s+/(?!\w)", "Cannot delete root filesystem"),
    (r"rm\s+-rf\s+~", "Cannot delete home directory"),
    (r"rm\s+-rf\s+\*", "Cannot delete everything in directory"),
    (r">\s*/dev/sd", "Cannot write directly to disk"),
    (r"mkfs\.", "Cannot format filesystem"),
    (r"dd\s+if=.*of=/dev/", "Cannot write directly to disk device"),
    (r":\(\)\{.*\|.*&\s*\};:", "Fork bomb detected"),
    (r"chmod\s+-R\s+777\s+/", "Cannot chmod 777 root"),
    (r"chown\s+-R\s+.*\s+/(?!\w)", "Cannot chown root"),
]

# Commands that require confirmation - significant risk
ASK_PATTERNS = [
    (r"rm\s+-rf", "Confirm: Recursively delete files?"),
    (r"git\s+push.*--force", "Confirm: Force push will overwrite remote history"),
    (r"git\s+reset\s+--hard", "Confirm: Hard reset will lose uncommitted changes"),
    (r"DROP\s+TABLE", "Confirm: Drop database table?"),
    (r"DROP\s+DATABASE", "Confirm: Drop entire database?"),
    (r"DELETE\s+FROM\s+\w+\s*;?\s*$", "Confirm: Delete all rows from table?"),
    (r"TRUNCATE\s+TABLE", "Confirm: Truncate table?"),
    (r"git\s+branch\s+-D", "Confirm: Force delete branch?"),
    (r"docker\s+system\s+prune", "Confirm: Prune Docker system?"),
    (r"kubectl\s+delete", "Confirm: Delete Kubernetes resource?"),
]

# Patterns that are allowed but worth noting (for logging)
WARN_PATTERNS = [
    (r"curl.*\|\s*(bash|sh)", "Piping curl to shell"),
    (r"wget.*\|\s*(bash|sh)", "Piping wget to shell"),
    (r"eval\s+", "Using eval"),
]


def main():
    # Read hook input from stdin
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # If no input or invalid JSON, allow (fail open for usability)
        sys.exit(0)

    # Get the command from tool input
    cmd = data.get("tool_input", {}).get("command", "")

    if not cmd:
        sys.exit(0)

    # Check blocked patterns first
    for pattern, msg in BLOCKED_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            print(f"BLOCKED: {msg}", file=sys.stderr)
            print(f"Command: {cmd}", file=sys.stderr)
            sys.exit(2)

    # Check ask patterns
    for pattern, msg in ASK_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            # Output JSON for ask behavior
            result = {"decision": "ask", "reason": msg, "command": cmd}
            print(json.dumps(result))
            sys.exit(0)

    # Check warn patterns (just log, don't block)
    for pattern, msg in WARN_PATTERNS:
        if re.search(pattern, cmd, re.IGNORECASE):
            print(f"WARNING: {msg}", file=sys.stderr)
            # Continue - don't block, just warn

    # Allow the command
    sys.exit(0)


if __name__ == "__main__":
    main()
