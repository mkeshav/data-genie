# Coding Principles

Behavioral guidelines to reduce common LLM coding mistakes.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

# Code Review

When asked to review a branch, compare it against `master` and produce the following:

## Inline comments
Call out specific lines or hunks with file + line reference. Label each as:
- **[BLOCKER]** — must be fixed before merge (correctness bugs, security issues, data loss risk)
- **[SUGGESTION]** — worth fixing but not a merge gate (style, minor perf, readability)

## Summary report
After the inline comments, write a short summary covering:
- What the branch does (1–2 sentences)
- Correctness — logic bugs, edge cases, error handling
- Security — injection, auth, secrets, input validation
- Code style — consistency with the existing codebase
- Performance — obvious inefficiencies
- Test coverage — are the changes tested adequately

## Merge recommendation
End with a clear recommendation: **Merge**, **Merge after fixing blockers**, or **Do not merge**, with a one-line reason. The final call is the user's.

---

# Session Protocol

At the start of every session, ask the user: **"Are we in PR mode or trunk mode?"**

---

## Trunk Mode

Work happens directly on `master`. No PRs involved.

### Take-off
1. **Open issues** — run `gh issue list --state open` and show a quick summary.
2. **Repo state** — check for unpushed commits (`git log origin/master..HEAD`) and uncommitted work (`git status`).
3. **Memory review** — scan `MEMORY.md` for relevant context from prior sessions.
4. **Graph review** — read `graphify-out/GRAPH_REPORT.md` for god nodes, community structure, and surprising connections to orient on the codebase.
5. **User check-in** — ask the user if there's anything to track or prioritize before starting.

### Landing
1. **Run tests** — confirm nothing is broken before wrapping up.
2. **GitHub issues** — ask the user if anything from the session should be tracked as an issue. Never create issues without confirming first.
3. **Memory review** — save new learnings, update stale entries, remove outdated ones from auto-memory.
4. **Commit** — commit the work, but **do not push** without asking the user first.
5. **Close issues** — only close an issue after the code has been pushed — a commit alone is not enough, since changes may still come.
6. **Session summary** — provide a brief summary of what was accomplished.

---

## PR Mode

A **Coder** (local model) writes code and opens PRs. A **Reviewer** (Claude Code) reviews and fixes.

### Coder — Take-off
1. **Pick an issue** — run `gh issue list --state open --assignee @me` first, then fall back to unassigned issues. Choose one to work on.
2. **Repo state** — pull latest `master`, create a feature branch named `<issue#>-<short-slug>`.
3. **Understand context** — read the issue description, related code, and any linked issues or discussions. Run `/graphify query` on the issue topic to find related code across communities.

### Coder — Landing
1. **Run tests** — confirm all tests pass before opening a PR.
2. **Open a PR** with this structure:
   - **Title**: short, under 70 characters
   - **Body**:
     - `Closes #<issue>` link
     - `## Summary` — 1–3 bullet points of what changed
     - `## Test plan` — how the changes were verified
3. **Request review** — assign the reviewer.

### Reviewer — Take-off
1. **Open issues** — run `gh issue list --state open` and show a quick summary.
2. **Open PRs** — run `gh pr list --state open` and flag any awaiting review.
3. **Repo state** — check for unpushed commits (`git log origin/master..HEAD`) and uncommitted work (`git status`).
4. **Memory review** — scan `MEMORY.md` for relevant context from prior sessions.
5. **Graph review** — read `graphify-out/GRAPH_REPORT.md` for god nodes, community structure, and surprising connections to orient on the codebase.
6. **User check-in** — ask the user if there's anything to track or prioritize before starting.

### Reviewer — Landing
1. **Run tests** — confirm nothing is broken before wrapping up.
2. **Fix blockers** — if a reviewed PR has blockers, fix them on the branch directly.
3. **GitHub issues** — ask the user if anything from the session should be tracked as an issue. Never create issues without confirming first.
4. **Memory review** — save new learnings, update stale entries, remove outdated ones from auto-memory.
5. **Commit** — commit the work, but **do not push** without asking the user first.
6. **Close issues** — only close an issue after the code has been pushed — a commit alone is not enough, since changes may still come.
7. **Session summary** — provide a brief summary of what was accomplished.

---
