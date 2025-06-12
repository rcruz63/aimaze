# **Plan de Desarrollo del MVP: AiMaze \- La Mazmorra Generativa**

Este documento detalla el plan de trabajo paso a paso para el desarrollo del Producto Mínimo Viable (MVP) de AiMaze, un juego de mazmorras interactivo impulsado por IA.

## **Filosofía de Desarrollo**

Adoptaremos un enfoque iterativo y de "test-driven development" (TDD) donde sea posible. La IA integrada en el IDE (este asistente) será utilizada activamente para la generación de código, la validación y la creación de pruebas.

## **Fase 1: Flujo Básico del Juego e Integración de IA (Generación de Texto)**

### **Objetivo de la Fase:**

Implementar el flujo básico del juego donde el jugador puede moverse a través de una mazmorra generada por IA, recibir descripciones de ubicación y opciones de acción, y resolver un tipo simple de evento.

### **Paso 1.1: Configuración del Entorno y Refinamiento del Esqueleto Inicial**

**Objetivo:** Establecer el entorno de desarrollo, las dependencias iniciales y asegurar que la estructura de módulos funciona correctamente.

**Acciones:**

1. **Crear archivo src/aimaze/\_\_init\_\_.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Por favor, crea el archivo src/aimaze/\_\_init\_\_.py. Debe estar vacío."  
2. **Configurar python-dotenv:**  
   * Prompt para la IA integrada en el IDE:  
     "Necesitamos configurar python-dotenv para cargar variables de entorno. Genera el código necesario en src/aimaze/config.py para cargar un archivo .env. Este módulo debería tener una función load\_environment\_variables() que inicialice las variables. Incluye un ejemplo de cómo cargar una variable OPENAI\_API\_KEY."  
   * Prompt para la IA integrada en el IDE:  
     "Genera un archivo .env de ejemplo en la raíz del proyecto con una variable OPENAI\_API\_KEY."  
3. **Actualizar game\_state.py para usar configuración:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/game\_state.py. Importa el módulo config y asegúrate de que, al inicializar el juego, se llamen a las funciones de config si es necesario para cargar variables de entorno que la IA podría necesitar más adelante."  
4. **Generar requirements.txt:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo requirements.txt en la raíz del proyecto. Debe incluir las dependencias iniciales: python-dotenv, openai, langchain, langfuse, pydantic."

**Tests:**

1. **Test básico de initialize\_game\_state:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test\_game\_state.py. Incluye un test que verifique que la función game\_state.initialize\_game\_state() devuelve un diccionario con las claves básicas esperadas (ej. player\_location\_id, game\_over, objective\_achieved). Utiliza unittest.mock para simular la importación de dungeon si es necesario."

### **Paso 1.2: Descripción de Ubicación Impulsada por IA (Primera Llamada LLM)**

**Objetivo:** Integrar la IA para generar descripciones de ubicación dinámicas y ASCII art, validando su salida con Pydantic.

**Acciones:**

1. **Crear src/aimaze/ai\_connector.py:**  
   * Este módulo encapsulará la lógica de interacción con la API de OpenAI/Langchain.  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo src/aimaze/ai\_connector.py. Este módulo debe:  
     * Importar os y load\_dotenv de dotenv.  
     * Importar ChatOpenAI de langchain.chat\_models.  
     * Importar PromptTemplate y ChatPromptTemplate de langchain.prompts.  
     * Importar PydanticOutputParser y OutputFixingParser de langchain.output\_parsers.  
     * Importar RunnablePassthrough de langchain.schema.runnable.  
     * Importar BaseModel, Field de pydantic.  
     * Importar langfuse\_handler de langfuse.callback para LangfuseCallbackHandler.  
     * Definir un Pydantic BaseModel llamado LocationDescription con dos campos: description: str \= Field(description='Detailed textual description of the location.') y ascii\_art: str \= Field(description='ASCII art representation of the location, using monochrome green style with non-filling characters for shadows. Max 20 lines, 80 characters per line.').  
     * Implementar una función generate\_location\_description(location\_id: str) \-\> LocationDescription: que:  
       * Cargue la OPENAI\_API\_KEY del entorno.  
       * Configure LangfuseCallbackHandler.  
       * Cree una instancia de ChatOpenAI (modelo gpt-3.5-turbo o similar, temperatura 0.7).  
       * Defina un PromptTemplate que pida a la IA generar una descripción detallada de una ubicación de mazmorra, un ASCII art y las opciones de salida. Enfatiza el estilo monocromático verde y el uso de caracteres ASCII.  
       * Use PydanticOutputParser para parsear la salida a LocationDescription. Incluye un OutputFixingParser para robustez.  
       * Devuelva una instancia de LocationDescription.  
     * Incluye un ejemplo de uso en un if \_\_name\_\_ \== "\_\_main\_\_": para probar la función."  
