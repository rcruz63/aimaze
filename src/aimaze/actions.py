# src/aimaze/actions.py

def process_player_action(game_state, raw_input):
    """
    Processes the player's action. Here the AI or game logic will decide the outcome.
    """
    valid_options = game_state.get("current_options_map", {})
    simulated_dungeon_layout = game_state.get("simulated_dungeon_layout", {})

    if raw_input in valid_options:
        chosen_action_id = valid_options[raw_input]
        print(f"\nYou chose: '{chosen_action_id.replace('_', ' ').capitalize()}'.")

        # --- Location transition logic (placeholder) ---
        if chosen_action_id in simulated_dungeon_layout:
            game_state["player_location_id"] = chosen_action_id
            print(f"Here the AI will register the location change to: {chosen_action_id}.")
            print("Here the AI might generate a random or predefined event for the new location.")
            print("Here player characteristics and dice rolls will be checked for possible events/traps.")
            print("Here player state will be updated (e.g., resource consumption, damage, etc.).")
            
            if chosen_action_id == "salir_mazmorra":
                game_state["objective_achieved"] = True
                print("\nCongratulations! You have found the exit and escaped the dungeon.")
        elif chosen_action_id == "salir_mazmorra": # Case where we are already at the exit and choose to exit
            game_state["objective_achieved"] = True
            print("\nCongratulations! You have found the exit and escaped the dungeon.")
        else:
            # Option that is not a direct location movement, but an action
            print(f"Here the AI will process the action '{chosen_action_id}' and describe the result.")
            print("For now, this action does not change your location.")
            # If it were an action requiring free text:
            # print("Here the user would be asked for text and the AI would process it.")

    else:
        print("Invalid option. Please enter the number of one of the available options.")

    # Here Game Over conditions would be checked (player death, failed objective, etc.)
    # For now, game_over is only activated if the objective is achieved.
    if game_state["objective_achieved"]:
        game_state["game_over"] = True

    return game_state
