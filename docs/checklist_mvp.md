# Checklist MVP

## Fase 1: Flujo Básico del Juego e Integración de IA (Generación de Texto)

### Paso 1.1: Configuración del Entorno y Refinamiento del Esqueleto Inicial
- [ ] Crear archivo src/aimaze/__init__.py
- [ ] Configurar python-dotenv
- [ ] Actualizar game_state.py para usar configuración
- [ ] Generar requirements.txt
- [ ] Test básico de initialize_game_state

### Paso 1.2: Descripción de Ubicación Impulsada por IA (Primera Llamada LLM)
- [ ] Crear src/aimaze/ai_connector.py
- [ ] Modificar src/aimaze/display.py
- [ ] Revisión Manual de Salida
- [ ] Mocking de Llamadas a LLM

### Paso 1.3: Generación Simple de Mazmorra (IA para Estructura)
- [ ] Definir Modelos Pydantic para Mazmorra en src/aimaze/dungeon.py
- [ ] Añadir Generación de Mazmorra a src/aimaze/ai_connector.py
- [ ] Integrar Generación en src/aimaze/game_state.py
- [ ] Validación de Conectividad y Linealidad
- [ ] Test de Generación de Mazmorra

### Paso 1.4: Opciones Dinámicas (Impulsadas por la Mazmorra Generada)
- [ ] Modificar src/aimaze/display.py y src/aimaze/actions.py
- [ ] Test de Opciones Dinámicas

### Paso 1.5: Atributos del Jugador y Experiencia (Local)
- [ ] Actualizar src/aimaze/game_state.py
- [ ] Test de Atributos y XP

### Paso 1.6: Generación y Resolución de Eventos Simples (Primer Encuentro)
- [ ] Crear src/aimaze/events.py
- [ ] Integrar Eventos en src/aimaze/actions.py
- [ ] Validación de Comportamiento de Eventos
- [ ] Test de Resolución de Eventos

### Paso 1.7: Condición de Game Over (Muerte)
- [ ] Actualizar src/aimaze/actions.py
- [ ] Test de Condición de Muerte

## Fase 2: Plan de Distribución del MVP
- [ ] Crear documento de plan de distribución