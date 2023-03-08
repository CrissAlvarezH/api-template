
dev:
	sh scripts.sh dev

start:
	sh scripts.sh start

prestart:
	sh scripts.sh prestart

publish:
	sh scripts.sh publish $(version)

deploy:
	sh scripts.sh deploy $(user) $(address)

reload-service:
	sh scripts.sh reload-service

setup:
	docker compose up -d database

up: setup
	docker compose up -d api

makemigrations:
	alembic revision --autogenerate -m $(m)

migrate:
	alembic upgrade head

tests: setup
	pytest -o log_cli=true

unit-tests:
	pytest -o log_cli=true app/tests/unit

integration-tests: setup
	pytest -o log_cli=true app/tests/integration

e2e-tests: setup
	pytest -o log_cli=true app/tests/e2e
