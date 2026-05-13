default:
    just --list

dev:
    docker compose -f compose-dev.yaml up -d

dev-down:
    docker compose -f compose-dev.yaml down

lint:
    uv run ruff check --fix
    uv run ruff format
    uv run ty check

tests:
    uv run pytest

migration *options="":
    uv run python -m scripts.migration {{ options }}
