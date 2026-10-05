---
name: code-review
description: Review code for bugs, style violations, security issues, and project guideline adherence. Checks CLAUDE.md compliance, identifies logic errors, and scores issues by confidence (code review, code quality, security, patterns, standards).
---

<!-- Derived from anthropics/claude-plugins-official plugins/code-review/commands/code-review.md and pr-review-toolkit/agents/code-reviewer.md (Apache-2.0). Adapted for G3 Code: simplified to linear review workflow without parallel agents; integrated code-reviewer agent guidance. -->

# Code Review

Review code for adherence to project guidelines, style guides, and best practices. This skill should be used proactively after writing or modifying code, especially before committing changes. It will check for style violations, potential issues, and ensure code follows established patterns in CLAUDE.md.

## Review Process

Follow a systematic approach to minimize false positives:

### 1. Determine Review Scope

By default, review unstaged changes from `git diff`. The user may specify different files, branches, or pull requests to review instead. If reviewing a GitHub pull request, use the GitHub CLI (if available) to fetch the PR details and file changes.

### 2. Check Eligibility

If reviewing a pull request, first verify:
- The PR is not closed
- The PR is not a draft
- The PR is not purely automated (e.g., dependency updates, formatting)
- You have not already reviewed this PR

If any of these conditions are met, do not proceed.

### 3. Gather Context

Read CLAUDE.md files from:
- The root of the project (if exists)
- Directories whose files were modified in the diff/PR

These files provide guidance for how Claude should write code in this project, which informs what issues matter.

### 4. Understand the Changes

Summarize the pull request or diff:
- What is being changed?
- Why are these changes being made?
- What files are affected?

### 5. Code Review - Three Passes

Perform three independent review passes, each with a specific focus:

**Pass A: Project Guidelines Compliance**
- Verify adherence to explicit project rules in CLAUDE.md (import patterns, framework conventions, language-specific style, function declarations, error handling, logging, testing practices, platform compatibility, naming conventions)
- Note any deviations from established project patterns

**Pass B: Bug Detection**
- Scan for obvious logic errors, null/undefined handling, race conditions, memory leaks
- Focus on large bugs that will impact functionality
- Avoid reading extra context beyond the changes; focus narrowly on what changed
- Ignore likely false positives

**Pass C: Code Quality & Context**
- Review code comments in modified files to ensure compliance with inline guidance
- Check git history/blame of modified code for context about why it was written that way
- Look for any patterns from related code that should be followed
- Evaluate code duplication, missing critical error handling, and maintainability

### 6. Confidence Scoring

For each potential issue found, score your confidence on a scale from 0-100:

- **0**: Not confident at all. This is a false positive, pre-existing issue, or doesn't stand up to scrutiny.
- **25**: Somewhat confident. Might be a real issue, but may also be a false positive. If stylistic, it wasn't explicitly called out in CLAUDE.md.
- **50**: Moderately confident. Real issue, but might be a nitpick or not happen often. Not very important relative to rest of changes.
- **75**: Highly confident. Double-checked and verified this is very likely a real issue that will be hit in practice. Directly mentioned in CLAUDE.md or will impact functionality.
- **100**: Absolutely certain. Confirmed this is definitely a real issue that will happen frequently. Evidence directly confirms this.

**Only report issues with confidence >= 80.**

### 7. Filter False Positives

Exclude issues if they are:
- Pre-existing (not introduced by this change)
- Something that looks like a bug but isn't actually a bug
- Pedantic nitpicks that a senior engineer wouldn't call out
- Would be caught by a linter, typechecker, or compiler (formatting, import validation)
- General code quality issues not explicitly required in CLAUDE.md
- Already silenced in code with lint ignore comments
- On lines the user did not modify in their pull request
- Changes likely intentional or directly related to the broader feature

### 8. Re-check Eligibility

Before finalizing the review, perform the eligibility check again to ensure the PR/diff is still valid for review.

### 9. Report Findings

If reviewing a GitHub PR and `gh` CLI is available, post findings as a comment on the PR. Otherwise, report findings as a formatted list.

Keep output brief. For each issue:
- Clear description of the bug
- Confidence score
- File path and line number (if available)
- Reason for flagging (e.g., "CLAUDE.md says X", "logic error in Y", "pattern conflict with Z")
- Link to relevant code or CLAUDE.md if possible

### Example Output Format

```
## Code Review

Found 2 issues:

1. Missing error handling in async operation (confidence: 85)
   File: src/api/handler.ts, lines 42-48
   CLAUDE.md requires explicit error handling for all Promise rejections
   
2. Incorrect import path pattern (confidence: 90)
   File: src/utils/helpers.ts, line 3
   CLAUDE.md specifies all relative imports should use absolute paths from project root
```

## Key Principles

- **Quality over quantity**: Report only issues that truly matter, not every possible improvement
- **Confidence-based filtering**: Use the scoring rubric strictly; don't report below 80
- **Context matters**: Read CLAUDE.md and understand project patterns before flagging issues
- **No false positives**: Avoid reporting pre-existing issues or stylistic preferences not in CLAUDE.md
- **Actionable feedback**: Each issue should have a clear fix or reference

## Notes

- Do not attempt to build or typecheck the application; assume CI will handle that
- Do not check test coverage unless explicitly required in CLAUDE.md
- Focus on bugs and CLAUDE.md compliance, not general code quality unless it's severe
- Always cite relevant code locations and CLAUDE.md references