2. **Modificar src/aimaze/display.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/display.py.  
     * Importa generate\_location\_description de src/aimaze/ai\_connector.py.  
     * En display\_scenario, reemplaza los placeholders de descripción y ASCII art por una llamada a generate\_location\_description usando el current\_loc\_id de game\_state.  
     * Almacena la descripción y el ASCII art en game\_state si es necesario para evitar regeneraciones costosas."

**Validación de IA:**

1. **Revisión Manual de Salida:**  
   * Después de ejecutar el juego una vez con este paso implementado, revisa manualmente las descripciones y el ASCII art generados por la IA.  
   * Prompt para la IA integrada en el IDE:  
     "Analiza la salida de generate\_location\_description cuando se le da el location\_id 'sala\_misteriosa'. ¿La descripción es coherente con una mazmorra? ¿El ASCII art es adecuado al estilo monocromático verde y usa caracteres para sombras? ¿Se adhiere a las restricciones de tamaño?" (Se hará esto para varias ubicaciones simuladas).

**Tests:**

1. **Mocking de Llamadas a LLM:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test\_display.py.  
     * Crea un test para display.display\_scenario que utilice unittest.mock.patch para simular la llamada a ai\_connector.generate\_location\_description. La función mockeada debe devolver una instancia de LocationDescription predefinida.  
     * Verifica que display\_scenario intenta imprimir el ASCII art y la descripción mockeados."

### **Paso 1.3: Generación Simple de Mazmorra (IA para Estructura)**

**Objetivo:** Permitir que la IA genere la estructura básica de la mazmorra (habitaciones y conexiones), asegurando que sea navegable y lineal para el MVP.

**Acciones:**

1. **Definir Modelos Pydantic para Mazmorra en src/aimaze/dungeon.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/dungeon.py.  
     * Importa BaseModel, Field de pydantic.  
     * Define un Pydantic BaseModel llamado Room con los siguientes campos: id: str \= Field(description='Unique identifier for the room.'), description\_id: str \= Field(description='Reference ID for the detailed description from AI.'), connections: Dict\[str, str\] \= Field(description='Dictionary mapping cardinal directions (e.g., "north", "east") or action numbers to the ID of the connected room or action.').  
     * Define un Pydantic BaseModel llamado DungeonLayout con un campo: rooms: Dict\[str, Room\] \= Field(description='Dictionary where keys are room IDs and values are Room objects.').  
2. **Añadir Generación de Mazmorra a src/aimaze/ai\_connector.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Añade a src/aimaze/ai\_connector.py una nueva función generate\_dungeon\_layout() \-\> DungeonLayout: que:  
     * Use ChatOpenAI.  
     * Defina un PromptTemplate para pedir a la IA que genere una *pequeña* mazmorra lineal (ej. 3-5 habitaciones conectadas) en formato JSON, adhiriéndose a la estructura de los modelos Room y DungeonLayout.  
     * Asegúrate de que la mazmorra tenga un 'inicio' y una 'salida' claramente definidos.  
     * Utiliza PydanticOutputParser y OutputFixingParser para validar la salida."  
3. **Integrar Generación en src/aimaze/game\_state.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/game\_state.py.  
     * Importa generate\_dungeon\_layout de src/aimaze/ai\_connector.py.  
     * En initialize\_game\_state, reemplaza la simulated\_dungeon\_layout estática por una llamada a ai\_connector.generate\_dungeon\_layout(). Almacena el resultado (un objeto DungeonLayout) en game\_state\["dungeon\_layout"\].  
     * Asegúrate de que player\_location\_id se inicialice con el ID de la habitación de inicio generada por la IA."

**Validación de IA:**

1. **Conectividad y Linealidad:**  
   * Prompt para la IA integrada en el IDE:  
     "Genera una mazmorra de ejemplo usando ai\_connector.generate\_dungeon\_layout(). Verifica manualmente:  
     * ¿Todas las habitaciones son accesibles desde el inicio?  
     * ¿Existe un camino claro hacia la salida?  
     * ¿La estructura es razonablemente lineal como se pidió para el MVP?"

**Tests:**

