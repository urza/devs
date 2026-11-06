# Coding principles

These are the user's own principles for every project. When the project's
AGENTS.md, CLAUDE.md, or coding standards say something different, the
project's rules win.

<!-- Only some roles read this file: plan, implement, and the neutral and
skeptic reviewers. Each one points here with its own line. Security,
performance, ux, and step back do not, so they stay in their own lanes.
To give the principles to another role, add the same line to its file. -->

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
