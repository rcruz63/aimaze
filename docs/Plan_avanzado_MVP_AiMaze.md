# **Plan Consolidado de Desarrollo del MVP: AiMaze - La Mazmorra Generativa**

Este documento detalla el plan de trabajo paso a paso para el desarrollo del Producto Mínimo Viable (MVP) de AiMaze, un juego de mazmorras interactivo y generativo impulsado por IA.

## **1. Filosofía de Desarrollo**

* **Iterativo e Incremental:** Construiremos el juego paso a paso, con pequeños incrementos, cada uno aportando una nueva funcionalidad verificable.
* **Test-Driven Development (TDD):** Priorizaremos la creación de tests para cada nueva funcionalidad, asegurando la validez del código y el comportamiento esperado.
* **IA como Núcleo Generativo:** La inteligencia artificial (LLM) será una parte fundamental del sistema para la generación de contenido dinámico (mazmorra, descripciones, eventos, enigmas, etc.).
* **Modularidad:** El código estará organizado en módulos claros, facilitando la escalabilidad, el mantenimiento y la colaboración.
* **Transparencia de Mecánicas:** Los resultados de las acciones del jugador (ej. "tiradas de dados") se explicarán narrativamente, sin exponer los números o la mecánica interna.
* **Enfoque en Enigmas:** El corazón de los quests serán los enigmas mentales, más que el combate puro.
* **Persistencia:** El estado del juego y de la mazmorra se mantendrá persistente para la coherencia y la reanudación de partidas.
* **Idioma:** Se preparará el sistema para la futura internacionalización desde el principio.
* **Arquitectura de Coordenadas:** Cada nivel es una matriz de n x m habitaciones. La ubicación del jugador se define por coordenadas (nivel:x:y). Cada nivel tiene coordenadas de inicio y salida definidas. La mazmorra tiene coordenadas de inicio y salida definidas.

## **1.1. Cambio Estratégico: Enfoque Híbrido Determinista**

**Problema Identificado:** Durante el desarrollo del Paso 1.4, se detectó que la generación completa de mazmorras por IA presentaba problemas de consistencia y debugging complejo. El error `KeyError: "'east'"` reveló que la IA no siempre genera estructuras JSON válidas para la lógica estructural.

**Solución Implementada:** Separación de responsabilidades entre **estructura determinista** y **creatividad narrativa**.

### **Enfoque Híbrido:**

**🔄 Generación Estructural (Determinista):**

* **Algoritmos deterministas** para crear la estructura de la mazmorra
* **Parámetros aleatorios controlados** (tamaño, densidad de habitaciones)
* **Pathfinding garantizado** desde entrada hasta salida
* **Validación automática** de coordenadas y conectividad
* **Sin dependencia de IA** para la lógica estructural

**🎨 Creatividad Narrativa (IA):**

* **Descripciones de habitaciones** generadas por IA
* **Eventos y encuentros** dinámicos y contextuales
* **ASCII art** para elementos visuales
* **Narrativa adaptativa** basada en el contexto del jugador
* **Enigmas y diálogos** generados por IA

### **Ventajas del Enfoque Híbrido:**

✅ **Confiabilidad:** La mazmorra siempre será navegable y funcional
✅ **Debugging:** Separación clara entre problemas estructurales y de IA
✅ **Escalabilidad:** Fácil extensión a múltiples niveles y configuraciones
✅ **Consistencia:** Coordenadas y conexiones siempre válidas
✅ **Creatividad:** La IA se enfoca en lo que hace mejor (narrativa)
✅ **Rendimiento:** Menos llamadas a IA para lógica estructural

### **Impacto en el Plan:**

* **Paso 1.4 actualizado** para usar `generate_dungeon_layout()`
* **Pasos 1.3, 1.6, 1.8** mantienen el uso de IA para contenido narrativo
* **Tests actualizados** para validar estructura determinista
* **Validación mejorada** con múltiples ejecuciones de prueba

## **2. Estructura de Módulos del Proyecto**

El proyecto se organizará en el directorio src/aimaze/ con los siguientes módulos:

src/aimaze/
├── \_\_init\_\_.py         # Marca el directorio como un paquete Python
├── main.py             # Bucle principal del juego y orquestador
├── config.py           # Carga de variables de entorno (API keys, etc.)
├── game_state.py       # Gestión del estado global y actual de la partida en memoria
├── display.py          # Gestión de toda la salida de información al usuario (texto, opciones)
├── input.py            # Captura y validación de la entrada del usuario
├── actions.py          # Procesa las acciones del jugador, delega a otros módulos para ejecutar consecuencias
├── dungeon.py          # Lógica de la estructura de la mazmorra, generación de niveles y habitaciones con coordenadas
├── ai_connector.py     # Interfaz con la IA (LLM), gestiona prompts, parsers, callbacks (Langfuse)
├── events.py           # Definición, generación y resolución de eventos (trampas, encuentros, situaciones) - INCLUYE ASCII ART
├── player.py           # Gestión de atributos del jugador, inventario, habilidades, experiencia
├── quest_manager.py    # Gestión de misiones (principal y secundarias), seguimiento de progreso de enigmas
├── characters.py       # Definición y lógica de Monstruos y NPCs (características, comportamientos)
├── localization.py     # Gestión de todos los textos del juego para soporte multi-idioma
└── save_load.py        # Gestión de guardar y cargar partidas (serialización/deserialización)

## **3. Fase 1: Core Game Loop e Integración Inicial de IA (MVP Local)**

### **Objetivo de la Fase:**

Desarrollar un juego de texto interactivo funcional en la terminal, donde la mazmorra y las descripciones son generadas por IA, el jugador puede moverse por coordenadas en múltiples niveles, resolver eventos simples, y se puede guardar/cargar la partida.

### **Paso 1.1: Configuración del Entorno y Estructura Modular Base**

**Objetivo:** Establecer el entorno de desarrollo y la estructura de módulos.

**Acciones:**

