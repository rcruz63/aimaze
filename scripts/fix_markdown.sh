#!/bin/bash
# Script para corregir automáticamente errores comunes de markdownlint

echo "🔧 Corrigiendo errores de Markdown automáticamente..."

# MD047: Añadir línea nueva final a archivos que no la tienen
find docs/ -name "*.md" -exec sh -c 'if [ "$(tail -c 1 "$1")" != "" ]; then echo "" >> "$1"; fi' _ {} \;

# MD009: Eliminar espacios al final de líneas
find docs/ -name "*.md" -exec sed -i '' 's/[[:space:]]*$//' {} \;

echo "✅ Correcciones automáticas aplicadas"
echo "📝 Errores restantes requieren revisión manual:"
echo "   - MD013: Líneas demasiado largas (dividir manualmente)"
echo "   - MD004: Cambiar guiones (-) por asteriscos (*) en listas"
echo "   - MD031: Añadir líneas en blanco alrededor de bloques de código"
echo "   - MD032: Añadir líneas en blanco alrededor de listas" 