1. **Test de Generación de Mazmorra:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test\_dungeon\_generation.py.  
     * Crea un test para ai\_connector.generate\_dungeon\_layout que use unittest.mock.patch para simular la respuesta del LLM (devuelve una cadena JSON que represente una DungeonLayout válida).  
     * Verifica que la función devuelve una instancia de DungeonLayout y que su estructura es correcta (contiene las habitaciones esperadas y conexiones válidas)."

### **Paso 1.4: Opciones Dinámicas (Impulsadas por la Mazmorra Generada)**

**Objetivo:** Asegurar que las opciones presentadas al jugador se basen directamente en la mazmorra generada por la IA.

**Acciones:**

1. **Modificar src/aimaze/display.py y src/aimaze/actions.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/display.py y src/aimaze/actions.py.  
     * En display\_scenario (en display.py), las opciones mostradas al usuario y almacenadas en game\_state\["current\_options\_map"\] deben derivarse directamente de las connections de la Room actual en game\_state\["dungeon\_layout"\]. Ya no usarán el simulated\_dungeon\_layout.  
     * Ajusta la lógica en process\_player\_action (en actions.py) para que la validación y el cambio de player\_location\_id se basen en las connections de la Room actual de game\_state\["dungeon\_layout"\] en lugar de simulated\_dungeon\_layout."

**Tests:**

1. **Test de Opciones Dinámicas:**  
   * Prompt para la IA integrada en el IDE:  
     "Actualiza tests/test\_display.py y tests/test\_actions.py.  
     * En test\_display.py, asegúrate de que el mock de game\_state incluya una dungeon\_layout generada (o mockeada) y verifica que display\_scenario muestra las opciones correctas basadas en las conexiones de la habitación actual.  
     * En test\_actions.py, verifica que process\_player\_action maneja correctamente las transiciones de ubicación basadas en las connections de la mazmorra generada."

### **Paso 1.5: Atributos del Jugador y Experiencia (Local)**

**Objetivo:** Implementar un sistema básico de atributos para el jugador y un placeholder para la ganancia de experiencia.

**Acciones:**

1. **Actualizar src/aimaze/game\_state.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/game\_state.py.  
     * En initialize\_game\_state, inicializa game\_state\["player\_attributes"\] con valores numéricos para: strength, dexterity, intelligence, perception, health (HP), max\_health, y experience (XP). Asigna valores iniciales razonables.  
     * Crea una nueva función update\_player\_xp(game\_state, amount: int) que añada amount a experience y, por ahora, solo imprima un mensaje cuando el jugador gane XP. No implementes la subida de nivel aún."

**Tests:**

1. **Test de Atributos y XP:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test\_player\_attributes.py.  
     * Crea un test para game\_state.initialize\_game\_state() que verifique que los atributos del jugador se inicializan correctamente.  
     * Crea un test para game\_state.update\_player\_xp() que verifique que la experiencia del jugador se actualiza correctamente."

### **Paso 1.6: Generación y Resolución de Eventos Simples (Primer Encuentro)**

**Objetivo:** Permitir que la IA genere eventos simples en las habitaciones y que el jugador los resuelva mediante un sistema de "tirada de dados" contra atributos.

**Acciones:**

