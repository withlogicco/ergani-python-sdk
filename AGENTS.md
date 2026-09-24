# Agent Instructions

- Before handing work over, run autofixable checks first. Use `uv run ruff format && uv run ruff check --fix`, then verify with `uv run ruff format --check && uv run ruff check`.
- For Python test validation in this repo, use `PYTHONPATH=$PWD uv run --no-project --with requests python3 -m unittest discover -s tests`.
- For an existing PR, make local follow-up changes on its existing head branch (use a worktree if needed).
- Keep tests focused on distinct behaviors rather than duplicating cases already covered.
