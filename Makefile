# Makefile para desarrollo de AiMaze

.PHONY: lint format check test run clean setup lint-md check-md

# Activar entorno virtual
VENV = source .venv/bin/activate

# Comandos de linting y formateo
lint:
	@echo "🔧 Corrigiendo formato automáticamente..."
	$(VENV) && autopep8 --in-place --recursive src/
	@echo "📝 Corrigiendo Markdown automáticamente..."
	./scripts/fix_markdown.sh
	@echo "🐍 Verificando archivos Python..."
	$(VENV) && flake8 src/
	@echo "📝 Verificando archivos Markdown (markdownlint)..."
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint -c .markdownlint.jsonc "docs/**/*.md"; \
	else \
		echo "⚠️  markdownlint no está instalado. Instálalo con: npm i -g markdownlint-cli"; \
	fi

format:
	@echo "🔧 Aplicando formato automático Python..."
	$(VENV) && autopep8 --in-place --recursive src/

format-md:
	@echo "🔧 Aplicando correcciones automáticas Markdown..."
	./scripts/fix_markdown.sh

check:
	@echo "🔍 Verificando código sin aplicar cambios..."
	$(VENV) && flake8 src/
	@$(MAKE) check-md

lint-md:
	@echo "📝 Corrigiendo Markdown automáticamente..."
	./scripts/fix_markdown.sh
	@$(MAKE) check-md

check-md:
	@echo "📝 Verificando archivos Markdown (markdownlint)..."
	@if command -v markdownlint >/dev/null 2>&1; then \
		markdownlint -c .markdownlint.jsonc "docs/**/*.md"; \
	else \
		echo "⚠️  markdownlint no está instalado. Instálalo con: npm i -g markdownlint-cli"; \
	fi

test:
	@echo "🧪 Ejecutando tests..."
	$(VENV) && python -m pytest tests/

run:
	@echo "🎮 Ejecutando AiMaze..."
	$(VENV) && python -m aimaze

clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

setup:
	@echo "⚙️  Configurando entorno de desarrollo..."
	@echo "Verificando que uv esté instalado..."
	@which uv || (echo "❌ uv no está instalado. Instálalo primero." && exit 1)
	@echo "Instalando dependencias..."
	uv sync
	@echo "✅ Entorno configurado correctamente"

# Comandos de ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make setup     - Configurar entorno de desarrollo"
	@echo "  make lint      - Formatear y verificar código (Python + Markdown)"
	@echo "  make format    - Solo aplicar formato automático Python"
	@echo "  make format-md - Solo aplicar correcciones automáticas Markdown"
	@echo "  make check     - Solo verificar código sin cambios"
	@echo "  make test      - Ejecutar tests"
	@echo "  make run       - Ejecutar el juego"
	@echo "  make clean     - Limpiar archivos temporales" 