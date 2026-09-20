#!/usr/bin/env bash
# SessionStart hook: put the competition summary and the latest experiment rows into context.
# Reads only local files; no network.
set -eu
cd "${CLAUDE_PROJECT_DIR:-.}"
[ -f docs/competition.md ] || exit 0
echo "== docs/competition.md (head) =="
head -40 docs/competition.md
echo
echo "== docs/experiments.md (tail) =="
[ -f docs/experiments.md ] && tail -25 docs/experiments.md
exit 0
