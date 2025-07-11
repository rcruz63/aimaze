# **Plan de Desarrollo del MVP: AiMaze \- La Mazmorra Generativa**

Este documento detalla el plan de trabajo paso a paso para el desarrollo del Producto Mínimo Viable (MVP) de AiMaze, un juego de mazmorras interactivo impulsado por IA.

## **Filosofía de Desarrollo**

Adoptaremos un enfoque iterativo y de "test-driven development" (TDD) donde sea posible. La IA integrada en el IDE (este asistente) será utilizada activamente para la generación de código, la validación y la creación de pruebas. Cada incremento será pequeño y completamente testeado, con funcionalidades únicas por solicitud.

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
     "Necesitamos configurar python-dotenv para cargar variables de entorno. Genera el código necesario en src/aimaze/config.py para cargar un archivo .env. Este módulo debería tener una función load\_environment\_variables() que inicialice las variables de entorno desde un archivo .env ubicado en la raíz del proyecto. La función debe usar load_dotenv() de python-dotenv y manejar el caso donde el archivo .env no existe sin fallar. Incluye un ejemplo de cómo cargar una variable OPENAI\_API\_KEY usando os.getenv() con un valor por defecto None. Añade documentación docstring explicando el propósito de cada función."
   * Prompt para la IA integrada en el IDE:
     "Genera un archivo .env de ejemplo en la raíz del proyecto con las siguientes variables: OPENAI\_API\_KEY=tu_clave_aqui, LANGFUSE\_PUBLIC\_KEY=tu_clave_publica_langfuse, LANGFUSE\_SECRET\_KEY=tu_clave_secreta_langfuse, LANGFUSE\_HOST=https://cloud.langfuse.com. Incluye comentarios explicando qué hace cada variable."
3. **Actualizar game\_state.py para usar configuración:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/game\_state.py. Importa el módulo config y asegúrate de que, al inicializar el juego, se llame a config.load\_environment\_variables() al principio de la función initialize\_game\_state(). Esto garantiza que las variables de entorno estén disponibles para las llamadas posteriores a la IA."
4. **Generar requirements.txt:**
   * Prompt para la IA integrada en el IDE:
     "Crea el archivo requirements.txt en la raíz del proyecto. Debe incluir las dependencias iniciales con versiones específicas: python-dotenv>=1.0.0, openai>=1.0.0, langchain>=0.1.0, langchain-openai>=0.1.0, langfuse>=2.0.0, pydantic>=2.0.0. Añade comentarios explicando para qué se usa cada dependencia."

**Tests:**

1. **Test básico de initialize\_game\_state:**
   * Prompt para la IA integrada en el IDE:
     "Crea un archivo de test tests/test\_game\_state.py. Incluye un test que verifique que la función game\_state.initialize\_game\_state() devuelve un diccionario con las claves básicas esperadas: player\_location\_id, game\_over, objective\_achieved, player\_attributes, dungeon\_layout. Utiliza unittest.mock.patch para simular config.load\_environment\_variables() y cualquier importación de dungeon si es necesario. El test debe verificar que cada clave existe y tiene el tipo de dato correcto."

### **Paso 1.2: Descripción de Ubicación Impulsada por IA (Primera Llamada LLM)**

**Objetivo:** Integrar la IA para generar descripciones de ubicación dinámicas y ASCII art, validando su salida con Pydantic.

**Acciones:**

