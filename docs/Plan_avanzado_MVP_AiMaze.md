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

## **2. Estructura de Módulos del Proyecto**

El proyecto se organizará en el directorio src/aimaze/ con los siguientes módulos:

src/aimaze/  
├── __init__.py         # Marca el directorio como un paquete Python  
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
2. **Crear src/aimaze/__init__.py:** Archivo vacío para marcar como paquete.  
   * Prompt para la IA integrada en el IDE:  
     "Por favor, crea el archivo src/aimaze/__init__.py. Debe estar vacío."  
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

### **Paso 1.4: Arquitectura de Coordenadas Multi-Nivel (dungeon.py, ai_connector.py, game_state.py)**

**Objetivo:** Implementar el sistema de coordenadas por nivel donde cada nivel es una matriz n x m, con coordenadas de inicio y salida definidas, y identificación de ubicación por coordenadas (nivel:x:y).

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
     "Reemplaza la función generate_dungeon_layout en src/aimaze/ai_connector.py para trabajar con la nueva arquitectura:  
     * La función debe devolver Dungeon (no DungeonLayout).  
     * Use ChatOpenAI y PromptTemplate para pedir a la IA que genere una pequeña mazmorra de UN SOLO NIVEL inicialmente (ej. 3x3 o 4x3), usando coordenadas específicas.  
     * La IA debe especificar claramente start_coords y exit_coords para el nivel.  
     * Cada Room debe tener coordinates y connections que referencien otras coordenadas válidas dentro del nivel.  
     * Utiliza PydanticOutputParser y OutputFixingParser para validar la salida."  
3. **Actualizar game_state.py para PlayerLocation:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/game_state.py para usar PlayerLocation:  
     * Importa PlayerLocation y Dungeon de src/aimaze/dungeon.py.  
     * Reemplaza player_location_id con player_location: PlayerLocation.  
     * En initialize_game_state(), llama a generate_dungeon_layout() y almacena el resultado como game_state['dungeon'].  
     * Inicializa game_state['player_location'] con las start_coords del nivel 1 del dungeon generado.  
     * Elimina referencias a simulated_dungeon_layout."

**Validación de IA (Paso 1.4):**

1. **Conectividad y Coordenadas:**  
   * Prompt para la IA integrada en el IDE:  
     "Genera una mazmorra de ejemplo usando ai_connector.generate_dungeon_layout(). Verifica manualmente: ¿Las coordenadas de las habitaciones están dentro de los límites del nivel? ¿Las connections apuntan a coordenadas válidas? ¿start_coords y exit_coords están especificadas correctamente?"

**Tests (Paso 1.4):**

1. **Test de nuevos modelos en dungeon.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test_dungeon_coordinates.py.  
     * Test PlayerLocation.to_string() devuelve formato correcto 'nivel:x:y'.  
     * Test get_room_at_coords() encuentra habitaciones por coordenadas correctamente.  
     * Test para ai_connector.generate_dungeon_layout que mock la respuesta del LLM y verifique que devuelve una instancia Dungeon válida con coordenadas consistentes."

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

### **Paso 1.6: Gestión de Eventos con ASCII Art y Narrativa (events.py, ai_connector.py, actions.py, display.py)**

**Objetivo:** La IA genera eventos que pueden incluir ASCII art y se resuelven con una "tirada de dados" narrativa.

**Acciones:**

1. **Modelos GameEvent en src/aimaze/events.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/events.py.  
     * Importa BaseModel, Field, Literal, Optional, Tuple y random.  
     * Define un Pydantic BaseModel GameEvent con: type (Literal: 'obstacle', 'monster', 'puzzle'), description: str, ascii_art: Optional[str] = Field(None, description='ASCII art representation of the event or character. Max 20 lines, 80 characters per line, monochrome green style.'), required_attribute: Optional[Literal['strength', ...]], difficulty_check: Optional[int], success_text: str, failure_text: str, xp_reward: int = 0, damage_on_failure: int = 0.  
     * Implementa una función resolve_event(game_state, event: GameEvent) -> Tuple[bool, str] que simule una tirada de d20 + atributo. Genera una narrativa del resultado (éxito/fracaso) sin mostrar números. Actualiza XP y salud del jugador vía player.py."  
