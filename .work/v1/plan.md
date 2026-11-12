# devs v1

Source: grilling session with the user, 2026-11-06.

## Problem

Today the user tells one agent what to build, and the agent builds it. A fresh
session that reviews the work later usually finds real issues. Nothing makes
this a habit, and nothing settles the findings, so the user must read every
detail. Agents also rarely step back to ask "is this worth it?".

## Solution

A small set of skills for a process with roles: grill the idea, write a plan,
review it with fresh agents, implement it, review the code the same way. The
user sees only the judgment calls and a "step back" verdict.

## Decisions

- **Reuse vs. own**: reuse Matt Pocock's `grilling` (copied, unchanged) and
  Ponytail (installed as its own plugin; changed 2026-11-06, see Skeptic).
  Write the rest ourselves.
  Rejected: Matt's full plugin (38 extra skills of noise).
- **Package**: one repo `repos/d3mnjx/devs`, a Claude Code plugin with neutral
  skill text. Rejected: manifests for other harnesses now (no user yet).
- **Driving**: one skill per stage, started by command or plain speech.
  Rejected: one `/ship` command (less control, harder to debug).
- **Reviewers**: neutral + skeptic always; security, performance, UX when the
  change needs them or the user asks. Rejected: all 5 every time (noise, cost).
- **Persona files**: plain `.md` with "On a plan" and "On code" sections, read
  by `review` and given to a fresh subagent. Rejected: native Claude Code agents
  (not portable).
- **Skeptic**: thin file that loads Ponytail plus tuning lines. Rejected: a copy
  of Ponytail (no updates).
- **Skeptic** (changed 2026-11-06): `skeptic.md` now holds its own adapted
  copy of Ponytail's "should it exist / can it be smaller" rules. Reason: the
  Ponytail plugin install asks about a webhook and a task board, and its hooks
  and changes are outside our control. Rejected: depending on the plugin.
- **Sorting**: the main session labels each finding FIX / CONTEST / ESCALATE /
  DECLINE and must open the cited code first. CONTEST needs checkable evidence.
  Rejected: a fresh judge (lacks context); a separate verify agent (extra part).
- **Step back**: a fresh agent after both reviews gives go / change course /
  stop. Rejected: plan review only.
- **Files**: `.work/<feature>/` with `plan.md`, `plan-review.md`,
  `code-review.md`, `base-commit`. Rejected: review results only in chat.
- **Start**: `plan` takes any input and grills only open gaps. Rejected: two
  commands for idea vs. spec.
- **plan.md**: Problem, Solution, Decisions (with rejected option), Out of
  scope, Testing, Steps. Rejected: Matt's long user-story list.
- **Implement**: works from `plan.md`, runs project checks until they pass,
  commits. Rejected: strict TDD (slow on small changes).
- **Rounds**: one review round; a second only on request. Rejected: automatic
  loops.
- **Summary**: verdict, escalated items one at a time, one count line.
  Rejected: full findings list in chat.
- **Grill**: one question at a time on top of unchanged `grilling`.
- **Brainstorm** (changed 2026-11-06): `grill` became `brainstorm`, a two-way
  talk where the model also brings options and opinions; grilling is its
  backbone. Rejected: separate `brainstorm` and `grill` commands (you must
  pick a style before you know what the session needs).
- **Models** (changed 2026-11-12): none hardcoded; each role uses the
  session model. `review` now says so in its own text, tells the user the
  model with the reviewer list, and writes it in the report. The user can
  name another model in plain words. Reason: in a Yap plan review a Fable
  session ran all seven reviewers on Opus; the skill was silent, and a
  workspace cost rule ("send subagent work to a cheaper model") filled the
  gap. Rejected: without it (the rule lived only in this file, which a
  working session does not read); a question before each review (the answer
  is nearly always "the same model", and `start` exists to cut questions);
  a model field in each persona (no run shows that a persona does its job
  better, or as well, on another model; all replays so far ran on Opus; and
  model names belong to one harness and go out of date. The model line in
  the report collects the data for this decision).
- **Principles** (added 2026-11-06): `skills/principles.md` holds the user's
  coding principles. plan and implement carry an inline copy (changed
  2026-11-06: direct text is stronger than "read this file"); review pastes
  the file into the neutral and skeptic briefs. Rejected: a session hook (Claude Code only, and
  active outside devs); copies in every file (drift).
- **Skeptic and minimalist** (changed 2026-11-09): the Ponytail-based
  reviewer is now `minimalist.md`. `skeptic.md` is a new open reviewer with
  the user's old prompt, "read the plan and give me the cons". It runs on
  every plan, has its own output contract, and the main session shows its
  cons to the user unfiltered. Reason: in the Yap link-card run no reviewer
  asked whether a 24-hour card refresh was needed; each stayed in its lane.
  Rejected: adding the open prompt to the Ponytail reviewer (its "no vague
  worries" rules would muzzle it, and the open prompt would blur the
  cutter).
