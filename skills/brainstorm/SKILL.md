---
name: brainstorm
description: Think through an idea together with the user before planning. A two-way conversation in which the model brings options, opinions, and prior art, and grills the user one question at a time until every decision is settled. Use when the user wants to brainstorm, discuss an idea, be grilled, or probe whether and how to build something.
---

Brainstorm the idea with the user until you both understand it the same way.
This is a conversation between two developers, not an interview.

## The backbone: grilling

Read `grilling.md` next to this file. Keep its design tree of open decisions
the whole time, and use its rules: you find facts yourself, the user makes the
decisions, and you are done when no open decision remains.

One change: ask **one question at a time**, not the whole frontier. Pick the
question that unblocks the most other decisions. Give the options and your
recommended answer, worded so "yes" accepts it.

Before you ask, find the crux: the one thing that, once decided, settles the
rest. Ask that in one or two sentences, with the options and your pick. If
the question needs a paragraph of setup, you have not found the crux yet.

<!-- Why grilling.md is a plain file and not edited: it stays a byte-for-byte
copy of upstream, so updates from mattpocock/skills are a plain file copy.
As a SKILL.md it showed up in the command menu as a confusing twin. -->

## Your part of the conversation

- **Contribute.** Propose options with their trade-offs. Say what you would
  choose and why. Do not only ask.
- **Bring facts.** Look up existing code, tools, and prior art when they
  matter, and report what you found in a few lines.
- **Challenge.** Name weak spots, hidden costs, and cheaper alternatives.
  Ask early whether this is the right problem and whether it is worth
  solving.
- **Follow the user.** The user can talk freely at any time: ask your opinion,
  think out loud, or change direction. Answer that first. Then update the
  tree and return to the next open question.
- **Match the tone.** "Just grill me" means mostly questions. "Let's think
  about this together" means more discussion. The tree stays the same.

Keep each message short. One topic or one question at a time.

## The end

When the tree has no open decisions, give a short summary of what you agreed
and ask the user to confirm it. Do not write files. After the user confirms,
load the `plan` skill with the summary as input, unless the user wants to
stop here.
