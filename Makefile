.PHONY: start
start:
	docker-compose up -d --wait
	docker-compose --profile one-off up db-migrations test-migrations

.PHONY: stop
stop:
	docker-compose --profile one-off down
