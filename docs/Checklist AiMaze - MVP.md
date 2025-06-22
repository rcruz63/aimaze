# **Checklist de Desarrollo: AiMaze - MVP**

Este documento sirve como una checklist concisa para seguir el progreso del desarrollo del Producto Mínimo Viable (MVP) de AiMaze, basado en el "Plan Consolidado de Desarrollo del MVP". Marca cada elemento completado para facilitar la reanudación de las tareas.

## **Fase 1: Core Game Loop e Integración Inicial de IA (MVP Local)**

**Objetivo de la Fase:** Desarrollar un juego de texto interactivo funcional en la terminal, donde la mazmorra y las descripciones son generadas por IA, el jugador puede moverse y resolver eventos simples, y se puede guardar/cargar la partida.

### **Paso 1.1: Configuración del Entorno y Estructura Modular Base**

* [x] Crear la estructura de directorios: src/aimaze/ y tests/.  
* [x] Crear src/aimaze/__init__.py (vacío).  
* [x] Configurar python-dotenv y src/aimaze/config.py con load_config().  
* [x] Generar un archivo .env de ejemplo con OPENAI_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY.  
* [x] Generar requirements.txt con las dependencias iniciales.  
* [x] Crear archivos vacíos para player.py, quest_manager.py, characters.py, localization.py, save_load.py en src/aimaze/.  
* [x] Actualizar módulos existentes para importar config y otros con rutas relativas.  
* [x] **Test (1.1):** Crear tests/test_config.py y verificar carga de variables de entorno.

### **Paso 1.2: Modelado del Jugador y Estado Básico (player.py, game_state.py)**

* [x] Definir Pydantic BaseModel Player en src/aimaze/player.py con atributos (strength, dexterity, health, xp, inventory), gain_xp(), y take_damage().  
* [x] Integrar Player en src/aimaze/game_state.py, inicializando game_state['player'].  
* [x] **Test (1.2):** Crear tests/test_player.py y verificar inicialización, gain_xp(), y take_damage().

### **Paso 1.3: Generación de Descripción de Ubicación y Arte ASCII (ai_connector.py, display.py)**

* [ ] Definir Pydantic BaseModel LocationDescription en src/aimaze/ai_connector.py.  
* [ ] Implementar generate_location_description(location_context: str) -> LocationDescription en ai_connector.py.  
* [ ] Modificar src/aimaze/display.py para usar generate_location_description() en display_scenario().  
* [ ] **Validación IA (1.3):** Revisión manual de la salida de la IA (coherencia, estilo, tamaño).  
* [ ] **Test (1.3):** Crear tests/test_display.py y mockear generate_location_description().

### **Paso 1.4: Generación de Estructura de Mazmorra (dungeon.py, ai_connector.py)**

* [ ] Definir Pydantic BaseModel Room y DungeonLayout en src/aimaze/dungeon.py.  
* [ ] Mover simulated_dungeon_layout a get_placeholder_dungeon_layout().  
* [ ] Implementar generate_dungeon_layout() -> DungeonLayout en src/aimaze/ai_connector.py.  
* [ ] Integrar generate_dungeon_layout() en src/aimaze/game_state.py, reemplazando el diseño simulado.  
* [ ] **Validación IA (1.4):** Verificar conectividad y linealidad de la mazmorra generada.  
* [ ] **Test (1.4):** Crear tests/test_dungeon_generation.py y mockear la respuesta del LLM.

### **Paso 1.5: Opciones Dinámicas y Proceso de Acción (display.py, actions.py)**

* [ ] Modificar src/aimaze/display.py para derivar opciones de dungeon_layout.  
* [ ] Modificar src/aimaze/actions.py para procesar acciones basadas en dungeon_layout y manejar la salida.  
* [ ] **Test (1.5):** Actualizar tests/test_display.py y tests/test_actions.py para reflejar las opciones dinámicas.

### **Paso 1.6: Gestión de Eventos Básicos (events.py, ai_connector.py, actions.py)**

* [ ] Definir Pydantic BaseModel GameEvent en src/aimaze/events.py.  
* [ ] Implementar resolve_event(game_state, event: GameEvent) en src/aimaze/events.py.  
* [ ] Implementar generate_random_event(location_context: str) -> Optional[GameEvent] en src/aimaze/ai_connector.py.  
* [ ] Integrar la generación y resolución de eventos en src/aimaze/actions.py.  
* [ ] **Validación IA (1.6):** Observar coherencia y narrativa de los eventos generados.  
* [ ] **Test (1.6):** Crear tests/test_events.py y mockear random.randint para resolve_event().

### **Paso 1.7: Condiciones de Fin de Juego y Guardado Básico (game_state.py, save_load.py)**

* [ ] Añadir check_game_over(game_state) en src/aimaze/game_state.py y usarlo en actions.py.  
* [ ] Crear src/aimaze/save_load.py con save_game() y load_game().  
* [ ] Integrar guardar/cargar en src/aimaze/main.py (cargar al inicio, opción de guardar).  
* [ ] **Test (1.7):** Crear tests/test_save_load.py y actualizar tests/test_actions.py para muerte.

### **Paso 1.8: Preparación para Quests y Personajes (quest_manager.py, characters.py)**

* [ ] Definir Pydantic BaseModel Quest y QuestManager en src/aimaze/quest_manager.py (placeholders).  
* [ ] Definir Pydantic BaseModel Character, Monster, NPC en src/aimaze/characters.py (placeholders).  
* [ ] **Test (1.8):** Crear tests/test_quest_manager.py y tests/test_characters.py para verificar creación de modelos.

### **Paso 1.9: Preparación para Localización (localization.py)**

* [ ] Modificar src/aimaze/localization.py para implementar LocalizationManager con set_language() y get_text().  
* [ ] Integrar LocalizationManager en src/aimaze/main.py y src/aimaze/display.py para mensajes básicos.  
* [ ] **Test (1.9):** Crear tests/test_localization.py y verificar funcionalidad de gestión de idiomas.

## **Próximos Pasos**

Una vez completados todos los puntos de la Fase 1 (MVP Local), se procederá a la **Fase 2: Plan de Distribución del MVP**, detallada en un documento separado.

¡Espero que esta checklist te sea de gran utilidad para llevar un seguimiento de tu proyecto!