1. **Crear src/aimaze/ai\_connector.py:**
   * Este módulo encapsulará la lógica de interacción con la API de OpenAI/Langchain.
   * Prompt para la IA integrada en el IDE:
     "Crea el archivo src/aimaze/ai\_connector.py. Este módulo debe:
     * Importar os, load\_dotenv de dotenv
     * Importar ChatOpenAI de langchain_openai
     * Importar PromptTemplate de langchain.prompts
     * Importar PydanticOutputParser, OutputFixingParser de langchain.output\_parsers
     * Importar BaseModel, Field de pydantic
     * Importar LangfuseCallbackHandler de langfuse.callback
     * Definir un Pydantic BaseModel llamado LocationDescription con campos: description: str = Field(description='Descripción textual detallada de la ubicación en español, mínimo 100 palabras, máximo 300 palabras'), ascii\_art: str = Field(description='Representación ASCII art de la ubicación, usando estilo monocromático verde con caracteres no rellenos para sombras. Máximo 20 líneas, 80 caracteres por línea')
     * Implementar función generate\_location\_description(location\_id: str, context: str = '') -> LocationDescription que:
       - Cargue OPENAI\_API\_KEY del entorno usando os.getenv()
       - Configure LangfuseCallbackHandler con las claves de entorno correspondientes
       - Cree instancia ChatOpenAI con modelo gpt-3.5-turbo, temperatura 0.7
       - Defina PromptTemplate que pida generar descripción detallada de ubicación de mazmorra medieval fantástica, ASCII art monocromático verde, considerando el context si se proporciona
       - Use PydanticOutputParser para parsear salida a LocationDescription
       - Incluya OutputFixingParser para robustez ante errores de formato
       - Maneje excepciones y devuelva descripción por defecto si falla
       - Registre la llamada en Langfuse con metadatos relevantes
     * Incluye ejemplo de uso en if \_\_name\_\_ == '\_\_main\_\_': que pruebe la función con location\_id 'entrada\_mazmorra'"

2. **Modificar src/aimaze/display.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/display.py para integrar la generación de descripciones por IA:
     * Importa generate\_location\_description de src/aimaze/ai\_connector
     * En display\_scenario, antes de mostrar la descripción:
       - Verifica si game\_state ya tiene una descripción cached para current\_loc\_id en game\_state.get('location\_descriptions', {})
       - Si no existe, llama a generate\_location\_description(current\_loc\_id) y guarda el resultado en game\_state['location\_descriptions'][current\_loc\_id]
       - Usa la descripción y ASCII art del LocationDescription obtenido
     * Inicializa game\_state['location\_descriptions'] como diccionario vacío si no existe
     * Maneja errores de generación mostrando descripción por defecto"

**Validación de IA:**

1. **Revisión Manual de Salida:**
   * Después de ejecutar el juego una vez con este paso implementado, revisa manualmente las descripciones y el ASCII art generados por la IA.
   * Prompt para la IA integrada en el IDE:
     "Ejecuta el juego y analiza la salida de generate\_location\_description para diferentes location\_id como 'entrada\_mazmorra', 'pasillo\_oscuro', 'sala\_tesoro'. Verifica: ¿La descripción es coherente con una mazmorra medieval fantástica? ¿El ASCII art usa estilo monocromático verde apropiado? ¿Se adhiere a las restricciones de tamaño (20 líneas, 80 caracteres)? ¿Las descripciones son suficientemente detalladas (100-300 palabras)? Documenta cualquier problema encontrado."

**Tests:**

1. **Mocking de Llamadas a LLM:**
   * Prompt para la IA integrada en el IDE:
     "Crea archivo tests/test\_ai\_connector.py con:
     * Test para generate\_location\_description usando unittest.mock.patch para simular ChatOpenAI
     * Mock debe devolver respuesta JSON válida que se parsee a LocationDescription
     * Verifica que función devuelve instancia LocationDescription con campos correctos
     * Test manejo de errores cuando API falla
     * Test que verifica llamada a Langfuse para tracking"
   * Prompt para la IA integrada en el IDE:
     "Actualiza tests/test\_display.py para:
     * Mockear ai\_connector.generate\_location\_description
     * Verificar que display\_scenario usa descripción cached cuando existe
     * Verificar que genera nueva descripción cuando no existe en cache
     * Verificar que maneja errores de generación apropiadamente"

### **Paso 1.3: Generación Simple de Mazmorra (IA para Estructura)**

**Objetivo:** Permitir que la IA genere la estructura básica de la mazmorra (habitaciones y conexiones), asegurando que sea navegable y lineal para el MVP.

**Acciones:**

1. **Definir Modelos Pydantic para Mazmorra en src/aimaze/dungeon.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/dungeon.py para definir modelos robustos de mazmorra:
     * Importa BaseModel, Field, validator de pydantic
     * Importa Dict, List, Optional de typing
     * Define Room con campos: id: str, description\_id: str, connections: Dict[str, str] (mapea direcciones cardinales a room\_ids), visited: bool = False, state: Dict[str, Any] = {}
     * Define Connection con campos: from\_room\_id: str, to\_room\_id: str, direction: str, reverse\_direction: str, is\_blocked: bool = False, block\_reason: Optional[str] = None
     * Define DungeonLayout con campos: rooms: Dict[str, Room], connections: List[Connection], start\_room\_id: str, end\_room\_id: str
     * Añade validator en DungeonLayout que verifique que start\_room\_id y end\_room\_id existen en rooms
     * Añade método get\_room\_connections(room\_id: str) -> List[Connection] que devuelva conexiones desde esa sala"

