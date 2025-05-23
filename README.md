# Decipher messages with Celery

This project demonstrates a basic Celery setup that is testable and 
observable.

The stack consists of 

- Flask app that receives messages ciphered with a substitution cipher.
  The app triggers a Celery pipeline which implements an evolutionary algorithm for
  deciphering the message.
- Postgres databases for 
  * storing operational data, including intermediate results between tasks,
  * a unit test database with identical schema as operational DB,
  * Celery result backend.
- RabbitMQ as the Celery broker.
- Jaeger for tracing.
- Flyway for database migrations.

## Running the project

`make start` starts docker containers and runs the Flask app in the shell.

`uv run send_cipher.py` send a ciphered message to the Flask app.

## Stop services

```bash
make stop
```
