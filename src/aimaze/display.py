# src/aimaze/display.py

from aimaze.ai_connector import generate_location_description
from aimaze.dungeon import get_room_at_coords


def display_scenario(game_state):
    """
    Displays the current location description and available options.
    Uses AI to generate immersive textual descriptions (no ASCII art).
    """
    # Obtener la ubicación actual del jugador
    player_location = game_state["player_location"]
    dungeon = game_state["dungeon"]
    
    # Obtener el nivel actual
    current_level = dungeon.levels[player_location.level]
    
    # Obtener la habitación actual usando coordenadas
    current_room = get_room_at_coords(current_level, player_location.x, player_location.y)
    
    if not current_room:
        print("\nERROR: Ubicación desconocida! Algo salió mal.")
        game_state["game_over"] = True
        return

    print("\n" + "="*50)
    print(f"[NIVEL {player_location.level} - POSICIÓN ({player_location.x}, {player_location.y})]")
    
    # Generar o recuperar descripción de la ubicación usando IA
    location_description_key = f"location_description_{player_location.to_string()}"
    
    if location_description_key not in game_state:
        # Generar nueva descripción usando IA
        location_context = f"Level {player_location.level} at ({player_location.x},{player_location.y}) - {current_room.id}"
        print("Generando descripción de la ubicación...")
        
        try:
            location_desc = generate_location_description(location_context)
            game_state[location_description_key] = location_desc
        except Exception as e:
            print(f"Error generando descripción: {e}")
            # Usar descripción de fallback
            from .ai_connector import LocationDescription
            location_desc = LocationDescription(
                description=f"Te encuentras en {current_room.id}. La atmósfera es misteriosa."
            )
            game_state[location_description_key] = location_desc
    else:
        # Usar descripción ya generada
        location_desc = game_state[location_description_key]
    
    # Mostrar descripción detallada (sin ASCII art)
    print(location_desc.description)

    print("\nOpciones:")
    options_map = {} # To map the option number to its destination coordinates
    option_num = 1
    
    # Mostrar opciones basadas en las conexiones de la habitación actual
    for direction, target_coords in current_room.connections.items():
        # Traducir dirección a texto amigable
        direction_text = {
            'north': 'Norte',
            'south': 'Sur', 
            'east': 'Este',
            'west': 'Oeste'
        }.get(direction, direction)
        
        print(f"{option_num}) Ir al {direction_text}")
        options_map[str(option_num)] = (direction, target_coords)
        option_num += 1
    
    # Verificar si estamos en la salida del nivel
    if (player_location.x, player_location.y) == current_level.exit_coords:
        print(f"{option_num}) ¡INTENTAR SALIR DEL NIVEL!")
        options_map[str(option_num)] = ("exit", None)
        option_num += 1

    game_state["current_options_map"] = options_map # Save for input validation
    print("="*50)
