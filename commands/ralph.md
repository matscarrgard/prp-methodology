# Ralph - Autonomous Feature Execution

Run the Ralph autonomous loop to execute a feature's stories.

## Input

$ARGUMENTS - Feature ID (e.g., `F0004c`) and optional max iterations (default: 15)

**Examples:**
- `/ralph F0004c` - Run Ralph for F0004c with default 15 iterations
- `/ralph F0004c 25` - Run Ralph for F0004c with 25 iterations

## What is Ralph?

Ralph is an autonomous execution loop named after Ralph Wiggum - he keeps trying until he succeeds.

```
Without Ralph (context degrades):
[Plan][Story1][Debug][Story2][Debug]...[DEGRADED]

With Ralph (fresh context each story):
Iteration 1: [Read Memory][Story1][Commit] → fresh
Iteration 2: [Read Memory][Story2][Commit] → fresh
```

Each iteration:
1. Feeds prompt to Claude Code
2. Claude works on ONE story until completion
3. Checks feature YAML for status
4. If not complete, loops with fresh context
5. Repeats until done or max iterations

## Prerequisites

Feature must have been planned with `/plan-feature` which creates:
- `features/F####-name/F####-tracking.yaml`
- `features/F####-name/F####-plan.md`

**Do NOT run bash commands to verify these exist** - if `/plan-feature` was run, they exist.

## Process

### Phase 1: Configure

1. **Read the tracking YAML** to get story counts
   - Use the Read tool on `features/F####-name/F####-tracking.yaml`

2. **Display configuration** to user:
   - Feature ID and name
   - Number of stories (pending/complete/blocked)
   - Max iterations (default: 15)
   - Estimated cost range

3. **Confirm execution**
   Ask user to confirm before starting autonomous loop.

### Phase 2: Execute

4. **Run Ralph in background**
   ```bash
   .prp/scripts/ralph.sh $MAX_ITERATIONS $TRACKING_FILE
   ```

   Run this command with `run_in_background: true` so you can monitor progress.

   The script will:
   - Create checkpoint commit
   - Loop through stories
   - Update YAML status after each
   - Commit after each successful story
   - Stop when all complete or max iterations

### Phase 3: Monitor

5. **Monitor with SIMPLE, SEPARATE commands**

   Run these as individual tool calls, NOT combined:
   ```bash
   sleep 60
   ```
   ```bash
   tail -50 ralph.log
   ```

   Repeat until Ralph completes or user interrupts.

   **WRONG** (do not combine):
   ```bash
   sleep 60 && tail -50 ralph.log  # NO!
   ```

   **To check story status**: Use the Read tool on the tracking YAML file.

   User can also monitor in another terminal with `tail -f ralph.log`.

## Output

Ralph runs autonomously. When complete:

- **Success**: All stories marked complete in YAML
- **Blocked**: Some stories blocked (need human help)
- **Max iterations**: Stopped at limit (can resume)

Check results:
```bash
git log --oneline -10
```

Then use Read tool on tracking YAML to see final story statuses, and run `/validate`.

## Rollback

If Ralph makes mistakes:
```bash
# Rollback last N commits
git reset --hard HEAD~N

# Or find checkpoint
git stash list  # Look for ralph-checkpoint-*
git stash pop stash@{N}
```

## Cost Estimates

| Story Size | Per Iteration | Feature (5-10 stories) |
|------------|---------------|------------------------|
| Simple | $0.50-1.50 | $5-15 |
| Medium | $1.50-3.00 | $15-30 |
| Complex | $3.00-6.00 | $30-60 |

## Example

```bash
# 1. Plan feature (creates tracking YAML)
/plan-feature F0004c

# 2. Run Ralph
/ralph F0004c

# 3. Monitor in another terminal
tail -f ralph.log

# 4. When done, validate
/validate
```

## Safety

- **Max iterations**: Always set a limit (default: 15)
- **Checkpoints**: Each story commits separately
- **Blocked detection**: Stops if story fails 3 times
- **Human on loop**: Check periodically, ready to `git reset`
