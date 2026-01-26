FROM python:3.13-slim

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry==1.8.3
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /code
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

COPY src ./src

EXPOSE 8000
CMD ["sh", "-c", "poetry run uvicorn src.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