1. **Crear la estructura de directorios:** src/aimaze/ y tests/.
2. **Crear src/aimaze/\_\_init\_\_.py:** Archivo vacío para marcar como paquete.
   * Prompt para la IA integrada en el IDE:
     "Por favor, crea el archivo src/aimaze/\_\_init\_\_.py. Debe estar vacío."
3. **Configurar python-dotenv y config.py:**
   * Prompt para la IA integrada en el IDE:
     "Necesitamos configurar python-dotenv para cargar variables de entorno. Genera el código necesario en src/aimaze/config.py para cargar un archivo .env. Este módulo debería tener una función load_environment_variables() que inicialice las variables. Incluye un ejemplo de cómo cargar una variable OPENAI_API_KEY."
   * Prompt para la IA integrada en el IDE:
     "Genera un archivo .env de ejemplo en la raíz del proyecto con una variable OPENAI_API_KEY y LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY."
4. **Generar requirements.txt:**
   * Prompt para la IA integrada en el IDE:
     "Crea el archivo requirements.txt en la raíz del proyecto. Debe incluir las dependencias iniciales: python-dotenv, openai, langchain, langfuse, pydantic, pytest, httpx."
5. **Crear módulos placeholder:** Crear archivos vacíos para player.py, quest_manager.py, characters.py, localization.py, save_load.py dentro de src/aimaze/.
   * Prompt para la IA integrada en el IDE:
     "Crea los siguientes archivos vacíos en src/aimaze/: player.py, quest_manager.py, characters.py, localization.py, save_load.py."
6. **Actualizar módulos existentes para importar config y otros:** Asegurarse de que main.py, game_state.py, ai_connector.py importen config cuando sea necesario y que los módulos se importen entre sí con rutas relativas (from . import ...).

**Tests (Paso 1.1):**

1. **Test de config.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test_config.py. Incluye un test que verifique que config.load_environment_variables() carga correctamente una variable de entorno de un .env simulado (usando unittest.mock.patch.dict para os.environ y mock_open para el archivo)."

### **Paso 1.2: Modelado del Jugador y Estado Básico (player.py, game_state.py)**

**Objetivo:** Definir las características iniciales del jugador y cómo se gestionan en el estado del juego.

**Acciones:**

1. **Definir Player en src/aimaze/player.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/player.py. Define un Pydantic BaseModel llamado Player con los siguientes campos y valores iniciales:
     * strength: int = 10
     * dexterity: int = 10
     * intelligence: int = 10
     * perception: int = 10
     * health: int = 100
     * max_health: int = 100
     * experience: int = 0
     * inventory: List[str] = Field(default_factory=list)
     * Añade un método gain_xp(amount: int) que actualice la experiencia y un take_damage(amount: int) que reduzca la salud."
2. **Integrar Player en src/aimaze/game_state.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/game_state.py.
     * Importa Player de src/aimaze/player.py.
     * En initialize_game_state(), inicializa game_state['player'] = Player().
     * Asegúrate de que las funciones futuras que interactúen con atributos del jugador lo hagan a través de game_state['player']."

**Tests (Paso 1.2):**

1. **Test de player.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test_player.py.
     * Incluye un test para verificar que una instancia de Player se inicializa con los atributos correctos.
     * Crea un test para gain_xp() que verifique que la experiencia se incrementa correctamente.
     * Crea un test para take_damage() que verifique que la salud se reduce correctamente."

### **Paso 1.3: Generación de Descripción de Ubicación (ai_connector.py, display.py)**

**Objetivo:** La IA genera descripciones textuales para cada ubicación. El ASCII art se gestionará por separado para eventos.

**Acciones:**

1. **Pydantic LocationDescription en src/aimaze/ai_connector.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/ai_connector.py.
     * Añade imports para os, ChatOpenAI, PromptTemplate, ChatPromptTemplate, PydanticOutputParser, OutputFixingParser, BaseModel, Field, LangfuseCallbackHandler.
     * Define un Pydantic BaseModel llamado LocationDescription con **un único campo**: description: str = Field(description='Detailed textual description of the location, describing the environment and any general atmospheric elements. DO NOT include ASCII art or specific event details in this description.').
     * Implementa la función generate_location_description(location_context: str) -> LocationDescription: que use ChatOpenAI (gpt-3.5-turbo temp 0.7).
     * El PromptTemplate debe pedir a la IA generar una descripción detallada de una ubicación de mazmorra, **sin incluir ASCII art ni detalles de eventos/monstruos específicos**.
     * Usa PydanticOutputParser y OutputFixingParser. Configura LangfuseCallbackHandler. Incluye un if __name__ == "__main__": para prueba."
2. **Modificar src/aimaze/display.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/display.py.
     * Importa generate_location_description de src/aimaze/ai_connector.py.
     * En display_scenario(), reemplaza los placeholders de descripción por una llamada a generate_location_description() usando el current_loc_id de game_state.
     * **Elimina cualquier referencia a ascii_art en esta función** o en el modelo LocationDescription para la visualización de la sala general."

**Validación de IA (Paso 1.3):**

1. **Revisión Manual de Salida:**
   * Prompt para la IA integrada en el IDE:
     "Después de ejecutar el juego con este paso implementado, ejecuta el juego y verifica las descripciones generadas por la IA. ¿Son coherentes con una mazmorra? ¿NO incluyen ASCII art ni detalles de eventos/monstruos? Si hay problemas, indica ajustes al prompt de generate_location_description."

**Tests (Paso 1.3):**

1. **Test de display.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea o actualiza el archivo de test tests/test_display.py.
     * Crea un test para display.display_scenario que use unittest.mock.patch para simular la llamada a ai_connector.generate_location_description. El mock debe devolver una LocationDescription predefinida sin ASCII art.
     * Verifica que display_scenario intenta imprimir la descripción mockeada."

### **Paso 1.4: Arquitectura de Coordenadas Multi-Nivel con Generación Determinista (dungeon.py, ai_connector.py, game_state.py)**

**Objetivo:** Implementar el sistema de coordenadas por nivel donde cada nivel es una matriz n x m, con coordenadas de inicio y salida definidas, y identificación de ubicación por coordenadas (nivel:x:y). **NUEVO ENFOQUE:** Separar la generación estructural (determinista) de la creatividad narrativa (IA).