2. **Añadir Generación de Mazmorra a src/aimaze/ai\_connector.py:**
   * Prompt para la IA integrada en el IDE:
     "Añade a src/aimaze/ai\_connector.py función generate\_dungeon\_layout(size: str = 'small') -> DungeonLayout:
     * Use ChatOpenAI con temperatura 0.5 para más consistencia
     * Defina PromptTemplate que pida generar mazmorra lineal JSON con:
       - Para size='small': 3-5 habitaciones conectadas linealmente
       - Habitaciones con ids descriptivos (ej: 'entrada', 'pasillo\_1', 'sala\_tesoro')
       - Conexiones bidireccionales claras (norte-sur, este-oeste)
       - Un inicio claro ('entrada') y final claro ('salida' o 'sala\_tesoro')
       - Estructura que garantice navegabilidad sin bucles complejos
     * Use PydanticOutputParser para DungeonLayout con OutputFixingParser
     * Valide que la mazmorra generada es navegable (existe camino de inicio a fin)
     * Registre generación en Langfuse con metadatos de tamaño y estructura
     * Maneje errores devolviendo mazmorra por defecto de 3 salas lineales"

3. **Integrar Generación en src/aimaze/game\_state.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/game\_state.py para usar generación de mazmorra:
     * Importa generate\_dungeon\_layout de ai\_connector
     * En initialize\_game\_state, reemplaza cualquier simulated\_dungeon\_layout estático
     * Llama a generate\_dungeon\_layout('small') y almacena resultado en game\_state['dungeon\_layout']
     * Inicializa player\_location\_id con dungeon\_layout.start\_room\_id
     * Añade game\_state['visited\_rooms'] = set() para tracking de salas visitadas
     * Añade game\_state['location\_descriptions'] = {} para cache de descripciones"

**Validación de IA:**

1. **Conectividad y Linealidad:**
   * Prompt para la IA integrada en el IDE:
     "Crea función de validación validate\_dungeon\_connectivity en src/aimaze/dungeon.py que:
     * Verifique que todas las habitaciones son accesibles desde start\_room\_id usando BFS
     * Verifique que existe camino de start\_room\_id a end\_room\_id
     * Verifique que conexiones son bidireccionales (si A conecta a B, B debe conectar a A)
     * Devuelva tuple (is\_valid: bool, errors: List[str]) con detalles de problemas encontrados
     * Ejecuta esta validación después de cada generación de mazmorra"

**Tests:**

1. **Test de Generación de Mazmorra:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test\_dungeon\_generation.py con:
     * Test para generate\_dungeon\_layout mockeando ChatOpenAI con respuesta JSON válida
     * Test que verifica estructura DungeonLayout devuelta es correcta
     * Test de validación de conectividad con mazmorras válidas e inválidas
     * Test manejo de errores cuando generación falla
     * Test que verifica que mazmorra por defecto es navegable"

### **Paso 1.4: Sistema de Coherencia de Mazmorra**

**Objetivo:** Implementar validación y mantenimiento de coherencia entre salas conectadas.

**Acciones:**

1. **Crear src/aimaze/coherence\_validator.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea src/aimaze/coherence\_validator.py con sistema de validación de coherencia:
     * Importa modelos de dungeon.py y typing
     * Función validate\_room\_coherence(room: Room, connected\_rooms: Dict[str, Room]) -> List[str] que verifique:
       - Si room tiene conexión 'norte' a sala X, sala X debe tener conexión 'sur' de vuelta
       - Conexiones bidireccionales son consistentes en direcciones opuestas
       - No hay conexiones a salas inexistentes
     * Función ensure\_bidirectional\_connections(layout: DungeonLayout) -> DungeonLayout que:
       - Recorra todas las conexiones y añada conexiones inversas faltantes
       - Marque conexiones inversas como potencialmente bloqueadas si no existían
       - Mantenga log de cambios realizados
     * Función validate\_dungeon\_coherence(layout: DungeonLayout) -> tuple[bool, List[str]] que ejecute todas las validaciones"

