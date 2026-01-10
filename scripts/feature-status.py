#!/usr/bin/env python3
"""
Feature status helper for Ralph loops.

Parses feature YAML files and provides status information.
Uses only stdlib (no external dependencies).

Usage:
    feature-status.py <command> [feature_file]

Commands:
    next        Print ID of next pending story (exit 1 if none)
    status      Print summary of all stories
    pending     Count of pending stories
    blocked     Count of blocked stories
    complete    Count of complete stories
    all-done    Exit 0 if all complete, exit 1 otherwise
    all-blocked Exit 0 if all remaining are blocked, exit 1 otherwise
    get <id>    Print story details as KEY=VALUE pairs

Examples:
    ./feature-status.py next features/F0001-epub-parsing/F0001-tracking.yaml
    ./feature-status.py status
    ./feature-status.py all-done && echo "Feature complete!"
"""

import sys
import re
from pathlib import Path


def parse_yaml_simple(content: str) -> dict:
    """
    Simple YAML parser for our feature format.
    Handles only the subset we need (no anchors, complex types, etc.)
    """
    result = {"stories": []}
    current_story = None
    current_list_key = None
    indent_stack = []

    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Skip comments and empty lines
        if not stripped or stripped.startswith("#"):
            i += 1
            continue

        # Calculate indent level
        indent = len(line) - len(line.lstrip())

        # Check for list item
        if stripped.startswith("- "):
            item_content = stripped[2:].strip()

            # Is this a new story?
            if current_list_key == "stories" or (
                indent_stack and indent_stack[-1][0] == "stories"
            ):
                # Check if it's a key-value in list
                if ":" in item_content:
                    key, value = item_content.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")

                    if key == "id":
                        # New story
                        if current_story:
                            result["stories"].append(current_story)
                        current_story = {"id": value, "criteria": []}
                    elif current_story:
                        current_story[key] = value
                elif current_list_key == "criteria" and current_story:
                    current_story["criteria"].append(item_content.strip('"').strip("'"))

            elif current_list_key == "criteria" and current_story:
                current_story["criteria"].append(item_content.strip('"').strip("'"))

            i += 1
            continue

        # Check for key: value
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key == "stories":
                current_list_key = "stories"
                indent_stack.append(("stories", indent))
            elif key == "criteria":
                current_list_key = "criteria"
            elif key == "validation":
                current_list_key = "validation"
                result["validation"] = {}
            elif key == "summary":
                current_list_key = "summary"
                result["summary"] = {}
            elif current_list_key == "validation" and value:
                result.setdefault("validation", {})[key] = value
            elif current_list_key == "summary" and value:
                result.setdefault("summary", {})[key] = value
            elif current_story and value:
                # Convert numeric strings
                if value.isdigit():
                    value = int(value)
                current_story[key] = value
            elif value and not current_story:
                # Top-level key
                result[key] = value

        i += 1

    # Don't forget the last story
    if current_story:
        result["stories"].append(current_story)

    return result


def find_feature_file() -> Path | None:
    """Find the current feature file."""
    features_dir = Path("features")
    if not features_dir.exists():
        return None

    # Look for YAML files matching F####-*.yaml pattern
    yaml_files = list(features_dir.glob("F[0-9][0-9][0-9][0-9]-*.yaml"))
    if yaml_files:
        # Return most recently modified
        return max(yaml_files, key=lambda p: p.stat().st_mtime)

    # Fallback to current.yaml
    current = features_dir / "current.yaml"
    if current.exists():
        return current

    return None


def load_feature(path: Path | None = None) -> dict:
    """Load and parse feature file."""
    if path is None:
        path = find_feature_file()

    if path is None or not path.exists():
        print(f"Error: Feature file not found", file=sys.stderr)
        sys.exit(1)

    content = path.read_text()
    return parse_yaml_simple(content)


def get_stories_by_status(feature: dict, status: str) -> list:
    """Get stories with given status."""
    return [s for s in feature.get("stories", []) if s.get("status") == status]


def get_next_pending(feature: dict) -> dict | None:
    """Get highest priority pending story."""
    pending = get_stories_by_status(feature, "pending")
    if not pending:
        return None
    # Sort by priority (lowest number = highest priority)
    pending.sort(key=lambda s: s.get("priority", 999))
    return pending[0]


def print_status(feature: dict):
    """Print status summary."""
    stories = feature.get("stories", [])
    total = len(stories)
    complete = len(get_stories_by_status(feature, "complete"))
    blocked = len(get_stories_by_status(feature, "blocked"))
    pending = len(get_stories_by_status(feature, "pending"))
    in_progress = len(get_stories_by_status(feature, "in_progress"))

    print(f"Feature: {feature.get('id', 'unknown')} - {feature.get('name', 'unnamed')}")
    print(f"Plan: {feature.get('plan', 'none')}")
    print(f"Branch: {feature.get('branch', 'none')}")
    print()
    print(f"Stories: {complete}/{total} complete")
    print(f"  Complete:    {complete}")
    print(f"  In Progress: {in_progress}")
    print(f"  Pending:     {pending}")
    print(f"  Blocked:     {blocked}")
    print()

    # List stories
    for story in sorted(stories, key=lambda s: s.get("priority", 999)):
        status_icon = {
            "complete": "[x]",
            "pending": "[ ]",
            "blocked": "[!]",
            "in_progress": "[>]",
        }.get(story.get("status", "pending"), "[?]")
        print(f"  {status_icon} {story.get('id', '???')}: {story.get('title', 'untitled')}")


def print_story(story: dict):
    """Print story as KEY=VALUE pairs for shell parsing."""
    for key, value in story.items():
        if key == "criteria":
            # Join criteria with |
            print(f"CRITERIA={' | '.join(value)}")
        else:
            print(f"{key.upper()}={value}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    feature_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    if command == "help" or command == "--help":
        print(__doc__)
        sys.exit(0)

    feature = load_feature(feature_file)

    if command == "next":
        story = get_next_pending(feature)
        if story:
            print(story.get("id", ""))
            sys.exit(0)
        else:
            sys.exit(1)

    elif command == "status":
        print_status(feature)

    elif command == "pending":
        print(len(get_stories_by_status(feature, "pending")))

    elif command == "blocked":
        print(len(get_stories_by_status(feature, "blocked")))

    elif command == "complete":
        print(len(get_stories_by_status(feature, "complete")))

    elif command == "all-done":
        pending = len(get_stories_by_status(feature, "pending"))
        in_progress = len(get_stories_by_status(feature, "in_progress"))
        if pending == 0 and in_progress == 0:
            sys.exit(0)
        sys.exit(1)

    elif command == "all-blocked":
        pending = len(get_stories_by_status(feature, "pending"))
        in_progress = len(get_stories_by_status(feature, "in_progress"))
        blocked = len(get_stories_by_status(feature, "blocked"))
        if pending == 0 and in_progress == 0 and blocked > 0:
            sys.exit(0)
        sys.exit(1)

    elif command == "get":
        if len(sys.argv) < 3:
            print("Error: get requires story ID", file=sys.stderr)
            sys.exit(1)
        story_id = sys.argv[2] if len(sys.argv) == 3 else sys.argv[3]
        for story in feature.get("stories", []):
            if story.get("id") == story_id:
                print_story(story)
                sys.exit(0)
        print(f"Error: Story {story_id} not found", file=sys.stderr)
        sys.exit(1)

    elif command == "validation":
        validation = feature.get("validation", {})
        for key, cmd in validation.items():
            print(f"{key.upper()}={cmd}")

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Run with --help for usage", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
