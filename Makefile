
dev:
	sh scripts.sh dev

start:
	sh scripts.sh start

prestart:
	sh scripts.sh prestart

makemigrations:
	alembic revision --autogenerate -m $(m)

migrate:
	alembic upgrade head

tests:
	pytest -o log_cli=true