"""Support executing the CLI by doing `python -m flappybird`."""
from __future__ import annotations

from flappybird.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
