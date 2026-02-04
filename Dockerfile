FROM python:3.13-slim

ENV POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install poetry==1.8.3
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /code

# Install dependencies first (cached layer)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root

# Copy application code
COPY src ./src
COPY scripts ./scripts
COPY src/agents/RAG_AGENT_INSTRUCTIONS.md ./src/agents/RAG_AGENT_INSTRUCTIONS.md
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create logs directory
RUN mkdir -p /code/logs

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