**Filosofía del Nuevo Enfoque:**

* **Estructura determinista:** La mazmorra siempre será navegable y funcional
* **Creatividad controlada:** La IA se enfoca en narrativa, descripciones y eventos
* **Debugging más fácil:** Separación clara entre problemas estructurales y de IA
* **Escalabilidad:** Fácil extensión a múltiples niveles y configuraciones

**Acciones:**

1. **Nuevos Modelos de Coordenadas en src/aimaze/dungeon.py:**
   * Prompt para la IA integrada en el IDE:
     "Reemplaza completamente src/aimaze/dungeon.py con la nueva arquitectura de coordenadas.
     * Importa BaseModel, Field, Dict, List, Tuple, Optional de pydantic y typing.
     * Define PlayerLocation(BaseModel): level: int, x: int, y: int con método to_string() -> str que devuelva 'nivel:x:y'.
     * Define Room(BaseModel): id: str, coordinates: Tuple[int, int], connections: Dict[str, Tuple[int, int]] donde las claves son direcciones ('north', 'south', 'east', 'west') y los valores son coordenadas (x, y) de habitaciones adyacentes dentro del mismo nivel.
     * Define Level(BaseModel): id: int, width: int, height: int, start_coords: Tuple[int, int], exit_coords: Tuple[int, int], rooms: Dict[str, Room] donde la clave es 'x,y'.
     * Define Dungeon(BaseModel): total_levels: int, current_level: int = 1, levels: Dict[int, Level].
     * Añade función helper get_room_at_coords(level: Level, x: int, y: int) -> Optional[Room]."

2. **Función generate_dungeon_layout en src/aimaze/ai_connector.py:**
   * Prompt para la IA integrada en el IDE:
     "Reemplaza la función generate_dungeon_layout en src/aimaze/ai_connector.py con una nueva función generate_dungeon_layout():
     * **ENFOQUE DETERMINISTA:** Genera estructura de mazmorra sin usar IA para la lógica estructural.
     * **Parámetros aleatorios controlados:** width = random.randint(3, 5), height = random.randint(3, 5).
     * **Puntos fijos:** start_coords = (0, 0), exit_coords = (width-1, height-1).
     * **Camino principal:** Genera un camino válido desde entrada hasta salida usando algoritmo de pathfinding simple.
     * **Habitaciones adicionales:** Añade habitaciones extra (80-100% del total) y las conecta al camino principal.
     * **Conexiones válidas:** Todas las connections apuntan a coordenadas válidas y habitaciones existentes.
     * **Sin IA:** No uses ChatOpenAI ni prompts para la estructura, solo para descripciones/eventos.
     * **Función helper:** Implementa generate_main_path(start, end, width, height) -> List[Tuple[int, int]].
     * **Función helper:** Implementa add_extra_rooms_and_connect(path_rooms, width, height) -> Dict[str, Room].
     * **Función helper:** Implementa create_dungeon_from_rooms(rooms, width, height, start, exit) -> Dungeon."

   2.1 **Puntos fijos:**

   * Escoger aleatoriamente un punto de inicio y un punto de salida.
   * El punto de inicio y el punto de salida no pueden coincidir. Si coinciden, escoger otro punto de salida.
   * Solicitar a la IA que genere una función que realice esta tarea.

   2.2 **Camino principal:**

   * Generar un número aleatorio entre .8 y 1.0, será el porcentaje de habitaciones pertenecientes al camino principal, la longitud del camino.
   * Prompt para la IA integrada en el IDE:
   "Genera una función Python que recbiendo un tamaño de matriz, un punto de inicio y un punto de salida y un tamaño de camino, genere un camino de longitud igual al tamaño de camino, que conecte el punto de inicio con el punto de salida (no se permiten conexiones oblicuas) sin visitar el mismo punto dos veces.
   Para ello debe generar todos los caminos posibles entre el punto de inicio y el punto de salida que no tengan repeticiones, escogeremos uno de ellos de forma aleatoria. Si no hubiera caminos posibles escogeremos el camino más largo posible".
   * Utilizando este camino generaremos las habitaciones del camino en la mazmorra indicando la puerta de entrada y la puerta de salida.

   2.3 **Habitaciones adicionales:**

   * Completar el resto de habitaciones de la mazmorra, para cada habitación que no pertnezca al camino principal abrir una puerta a una habitación adyacente, siempre que esa habitacion no sea la de inicio o la de salida.
   * Solicitar a la IA que genere una función que realice esta tarea.

3. **Actualizar game_state.py para PlayerLocation:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/game_state.py para usar PlayerLocation:
     * Importa PlayerLocation y Dungeon de src/aimaze/dungeon.py.
     * Reemplaza player_location_id con player_location: PlayerLocation.
     * En initialize_game_state(), llama a generate_dungeon_layout() y almacena el resultado como game_state['dungeon'].
     * Inicializa game_state['player_location'] con las start_coords del nivel 1 del dungeon generado.
     * Elimina referencias a simulated_dungeon_layout."

**Validación de Estructura Determinista (Paso 1.4):**

1. **Conectividad y Coordenadas:**
   * Prompt para la IA integrada en el IDE:
     "Genera múltiples mazmorras usando generate_dungeon_layout(). Verifica manualmente: ¿Las coordenadas están siempre dentro de límites? ¿Las connections apuntan siempre a coordenadas válidas? ¿Existe siempre un camino desde start_coords hasta exit_coords? ¿La estructura es consistente y navegable?"

**Tests (Paso 1.4):**

1. **Test de generación determinista:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test_dungeon_deterministic.py.
     * Test que generate_dungeon_layout() siempre devuelve una Dungeon válida.
     * Test que verifica conectividad completa (todas las habitaciones alcanzables).
     * Test que valida coordenadas dentro de límites para múltiples ejecuciones.
     * Test que confirma que start_coords y exit_coords están correctamente definidas.
     * Test que verifica que el camino principal existe y es navegable."

