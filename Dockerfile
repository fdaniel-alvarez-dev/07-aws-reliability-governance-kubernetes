FROM python:3.12-slim

WORKDIR /app

COPY pipelines ./pipelines
COPY data ./data

RUN addgroup --system app && adduser --system --ingroup app app && \
    mkdir -p /app/data/processed && \
    chown -R app:app /app

USER app

ENTRYPOINT ["python", "-m", "pipelines.pipeline"]