**Tests:**

1. **Test de Coherencia:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test\_coherence\_validator.py con:
     * Test casos donde conexiones son coherentes
     * Test casos donde faltan conexiones bidireccionales
     * Test corrección automática de conexiones faltantes
     * Test detección de conexiones a salas inexistentes"

### **Paso 1.5: Opciones Dinámicas (Impulsadas por la Mazmorra Generada)**

**Objetivo:** Asegurar que las opciones presentadas al jugador se basen directamente en la mazmorra generada por la IA.

**Acciones:**

1. **Modificar src/aimaze/display.py y src/aimaze/actions.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/display.py para opciones dinámicas:
     * En display\_scenario, obtén Room actual de game\_state['dungeon\_layout'].rooms[current\_loc\_id]
     * Genera opciones basadas en room.connections, mostrando direcciones disponibles
     * Para cada conexión, verifica si está bloqueada y muestra estado apropiado
     * Almacena opciones en game\_state['current\_options\_map'] mapeando números a room\_ids destino
     * Muestra opciones numeradas con descripciones claras (ej: '1. Ir al norte hacia el pasillo oscuro')"
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/actions.py para usar opciones dinámicas:
     * En process\_player\_action, valida acción contra game\_state['current\_options\_map']
     * Si acción válida, obtén destination\_room\_id del mapa de opciones
     * Verifica que conexión no esté bloqueada antes de permitir movimiento
     * Actualiza player\_location\_id al destino y marca sala como visitada
     * Maneja casos donde conexión está bloqueada con mensaje apropiado"

**Tests:**

1. **Test de Opciones Dinámicas:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza tests/test\_display.py y crea tests/test\_actions.py:
     * Test que display\_scenario genera opciones correctas basadas en conexiones de sala actual
     * Test que opciones bloqueadas se muestran apropiadamente
     * Test que process\_player\_action valida acciones contra opciones disponibles
     * Test transiciones de ubicación correctas
     * Test manejo de acciones inválidas"

### **Paso 1.6: Atributos del Jugador y Experiencia (Local)**

**Objetivo:** Implementar un sistema básico de atributos para el jugador y un placeholder para la ganancia de experiencia.

**Acciones:**

1. **Actualizar src/aimaze/game\_state.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/game\_state.py para sistema de atributos:
     * En initialize\_game\_state, inicializa game\_state['player\_attributes'] con:
       - strength: int = 12 (fuerza física)
       - dexterity: int = 14 (agilidad y destreza)
       - intelligence: int = 13 (capacidad mental)
       - perception: int = 15 (percepción y awareness)
       - health: int = 100 (puntos de vida actuales)
       - max\_health: int = 100 (puntos de vida máximos)
       - experience: int = 0 (puntos de experiencia)
       - level: int = 1 (nivel del jugador)
     * Crea función update\_player\_xp(game\_state: dict, amount: int) -> bool que:
       - Añada amount a experience
       - Calcule si jugador sube de nivel (cada 100 XP)
       - Si sube nivel, incremente level y mejore atributos ligeramente
       - Imprima mensaje narrativo de ganancia de XP y subida de nivel
       - Devuelva True si subió de nivel, False si no
     * Crea función get\_attribute\_modifier(attribute\_value: int) -> int que calcule modificador D&D (valor-10)//2"

**Tests:**

1. **Test de Atributos y XP:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test\_player\_attributes.py con:
     * Test que initialize\_game\_state inicializa atributos correctamente
     * Test que update\_player\_xp añade experiencia correctamente
     * Test subida de nivel cuando se alcanza umbral de XP
     * Test cálculo de modificadores de atributos
     * Test que atributos se mejoran al subir de nivel"

### **Paso 1.7: Generación y Resolución de Eventos Simples (Primer Encuentro)**

**Objetivo:** Permitir que la IA genere eventos simples en las habitaciones y que el jugador los resuelva mediante un sistema de "tirada de dados" contra atributos.

**Acciones:**

