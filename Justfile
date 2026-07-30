default:
    just --list

dev:
    docker compose -f compose-dev.yaml up -d

dev-down:
    docker compose -f compose-dev.yaml down

[working-directory: 'backend']
sync:
    uv sync

[working-directory: 'backend']
lint:
    uv run ruff check --fix || true
    uv run ruff format
    uv run ty check

[working-directory: 'backend']
tests:
    uv run pytest

[working-directory: 'backend']
build:
    docker buildx build --platform linux/amd64,linux/arm64 -t backend .

migration *options="":
    uv run python -m scripts.migration {{ options }}
