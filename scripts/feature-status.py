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
    testing <id>  Print testing requirements for a story (unit,integration,api,ui)
    feature-testing  Print aggregated testing requirements for all stories

Examples:
    ./feature-status.py next features/F0001-epub-parsing/F0001-tracking.yaml
    ./feature-status.py status
    ./feature-status.py all-done && echo "Feature complete!"
    ./feature-status.py testing F0004c-04
"""

import sys
from pathlib import Path


def parse_yaml_simple(content: str) -> dict:
    """
    Simple YAML parser for our feature format.
    Handles only the subset we need (no anchors, complex types, etc.)

    Supports:
    - stories with id, title, status, priority, criteria (list), testing (list)
    - ui_validation with pages (list), viewports (list), capture, analyze
    """
    result = {"stories": []}
    current_story = None
    current_list_key = None
    current_dict_key = None
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
                        current_story = {"id": value, "criteria": [], "testing": ["unit"]}
                    elif current_story:
                        current_story[key] = value
                elif current_list_key == "criteria" and current_story:
                    current_story["criteria"].append(item_content.strip('"').strip("'"))
                elif current_list_key == "testing" and current_story:
                    current_story.setdefault("testing", []).append(item_content.strip('"').strip("'"))
                elif current_list_key == "pages" and current_story and "ui_validation" in current_story:
                    current_story["ui_validation"].setdefault("pages", []).append(item_content.strip('"').strip("'"))
                elif current_list_key == "viewports" and current_story and "ui_validation" in current_story:
                    try:
                        current_story["ui_validation"].setdefault("viewports", []).append(int(item_content))
                    except ValueError:
                        pass

            elif current_list_key == "criteria" and current_story:
                current_story["criteria"].append(item_content.strip('"').strip("'"))
            elif current_list_key == "testing" and current_story:
                # Handle inline list format: testing: [unit, ui]
                current_story.setdefault("testing", []).append(item_content.strip('"').strip("'"))
            elif current_list_key == "pages" and current_story:
                current_story.setdefault("ui_validation", {}).setdefault("pages", []).append(item_content.strip('"').strip("'"))

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
            elif key == "testing":
                current_list_key = "testing"
                # Handle inline list format: testing: [unit, ui]
                if value.startswith("[") and value.endswith("]"):
                    items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
                    if current_story:
                        current_story["testing"] = [i for i in items if i]
                    current_list_key = None
                elif current_story:
                    current_story["testing"] = []
            elif key == "ui_validation":
                current_dict_key = "ui_validation"
                if current_story:
                    current_story["ui_validation"] = {}
            elif key == "pages":
                current_list_key = "pages"
                # Handle inline list format: pages: [/library, /about]
                if value.startswith("[") and value.endswith("]"):
                    items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",")]
                    if current_story and "ui_validation" in current_story:
                        current_story["ui_validation"]["pages"] = [i for i in items if i]
                    current_list_key = None
            elif key == "viewports":
                current_list_key = "viewports"
                # Handle inline list format: viewports: [375, 768, 1280]
                if value.startswith("[") and value.endswith("]"):
                    try:
                        items = [int(v.strip()) for v in value[1:-1].split(",") if v.strip()]
                        if current_story and "ui_validation" in current_story:
                            current_story["ui_validation"]["viewports"] = items
                    except ValueError:
                        pass
                    current_list_key = None
            elif key == "validation":
                current_list_key = "validation"
                current_dict_key = None
                result["validation"] = {}
            elif key == "summary":
                current_list_key = "summary"
                current_dict_key = None
                result["summary"] = {}
            elif current_dict_key == "ui_validation" and current_story and value:
                # Handle ui_validation sub-keys like capture, analyze
                if value.lower() in ("true", "false"):
                    current_story["ui_validation"][key] = value.lower() == "true"
                else:
                    current_story["ui_validation"][key] = value
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
        print("Error: Feature file not found", file=sys.stderr)
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
        elif key == "testing":
            # Join testing with comma
            print(f"TESTING={','.join(value)}")
        elif key == "ui_validation":
            # Flatten ui_validation
            for k, v in value.items():
                if isinstance(v, list):
                    print(f"UI_{k.upper()}={','.join(str(x) for x in v)}")
                else:
                    print(f"UI_{k.upper()}={v}")
        else:
            print(f"{key.upper()}={value}")


def get_story_testing(feature: dict, story_id: str) -> list[str]:
    """Get testing requirements for a story."""
    for story in feature.get("stories", []):
        if story.get("id") == story_id:
            return story.get("testing", ["unit"])
    return ["unit"]


def get_feature_testing(feature: dict) -> list[str]:
    """Get aggregated testing requirements for all stories."""
    all_testing = set()
    for story in feature.get("stories", []):
        testing = story.get("testing", ["unit"])
        all_testing.update(testing)
    return sorted(list(all_testing))


def get_story_ui_validation(feature: dict, story_id: str) -> dict:
    """Get UI validation config for a story."""
    for story in feature.get("stories", []):
        if story.get("id") == story_id:
            return story.get("ui_validation", {})
    return {}


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

    elif command == "testing":
        if len(sys.argv) < 3:
            print("Error: testing requires story ID", file=sys.stderr)
            sys.exit(1)
        story_id = sys.argv[2] if len(sys.argv) == 3 else sys.argv[3]
        testing = get_story_testing(feature, story_id)
        print(",".join(testing))

    elif command == "feature-testing":
        testing = get_feature_testing(feature)
        print(",".join(testing))

    elif command == "ui-validation":
        if len(sys.argv) < 3:
            print("Error: ui-validation requires story ID", file=sys.stderr)
            sys.exit(1)
        story_id = sys.argv[2] if len(sys.argv) == 3 else sys.argv[3]
        ui_val = get_story_ui_validation(feature, story_id)
        if ui_val:
            pages = ui_val.get("pages", ["/", "/library", "/about"])
            viewports = ui_val.get("viewports", [375, 768, 1280])
            print(f"PAGES={','.join(pages)}")
            print(f"VIEWPORTS={','.join(str(v) for v in viewports)}")
            print(f"CAPTURE={ui_val.get('capture', 'always')}")
            print(f"ANALYZE={ui_val.get('analyze', True)}")
        else:
            # Defaults for stories with ui testing
            testing = get_story_testing(feature, story_id)
            if "ui" in testing:
                print("PAGES=/,/library,/about")
                print("VIEWPORTS=375,768,1280")
                print("CAPTURE=always")
                print("ANALYZE=true")
            else:
                sys.exit(1)  # No UI validation needed

    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Run with --help for usage", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
