# Build image
FROM python:3.10-buster

ENV POETRY_VERSION=1.3.2 \
    # Do not ask any interactive question
    POETRY_NO_INTERACTION=1

RUN curl -sSL https://install.python-poetry.org | python -

# Equivalent to venv activate / poetry shell to enforce venv use
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Install dependencies before code so that they are cached
COPY poetry.lock pyproject.toml ./

# Install poetry and prepare venv
RUN poetry config virtualenvs.create false \
    && poetry self add keyrings.google-artifactregistry-auth \
    && poetry install --no-interaction --no-ansi --only main

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

ENV PYTHONPATH "${PYTHONPATH}:/app/"

EXPOSE 8080
CMD ["/app/entry.sh"]