2. **Test de nuevos modelos en dungeon.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test_dungeon_coordinates.py.
     * Test PlayerLocation.to_string() devuelve formato correcto 'nivel:x:y'.
     * Test get_room_at_coords() encuentra habitaciones por coordenadas correctamente.
     * Test para generate_dungeon_layout que verifique que devuelve una instancia Dungeon válida con coordenadas consistentes."

### **Paso 1.5: Opciones Dinámicas basadas en Coordenadas (display.py, actions.py)**

**Objetivo:** Las opciones del jugador se basan en las connections de la habitación actual usando coordenadas, y las acciones actualizan PlayerLocation correctamente.

**Acciones:**

1. **Modificar src/aimaze/display.py:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza completamente src/aimaze/display.py para trabajar con coordenadas:
     * La función display_scenario debe obtener la habitación actual usando game_state['player_location'] y game_state['dungeon'].
     * Usar get_room_at_coords() para obtener la Room actual.
     * Las opciones mostradas deben derivarse de room.connections (direcciones cardinales disponibles).
     * El contexto para generate_location_description debe incluir las coordenadas: 'Level {nivel} at ({x},{y})'."
2. **Modificar src/aimaze/actions.py:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza src/aimaze/actions.py para manejar PlayerLocation:
     * process_player_action debe validar que la dirección elegida existe en room.connections.
     * Al moverse, actualizar game_state['player_location'] con las nuevas coordenadas del connections.
     * Verificar si las nuevas coordenadas son exit_coords del nivel actual para establecer objective_achieved = True.
     * Añadir validación de límites (coordenadas dentro de level.width y level.height)."

**Tests (Paso 1.5):**

1. **Test de display y actions con coordenadas:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza tests/test_display.py y crea tests/test_actions_coordinates.py:
     * En test_display.py, mockea un game_state con Dungeon y PlayerLocation válidos, verifica que display_scenario muestra opciones basadas en coordenadas.
     * En test_actions_coordinates.py, verifica que process_player_action actualiza correctamente PlayerLocation y detecta condiciones de salida basadas en exit_coords."

### **Paso 1.6: Sistema Extensible de Eventos con Énfasis en Enigmas (events.py, ai_connector.py, actions.py, display.py)**

**Objetivo:** Establecer un sistema de eventos extensible que priorice enigmas mentales sobre mecánicas de dados, con ASCII art y estructura preparada para eventos multi-habitación en futuras fases.

**Filosofía de Eventos:**

* **Enigmas primero:** Los eventos se resuelven principalmente mediante retos mentales y lógica
* **Mecánicas de dados secundarias:** Solo para eventos de acción cuando sea narrativamente apropiado
* **Estructura extensible:** Tipologías de eventos fácilmente ampliables
* **Multi-habitación preparado:** Bases para eventos complejos en fases posteriores

**Acciones:**

1. **Sistema de Tipologías Extensible en src/aimaze/events.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/events.py.
     * Importa BaseModel, Field, Literal, Optional, Tuple, Dict, Enum y random.
     * Define un Enum EventType con valores iniciales: PUZZLE_RIDDLE, PUZZLE_LOGIC, PUZZLE_OBSERVATION, OBSTACLE_PHYSICAL, ENCOUNTER_CREATURE, ENCOUNTER_NPC.
     * Define un Dict EVENT_TYPE_PROMPTS que mapee cada EventType a un texto guía para la IA:
       * PUZZLE_RIDDLE: 'Generate a riddle or word puzzle that requires mental reasoning'
       * PUZZLE_LOGIC: 'Create a logic puzzle or pattern recognition challenge'
       * PUZZLE_OBSERVATION: 'Design a puzzle requiring careful observation of details'
       * OBSTACLE_PHYSICAL: 'Create a physical obstacle requiring attribute check'
       * ENCOUNTER_CREATURE: 'Generate a creature encounter (may require combat or cleverness)'
       * ENCOUNTER_NPC: 'Create an NPC interaction with dialogue or task'
     * Define un Pydantic BaseModel GameEvent con:
       * event_type: EventType
       * description: str
       * ascii_art: Optional[str] = Field(None, description='ASCII art for the event (onomatopeyas, drawings, mysterious text)')
       * puzzle_solution: Optional[str] = Field(None, description='Expected solution for puzzle events')
       * alternative_solutions: List[str] = Field(default_factory=list, description='Alternative valid solutions')
       * success_text: str
       * failure_text: str
       * xp_reward: int = 0
       * item_reward: Optional[str] = Field(None, description='Item ID awarded on success')
       * clue_reward: Optional[str] = Field(None, description='Clue text awarded on success')
       * damage_on_failure: int = 0
       > Campos para futuras fases multi-habitación:
       * event_size: int = Field(1, description='Number of key rooms involved (for future multi-room events)')
       * related_locations: List[str] = Field(default_factory=list, description='Other room coordinates involved')
     * Implementa resolve_event(game_state, event: GameEvent, player_input: str) -> Tuple[bool, str] que:
       * Para eventos PUZZLE_*: Compare player_input con puzzle_solution y alternative_solutions (case-insensitive, stripped)
       * Para otros eventos: Use mecánica de atributos + dado solo si es narrativamente apropiado
       * Actualice XP, salud, inventario según el resultado
       * Genere narrativa sin mostrar mecánicas internas"

2. **Generación Inteligente por Tipo en src/aimaze/ai_connector.py:**
   * Prompt para la IA integrada en el IDE:
     "Añade a src/aimaze/ai_connector.py:
     * Función generate_event_by_type(event_type: EventType, location_context: str) -> Optional[GameEvent] que:
       * Use el prompt específico de EVENT_TYPE_PROMPTS[event_type]
       * Incluya el contexto de la ubicación actual
       * Para eventos PUZZLE_*: Instruya a la IA a generar tanto la pregunta como la respuesta esperada
       * Para ASCII art: Solo genere cuando sea apropiado (criaturas, efectos visuales, textos misteriosos)
       * Use PydanticOutputParser y OutputFixingParser
     * Función generate_random_event(location_context: str) -> Optional[GameEvent] que:
       * Escoja aleatoriamente un EventType (favoreciendo PUZZLE_* con 60% probabilidad)
       * Delegue a generate_event_by_type()"

