# Coding principles

These are the user's own principles for every project. When the project's
AGENTS.md, CLAUDE.md, or coding standards say something different, the
project's rules win.

<!-- Who gets these principles, and how:
- plan/SKILL.md and implement/SKILL.md hold inline copies (direct text is
  followed more reliably than "read this file"). plan leaves out the comments
  part, because it writes no code. Keep the copies the same as this file.
- neutral.md and skeptic.md point here, and review pastes this file into
  their briefs, so the reviewers also get direct text.
- security, performance, ux, and step back do not get it, so they stay in
  their own lanes. To add a reviewer, copy the pointer line into its file. -->

## Core values

- **Simplicity:** prefer straightforward solutions over over-engineered ones.
- **Maintainability:** write code that is easy to change. Avoid tight
  coupling, and keep components focused.
- **Understandability:** think about the next developer, including future
  you. Will they understand this?
- **Elegance:** aim for solutions that feel right: minimal moving parts,
  clear intent, no unnecessary complexity.

When in doubt, choose the simpler path. Refactor when patterns emerge, not in
anticipation of hypothetical needs.

## Comments explain "why"

Comments carry the reasoning that the code cannot show:

- **Record the why:** the constraint, bug, or trade-off that shaped the code.
- **Guard invariants where they would break:** when a line looks removable or
  wrong but is deliberate, say so at that line. That is where a future
  cleanup would silently break it.
- **Keep it at the code,** not only in docs or commit messages. The next
  reader has the file open, nothing else.
