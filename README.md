# 🎲 AiMaze - La Mazmorra Generativa

> *"Donde la IA se encuentra con el papel y lápiz"*

## 🎯 ¿Qué es AiMaze?

**AiMaze** es un juego de mazmorras interactivo impulsado por inteligencia artificial que combina la nostalgia de los juegos de texto clásicos con la creatividad generativa moderna. Imagina un Dungeon Master virtual que crea mazmorras únicas, genera descripciones atmosféricas y teje historias dinámicas en tiempo real.

### 🌟 Características Principales

- **🎨 Mazmorras Generativas**: Cada partida es única gracias a la IA que crea estructuras de mazmorra dinámicas
- **📖 Narrativa Adaptativa**: Descripciones y eventos que se adaptan a tus decisiones
- **🧩 Enigmas Inteligentes**: Enfocado en puzzles mentales más que combate puro
- **🎭 Arte ASCII**: Visualizaciones monocromáticas que despiertan la imaginación
- **💾 Persistencia**: Guarda y continúa tus aventuras cuando quieras
- **🌍 Multi-idioma**: Preparado para internacionalización desde el inicio

## 🚀 Hitos del Desarrollo

### ✅ **Fase 1: MVP Local** (En Progreso)
- [x] Configuración del entorno y estructura modular
- [x] Modelado del jugador y estado básico
- [ ] Generación de descripciones por IA
- [ ] Sistema de coordenadas multi-nivel
- [ ] Opciones dinámicas basadas en la mazmorra
- [ ] Gestión de eventos básicos
- [ ] Sistema de guardado/carga
- [ ] Preparación para quests y personajes
- [ ] Sistema de localización

### 🔮 **Fase 2: Distribución del MVP**
- Interfaz web básica
- Integración con APIs externas
- Sistema de usuarios
- Analytics y métricas

### 🎮 **Fase 3: Características Avanzadas**
- Quests complejos y ramificados
- Sistema de combate estratégico
- Personajes NPC dinámicos
- Múltiples niveles de mazmorra
- Modo multijugador

## 🛠️ Filosofía de Desarrollo

**AiMaze** sigue un enfoque híbrido inteligente:

- **🔄 Estructura Determinista**: Algoritmos confiables para crear mazmorras navegables
- **🎨 Creatividad Narrativa**: IA enfocada en generar historias y descripciones únicas
- **🧪 Test-Driven Development**: Cada funcionalidad se prueba antes de implementarse
- **📦 Modularidad**: Código organizado en módulos claros y escalables
- **🎯 Iterativo**: Pequeños incrementos con funcionalidades verificables

## 🎲 Cómo Jugar

```bash
# Configurar el entorno
make setup

# Ejecutar el juego
make run

# O manualmente
python -m src.aimaze.main
```

## 🏗️ Arquitectura Técnica

```
src/aimaze/
├── main.py              # Bucle principal del juego
├── config.py            # Gestión de variables de entorno
├── game_state.py        # Estado global de la partida
├── display.py           # Salida de información al usuario
├── input.py             # Captura de entrada del usuario
├── actions.py           # Procesamiento de acciones
├── dungeon.py           # Lógica de mazmorra y coordenadas
├── ai_connector.py      # Interfaz con IA (OpenAI/LangChain)
├── events.py            # Generación y resolución de eventos
├── player.py            # Gestión del jugador
├── quest_manager.py     # Sistema de misiones
├── characters.py        # NPCs y monstruos
├── localization.py      # Soporte multi-idioma
└── save_load.py         # Persistencia de partidas
```

## 🎯 Objetivos del Proyecto

1. **Demostrar el potencial de la IA generativa** en la creación de experiencias de juego únicas
2. **Revivir la magia de los juegos de texto** con tecnología moderna
3. **Crear una plataforma escalable** para experimentar con narrativa generativa
4. **Fomentar la creatividad** a través de enigmas y puzzles inteligentes
5. **Construir una base sólida** para futuras expansiones y características

---

*¿Listo para adentrarte en la mazmorra generativa? ¡La IA te espera! 🗝️*
