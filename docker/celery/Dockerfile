FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS build

WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./
RUN uv export --no-hashes --format requirements-txt > requirements.txt

FROM python:3.13-slim AS final

RUN apt-get update && \
    apt-get install curl build-essential supervisor -y

WORKDIR /app

COPY --link celery_decipher ./celery_decipher
COPY --from=build /app/requirements.txt .
COPY --link ./docker/celery/supervisord.conf .

RUN cat requirements.txt
RUN pip install -r requirements.txt

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8000

CMD ["supervisord", "-c", "/app/supervisord.conf"]