1. **Crear src/aimaze/events.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea el archivo src/aimaze/events.py. Este módulo debe:  
     * Importar BaseModel, Field de pydantic.  
     * Importar random.  
     * Importar Literal, Optional, Tuple de typing.  
     * Definir un Pydantic BaseModel llamado GameEvent con los siguientes campos:  
       * type: Literal\['obstacle', 'monster', 'puzzle'\] \= Field(..., description='Type of the event.')  
       * description: str \= Field(..., description='Detailed textual description of the event.')  
       * required\_attribute: Optional\[Literal\['strength', 'dexterity', 'intelligence', 'perception'\]\] \= Field(None, description='Attribute required to attempt to resolve the event.')  
       * difficulty\_check: Optional\[int\] \= Field(None, description='Target number for a d20 roll \+ attribute to succeed.')  
       * success\_text: str \= Field(..., description='Narrative text on successful event resolution.')  
       * failure\_text: str \= Field(..., description='Narrative text on failed event resolution.')  
       * xp\_reward: int \= Field(0, description='Experience points awarded on success.')  
       * damage\_on\_failure: int \= Field(0, description='Health damage taken on failure.')  
     * Implementar una función generate\_random\_event(location\_id: str) \-\> Optional\[GameEvent\] que:  
       * Use ChatOpenAI (vía ai\_connector).  
       * Defina un PromptTemplate que pida a la IA generar un evento simple (ej. un pequeño obstáculo en el camino, una criatura débil, un enigma sencillo) adhiriéndose a la estructura de GameEvent. Asegúrate de que la IA genere un solo tipo de evento por llamada.  
       * Utiliza PydanticOutputParser y OutputFixingParser.  
       * Devuelve una instancia de GameEvent o None si no hay evento.  
     * Implementar una función resolve\_event(game\_state, event: GameEvent) \-\> Tuple\[bool, str\] que:  
       * Simule una "tirada de d20" (random.randint(1, 20)).  
       * Si el evento tiene required\_attribute y difficulty\_check:  
         * Sume la tirada al atributo del jugador.  
         * Compare con difficulty\_check.  
         * Imprima un mensaje descriptivo del intento (sin números).  
         * Si tiene éxito, aplique xp\_reward (llamando a game\_state.update\_player\_xp) e imprima event.success\_text. Devuelva (True, event.success\_text).  
         * Si falla, aplique damage\_on\_failure a game\_state\["player\_attributes"\]\["health"\] e imprima event.failure\_text. Devuelve (False, event.failure\_text).  
       * Si el evento no tiene required\_attribute o difficulty\_check (ej. solo narrativa):  
         * Simplemente imprima event.description y event.success\_text. Devuelva (True, event.success\_text).  
       * Asegúrate de manejar el caso donde la IA generaría la narrativa de éxito o fracaso, y no la imprimas directamente si ya está incluida en success\_text/failure\_text.  
     * Añade un ejemplo de uso en un if \_\_name\_\_ \== "\_\_main\_\_":."  
2. **Integrar Eventos en src/aimaze/actions.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/actions.py.  
     * Importa generate\_random\_event y resolve\_event de src/aimaze/events.py.  
     * En process\_player\_action, después de que el jugador se mueva a una nueva ubicación, introduce una probabilidad (ej. 30%) de generar y resolver un evento aleatorio llamando a generate\_random\_event() y luego a resolve\_event().  
     * Asegúrate de que el estado del jugador (health, experience) se actualice después de la resolución del evento."

**Validación de IA:**

1. **Comportamiento de Eventos:**  
   * Prompt para la IA integrada en el IDE:  
     "Ejecuta el juego varias veces. Observa los eventos generados por la IA:  
     * ¿Son coherentes con los tipos definidos (obstacle, monster, puzzle)?  
     * ¿Las descripciones son apropiadas?  
     * ¿Los textos de éxito/fracaso son narrativos y relevantes al tipo de evento?  
     * ¿El sistema de "tirada de dados" parece funcionar correctamente (impresión del resultado narrativo)?"

**Tests:**

1. **Test de Resolución de Eventos:**  
   * Prompt para la IA integrada en el IDE:  
     "Crea un archivo de test tests/test\_events.py.  
     * Crea un test para events.resolve\_event que use unittest.mock.patch para simular random.randint (para controlar la tirada de dados) y también para game\_state.update\_player\_xp.  
     * Define un GameEvent de prueba y un estado inicial del jugador.  
     * Verifica los resultados de éxito y fracaso del evento (cambios en HP, XP, y los mensajes de texto devueltos)."

### **Paso 1.7: Condición de Game Over (Muerte)**

**Objetivo:** Implementar la condición de "Game Over" cuando la salud del jugador llega a cero.

**Acciones:**

1. **Actualizar src/aimaze/actions.py:**  
   * Prompt para la IA integrada en el IDE:  
     "Modifica src/aimaze/actions.py.  
     * En process\_player\_action, después de cualquier lógica que pueda reducir la salud del jugador (ej. fallar un evento), añade una comprobación: if game\_state\["player\_attributes"\]\["health"\] \<= 0: game\_state\["game\_over"\] \= True.  
     * Asegúrate de que el bucle principal en main.py maneje esta nueva condición de game\_over para salir del bucle."

**Tests:**

1. **Test de Condición de Muerte:**  
   * Prompt para la IA integrada en el IDE:  
     "Actualiza tests/test\_actions.py.  
     * Crea un test que configure un game\_state donde la salud del jugador sea muy baja.  
     * Llama a process\_player\_action con una acción que resulte en daño (simulando un evento fallido).  
     * Verifica que game\_state\["game\_over"\] se establece en True."

## **Fase 2: Plan de Distribución del MVP (Documento Separado)**

Este será un documento Markdown independiente que abordará las herramientas y los pasos necesarios para hacer que el juego sea accesible para otros, incluyendo manejo de sesiones, persistencia con Supabase, una interfaz web gráfica (simulando texto), contenerización y despliegue en Google Cloud.