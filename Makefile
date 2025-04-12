.PHONY: docker-up
docker-up:
	docker-compose up -d --wait --force-recreate
	docker-compose --profile one-off up db-migrations test-migrations --force-recreate

.PHONY: docker-down
docker-down:
	docker-compose down

.PHONY: start
start: docker-up
	@uv run uvicorn celery_decipher.main:app --host 0.0.0.0 --port 8000 --reload

.PHONY: stop
stop:
	docker-compose --profile one-off down

.PHONY: test
test: docker-up
	@uv run pytest -v -s

.PHONY: check
check:
	@uv run ruff check celery_decipher
	@uv run basedpyright --level error

.PHONY: format
format:
	@uv run ruff check --select I --fix celery_decipher
	@uv run ruff format celery_decipher

.PHONY: db-shell
db-shell:
	@docker-compose exec postgres bash -c "psql -U postgres -d operational"
