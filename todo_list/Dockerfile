FROM python:3.11-slim as base

ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY pyproject.toml /code/

# Installing system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Add local non-root user to avoid issue with files
ARG USERNAME=code
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash


FROM base as dev

# Installing Poetry and dependencies (including dev dependencies)
RUN pip install --upgrade pip setuptools \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install

COPY . /code/

# Select internal user
USER code


FROM base as prod

# Installing Poetry and only core dependencies (no dev dependencies)
RUN pip install --upgrade pip setuptools \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY . /code/

# Select internal user
USER code