3. **Integración Preparada para Expansión en src/aimaze/actions.py y display.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/actions.py y src/aimaze/display.py:
     * En actions.py:
       * Al moverse a nueva ubicación, probabilidad 30% de generar evento
       * Si hay evento activo tipo PUZZLE_*, permitir que el jugador escriba respuestas libres
       * Si hay evento activo tipo ENCOUNTER_*, mostrar opciones específicas (huir, negociar, enfrentar)
       * Almacenar eventos resueltos en game_state['completed_events'] para futuras referencias
     * En display.py:
       * Si existe evento activo con ascii_art, mostrarlo prominentemente
       * Para eventos PUZZLE_*: Mostrar prompt para respuesta libre del jugador
       * Para otros eventos: Mostrar opciones predefinidas
       * Indicar tipo de evento sutilmente en la narrativa (sin exponer mecánicas)"

**Preparación para Fases Futuras:**

**Comentarios de Arquitectura Multi-Habitación:**

* Prompt para la IA integrada en el IDE:
   "Añade comentarios en src/aimaze/events.py y src/aimaze/quest_manager.py:
      * En events.py: Comentario detallando cómo event_size y related_locations se usarán en Fase 2 para eventos como 'puerta cerrada en (1,1) requiere llave de NPC en (3,2)'
      * En quest_manager.py: Comentario sobre futura integración con sistema de eventos para crear cadenas de eventos interconectados"

**Validación de IA Mejorada (Paso 1.6):**

1. **Calidad de Enigmas:**
   * Prompt para la IA integrada en el IDE:
     "Ejecuta generate_event_by_type() para cada tipo PUZZLE_*. Verifica: ¿Los enigmas son apropiados para el nivel? ¿Las soluciones están claras? ¿El ASCII art es relevante? ¿Los textos guía producen eventos coherentes? Ajusta EVENT_TYPE_PROMPTS según resultados."

**Tests Actualizados (Paso 1.6):**

1. **Test del Sistema de Tipologías:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test_events.py:
     * Test que verify que cada EventType tiene su prompt correspondiente en EVENT_TYPE_PROMPTS
     * Test resolve_event() con diferentes tipos de eventos y entradas del jugador
     * Test para puzzle events que verifique matching de soluciones (incluyendo alternativas)
     * Test para mecánica de atributos en eventos no-puzzle
     * Mock test para verificar que eventos completados se almacenan correctamente"

2. **Test de Generación por Tipo:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza tests/test_display.py:
     * Test que simule diferentes tipos de eventos activos
     * Verificar que se muestran las opciones correctas según el tipo de evento
     * Test de integración ASCII art con diferentes tipos de eventos"

### **Paso 1.7: Condiciones de Fin de Juego y Guardado Básico (game_state.py, save_load.py)**

**Objetivo:** Implementar la condición de "Game Over" por muerte del jugador y la capacidad de guardar/cargar una única partida localmente.

**Acciones:**

1. **Condición de Muerte en src/aimaze/game_state.py y actions.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/game_state.py y src/aimaze/actions.py.
     * En game_state.py, añade una función check_game_over(game_state) que devuelva True si game_state['player'].health <= 0.
     * En actions.py, después de cualquier lógica que pueda reducir la salud del jugador (ej. fallar un evento), llama a game_state.check_game_over() y, si devuelve True, establece game_state["game_over"] = True."
2. **Módulo save_load.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea el archivo src/aimaze/save_load.py. Este módulo debe:
     * Importar json.
     * Implementar save_game(game_state, filename='savegame.json') que serialice el game_state (asegurándose de que los objetos Pydantic se conviertan a dicts) y lo guarde en un archivo JSON local.
     * Implementar load_game(filename='savegame.json') que cargue el estado desde el archivo JSON y lo deserialice a los tipos Pydantic correctos (especialmente Player, DungeonLayout, GameEvent)."
3. **Integrar Guardado/Carga en src/aimaze/main.py y game_state.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/main.py y src/aimaze/game_state.py.
     * En main.py, al inicio de game_loop(), intenta cargar una partida existente usando save_load.load_game(). Si no existe o falla, llama a game_state.initialize_game_state().
     * Añade una opción de acción al jugador para 'Guardar partida' en actions.py (ej. si el usuario escribe 'save' o elige una opción numérica '0'). Al procesar esta acción, llama a save_load.save_game()."

**Tests (Paso 1.7):**

1. **Test de save_load.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test_save_load.py.
     * Crea un test que inicialice un game_state (mockeado o real), lo guarde con save_load.save_game(), y luego lo cargue con save_load.load_game().
     * Verifica que el estado cargado es idéntico al original."
2. **Test de Muerte:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza tests/test_actions.py.
     * Crea un test que configure un game_state con la salud del jugador en 1.
     * Simula una acción que cause 1 punto de daño.
     * Verifica que game_state["game_over"] se establece en True y que el bucle principal terminaría."

### **Paso 1.8: Preparación para Quests, Personajes, Objetos y Hechizos (quest_manager.py, characters.py, player.py, dungeon.py)**

**Objetivo:** Establecer la estructura básica para la futura gestión de quests, personajes, objetos con clases y hechizos como entradas de texto.

**Acciones:**

1. **Modelos Placeholder en src/aimaze/quest_manager.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/quest_manager.py.
     * Define un Pydantic BaseModel Quest con campos placeholder como id: str, description: str, is_completed: bool = False, required_puzzles: List[str] = Field(default_factory=list).
     * Define una clase QuestManager con un método initialize_quests(game_state) que solo inicialice una lista vacía de quests y un check_quest_progress(game_state, action_context) que no haga nada aún."
2. **Modelos Placeholder en src/aimaze/characters.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/characters.py.
     * Define un Pydantic BaseModel Character con campos placeholder como id: str, name: str, type: Literal['monster', 'npc'], health: int, description: str.
     * Define un Pydantic BaseModel Monster que herede de Character y NPC que herede de Character."
