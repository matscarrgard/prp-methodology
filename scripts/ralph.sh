#!/bin/bash
# ralph.sh - Outer orchestrator for autonomous Claude Code execution
#
# Usage:
#   ./ralph.sh [max_iterations] [feature_file]
#
# Examples:
#   ./ralph.sh                              # Default: 15 iterations, auto-detect feature
#   ./ralph.sh 25                           # 25 iterations
#   ./ralph.sh 20 features/F0001-auth/F0001-tracking.yaml  # Specific feature file
#
# Prerequisites:
#   - Git repository
#   - claude CLI installed
#   - Feature tracking file (features/F####-name/F####-tracking.yaml)
#   - ralph-prompt.md in project root

set -e

# Get script directory for finding helper scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUS_SCRIPT="$SCRIPT_DIR/feature-status.py"
SCREENSHOT_SCRIPT="$SCRIPT_DIR/capture-screenshots.py"

# Configuration
MAX_ITERATIONS=${1:-15}
FEATURE_FILE=${2:-""}  # Empty = auto-detect
PROMPT_FILE="ralph-prompt.md"
PROGRESS_FILE="features/progress.txt"
LOG_FILE="ralph.log"

# Test scope commands
declare -A TEST_COMMANDS
TEST_COMMANDS[unit]="uv run pytest tests/unit/ -x -q"
TEST_COMMANDS[integration]="uv run pytest tests/integration/ -x -q"
TEST_COMMANDS[api]="uv run pytest tests/integration/ -x -q -k 'route or endpoint'"
TEST_COMMANDS[ui]="uv run pytest tests/e2e/ --e2e -x -q"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialize
ITERATION=0
START_TIME=$(date +%s)

# Logging function
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo -e "$msg"
    echo "$msg" >> "$LOG_FILE"
}

# Check prerequisites
preflight_check() {
    # Check for prompt file
    if [ ! -f "$PROMPT_FILE" ]; then
        echo -e "${RED}Error: Prompt file not found: $PROMPT_FILE${NC}"
        echo "Copy from .prp/templates/ralph-prompt.template.md or create your own."
        exit 1
    fi

    # Check git repo
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi

    # Check claude CLI
    if ! command -v claude &> /dev/null; then
        echo -e "${RED}Error: claude CLI not found${NC}"
        exit 1
    fi

    # Check for feature file
    if [ -n "$FEATURE_FILE" ]; then
        if [ ! -f "$FEATURE_FILE" ]; then
            echo -e "${RED}Error: Feature file not found: $FEATURE_FILE${NC}"
            exit 1
        fi
    else
        # Auto-detect feature file (look in subdirectories)
        FEATURE_FILE=$(find features -path "features/F[0-9][0-9][0-9][0-9]-*/*-tracking.yaml" 2>/dev/null | head -1)
        if [ -z "$FEATURE_FILE" ]; then
            echo -e "${RED}Error: No feature tracking file found${NC}"
            echo "Create one with /plan-feature at features/F####-name/F####-tracking.yaml"
            exit 1
        fi
    fi

    # Check status script
    if [ ! -f "$STATUS_SCRIPT" ]; then
        echo -e "${RED}Error: Status script not found: $STATUS_SCRIPT${NC}"
        exit 1
    fi

    # Ensure progress file exists
    mkdir -p features
    if [ ! -f "$PROGRESS_FILE" ]; then
        cat > "$PROGRESS_FILE" << 'EOF'
# Progress Log

## Codebase Patterns
<!-- Learnings that benefit ALL iterations - READ FIRST -->

---

## Iteration Log

EOF
    fi

    echo -e "${BLUE}Feature file: $FEATURE_FILE${NC}"
}

# Create checkpoint for rollback
create_checkpoint() {
    log "Creating checkpoint..."
    git stash push -m "ralph-checkpoint-$(date +%Y%m%d-%H%M%S)" 2>/dev/null || true
}

# Check story status using Python helper
check_all_done() {
    python3 "$STATUS_SCRIPT" all-done "$FEATURE_FILE" 2>/dev/null
    return $?
}

check_all_blocked() {
    python3 "$STATUS_SCRIPT" all-blocked "$FEATURE_FILE" 2>/dev/null
    return $?
}

get_next_story() {
    python3 "$STATUS_SCRIPT" next "$FEATURE_FILE" 2>/dev/null
}

get_pending_count() {
    python3 "$STATUS_SCRIPT" pending "$FEATURE_FILE" 2>/dev/null
}

get_complete_count() {
    python3 "$STATUS_SCRIPT" complete "$FEATURE_FILE" 2>/dev/null
}

get_story_testing() {
    # Get testing requirements for a story (comma-separated: unit,ui,integration)
    local story_id=$1
    python3 "$STATUS_SCRIPT" testing "$story_id" "$FEATURE_FILE" 2>/dev/null
}

get_feature_dir() {
    # Extract feature directory from feature file path
    dirname "$FEATURE_FILE"
}

