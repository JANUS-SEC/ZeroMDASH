"""Command-line entry point for the research framework.

Keeping execution outside ``runner.py`` ensures that every caller imports the
runner under its canonical module name.  In particular, ``TaskPrompt`` and
``ClaudeRunner`` then have one shared class identity across the LangGraph
module and the CLI.
"""

from __future__ import annotations

from collections.abc import Sequence


def cli(argv: Sequence[str] | None = None) -> int:
    from research.framework.runner import main

    try:
        return main(list(argv) if argv is not None else None)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(cli())
