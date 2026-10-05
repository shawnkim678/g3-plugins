---
name: git-commit
description: Git workflow commands for committing, pushing, and managing branches. Includes commit creation, PR workflow, and cleanup of stale branches (git, commit, push, pull request, branch).
---

<!-- Derived from anthropics/claude-plugins-official plugins/commit-commands/commands/commit.md, commit-push-pr.md, and clean_gone.md (Apache-2.0). Adapted for G3 Code: consolidated to single skill with subprocess workflow guidance. -->

# Git Commit Workflow

This skill provides tools for managing git commits, pushing changes, creating pull requests, and cleaning up stale branches.

## Commit Creation

Create a git commit from staged and unstaged changes.

### Steps

1. Review current git status using `git status`
2. Review staged and unstaged changes using `git diff HEAD`
3. Check current branch using `git branch --show-current`
4. Review recent commits using `git log --oneline -10`
5. Stage relevant files using `git add`
6. Create a single commit with an appropriate message using `git commit -m`

### Notes

- Craft a descriptive commit message that explains the "why" behind the changes
- Stage only the files that should be committed; avoid `git add .` without reviewing what's included
- Use conventional commit format if the project specifies one in CLAUDE.md
- Create a single logical commit per request unless explicitly instructed otherwise

## Commit, Push, and Create Pull Request

Create a commit, push to a remote branch, and open a pull request in one workflow.

### Steps

1. Check git status and review changes
2. If on main branch: create a new feature branch with `git checkout -b <branch-name>`
3. Stage relevant changes with `git add`
4. Create a single commit with appropriate message
5. Push the branch to origin with `git push -u origin <branch-name>`
6. Create a pull request using `gh pr create` (if GitHub CLI is available)

### GitHub CLI Requirements

Pull request creation requires the `gh` command-line tool to be installed and authenticated. If `gh` is not available, provide the user with:
- The branch name pushed to origin
- A link to create the PR manually: `https://github.com/<owner>/<repo>/compare/<branch-name>`
- Suggested PR title and description based on the commit message

### Notes

- Use `git push -u origin` to create the remote tracking branch
- If gh is available, provide a descriptive PR title and body
- Reference relevant issues in the PR description (e.g., "Fixes #123")

## Clean Up Stale Branches

Remove local branches that have been deleted from the remote repository, including associated worktrees.

### Steps

1. List all branches to identify [gone] branches:
   ```bash
   git branch -v
   ```
   Note: Branches with '+' prefix have associated worktrees.

2. List worktrees to identify those associated with [gone] branches:
   ```bash
   git worktree list
   ```

3. Remove worktrees and delete [gone] branches:
   - For each branch marked [gone]:
     - Find associated worktree (if any)
     - Remove worktree with `git worktree remove --force <path>`
     - Delete branch with `git branch -D <branch-name>`

### Implementation

Execute the following to clean all [gone] branches and their worktrees:

```bash
git branch -v | grep '\[gone\]' | sed 's/^[+* ]//' | awk '{print $1}' | while read branch; do
  echo "Processing branch: $branch"
  worktree=$(git worktree list | grep "\\[$branch\\]" | awk '{print $1}')
  if [ ! -z "$worktree" ] && [ "$worktree" != "$(git rev-parse --show-toplevel)" ]; then
    echo "  Removing worktree: $worktree"
    git worktree remove --force "$worktree"
  fi
  echo "  Deleting branch: $branch"
  git branch -D "$branch"
done
```

### Expected Result

- All worktrees associated with [gone] branches are removed
- All [gone] branches are deleted locally
- Status message confirms which worktrees and branches were cleaned up
- If no [gone] branches exist, report that no cleanup was needed

## Best Practices

- **Review before committing**: Always run `git status` and `git diff` to verify changes before committing
- **Descriptive messages**: Write commit messages that explain why changes were made, not just what changed
- **One feature per branch**: Use feature branches for new work, fixes, or experiments
- **Keep branches clean**: Regularly remove merged and stale branches
- **Atomic commits**: Create commits that represent a single logical change
