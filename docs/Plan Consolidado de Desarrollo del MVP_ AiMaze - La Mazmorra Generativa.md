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

## **2. Estructura de Módulos del Proyecto**

El proyecto se organizará en el directorio src/aimaze/ con los siguientes módulos:

src/aimaze/  
├── __init__.py         # Marca el directorio como un paquete Python  
├── main.py             # Bucle principal del juego y orquestador  
├── config.py           # Carga de variables de entorno (API keys, etc.)  
├── game_state.py       # Gestión del estado global y actual de la partida en memoria  
├── display.py          # Gestión de toda la salida de información al usuario (texto, ASCII art, opciones)  
├── input.py            # Captura y validación de la entrada del usuario  
├── actions.py          # Procesa las acciones del jugador, delega a otros módulos para ejecutar consecuencias  
├── dungeon.py          # Lógica de la estructura de la mazmorra, generación de niveles y habitaciones  
├── ai_connector.py     # Interfaz con la IA (LLM), gestiona prompts, parsers, callbacks (Langfuse)  
├── events.py           # Definición, generación y resolución de eventos (trampas, encuentros, situaciones)  
├── player.py           # Gestión de atributos del jugador, inventario, habilidades, experiencia  
├── quest_manager.py    # Gestión de misiones (principal y secundarias), seguimiento de progreso de enigmas  
├── characters.py       # Definición y lógica de Monstruos y NPCs (características, comportamientos)  
├── localization.py     # Gestión de todos los textos del juego para soporte multi-idioma  
└── save_load.py        # Gestión de guardar y cargar partidas (serialización/deserialización)

## **3. Fase 1: Core Game Loop e Integración Inicial de IA (MVP Local)**

### **Objetivo de la Fase:**

Desarrollar un juego de texto interactivo funcional en la terminal, donde la mazmorra y las descripciones son generadas por IA, el jugador puede moverse y resolver eventos simples, y se puede guardar/cargar la partida.

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

### **Paso 1.4: Generación de Estructura de Mazmorra con Puertas (dungeon.py, ai_connector.py)**

**Objetivo:** La IA genera la estructura de la mazmorra (habitaciones, conexiones y la presencia/dirección de puertas).

**Acciones:**

1. **Modelos Room y DungeonLayout en src/aimaze/dungeon.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/dungeon.py.  
     * Importa BaseModel, Field, Dict, List de pydantic y typing.  
     * Define un Pydantic BaseModel Room con: id: str, connections: Dict[str, str] (ej. {'north': 'room_b', 'east': 'room_c'}). Las claves del diccionario connections deben ser direcciones cardinales ('north', 'south', 'east', 'west') que indiquen la existencia de una puerta/pasaje en esa dirección.  
     * Define un Pydantic BaseModel DungeonLayout con: rooms: Dict[str, Room].  
     * Mueve la simulated_dungeon_layout existente dentro de una función get_placeholder_dungeon_layout() para que pueda ser referenciada o reemplazada."  
2. **Función generate_dungeon_layout en src/aimaze/ai_connector.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Añade a src/aimaze/ai_connector.py una nueva función generate_dungeon_layout() -> DungeonLayout: que:  
     * Use ChatOpenAI y un PromptTemplate para pedir a la IA que genere una *pequeña* mazmorra lineal (ej. 3-5 habitaciones conectadas) en formato JSON, adhiriéndose a la estructura de Room y DungeonLayout.  
     * Enfatiza que las connections de cada Room deben usar direcciones cardinales ('north', 'south', 'east', 'west') para indicar las puertas existentes y su destino.  
     * Asegúrate de que la mazmorra tenga un punto de inicio y una salida clara.  
     * Utiliza PydanticOutputParser y OutputFixingParser para validar la salida."  
3. **Integrar Generación en src/aimaze/game_state.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/game_state.py.  
     * Importa generate_dungeon_layout de src/aimaze/ai_connector.py.  
     * En initialize_game_state(), reemplaza la simulated_dungeon_layout por una llamada a ai_connector.generate_dungeon_layout(). Almacena el resultado (un objeto DungeonLayout) en game_state["dungeon_layout"].  
     * Asegúrate de que player_location_id se inicialice con el ID de la habitación de inicio generada por la IA."

**Validación de IA (Paso 1.4):**

1. **Conectividad y Linealidad:**  
   * Prompt para la IA integrada en el IDE:  
     "Genera una mazmorra de ejemplo usando ai_connector.generate_dungeon_layout(). Verifica manualmente: ¿Todas las habitaciones son accesibles desde el inicio? ¿Existe un camino claro hacia la salida? ¿Las connections usan direcciones cardinales? ¿La estructura es razonablemente lineal como se pidió para el MVP?"

**Tests (Paso 1.4):**

1. **Test de dungeon y ai_connector:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test_dungeon_generation.py.  
     * Crea un test para ai_connector.generate_dungeon_layout que use unittest.mock.patch para simular la respuesta del LLM (devolviendo un JSON que represente una DungeonLayout válida con conexiones cardinales).  
     * Verifica que la función devuelve una instancia de DungeonLayout y que su estructura básica es correcta (contiene las habitaciones esperadas y conexiones válidas)."

### **Paso 1.5: Opciones Dinámicas y Proceso de Acción (display.py, actions.py)**

**Objetivo:** Las opciones del jugador se basan en la estructura de la mazmorra generada, y las acciones actualizan la ubicación del jugador.

**Acciones:**

1. **Modificar src/aimaze/display.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/display.py.  
     * Ajusta display_scenario para que las opciones mostradas y almacenadas en game_state["current_options_map"] se deriven directamente de las connections de la Room actual en game_state["dungeon_layout"].  
     * Las descripciones de las opciones deben ser claras, utilizando las direcciones cardinales (ej. 'Ir al Norte', 'Ir al Este', 'Salir')."  
2. **Modificar src/aimaze/actions.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/actions.py.  
     * Ajusta process_player_action para que la validación de la elección y el cambio de player_location_id se basen en las connections de la Room actual de game_state["dungeon_layout"].  
     * Asegúrate de que se maneje la condición de "salir_mazmorra" para establecer objective_achieved = True."

**Tests (Paso 1.5):**

1. **Test de display y actions:**  
   * Prompt para la IA integrada en el IDE:  
     "Actualiza tests/test_display.py y tests/test_actions.py.  
     * En test_display.py, configura un game_state con una dungeon_layout mockeada y verifica que display_scenario muestra las opciones correctas basadas en las conexiones de la habitación actual (direcciones cardinales).  
     * En test_actions.py, verifica que process_player_action maneja correctamente las transiciones de ubicación basadas en las conexiones de la mazmorra generada y que la condición de salida se activa correctamente."

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

## **4. Fase 2: Plan de Distribución del MVP**

Este será un documento Markdown independiente que abordará las herramientas y los pasos necesarios para hacer que el juego sea accesible para otros, incluyendo manejo de sesiones, persistencia con Supabase, una interfaz web gráfica (simulando texto), contenerización y despliegue en Google Cloud. Este plan se abordará una vez que el MVP local esté funcional y probado.

Este plan detallado nos guiará a través del desarrollo del MVP con las nuevas especificaciones. Estoy listo para que empecemos con el **Paso 1.1** o cualquier otra modificación que desees hacer.