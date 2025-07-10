# src/aimaze/display.py

from aimaze.ai_connector import generate_location_description
from aimaze.dungeon import get_room_at_coords


def display_scenario(game_state):
    """
    Displays the current location description and available options.
    Uses AI to generate immersive textual descriptions based on coordinates.
    Options are derived from room connections.
    """
    # Obtener la ubicación actual del jugador usando coordenadas
    player_location = game_state["player_location"]
    dungeon = game_state["dungeon"]

    # Obtener el nivel actual
    current_level = dungeon.levels[player_location.level]

    # Usar get_room_at_coords() para obtener la Room actual
    current_room = get_room_at_coords(
        current_level, player_location.x, player_location.y)

    if not current_room:
        print("\nERROR: Ubicación desconocida! Algo salió mal.")
        game_state["game_over"] = True
        return

    print("\n" + "=" * 50)
    print(
        f"[NIVEL {player_location.level} - POSICIÓN ({player_location.x}, {player_location.y})]")

    # Generar o recuperar descripción de la ubicación usando IA
    location_description_key = f"location_description_{player_location.to_string()}"

    if location_description_key not in game_state:
        # El contexto incluye las coordenadas según especificación: 'Level {nivel} at ({x},{y})'
        location_context = f"Level {player_location.level} at ({player_location.x},{player_location.y})"
        print("Generando descripción de la ubicación...")

        try:
            location_desc = generate_location_description(location_context)
            game_state[location_description_key] = location_desc
        except Exception as e:
            print(f"Error generando descripción: {e}")
            # Usar descripción de fallback
            from .ai_connector import LocationDescription
            location_desc = LocationDescription(
                description=f"Te encuentras en una habitación de la mazmorra en el nivel {player_location.level}, coordenadas ({player_location.x},{player_location.y}). La atmósfera es misteriosa."
            )
            game_state[location_description_key] = location_desc
    else:
        # Usar descripción ya generada
        location_desc = game_state[location_description_key]

    # Mostrar descripción detallada
    print(location_desc.description)

    print("\nOpciones:")
    options_map = {}  # Mapear número de opción a acción
    option_num = 1

    # Las opciones se derivan de room.connections (direcciones cardinales disponibles)
    for direction, target_coords in current_room.connections.items():
        # Traducir dirección a texto amigable
        direction_text = {
            'north': 'Norte',
            'south': 'Sur',
            'east': 'Este',
            'west': 'Oeste'
        }.get(direction, direction.capitalize())

        print(f"{option_num}) Ir al {direction_text}")
        options_map[str(option_num)] = (direction, target_coords)
        option_num += 1

    # Verificar si estamos en las coordenadas de salida del nivel
    if (player_location.x, player_location.y) == current_level.exit_coords:
        print(f"{option_num}) ¡INTENTAR SALIR DEL NIVEL!")
        options_map[str(option_num)] = ("exit", None)
        option_num += 1

    # Opción para guardar partida
    print(f"{option_num}) Guardar partida")
    options_map[str(option_num)] = ("save", None)

    # Guardar el mapa de opciones para validación en actions.py
    game_state["current_options_map"] = options_map
    print("=" * 50)


def display_game_over(game_state):
    """
    Displays game over message.
    """
    print("\n" + "=" * 50)
    print("¡GAME OVER!")

    player = game_state.get("player")
    if player and player.health <= 0:
        print("Has sucumbido a los peligros de la mazmorra...")
        print(f"Tu aventura termina en el nivel {game_state['player_location'].level}")
    else:
        print("Tu aventura ha llegado a su fin.")

    print("=" * 50)


def display_victory(game_state):
    """
    Displays victory message.
    """
    print("\n" + "=" * 50)
    print("¡VICTORIA!")
    print("¡Has logrado escapar de la mazmorra!")

    player = game_state.get("player")
    if player:
        print(f"Experiencia ganada: {player.experience} XP")
        print(f"Salud restante: {player.health}/{player.max_health}")

    print("¡Felicidades, aventurero!")
    print("=" * 50)


def display_error(message):
    """
    Displays error messages with consistent formatting.
    """
    print(f"\nError: {message}")


def display_info(message):
    """
    Displays informational messages.
    """
    print(f"\nInfo: {message}")
