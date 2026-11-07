---
name: review
description: Review a plan or code with fresh-context reviewer personas (neutral, skeptic, and security, performance, or UX when needed), sort the findings, apply the clear fixes, get a step back verdict, and show the user only the judgment calls. Use when the user wants a review, e.g. "review the plan" or "review this with security and skeptic".
---

You are the main session. You keep the context; the reviewers do not.
Your job is to run the reviewers, sort what they find, fix what is clear, and
bring the user only the decisions that need them.

## 1. Pick the target

- Find the feature folder in `.work/`. If more than one could match, ask.
- **Plan or code?** Use what the user says. Otherwise: if
  `.work/<feature>/base-commit` exists and commits follow it, review the
  **code**; else review the **plan**.
- Plan target: `.work/<feature>/plan.md`.
- Code target: `git diff <base-commit>...HEAD`, plus `plan.md` as the spec.

## 2. Pick the reviewers

Persona files are in `personas/` next to this file.

- **Always:** `neutral.md`, `skeptic.md`.
- **When the target touches the area, or the user names it:**
  - `security.md`: input from users, network, or files; auth; permissions;
    secrets; crypto; shell commands; new dependencies.
  - `performance.md`: data that can grow; loops over it; queries; network
    calls; hot paths; startup; large files.
  - `ux.md`: anything a person sees or types: UI, CLI, API shape, error
    messages, docs.
- The user can name any persona in plain words. A name with no file becomes a
  one-line brief from the user's words.

Tell the user the list in one line, with the reason for each conditional one.

## 3. Run the reviewers

Start one **fresh subagent per persona, in parallel**, with no chat history.
Fresh context is the point: a reviewer that saw our conversation shares our
blind spots. If your harness cannot start fresh subagents, stop and tell the
user. Do not review in this session instead.

Give each reviewer this brief, and nothing from our conversation:

- The persona file text: its intro and the section for this target
  ("On a plan" or "On code"). If the persona file points to another file
  (for example `../../principles.md`), paste that file's text too. The
  reviewer cannot resolve paths relative to the persona file.
- The target: the `plan.md` path, or the diff command and `plan.md` path.
  The reviewer may read any file in the repo.
- This output contract:

  > Return findings only, most severe first, under 400 words. For each:
  > **title**, **severity** (Blocker / Major / Nit), **where** (file:line or
  > plan section), **problem** (a concrete case: this input or situation
  > leads to this wrong result), **fix** (the smallest one). No case, no
  > finding. If you find nothing in your area, say "All good" and what you
  > checked. That is a valid result. Never invent an issue to have
  > something to report. Change no files.

## 4. Sort the findings

Merge findings that describe the same problem into one entry, and keep all
reviewer names on it. Then, for each finding, **open the cited code or plan
section first**. Never label from the reviewer's text alone. Give one label:

- **FIX**: the finding is right and the fix is clear. Apply it.
- **CONTEST**: the finding is wrong. Cite evidence anyone can check: a file
  and line, a test, a decision in `plan.md`. "It is on purpose" is not
  evidence.
- **ESCALATE**: the finding needs the user's knowledge or a judgment call
  (scope, product, trade-off, cost). Write it as a question with your
  recommended answer.
- **DECLINE**: the finding is right but too small to matter (a nit). Record
  it, change nothing.

Rules:
- Keep the reviewer's severity. If you disagree, CONTEST with reasons.
- FIX vs. ESCALATE: a fix that changes what the user gets, or costs real
  time, is ESCALATE. A fix that only makes the work correct is FIX.
- Plan target: apply FIX items to `plan.md`.
- Code target: apply FIX items to the code, run the project's checks, and
  commit them as "review fixes" with a pointer to the report.

## 5. Write the report

Write `.work/<feature>/plan-review.md` or `code-review.md`. If the file
exists, append a new `# Round N` section; do not delete the old round.

```markdown
# Round 1 (YYYY-MM-DD)

Reviewers: neutral, skeptic, security (reason: parses uploaded files)

## Step back
Verdict: GO | CHANGE COURSE | STOP
<the step back agent's text>

## Findings
### 1. <title>: <severity>, <LABEL>
Reviewers: <names>. Where: <location>
Finding: <one or two lines>
Resolution: <what was changed | the evidence | the question and the user's answer | why declined>
```

## 6. Step back

Start one more **fresh subagent** with `personas/step-back.md`. Give it the
`plan.md` path, the report path, and for code the output of
`git diff --stat <base-commit>...HEAD`. Write its answer into the report's
"Step back" section.

## 7. Tell the user

Keep it to about 15 lines:

1. **Step back verdict** with its 1 or 2 lines of why.
2. **One count line:** "Fixed N, contested N, declined N, escalated N" and
   the report path.
3. **Escalated items, one at a time:** the question and your recommended
   answer, worded so "yes" accepts it. Wait for each answer. Apply it, and
   record it in the report.

Then act on the verdict, after all escalations have answers:

- Plan review GO: load the `implement` skill, unless the user asked for the
  review only.
- Code review GO: done. Tell the user the branch is ready to merge. Never
  merge or push.
- CHANGE COURSE or STOP: stop and ask the user. Recommend `plan`,
  `implement`, or an end. The verdict is advice; the user decides.

One round only. Run a second round only when the user asks.
