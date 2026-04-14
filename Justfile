default:
    just --list

migration *options="":
    uv run python -m scripts.migration {{ options }}