3. **Diseño Futuro de Objetos en src/aimaze/player.py (Notas):**
   * Prompt para la IA integrada en el IDE:
     "Añade comentarios en src/aimaze/player.py cerca de la definición de inventory indicando que en futuras versiones los objetos podrían ser Pydantic models con campos como item_id: str, name: str, type: Literal['key', 'weapon', 'consumable'], y class_id: Optional[str] para llaves específicas (ej. 'golden_key')."
4. **Diseño Futuro de Hechizos en src/aimaze/player.py y src/aimaze/dungeon.py (Notas):**
   * Prompt para la IA integrada en el IDE:
     "Añade comentarios en src/aimaze/player.py indicando que en futuras versiones el jugador podría tener un campo known_spells: List[str] para almacenar las frases/palabras de hechizos.
     * Añade comentarios en src/aimaze/dungeon.py cerca de la definición de Room o en un nuevo modelo de Door (futuro) indicando que las puertas podrían tener un required_spell: Optional[str] o required_item_class: Optional[str] para su apertura o visibilidad."

**Tests (Paso 1.8):**

1. **Test de Creación de Modelos:**
   * Prompt para la IA integrada en el IDE:
     "Crea archivos de test tests/test_quest_manager.py y tests/test_characters.py.
     * Incluye tests básicos para verificar que las instancias de los modelos Quest, Character, Monster, NPC se pueden crear correctamente."

### **Paso 1.9: Preparación para Localización (localization.py)**

**Objetivo:** Crear un módulo para gestionar textos en diferentes idiomas.

**Acciones:**

1. **Módulo localization.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/localization.py.
     * Implementa una clase LocalizationManager con un diccionario interno para almacenar textos por idioma (ej. {'en': {'welcome': 'Welcome!'}, 'es': {'welcome': '¡Bienvenido!'}}).
     * Añade un método set_language(lang_code: str) y get_text(key: str, lang_code: str = 'en') -> str.
     * Hardcodea unos pocos mensajes de ejemplo (welcome_message, invalid_option)."
2. **Integrar en main.py y display.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/main.py y src/aimaze/display.py.
     * En main.py, inicializa una instancia de LocalizationManager y úsala para el mensaje de bienvenida.
     * En display.py, usa LocalizationManager para los mensajes básicos como "Opciones", "Error: Ubicación desconocida", etc."

**Tests (Paso 1.9):**

1. **Test de localization.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test_localization.py.
     * Crea tests para verificar que LocalizationManager puede establecer el idioma y recuperar textos correctamente para diferentes idiomas y claves."

## **4. Puntos Clave de la Nueva Arquitectura**

### **4.1. Sistema de Coordenadas**

* **PlayerLocation:** Identifica la posición como (nivel:x:y)
* **Level:** Matriz n x m con coordenadas de inicio y salida explícitas
* **Dungeon:** Colección de niveles con navegación multi-nivel
* **Room:** Coordenadas específicas dentro de un nivel con connections a coordenadas adyacentes

### **4.2. Separación de Contenido Visual**

* **LocationDescription:** Solo descripción textual, sin ASCII art
* **GameEvent:** Incluye ASCII art cuando es relevante (monstruos, trampas, efectos)
* **Display Logic:** Maneja ambos tipos de contenido apropiadamente

### **4.3. Escalabilidad**

* **Multi-nivel:** Preparado para múltiples niveles de mazmorra
* **Coordenadas flexibles:** Cada nivel puede tener dimensiones diferentes
* **Navegación consistente:** Sistema unificado de movimiento por coordenadas

### **4.4. Cambios Críticos vs Implementación Actual**

* **ELIMINADO:** `player_location_id` → **NUEVO:** `PlayerLocation(level, x, y)`
* **ELIMINADO:** `simulated_dungeon_layout` → **NUEVO:** `Dungeon` con `Level` y coordenadas
* **ELIMINADO:** `ascii_art` en `LocationDescription` → **MOVIDO:** a `GameEvent` cuando sea apropiado
* **ACTUALIZADO:** Toda la lógica de navegación para usar coordenadas

## **5. Fase 2: Plan de Distribución del MVP**

Este será un documento Markdown independiente que abordará las herramientas y los pasos necesarios para hacer que el juego sea accesible para otros, incluyendo manejo de sesiones, persistencia con Supabase, una interfaz web gráfica (simulando texto), contenerización y despliegue en Google Cloud. Este plan se abordará una vez que el MVP local esté funcional y probado con la nueva arquitectura de coordenadas.

## **6. Fase 3: Optimización de Experiencia de Usuario**

### **Objetivo de la Fase 3:**

Mejorar la experiencia del jugador mediante la optimización del cache de contenido generado por IA y la implementación de un sistema de opciones de usuario más avanzado.

### **Paso 3.1: Cache de Descripciones de Habitaciones**

**Objetivo:** Evitar regeneración innecesaria de descripciones y mantener consistencia narrativa.

**Problema Identificado:**

* Las descripciones se regeneran cada vez que el jugador visita una habitación
* Inconsistencias narrativas (ej. "hay una ventana" vs "habitación cerrada")
* Costo computacional innecesario en llamadas a la IA

**Acciones:**

1. **Modificar Room Model en src/aimaze/dungeon.py:**
   * Añadir campo `cached_description: Optional[str] = None`
   * Añadir campo `description_generated: bool = False`
   * Añadir timestamp `description_timestamp: Optional[datetime] = None`

2. **Implementar Cache Logic en src/aimaze/ai_connector.py:**
   * Modificar `generate_location_description()` para verificar cache
   * Solo generar nueva descripción si `cached_description` es None
   * Almacenar resultado en `room.cached_description`

3. **Actualizar display.py:**
   * Usar `room.cached_description` si existe
   * Fallback a generación solo si cache está vacío

**Tests:**

* Verificar que descripciones se cachean correctamente
* Confirmar que no se regeneran en visitas subsecuentes
* Validar consistencia entre visitas

