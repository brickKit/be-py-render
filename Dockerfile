# The Python render shell: members are installed from their tags (uv.lock), never from a local path. Debian slim:
# infra/print's renderer (Typst) ships glibc wheels only; wget is for the platform's health check (/bin/sh and wget).
FROM python:3.15.0-slim-trixie AS build
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.15.0-slim-trixie
RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/.venv /app/.venv
# the shell's own port (health, readiness, description, every member's metrics); members listen on their own ports
ENV PATH=/app/.venv/bin:$PATH PORT=8402
EXPOSE 8402
ENTRYPOINT ["python", "-m", "be_py_render"]
