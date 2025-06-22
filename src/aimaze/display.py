# src/aimaze/display.py

from .ai_connector import generate_location_description


def display_scenario(game_state):
    """
    Displays the current location description and available options.
    Uses AI to generate immersive textual descriptions (no ASCII art).
    """
    current_loc_id = game_state["player_location_id"]
    scenario_data = game_state["simulated_dungeon_layout"].get(current_loc_id)

    if not scenario_data:
        print("\nERROR: Unknown location! Something went wrong.")
        game_state["game_over"] = True
        return

    print("\n" + "="*50)
    print(f"[{current_loc_id.replace('_', ' ').upper()}]")
    
    # Generar o recuperar descripción de la ubicación usando IA
    location_description_key = f"location_description_{current_loc_id}"
    
    if location_description_key not in game_state:
        # Generar nueva descripción usando IA
        location_context = f"{current_loc_id} - {scenario_data.get('description_id', 'ubicación misteriosa')}"
        print("Generando descripción de la ubicación...")
        
        try:
            location_desc = generate_location_description(location_context)
            game_state[location_description_key] = location_desc
        except Exception as e:
            print(f"Error generando descripción: {e}")
            # Usar descripción de fallback
            from .ai_connector import LocationDescription
            location_desc = LocationDescription(
                description=f"Te encuentras en {current_loc_id.replace('_', ' ')}. La atmósfera es misteriosa."
            )
            game_state[location_description_key] = location_desc
    else:
        # Usar descripción ya generada
        location_desc = game_state[location_description_key]
    
    # Mostrar descripción detallada (sin ASCII art)
    print(location_desc.description)

    print("\nOptions:")
    options_map = {} # To map the option number to its destination ID
    option_num = 1
    for key, value in scenario_data["options"].items():
        # Here the option ID would be translated into a user-friendly text
        display_text = f"Go to {value.replace('_', ' ').capitalize()}"
        if value == "salir_mazmorra":
            display_text = "¡Attempt to EXIT the dungeon!"
        elif "mirar_alrededor" in value:
            display_text = "Look carefully around."
        elif "examinar_sala" in value:
            display_text = "Examine the room in more detail."
        elif "retroceder" in value:
            display_text = "Go back."

        print(f"{option_num}) {display_text}")
        options_map[str(option_num)] = value
        option_num += 1

    game_state["current_options_map"] = options_map # Save for input validation
    print("="*50)