### **Paso 3.2: Sistema de Opciones de Usuario Avanzadas**

**Objetivo:** Implementar opciones contextuales más allá del simple movimiento.

**Problema Identificado:**

* Solo opciones de movimiento cardinal disponibles
* Falta interacción con el entorno (examinar, buscar, usar)
* Experiencia limitada para el jugador

**Acciones:**

1. **Extender Room Model en src/aimaze/dungeon.py:**
   * Añadir campo `contextual_actions: List[str] = Field(default_factory=list)`
   * Ejemplos: ["examinar_pared", "buscar_objetos", "tocar_estatua"]

2. **Implementar Dynamic Actions en src/aimaze/ai_connector.py:**
   * Nueva función `generate_contextual_actions(room_context: str) -> List[str]`
   * IA genera acciones basadas en la descripción de la habitación

3. **Actualizar display.py y actions.py:**
   * Mostrar opciones de movimiento + opciones contextuales
   * Procesar acciones contextuales con respuestas narrativas

**Tests:**

* Verificar generación de acciones contextuales
* Confirmar que se muestran junto con opciones de movimiento
* Validar procesamiento de acciones no-movimiento

### **Paso 3.3: Sistema de Regeneración Inteligente**

**Objetivo:** Permitir regeneración selectiva de contenido cuando sea apropiado.

**Acciones:**

1. **Condiciones de Regeneración:**
   * Cambios significativos en el estado del juego
   * Eventos que modifiquen la habitación
   * Comando explícito del jugador ("mirar de nuevo")

2. **Implementar en ai_connector.py:**
   * Función `should_regenerate_description(room: Room, game_state: dict) -> bool`
   * Lógica para determinar cuándo regenerar

3. **Comando de Usuario:**
   * Añadir opción "Mirar detenidamente" que fuerce regeneración
   * Útil para obtener perspectivas diferentes

## **7. Fase 4: Expansión de Contenido Dinámico**

### **Objetivo de la Fase 4:**

Expandir las capacidades de generación de contenido dinámico y mejorar la narrativa.

### **Paso 4.1: Objetos Interactivos Generados por IA**

**Objetivo:** Generar objetos y elementos interactivos dinámicamente.

**Acciones:**

1. **Nuevo modelo InteractiveObject:**
   * `id: str`, `name: str`, `description: str`
   * `interaction_type: Literal['examine', 'take', 'use', 'trigger']`
   * `interaction_result: str`

2. **Integración con Room:**
   * Campo `interactive_objects: List[InteractiveObject]`
   * Generación dinámica basada en contexto

### **Paso 4.2: Narrativa Adaptativa**

**Objetivo:** Adaptar descripciones y eventos basados en el historial del jugador.

**Acciones:**

1. **Player History Tracking:**
   * `visited_rooms: List[str]`
   * `completed_actions: List[str]`
   * `player_preferences: Dict[str, Any]`

2. **Context-Aware Generation:**
   * Modificar prompts para incluir historial
   * Descripciones que referencien acciones pasadas

## **8. Consideraciones de Implementación**

### **8.1. Orden de Implementación**

1. **Completar Fase 1 (MVP Básico)** - Prioridad Alta
2. **Fase 2 (Distribución)** - Prioridad Alta
3. **Fase 3 (Optimización UX)** - Prioridad Media
4. **Fase 4 (Contenido Dinámico)** - Prioridad Media

### **8.2. Métricas de Éxito**

* **Fase 3:** Reducción del 80% en llamadas redundantes a IA, incremento en opciones disponibles por habitación
* **Fase 4:** Mayor variedad en descripciones, retroalimentación positiva sobre narrativa adaptativa

### **8.3. Backward Compatibility**

* Todas las mejoras deben mantener compatibilidad con save games existentes
* Migrations automáticas para nuevos campos en modelos Pydantic

---

**Estas fases de mejora se implementarán después de completar el MVP básico funcional. Las mejoras están diseñadas para ser iterativas y no bloquear el desarrollo del núcleo del juego.**

## Apuntes para que no se me olviden

* En la generación de la mazmorra debe exitir la posibilidad de crear caminos sin salida que te obliguen a volver hacia atras.

## **9. Fase 5: Sistema de Eventos Multi-Habitación y Complejos**

### **Objetivo de la Fase 5:**

Implementar eventos complejos que involucren múltiples habitaciones, cadenas de eventos interconectados y mini-aventuras dentro del juego.

### **Paso 5.1: Eventos Multi-Habitación**

**Objetivo:** Crear eventos que requieran la interacción entre múltiples habitaciones.

**Ejemplos de Eventos Multi-Habitación:**
- **Puerta Cerrada + Llave:** Puerta en (1,1) requiere llave que está con NPC en (3,2)
- **Enigma Distribuido:** Pistas en 3 habitaciones diferentes para resolver un enigma final
- **Secuencia Temporal:** Activar mecanismos en orden específico en diferentes habitaciones

**Acciones:**

1. **Extender GameEvent para Multi-Habitación:**
   ```python
   # Nuevos campos en GameEvent:
   event_chain_id: Optional[str] = None  # ID único para eventos conectados
   prerequisite_events: List[str] = []   # IDs de eventos que deben completarse primero
   triggers_events: List[str] = []       # IDs de eventos que se activan al completar este
   primary_location: str                 # Coordenadas de la habitación principal
   secondary_locations: List[str] = []   # Coordenadas de habitaciones secundarias
   ```

2. **Event Chain Manager:**
   - Clase `EventChainManager` que rastree el progreso de eventos complejos
   - Método `check_chain_completion()` para verificar si una cadena está completa
   - Integración con `quest_manager.py` para eventos que forman parte de quests

3. **Generación Inteligente de Cadenas:**
   - IA que genere eventos considerando la topología de la mazmorra
   - Algoritmos que garanticen que las cadenas de eventos sean solucionables
   - Validación de que todas las habitaciones requeridas son accesibles

### **Paso 5.2: Tipos de Eventos Complejos**

**Objetivo:** Implementar tipologías específicas de eventos multi-habitación.

