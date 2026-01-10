#!/bin/bash
# ralph.sh - Outer orchestrator for autonomous Claude Code execution
#
# Usage:
#   ./ralph.sh [max_iterations] [prompt_file]
#
# Examples:
#   ./ralph.sh                    # Default: 15 iterations, ralph-prompt.md
#   ./ralph.sh 25                 # 25 iterations
#   ./ralph.sh 20 my-prompt.md    # Custom prompt file

set -e

# Configuration
MAX_ITERATIONS=${1:-15}
PROMPT_FILE=${2:-"ralph-prompt.md"}
PROGRESS_FILE="features/progress.txt"
LOG_FILE="ralph.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
    if [ ! -f "$PROMPT_FILE" ]; then
        echo -e "${RED}Error: Prompt file not found: $PROMPT_FILE${NC}"
        echo "Create a ralph-prompt.md with your execution instructions."
        exit 1
    fi

    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}Error: Not in a git repository${NC}"
        exit 1
    fi

    if ! command -v claude &> /dev/null; then
        echo -e "${RED}Error: claude CLI not found${NC}"
        exit 1
    fi

    # Create progress file if it doesn't exist
    mkdir -p features
    if [ ! -f "$PROGRESS_FILE" ]; then
        echo "# Progress Log" > "$PROGRESS_FILE"
        echo "" >> "$PROGRESS_FILE"
        echo "## Codebase Patterns" >> "$PROGRESS_FILE"
        echo "" >> "$PROGRESS_FILE"
    fi
}

# Create checkpoint for rollback
create_checkpoint() {
    log "Creating checkpoint..."
    git stash push -m "ralph-checkpoint-$(date +%Y%m%d-%H%M%S)" 2>/dev/null || true
}

# Check for completion markers
check_completion() {
    if grep -q "FEATURE_COMPLETE" "$PROGRESS_FILE" 2>/dev/null; then
        return 0  # Complete
    fi
    return 1  # Not complete
}

# Check for blocked state
check_blocked() {
    if grep -q "ALL_BLOCKED" "$PROGRESS_FILE" 2>/dev/null; then
        return 0  # Blocked
    fi
    return 1  # Not blocked
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
        echo "Recent commits:"
        git log --oneline -5
    fi
}

trap cleanup EXIT

# Main loop
main() {
    preflight_check
    create_checkpoint

    echo -e "${GREEN}Starting Ralph loop${NC}"
    echo "Max iterations: $MAX_ITERATIONS"
    echo "Prompt file: $PROMPT_FILE"
    echo "Progress file: $PROGRESS_FILE"
    echo ""

    log "=== Ralph Loop Started ==="

    while [ $ITERATION -lt $MAX_ITERATIONS ]; do
        ITERATION=$((ITERATION + 1))

        echo ""
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        log "Iteration $ITERATION of $MAX_ITERATIONS"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

        # Run Claude with the prompt
        if ! cat "$PROMPT_FILE" | claude --print 2>&1 | tee -a "$LOG_FILE"; then
            log "Claude exited with error"
        fi

        # Check for completion
        if check_completion; then
            echo ""
            echo -e "${GREEN}✓ FEATURE_COMPLETE detected${NC}"
            log "Feature completed successfully"
            exit 0
        fi

        # Check for blocked state
        if check_blocked; then
            echo ""
            echo -e "${RED}✗ ALL_BLOCKED detected${NC}"
            log "All stories blocked - human intervention needed"
            exit 1
        fi

        # Brief pause between iterations
        sleep 2
    done

    echo ""
    echo -e "${YELLOW}⚠ Max iterations reached${NC}"
    log "Max iterations ($MAX_ITERATIONS) reached"
    exit 2
}

main
