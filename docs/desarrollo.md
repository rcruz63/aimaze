# Guía de Desarrollo - AiMaze

## Configuración del Entorno

### Requisitos Previos

- Python 3.12+ (gestionado con pyenv)
- uv (para gestión de paquetes)
- Git

### Configuración Inicial

```bash
# Clonar repositorio
git clone [url-del-repositorio]
cd aimaze

# Configurar entorno con Make
make setup

# O manualmente:
source .venv/bin/activate
uv sync
```

## Estándares de Código

### Para Archivos Python

**Linter**: flake8
**Formateo automático**: autopep8

**Configuración**: Ver `.flake8`

- Líneas máximo 88 caracteres
- Complejidad ciclomática máximo 10
- Imports no utilizados permitidos solo en `__init__.py`

### Para Archivos Markdown

**Linter**: pymarkdownlnt

**Configuración**: Ver `pyproject.toml`

- Líneas máximo 100 caracteres
- Archivos deben terminar con línea nueva

## Comandos de Desarrollo

### Usando Make (Recomendado)

```bash
# Configurar entorno
make setup

# Formatear y verificar código
make lint

# Solo formatear automáticamente
make format

# Solo verificar sin cambios
make check

# Ejecutar tests
make test

# Ejecutar juego
make run

# Limpiar archivos temporales
make clean

# Ver ayuda
make help
```

### Usando comandos manuales

```bash
# Activar entorno virtual
source .venv/bin/activate

# Formatear código Python automáticamente
autopep8 --in-place --recursive src/

# Verificar código Python
flake8 src/

# Verificar archivos Markdown
pymarkdownlnt scan docs/
```

## Workflow de Desarrollo

### Antes de Crear un Commit

```bash
# 1. Formatear código
make format

# 2. Verificar que no hay errores
make check

# 3. Ejecutar tests
make test

# 4. Si todo pasa, hacer commit
git add .
git commit -m "Descripción del cambio"
```

### Errores Comunes y Soluciones

#### Líneas demasiado largas (E501)

```python
# ❌ Malo
resultado = funcion_muy_larga_con_muchos_parametros(parametro1, parametro2, parametro3, parametro4)

# ✅ Bueno
resultado = funcion_muy_larga_con_muchos_parametros(
    parametro1, parametro2, parametro3, parametro4
)
```

#### Imports no utilizados (F401)

```python
# ❌ Malo
from typing import List, Dict, Optional  # List no se usa

# ✅ Bueno
from typing import Dict, Optional
```

#### Espacios en blanco en líneas vacías (W293)

```python
# ❌ Malo
def funcion():
    pass
    # línea vacía con espacios
    return

# ✅ Bueno
def funcion():
    pass

    return
```

### Funciones Demasiado Complejas (C901)

Este error indica que una función tiene demasiada complejidad ciclomática.
**Solución**: Refactorizar dividiendo en funciones más pequeñas.

```python
# ❌ Malo - función muy compleja
def procesar_accion(accion):
    if accion == "north":
        if puede_ir_north():
            if hay_monstruo():
                if puede_luchar():
                    return luchar()
                else:
                    return huir()
            else:
                return moverse_north()
        else:
            return "No puedes ir ahí"
    elif accion == "south":
        # ... más lógica compleja
    # ... más condiciones

# ✅ Bueno - funciones separadas
def procesar_movimiento_north():
    if not puede_ir_north():
        return "No puedes ir ahí"

    if hay_monstruo():
        return manejar_encuentro()

    return moverse_north()

def manejar_encuentro():
    if puede_luchar():
        return luchar()
    return huir()

def procesar_accion(accion):
    if accion == "north":
        return procesar_movimiento_north()
    elif accion == "south":
        return procesar_movimiento_south()
    # ... lógica más simple
```

## Herramientas Configuradas

### Linters Instalados

- **flake8**: Verificación de código Python
- **autopep8**: Formateo automático Python
- **pymarkdownlnt**: Verificación de archivos Markdown

### Configuración de Editor

Para VS Code, añadir al `settings.json`:

```json
{
    "python.linting.flake8Enabled": true,
    "python.linting.enabled": true,
    "python.formatting.provider": "autopep8",
    "python.formatting.autopep8Args": [
        "--max-line-length=88"
    ],
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true
}
```

## Contribuir

1. Hacer fork del proyecto
2. Crear rama para feature: `git checkout -b feature/nueva-funcionalidad`
3. Seguir estándares de código
4. Hacer commit con mensajes descriptivos
5. Push a la rama: `git push origin feature/nueva-funcionalidad`
6. Crear Pull Request

## Solución de Problemas

### Error: "uv command not found"

```bash
# Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Error: "pyenv command not found"

```bash
# Instalar pyenv (macOS)
brew install pyenv

# Instalar pyenv (Linux)
curl https://pyenv.run | bash
```

### Error: "flake8 command not found"

```bash
# Asegurar que el entorno virtual esté activo
source .venv/bin/activate

# Reinstalar dependencias
uv sync
```