**Nuevos Tipos de Eventos:**

1. **QUEST_FETCH:** "Trae X objeto de la habitación Y"
2. **QUEST_DELIVERY:** "Lleva este objeto a la habitación Z"
3. **PUZZLE_DISTRIBUTED:** "Recolecta pistas de N habitaciones"
4. **SEQUENCE_RITUAL:** "Activa elementos en orden específico"
5. **EXPLORATION_MAPPING:** "Encuentra y reporta sobre habitaciones específicas"

**Implementación:**
```python
# Extensión de EVENT_TYPE_PROMPTS:
EVENT_TYPE_PROMPTS.update({
    EventType.QUEST_FETCH: "Create a fetch quest requiring the player to retrieve a specific item from another room",
    EventType.QUEST_DELIVERY: "Generate a delivery quest where player must transport an item to a specific location",
    EventType.PUZZLE_DISTRIBUTED: "Design a puzzle that requires collecting clues from multiple rooms",
    EventType.SEQUENCE_RITUAL: "Create a ritual or sequence that must be performed across multiple locations",
    EventType.EXPLORATION_MAPPING: "Generate an exploration task requiring discovery of specific rooms or features"
})
```

### **Paso 5.3: Sistema de Objetos Inteligente**

**Objetivo:** Crear objetos que interactúen naturalmente con el sistema de eventos.

**Tipos de Objetos:**
- **Llaves Específicas:** `golden_key`, `crystal_key`, etc.
- **Componentes de Enigma:** `ancient_scroll_piece_1`, `rune_stone_fire`
- **Herramientas:** `magic_mirror` (revela pistas), `skeleton_key` (abre múltiples puertas)
- **Consumibles:** `health_potion`, `wisdom_elixir` (mejora resolución de enigmas)

**Integración con Eventos:**
```python
# Ejemplo de evento que otorga objeto específico:
GameEvent(
    event_type=EventType.PUZZLE_RIDDLE,
    description="An ancient statue poses a riddle...",
    puzzle_solution="time",
    item_reward="golden_key",
    success_text="The statue's eyes glow and it presents you with a golden key!"
)
```

### **Paso 5.4: IA Contextual para Eventos**

**Objetivo:** Hacer que la IA genere eventos considerando el contexto completo de la mazmorra.

**Características:**
- **Contexto Espacial:** IA conoce la topología de la mazmorra al generar eventos
- **Contexto Temporal:** Considera eventos previos del jugador
- **Contexto de Inventario:** Genera eventos apropiados según objetos disponibles
- **Contexto de Progreso:** Adapta dificultad según experiencia del jugador

**Implementación:**
```python
def generate_contextual_event(
    current_location: PlayerLocation,
    dungeon: Dungeon,
    player_history: List[str],
    player_inventory: List[str],
    player_level: int
) -> Optional[GameEvent]:
    # IA genera eventos considerando todo el contexto
    context = {
        "current_room": current_location.to_string(),
        "accessible_rooms": get_accessible_rooms(current_location, dungeon),
        "player_history": player_history,
        "inventory": player_inventory,
        "experience_level": player_level
    }
    return ai_generate_smart_event(context)
```

## **10. Fase 6: Narrativa Emergente y Eventos Adaptativos**

### **Objetivo de la Fase 6:**

Crear un sistema donde los eventos se adapten dinámicamente a las decisiones del jugador y generen narrativa emergente.

### **Paso 6.1: Memoria de Eventos**

**Objetivo:** El sistema recuerda las decisiones del jugador y adapta eventos futuros.

**Características:**
- **Historial de Decisiones:** Registro de cómo el jugador resuelve diferentes tipos de eventos
- **Preferencias Detectadas:** IA detecta si el jugador prefiere enigmas, exploración, interacción social
- **Consecuencias a Largo Plazo:** Decisiones en eventos tempranos afectan eventos posteriores

### **Paso 6.2: Eventos Generativos**

**Objetivo:** Eventos que generan otros eventos basados en las acciones del jugador.

**Ejemplos:**
- **Ayudar NPC:** Genera eventos de recompensa en habitaciones futuras
- **Resolver Enigma Brillantemente:** Desbloquea eventos de mayor dificultad
- **Fallar Repetidamente:** Genera eventos de ayuda o pistas adicionales

### **Paso 6.3: Narrativa Coherente**

**Objetivo:** Asegurar que todos los eventos contribuyan a una narrativa coherente.

**Características:**
- **Temas Consistentes:** Los eventos mantienen coherencia temática
- **Arcos Narrativos:** Eventos forman arcos narrativos satisfactorios
- **Resolución Significativa:** Los eventos complejos tienen resoluciones narrativamente satisfactorias

---

**Estas fases avanzadas se implementarán después de validar el sistema básico del Paso 1.6. Cada fase construye sobre la anterior, manteniendo la compatibilidad hacia atrás y añadiendo capas de complejidad de forma gradual.**

## **Consideraciones de Implementación para Eventos**

### **Prioridades de Desarrollo:**

1. **Paso 1.6 (MVP):** Sistema básico extensible ✅
2. **Fase 2:** Distribución y persistencia de eventos
3. **Fase 5:** Eventos multi-habitación
4. **Fase 6:** Narrativa emergente

### **Métricas de Éxito:**

- **Paso 1.6:** 60% de eventos son enigmas, ASCII art relevante, resolución narrativa fluida
- **Fase 5:** Eventos multi-habitación funcionales y narrativamente coherentes
- **Fase 6:** Jugadores reportan sensación de narrativa personalizada y emergente

### **Compatibilidad:**

- Todos los campos nuevos deben tener valores por defecto
- Sistema de migración automática para save games
- Retrocompatibilidad garantizada para eventos simples

---

## Apuntes para que no se me olviden

* En la generación de la mazmorra debe exitir la posibilidad de crear caminos sin salida que te obliguen a volver hacia atras.
* **EVENTOS:** Priorizar enigmas mentales sobre mecánicas de dados. Estructura extensible. ASCII art contextual. Preparación para eventos multi-habitación.
