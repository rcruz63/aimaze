# Makefile para desarrollo de AiMaze

.PHONY: lint format check test run clean setup

# Activar entorno virtual
VENV = source .venv/bin/activate

# Comandos de linting y formateo
lint:
	@echo "🔧 Corrigiendo formato automáticamente..."
	$(VENV) && autopep8 --in-place --recursive src/
	@echo "🐍 Verificando archivos Python..."
	$(VENV) && flake8 src/
	@echo "📝 Verificando archivos Markdown..."
	$(VENV) && pymarkdownlnt scan docs/

format:
	@echo "🔧 Aplicando formato automático..."
	$(VENV) && autopep8 --in-place --recursive src/

check:
	@echo "🔍 Verificando código sin aplicar cambios..."
	$(VENV) && flake8 src/
	$(VENV) && pymarkdownlnt scan docs/

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
	@echo "  make setup   - Configurar entorno de desarrollo"
	@echo "  make lint    - Formatear y verificar código"
	@echo "  make format  - Solo aplicar formato automático"
	@echo "  make check   - Solo verificar código sin cambios"
	@echo "  make test    - Ejecutar tests"
	@echo "  make run     - Ejecutar el juego"
	@echo "  make clean   - Limpiar archivos temporales" 