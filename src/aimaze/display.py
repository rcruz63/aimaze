# src/aimaze/display.py

def display_scenario(game_state):
    """
    Displays the current location description and available options.
    Here the AI or pre-generated data will fill in the details.
    """
    current_loc_id = game_state["player_location_id"]
    scenario_data = game_state["simulated_dungeon_layout"].get(current_loc_id)

    if not scenario_data:
        print("\nERROR: Unknown location! Something went wrong.")
        game_state["game_over"] = True
        return

    print("\n" + "="*50)
    print(f"[{current_loc_id.replace('_', ' ').upper()}]")
    print("Here the AI will generate/display the ASCII art for the location.")
    print("Here the AI will generate/display the detailed description of the location")
    # Placeholder example for the description
    description_placeholders = {
        "inicio_desc": "You are at the dusty entrance of the dungeon. A cold breeze embraces you.",
        "pasillo_desc": "A winding, damp corridor stretches before you. Water drips resonate.",
        "sala_desc": "A room with strange runes carved into the walls. A faint glow emanates from the center.",
        "final_desc": "Before you stands a large door, it seems to be the exit. The light outside is a beacon of hope."
    }
    print(description_placeholders.get(scenario_data["description_id"], "Description by the AI."))

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