- **Decision owners** (added 2026-11-09): each decision in `plan.md` is
  tagged `(user)` or `(agent)`; `plan` lists the `(agent)` ones for the user
  before the review. The tag protects nothing. It only routes: a finding
  against a `(user)` decision always goes to the user. Rejected: `(user)`
  decisions closed to review (the user wants to be checked too).
- **Briefs** (added 2026-11-09): the main session adds nothing to a
  reviewer's brief about what is settled or who chose it. Rejected: scope
  notes "to save the reviewers time" (they silenced the right finding).
- **Zero option** (added 2026-11-09): a decision that adds a mechanism must
  reject "without it" first. Rejected: any alternative counts (a different
  number hid the option of no mechanism).
- **Open lists** (added 2026-11-12): each reviewer file states its purpose
  first. Its lists are examples, and a paragraph in the intro says so: the
  reviewer reports what fits its purpose, also when no line names it. The
  guard of each file (a real path, the two loads, a concrete case, "taste
  is not a finding") stays the limit. The skeptic has no lists and does not
  change. Not replayed yet on a test case. Rejected: longer lists (no list
  is complete); a motto line for each persona (tried the same day, the user
  liked none; only the minimalist keeps its own).
- **Later load** (added 2026-11-12): the performance reviewer judges against
  two loads: today, and the same users after months of normal use. Reason:
  in Yap a jump to a pinned message was quick on day 1 and took 7 seconds a
  few weeks later (history loaded in batches of 50, one request per batch,
  with a 50 ms wait). "Judge only against the real load" let it pass.
  Rejected: any future scale (the reviewer then asks for scale that the
  project does not have).

- **Chain** (added 2026-11-07): each skill loads the next one when it ends,
  and a `start` skill takes the input and runs the whole flow. It stops only
  for the user's answers, a CHANGE COURSE or STOP verdict, or a failed
  build. It never merges or pushes. Rejected: a pause for "go" between
  stages (the user asked to type nothing between stages); chain only inside
  `start` (a stage run alone would still need typed commands).

- **First real run** (changed 2026-11-08, on Yap): review takes a commit range
  and has a report-only mode; neutral checks the plan's facts against the
  code; implement leaves unrelated untracked files alone and records wrong
  plan facts in `plan.md`. Rejected: a separate "audit" skill for merged
  commits (the review steps are the same).

- **Step back review of devs** (added 2026-11-09, from the facts of the
  three Yap runs: 6 rounds, 34 findings, 27 FIX, 0 CONTEST, 6 of 6 GO):
  - **FIX only corrects or removes.** A fix that adds a mechanism, an
    option, or a dependency is ESCALATE. Reason: a plan-review FIX added a
    download gate that caused three code-review findings. Rejected: adding
    it to the `(agent)` decision list (that list is shown before the
    review, so a second list would be a second stop).
  - **Step back remarks.** The step back output has a "Remarks" part, shown
    to the user as written, together with the skeptic's cons. Reason: five
    of six GO texts held a point that reached nobody. Rejected: without it
    (the verdict alone lost "You can drop fix 5"); the main session picks
    the remarks worth showing (it is a biased judge of them).
  - **Small path.** `start` offers plan, implement, and one neutral
    reviewer on the code, and takes it only on the user's yes. `plan.md`
    carries `Path: small`. Reason: five nit fixes got 14 agents. Rejected:
    without it (the user pays the full flow for 49 lines); the model picks
    the path alone (a wrong "small" skips the plan review silently); no
    plan on the small path (the `(agent)` decision list is the one check
    that needs no model to notice something).
  - **Status line.** `review` ends a round with `Status: done` after the
    user's last answer, and `start` returns to a round without it. Reason:
    the report file exists before the user answers. Rejected: without it
    (an interrupted review skips the cons and the escalations).
  - **Kept as it is:** the persona mix on a plan (detail personas and
    larger-picture personas both run; the 2026-11-09 skeptic fills the gap
    the Yap run showed); the harness-neutral rule (no Yap failure came from
    it; drop it when a persona needs its own model); reports that cite
    commits a later squash removes (the report holds the finding in words).

## Out of scope

- Manifests for harnesses other than Claude Code.
- A `/ship` command (merge, push), `retro`, automatic review loops, a verify agent.
- Model selection per persona (see **Models** for the reason).

## Testing

Run the flow on one small real feature in a workspace project. Check that
each stage writes its file, that reviewers run with fresh context, and that
the summary shows only the verdict, escalations and the count line.

## Steps

1. Plugin manifest and marketplace file.
2. Copy `grilling` with its MIT license.
3. Skills: `brainstorm`, `plan`, `implement`, `review`.
4. Persona files: neutral, skeptic, security, performance, ux, step-back.
5. README, AGENTS.md, workspace README entry.
6. Validate the plugin; dry-run on a real feature.
