---
name: implement
description: Build the feature described in .work/<feature>/plan.md, run the project's checks until they pass, and commit. Use when the user wants to implement a reviewed plan.
---

## 1. Read the plan

Find the feature folder in `.work/`. If more than one could match, ask which.
`plan.md` is the source of truth; it works the same in this session or a fresh
one. If `plan-review.md` ends with a **stop** verdict that the user did not
overrule, say so and ask before you start.

## 2. Prepare git

- If the working tree has uncommitted changes that are not part of this work,
  tell the user and ask before you continue.
- If you are on the default branch, create a branch named after the feature
  folder.
- Write the current commit (`git rev-parse HEAD`) to
  `.work/<feature>/base-commit`, unless that file already exists.
  The code review diffs against this commit, so do not overwrite it on a
  second run.

## 3. Build

- Read the user's coding principles in `../principles.md` and follow them.
  The project's own rules win where they differ.
- Follow **Steps** in order. Write the tests that **Testing** asks for.
- Stay inside the plan. If the plan is wrong or a step cannot work, stop and
  tell the user. Suggest a return to the `plan` skill. Do not redesign
  silently.
- Find the project's checks (types, lint, tests) in its README, AGENTS.md,
  build files, or CI config. Run them, and fix failures until they pass.
  After 3 failed attempts on the same failure, stop and report it.

## 4. Commit

Commit when the checks pass. The message says what was built and points to
`.work/<feature>/plan.md`.

## 5. Hand off

End with 2 or 3 lines: what you built, and what you skipped or could not
check. Suggest the `review` skill on the code as the next step.
