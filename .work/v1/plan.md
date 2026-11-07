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
- **Models**: none hardcoded; each role uses the session model.
- **Principles** (added 2026-11-06): `skills/principles.md` holds the user's
  coding principles. plan and implement carry an inline copy (changed
  2026-11-06: direct text is stronger than "read this file"); review pastes
  the file into the neutral and skeptic briefs. Rejected: a session hook (Claude Code only, and
  active outside devs); copies in every file (drift).

- **Chain** (added 2026-11-07): each skill loads the next one when it ends,
  and a `start` skill takes the input and runs the whole flow. It stops only
  for the user's answers, a CHANGE COURSE or STOP verdict, or a failed
  build. It never merges or pushes. Rejected: a pause for "go" between
  stages (the user asked to type nothing between stages); chain only inside
  `start` (a stage run alone would still need typed commands).

## Out of scope

- Manifests for harnesses other than Claude Code.
- A `/ship` command (merge, push), `retro`, automatic review loops, a verify agent.
- Model selection per persona.

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
