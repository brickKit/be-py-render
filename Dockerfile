# The Python render shell: members are installed from their tags (uv.lock), never from a local path.
FROM python:3.14.4-alpine AS build
COPY --from=ghcr.io/astral-sh/uv:0.12.1 /uv /bin/uv
RUN apk add --no-cache git
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev --no-editable

FROM python:3.14.4-alpine
COPY --from=build /app/.venv /app/.venv
# the shell's own port (health, readiness, description, every member's metrics); members listen on their own ports
ENV PATH=/app/.venv/bin:$PATH PORT=8402
EXPOSE 8402
ENTRYPOINT ["python", "-m", "be_py_render"]
