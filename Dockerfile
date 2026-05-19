FROM ghcr.io/withlogicco/python:3.13

WORKDIR /usr/src/app
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-install-project

COPY ./ ./
RUN uv sync --locked
