# src/aimaze/actions.py

from aimaze.dungeon import get_room_at_coords
from aimaze.game_state import check_game_over
from aimaze.save_load import save_game


def process_player_action(game_state, raw_input):
    """
    Processes the player's action using the coordinate-based system.
    Validates movement through room connections and manages game state.
    """
    valid_options = game_state.get("current_options_map", {})
    player_location = game_state["player_location"]
    dungeon = game_state["dungeon"]
    current_level = dungeon.levels[player_location.level]

    # Obtener la habitación actual usando get_room_at_coords()
    current_room = get_room_at_coords(
        current_level, player_location.x, player_location.y)

    if not current_room:
        print("\nError: No se puede determinar la habitación actual.")
        game_state["game_over"] = True
        return game_state

    if raw_input in valid_options:
        chosen_action = valid_options[raw_input]

        if isinstance(chosen_action, tuple) and len(chosen_action) == 2:
            action_type, target_coords = chosen_action

            if action_type == "exit":
                # El jugador intenta salir del nivel
                if (player_location.x, player_location.y) == current_level.exit_coords:
                    game_state["objective_achieved"] = True
                    print("\n¡Felicidades! Has encontrado la salida y has escapado de la mazmorra.")
                else:
                    print("\nNo puedes salir desde aquí. Necesitas encontrar la salida del nivel.")

            elif action_type == "save":
                # Guardar partida
                try:
                    save_game(game_state)
                    print("\n¡Partida guardada exitosamente!")
                except Exception as e:
                    print(f"\nError al guardar la partida: {e}")

            else:
                # Validar que la dirección elegida existe en room.connections
                direction = action_type
                if direction not in current_room.connections:
                    print(
                        f"\nError: No puedes ir hacia el {direction} desde esta habitación.")
                    return game_state

                # Obtener las coordenadas objetivo desde room.connections
                new_x, new_y = current_room.connections[direction]

                # Validación de límites (coordenadas dentro de level.width y level.height)
                if not (0 <= new_x < current_level.width and 0 <= new_y < current_level.height):
                    print(
                        f"\nError: Coordenadas ({new_x}, {new_y}) fuera de los límites del nivel ({current_level.width}x{current_level.height}).")
                    return game_state

                # Verificar que existe una habitación en las coordenadas objetivo
                target_room = get_room_at_coords(current_level, new_x, new_y)
                if not target_room:
                    print(
                        f"\nError: No hay habitación en las coordenadas ({new_x}, {new_y}).")
                    return game_state

                # Al moverse, actualizar game_state['player_location'] con las nuevas coordenadas
                player_location.x = new_x
                player_location.y = new_y

                # Traducir dirección a texto amigable
                direction_text = {
                    'north': 'Norte',
                    'south': 'Sur',
                    'east': 'Este',
                    'west': 'Oeste'
                }.get(direction, direction.capitalize())

                print(f"\nTe mueves hacia el {direction_text}.")
                print(f"Ahora estás en la posición ({new_x}, {new_y}).")

                # Verificar si las nuevas coordenadas son exit_coords del nivel actual para establecer objective_achieved = True
                if (new_x, new_y) == current_level.exit_coords:
                    print("¡Has encontrado la salida del nivel!")
                    # No establecer objective_achieved aquí, el jugador debe elegir explícitamente "INTENTAR SALIR"

                # Aquí se podría integrar la generación de eventos aleatorios (Paso 1.6)
                # Por ahora dejamos placeholders para futura implementación

        else:
            print(f"\nAcción no reconocida: {chosen_action}")
    else:
        print("Opción inválida. Por favor ingresa el número de una de las opciones disponibles.")

    # Verificar condiciones de fin de juego
    if check_game_over(game_state):
        game_state["game_over"] = True

    if game_state.get("objective_achieved", False):
        game_state["game_over"] = True

    return game_state


def validate_player_input(raw_input, valid_options):
    """
    Validates that the player input corresponds to a valid option.

    Args:
        raw_input: The raw input from the player
        valid_options: Dictionary of valid options from current_options_map

    Returns:
        bool: True if input is valid, False otherwise
    """
    return raw_input in valid_options


def get_action_description(action_type, target_coords=None):
    """
    Returns a human-readable description of an action.

    Args:
        action_type: The type of action ('north', 'south', 'east', 'west', 'exit', 'save')
        target_coords: Target coordinates for movement actions

    Returns:
        str: Human-readable description of the action
    """
    if action_type in ['north', 'south', 'east', 'west']:
        direction_text = {
            'north': 'Norte',
            'south': 'Sur',
            'east': 'Este',
            'west': 'Oeste'
        }.get(action_type, action_type.capitalize())

        if target_coords:
            return f"Moverse hacia el {direction_text} a las coordenadas {target_coords}"
        else:
            return f"Moverse hacia el {direction_text}"

    elif action_type == "exit":
        return "Intentar salir del nivel"
    elif action_type == "save":
        return "Guardar partida"
    else:
        return f"Acción desconocida: {action_type}"
