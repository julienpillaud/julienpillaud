default:
    just --list

dev:
    docker compose -f compose-dev.yaml up -d

dev-down:
    docker compose -f compose-dev.yaml down

preprod:
    docker compose -f compose-preprod.yaml up -d --build

# Bacakend
[working-directory('backend')]
sync:
    uv sync

[working-directory('backend')]
lint-back:
    uv run ruff check --fix || true
    uv run ruff format
    uv run ty check

[working-directory('backend')]
tests:
    uv run pytest

# Frontend
[working-directory('frontend')]
lint-front:
    bun format
    bun lint
    bun type-check
