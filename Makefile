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
	@echo "  status - Mostra o status do git"
	@echo "  add    - Adiciona arquivos ao stage"
	@echo "  commit - Cria um commit (msg='mensagem')"
	@echo "  push   - Envia alterações para o repositório remoto"
	@echo "  pull   - Atualiza o repositório local"
	@echo "  loggit - Mostra histórico de commits"

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

# -------------------------
# GIT
# -------------------------

status:
	git status

add:
	git add .

commit:
	git commit -m "$(msg)"

push:
	git push

pull:
	git pull --rebase

loggit:
	git log --oneline --graph --decorate