# Post-story validation for UI stories
run_ui_validation() {
    local story_id=$1
    local feature_dir=$(get_feature_dir)
    local testing=$(get_story_testing "$story_id")

    # Check if UI testing is required
    if [[ "$testing" == *"ui"* ]]; then
        log "UI validation required for $story_id"

        # Check if screenshots exist
        local screenshot_dir="$feature_dir/screenshots/$story_id"
        if [ -d "$screenshot_dir" ] && [ "$(ls -A $screenshot_dir 2>/dev/null)" ]; then
            log "Screenshots found in $screenshot_dir"
        else
            log "Capturing screenshots for $story_id..."
            if [ -f "$SCREENSHOT_SCRIPT" ]; then
                python3 "$SCREENSHOT_SCRIPT" "$feature_dir" "$story_id" --start-server 2>&1 | tee -a "$LOG_FILE"
            else
                echo -e "${YELLOW}Warning: Screenshot script not found${NC}"
            fi
        fi
    fi
}

# Print current status
print_status() {
    echo ""
    echo -e "${BLUE}=== Feature Status ===${NC}"
    python3 "$STATUS_SCRIPT" status "$FEATURE_FILE" 2>/dev/null || true
    echo ""
}

# Cleanup on exit
cleanup() {
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    log "Ralph finished after $ITERATION iterations in ${DURATION}s"

    if [ $ITERATION -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}=== Summary ===${NC}"
        echo "Iterations: $ITERATION / $MAX_ITERATIONS"
        echo "Duration: ${DURATION}s"
        echo "Log: $LOG_FILE"
        echo ""

        # Show final status
        COMPLETE=$(get_complete_count)
        PENDING=$(get_pending_count)
        echo "Stories complete: $COMPLETE"
        echo "Stories pending: $PENDING"
        echo ""

        echo "Recent commits:"
        git log --oneline -5
    fi
}

trap cleanup EXIT

# Main loop
main() {
    preflight_check
    print_status
    create_checkpoint

    echo -e "${GREEN}Starting Ralph loop${NC}"
    echo "Max iterations: $MAX_ITERATIONS"
    echo "Prompt file: $PROMPT_FILE"
    echo "Feature file: $FEATURE_FILE"
    echo ""

    log "=== Ralph Loop Started ==="
    log "Feature: $FEATURE_FILE"

    while [ $ITERATION -lt $MAX_ITERATIONS ]; do
        ITERATION=$((ITERATION + 1))

        # Get next story to work on
        NEXT_STORY=$(get_next_story)

        echo ""
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        log "Iteration $ITERATION of $MAX_ITERATIONS"
        if [ -n "$NEXT_STORY" ]; then
            echo -e "${BLUE}Next story: $NEXT_STORY${NC}"
        fi
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        # Run Claude with the prompt
        # Using --dangerously-skip-permissions since hooks handle safety
        if ! claude --dangerously-skip-permissions -p "$(cat "$PROMPT_FILE")" 2>&1 | tee -a "$LOG_FILE"; then
            log "Claude exited with error"
        fi

        # Post-iteration validation: check if story just completed needs UI validation
        if [ -n "$NEXT_STORY" ]; then
            # Check if the story was just completed
            local story_status=$(python3 "$STATUS_SCRIPT" get "$NEXT_STORY" "$FEATURE_FILE" 2>/dev/null | grep "^STATUS=" | cut -d= -f2)
            if [ "$story_status" = "complete" ]; then
                run_ui_validation "$NEXT_STORY"
            fi
        fi

        # Check for completion (all stories done)
        if check_all_done; then
            echo ""
            echo -e "${GREEN}✓ All stories complete!${NC}"
            log "Feature completed successfully"

            # Append completion marker to progress file
            echo "" >> "$PROGRESS_FILE"
            echo "---" >> "$PROGRESS_FILE"
            echo "## FEATURE_COMPLETE" >> "$PROGRESS_FILE"
            echo "Completed at: $(date '+%Y-%m-%d %H:%M:%S')" >> "$PROGRESS_FILE"
            echo "Iterations: $ITERATION" >> "$PROGRESS_FILE"

            exit 0
        fi

        # Check for blocked state (all remaining are blocked)
        if check_all_blocked; then
            echo ""
            echo -e "${RED}✗ All remaining stories blocked${NC}"
            log "All stories blocked - human intervention needed"

            # Append blocked marker to progress file
            echo "" >> "$PROGRESS_FILE"
            echo "---" >> "$PROGRESS_FILE"
            echo "## ALL_BLOCKED" >> "$PROGRESS_FILE"
            echo "Blocked at: $(date '+%Y-%m-%d %H:%M:%S')" >> "$PROGRESS_FILE"
            echo "Iterations: $ITERATION" >> "$PROGRESS_FILE"

            exit 1
        fi

        # Brief pause between iterations
        sleep 2
    done

    echo ""
    echo -e "${YELLOW}⚠ Max iterations reached${NC}"
    log "Max iterations ($MAX_ITERATIONS) reached"

    # Show what's left
    PENDING=$(get_pending_count)
    echo "Stories still pending: $PENDING"

    exit 2
}

main
