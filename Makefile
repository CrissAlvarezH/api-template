
dev:
	sh scripts.sh dev

start:
	sh scripts.sh start

prestart:
	sh scripts.sh prestart

setup:
	docker compose up -d database

makemigrations:
	alembic revision --autogenerate -m $(m)

migrate:
	alembic upgrade head

tests: setup
	pytest -o log_cli=true