1. **Crear src/aimaze/events.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea src/aimaze/events.py con sistema completo de eventos:
     * Importa BaseModel, Field de pydantic, random, Literal, Optional, Tuple de typing
     * Define GameEvent con campos:
       - id: str = Field(description='Identificador único del evento')
       - type: Literal['obstacle', 'monster', 'puzzle', 'treasure'] = Field(description='Tipo de evento')
       - description: str = Field(description='Descripción detallada del evento en español')
       - required\_attribute: Optional[Literal['strength', 'dexterity', 'intelligence', 'perception']] = Field(description='Atributo requerido para resolver')
       - difficulty\_check: Optional[int] = Field(description='Número objetivo para tirada d20 + atributo')
       - success\_text: str = Field(description='Texto narrativo de éxito')
       - failure\_text: str = Field(description='Texto narrativo de fracaso')
       - xp\_reward: int = Field(default=10, description='XP otorgado por éxito')
       - damage\_on\_failure: int = Field(default=0, description='Daño por fracaso')
       - can\_retry: bool = Field(default=False, description='Si se puede reintentar')
     * Función generate\_random\_event(location\_id: str, player\_level: int = 1) -> Optional[GameEvent] que:
       - Use ChatOpenAI para generar evento apropiado para ubicación y nivel
       - Prompt detallado pidiendo evento coherente con location\_id
       - Ajuste dificultad basada en player\_level
       - Use PydanticOutputParser con OutputFixingParser
       - 30% probabilidad de no generar evento (devolver None)
       - Registre generación en Langfuse
     * Función resolve\_event(game\_state: dict, event: GameEvent) -> Tuple[bool, str, dict] que:
       - Simule tirada d20 con random.randint(1, 20)
       - Si evento requiere atributo, sume modificador de atributo
       - Compare total con difficulty\_check
       - En éxito: aplique xp\_reward, devuelva (True, success\_text, cambios)
       - En fracaso: aplique damage\_on\_failure, devuelva (False, failure\_text, cambios)
       - Para eventos sin check: devuelva (True, description, {})
       - Imprima narrativa sin mostrar números de dados
     * Incluye ejemplo de uso completo en \_\_main\_\_"

2. **Integrar Eventos en src/aimaze/actions.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/actions.py para integrar eventos:
     * Importa generate\_random\_event, resolve\_event de events
     * Importa update\_player\_xp de game\_state
     * En process\_player\_action, después de movimiento exitoso a nueva ubicación:
       - Verifica si sala ya fue visitada (game\_state['visited\_rooms'])
       - Si es nueva sala, 40% probabilidad de generar evento
       - Si se genera evento, llama a resolve\_event
       - Aplica cambios de estado (XP, daño) usando funciones apropiadas
       - Marca sala como visitada en game\_state['visited\_rooms']
       - Guarda evento resuelto en game\_state para evitar repetición"

**Validación de IA:**

1. **Comportamiento de Eventos:**
   * Prompt para la IA integrada en el IDE:
     "Ejecuta el juego múltiples veces y documenta eventos generados:
     * ¿Eventos son coherentes con tipos definidos y ubicaciones?
     * ¿Descripciones son apropiadas y narrativamente ricas?
     * ¿Dificultad escala apropiadamente con nivel de jugador?
     * ¿Textos de éxito/fracaso son relevantes al tipo de evento?
     * ¿Sistema de tiradas funciona sin mostrar mecánicas al jugador?
     * Documenta cualquier evento incoherente o mal generado"

**Tests:**

1. **Test de Resolución de Eventos:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test\_events.py con cobertura completa:
     * Test generate\_random\_event mockeando ChatOpenAI
     * Test resolve\_event con diferentes tipos de eventos
     * Test tiradas exitosas y fallidas controlando random.randint
     * Test aplicación correcta de XP y daño
     * Test eventos sin checks de dificultad
     * Test integración con game\_state y update\_player\_xp
     * Test manejo de errores en generación de eventos"

### **Paso 1.8: Sistema de Quest Básico**

**Objetivo:** Implementar un sistema de quest simple con objetivos claros y seguimiento de progreso.

**Acciones:**