2. **Función generate_random_event en src/aimaze/ai_connector.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Añade a src/aimaze/ai_connector.py una nueva función generate_random_event(location_context: str) -> Optional[GameEvent] que:  
     * Use ChatOpenAI y PromptTemplate para pedir a la IA que genere un evento significativo (ej. un pequeño obstáculo, una criatura débil, un enigma sencillo) siguiendo la estructura GameEvent.  
     * **La IA debe generar ascii_art solo cuando sea apropiado para el evento (monstruos, trampas visuales, efectos mágicos), y None en caso contrario.**  
     * La IA debe generar un solo evento por llamada o None.  
     * Utiliza PydanticOutputParser y OutputFixingParser."  
3. **Integrar Eventos y ASCII Art en src/aimaze/actions.py y display.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/actions.py y src/aimaze/display.py.  
     * En actions.py, después de que el jugador se mueva a una nueva ubicación, introduce una probabilidad (ej. 30%) de generar un evento aleatorio. Si se genera, almacena el evento en game_state para que display.py pueda mostrarlo.  
     * En display.py, antes de mostrar las opciones, **si existe un evento activo en game_state y tiene ascii_art**, imprímelo. Luego, imprime la event.description."

**Validación de IA (Paso 1.6):**

1. **Comportamiento de Eventos y ASCII Art:**  
   * Prompt para la IA integrada en el IDE:  
     "Ejecuta el juego varias veces. Observa los eventos generados por la IA: ¿Son coherentes con los tipos definidos? ¿Las descripciones son apropiadas? ¿Los textos de éxito/fracaso son narrativos y sin números? ¿El ASCII art aparece solo cuando es relevante y sigue el estilo? Si hay problemas, indica ajustes al prompt de generate_random_event."

**Tests (Paso 1.6):**

1. **Test de events.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea o actualiza un archivo de test tests/test_events.py.  
     * Crea un test para events.resolve_event que use unittest.mock.patch para simular random.randint (para controlar la tirada) y que verifique los resultados de éxito y fracaso (cambios en HP, XP, y los mensajes narrativos).  
     * Asegúrate de que el GameEvent de prueba pueda incluir ascii_art y que la función lo maneje correctamente (aunque la función resolve_event no lo 'muestra', solo lo 'tiene')."  
2. **Test de Integración de ASCII Art en display.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Actualiza tests/test_display.py.  
     * Añade un test que simule un game_state con un GameEvent activo que contenga ascii_art.  
     * Verifica que display.display_scenario intenta imprimir este ascii_art cuando se invoca."

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

- **PlayerLocation:** Identifica la posición como (nivel:x:y)
- **Level:** Matriz n x m con coordenadas de inicio y salida explícitas
- **Dungeon:** Colección de niveles con navegación multi-nivel
- **Room:** Coordenadas específicas dentro de un nivel con connections a coordenadas adyacentes

### **4.2. Separación de Contenido Visual**

- **LocationDescription:** Solo descripción textual, sin ASCII art
- **GameEvent:** Incluye ASCII art cuando es relevante (monstruos, trampas, efectos)
- **Display Logic:** Maneja ambos tipos de contenido apropiadamente

### **4.3. Escalabilidad**

- **Multi-nivel:** Preparado para múltiples niveles de mazmorra
- **Coordenadas flexibles:** Cada nivel puede tener dimensiones diferentes
- **Navegación consistente:** Sistema unificado de movimiento por coordenadas

### **4.4. Cambios Críticos vs Implementación Actual**

- **ELIMINADO:** `player_location_id` → **NUEVO:** `PlayerLocation(level, x, y)`
- **ELIMINADO:** `simulated_dungeon_layout` → **NUEVO:** `Dungeon` con `Level` y coordenadas
- **ELIMINADO:** `ascii_art` en `LocationDescription` → **MOVIDO:** a `GameEvent` cuando sea apropiado
- **ACTUALIZADO:** Toda la lógica de navegación para usar coordenadas

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
