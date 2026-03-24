.DEFAULT_GOAL := help

help:
	@echo "Comandos disponíveis:"
	@echo "  sync   - Instala dependências usando uv"
	@echo "  build  - Instala as dependências e constrói os containers"
	@echo "  up     - Inicia os containers (modo interativo)"
	@echo "  dup    - Inicia os containers (modo destacado)"
	@echo "  stop   - Para os containers"
	@echo "  down   - Para e remove os containers"
	@echo "  ps     - Lista os containers em execução"
	@echo "  logs   - Exibe os logs dos containers"

sync:
	uv sync --all-groups --all-extras

build:
	docker compose build --no-cache

up:
	docker-compose up

dup:
	docker-compose up -d

stop:
	docker-compose stop

down:
	docker-compose down

ps:
	docker-compose ps

logs:
	docker-compose logs -f
