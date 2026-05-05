default:
    just --list

dev:
    docker compose -f compose-dev.yaml up -d

dev-down:
    docker compose -f compose-dev.yaml down

migration *options="":
    uv run python -m scripts.migration {{ options }}