1. **Crear src/aimaze/quest\_system.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea src/aimaze/quest\_system.py con sistema de quests:
     * Importa modelos necesarios y typing
     * Define Quest con campos:
       - id: str, title: str, description: str
       - objectives: List[str] (lista de objetivos a completar)
       - completed\_objectives: List[bool] (estado de cada objetivo)
       - reward\_xp: int, reward\_items: List[str]
       - is\_completed: bool, is\_active: bool
     * Define QuestObjective con campos:
       - id: str, description: str, type: Literal['reach\_room', 'defeat\_monster', 'find\_item']
       - target: str (room\_id, monster\_id, item\_id según type)
       - is\_completed: bool
     * Función generate\_main\_quest(dungeon\_layout: DungeonLayout) -> Quest que:
       - Cree quest principal para llegar a end\_room\_id
       - Añada objetivos intermedios basados en estructura de mazmorra
       - Use IA para generar título y descripción narrativa del quest
       - Asegure que quest es completable con mazmorra dada
     * Función update\_quest\_progress(game\_state: dict, action\_type: str, target: str) -> List[str] que:
       - Verifique objetivos activos contra acción realizada
       - Marque objetivos completados cuando se cumplan
       - Devuelva lista de mensajes de progreso
     * Función check\_quest\_completion(quest: Quest) -> bool"

**Tests:**

1. **Test de Sistema de Quest:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test\_quest\_system.py con:
     * Test generación de quest principal
     * Test actualización de progreso de quest
     * Test detección de completación de quest
     * Test integración con estructura de mazmorra"

### **Paso 1.9: Condición de Game Over y Victoria**

**Objetivo:** Implementar condiciones de "Game Over" por muerte y condición de victoria por completar quest principal.

**Acciones:**

1. **Actualizar src/aimaze/actions.py:**
   * Prompt para la IA integrada en el IDE:
     "Modifica src/aimaze/actions.py para condiciones de fin de juego:
     * Después de cualquier lógica que reduzca health del jugador:
       - Verifica if game\_state['player\_attributes']['health'] <= 0
       - Si es así, establece game\_state['game\_over'] = True
       - Establece game\_state['death\_reason'] con descripción narrativa
       - Imprime mensaje dramático de muerte
     * Después de actualizar progreso de quest:
       - Verifica si quest principal está completado
       - Si es así, establece game\_state['objective\_achieved'] = True
       - Imprime mensaje de victoria narrativo
       - Calcula y muestra estadísticas finales (XP total, salas visitadas, etc.)
     * Asegura que bucle principal en main.py maneje ambas condiciones de salida"

**Tests:**

1. **Test de Condiciones de Fin:**
   * Prompt para la IA integrada en el IDE:
     "Actualiza tests/test\_actions.py con:
     * Test condición de muerte cuando health <= 0
     * Test condición de victoria cuando quest principal se completa
     * Test que game\_state se actualiza correctamente en ambos casos
     * Test mensajes apropiados se muestran"

### **Paso 1.10: Integración Completa de Langfuse**

**Objetivo:** Implementar tracking completo de todas las interacciones con IA usando Langfuse.

**Acciones:**

1. **Crear src/aimaze/langfuse\_integration.py:**
   * Prompt para la IA integrada en el IDE:
     "Crea src/aimaze/langfuse\_integration.py con tracking completo:
     * Importa Langfuse, LangfuseCallbackHandler
     * Clase LangfuseTracker con métodos:
       - \_\_init\_\_(self) que configure cliente Langfuse
       - track\_generation(self, type: str, input\_data: dict, output\_data: dict, metadata: dict)
       - track\_validation(self, type: str, input\_data: dict, result: bool, errors: List[str])
       - track\_game\_event(self, event\_type: str, player\_state: dict, outcome: dict)
       - start\_game\_session(self, session\_id: str) -> str
       - end\_game\_session(self, session\_id: str, final\_state: dict)
     * Integra tracking en todas las llamadas a IA existentes
     * Añade metadatos útiles: timestamp, player\_level, location, etc."

**Tests:**

1. **Test de Langfuse:**
   * Prompt para la IA integrada en el IDE:
     "Crea tests/test\_langfuse\_integration.py con:
     * Test inicialización de LangfuseTracker
     * Test tracking de diferentes tipos de eventos
     * Test manejo de errores cuando Langfuse no está disponible
     * Mock de llamadas a Langfuse para evitar dependencias externas en tests"

## **Fase 2: Plan de Distribución del MVP (Documento Separado)**

Este será un documento Markdown independiente que abordará las herramientas y los pasos necesarios para hacer que el juego sea accesible para otros, incluyendo manejo de sesiones, persistencia con Supabase, una interfaz web gráfica (simulando texto), contenerización y despliegue en Google Cloud.
