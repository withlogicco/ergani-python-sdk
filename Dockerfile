FROM ghcr.io/withlogicco/poetry:1.6.1-python-3.11

WORKDIR /usr/src/app
COPY pyproject.toml poetry.lock ./
RUN poetry check && poetry lock --check
RUN poetry install

COPY ./ ./
