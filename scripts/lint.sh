#!/bin/bash
# Script para ejecutar linting en el proyecto AiMaze

# Activar entorno virtual
source .venv/bin/activate

echo "🔍 Ejecutando linting..."
echo

# Ejecutar autopep8 para corregir automáticamente
echo "🔧 Corrigiendo formato automáticamente con autopep8..."
autopep8 --in-place --recursive src/

# Verificar archivos Python con flake8
echo "🐍 Verificando archivos Python con flake8..."
flake8 src/

echo
echo "📝 Verificando archivos Markdown con pymarkdownlnt..."
pymarkdownlnt scan docs/

echo
echo "✅ Linting completado." 