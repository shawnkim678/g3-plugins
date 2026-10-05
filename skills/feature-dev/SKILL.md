---
name: feature-dev
description: Guided feature development workflow combining codebase exploration, architecture design, and implementation with quality reviews (feature development, architecture, implementation, design).
---

<!-- Derived from anthropics/claude-plugins-official plugins/feature-dev/commands/feature-dev.md and agents/* (Apache-2.0). Adapted for G3 Code: consolidated agent workflows into sequential skill phases with direct tool execution. -->

# Feature Development

Systematic approach to implementing new features: understand the codebase deeply, clarify all requirements, design elegant architectures, then implement and review.

## Core Principles

- **Ask clarifying questions**: Identify all ambiguities, edge cases, and underspecified behaviors before designing
- **Understand before acting**: Read and comprehend existing code patterns first
- **Simple and elegant**: Prioritize readable, maintainable, architecturally sound code
- **Use TodoWrite**: Track all progress throughout the workflow

## Phase 1: Discovery

**Goal**: Understand what needs to be built

### Actions

1. Create a todo list with all 7 phases
2. If feature description is unclear, ask user for:
   - What problem are they solving?
   - What should the feature do?
   - Any constraints or requirements?
3. Summarize understanding and confirm with user

## Phase 2: Codebase Exploration

**Goal**: Understand relevant existing code and patterns

### Actions

1. Search the codebase for:
   - Similar features or functionality that can serve as patterns
   - High-level architecture and component organization
   - Existing patterns in relevant directories
   - Extension points and integration patterns

2. For each area explored, identify:
   - Key abstractions and architectural layers
   - How data flows through the system
   - Common patterns and conventions
   - Files that are critical to understand the feature area

3. Document findings:
   - List of 5-10 key files to read
   - Architecture overview for the relevant feature area
   - Patterns and conventions used
   - Integration points and dependencies

## Phase 3: Clarifying Questions

**Goal**: Fill in gaps and resolve all ambiguities before designing

### Critical Note

This phase is essential. Do not skip.

### Actions

1. Review codebase findings and original feature request
2. Identify underspecified aspects:
   - Edge cases and error handling
   - Integration points and scope boundaries
   - Design preferences and constraints
   - Backward compatibility requirements
   - Performance needs and limitations
3. **Present all questions to user in a clear list**
4. **Wait for user answers before proceeding**

If user says "whatever you think is best", provide your recommendation and get explicit confirmation.

## Phase 4: Architecture Design

**Goal**: Design implementation approach with clear trade-offs

### Actions

1. Analyze potential approaches with different focuses:
   - **Minimal changes**: Smallest change, maximum code reuse
   - **Clean architecture**: Prioritize maintainability and elegant abstractions
   - **Pragmatic balance**: Balance speed and quality, practical for constraints

2. For each approach:
   - Identify files to create/modify
   - Describe component design and responsibilities
   - Document data flow and integration points
   - Note trade-offs and implications

3. **Form your recommendation** based on project context:
   - Is this a small fix or large feature?
   - What's the urgency?
   - What's the complexity?
   - What does the codebase style suggest?

4. **Present to user**: 
   - Brief summary of each approach
   - Trade-offs comparison
   - Your recommendation with reasoning
   - Ask user which approach they prefer

## Phase 5: Implementation

**Goal**: Build the feature

### Prerequisites

Do not start without explicit user approval of the chosen approach

### Actions

1. Confirm user approval
2. Read all relevant files identified in previous phases
3. Implement following chosen architecture:
   - Follow codebase conventions strictly
   - Write clean, well-documented code
   - Create files/modify code as specified in architecture
   - Handle errors appropriately
4. Update todos as you progress
5. Test manually if possible

## Phase 6: Quality Review

**Goal**: Ensure code is simple, DRY, elegant, and functionally correct

### Actions

1. Review the implemented code focusing on:

   **Simplicity & DRY**:
   - Are there redundant code sections that can be consolidated?
   - Can any abstractions be simplified?
   - Is the code readable and clear?
   - Could variable/function names be more descriptive?

   **Functional Correctness**:
   - Are there any logic errors or edge cases missed?
   - Is error handling adequate?
   - Do all paths work as intended?
   - Are there any off-by-one errors or boundary issues?

   **Project Conventions**:
   - Does code follow patterns in CLAUDE.md?
   - Are naming conventions consistent?
   - Do new components follow existing architectural patterns?
   - Is there adequate documentation/comments?

2. Consolidate findings and identify highest priority issues
3. **Present findings to user**:
   - What works well
   - Issues found with severity levels
   - Ask what they want to do: fix now, fix later, or proceed as-is
4. Address issues based on user decision

## Phase 7: Summary

**Goal**: Document what was accomplished

### Actions

1. Mark all todos complete
2. Summarize:
   - What was built (feature description)
   - Key architectural decisions made
   - Files modified/created
   - Testing performed (if any)
   - Suggested next steps
3. Confirm user satisfaction

## Best Practices

- **Read CLAUDE.md first**: Understand project conventions before designing
- **Trace existing features**: Study similar features to understand patterns
- **Ask clarifying questions early**: Resolve ambiguity before architecture design
- **Get user approval**: Confirm approach before implementing
- **Review your own work**: Catch issues before declaring done
- **Document decisions**: Explain why architectural choices were made
- **Keep it simple**: Default to straightforward solutions over clever ones
