# src/aimaze/game_state.py

from aimaze.dungeon import get_simulated_dungeon_layout
from aimaze.config import load_config


def initialize_game_state():
    """
    Initializes the global game state and player data.
    This is where the AI would start preparing the environment.
    """
    print("--- INICIALIZANDO JUEGO ---")
    load_config()

    game_state = {
        "player_location_id": "inicio",  # ID of the player's current location
        "game_over": False,
        "objective_achieved": False,
        "player_attributes": {},         # Placeholder for player attributes (strength, dexterity, etc.)
        "inventory": []                  # Placeholder for player inventory
    }

    print("Here the AI will be asked to: ")
    print("  - Generate the initial dungeon and its characteristics (rooms, corridors).")
    print("  - Populate the dungeon with events, monsters, traps, treasures, puzzles.")
    print("  - Define the main objective of the game for this specific run.")
    print("  - Store the dungeon structure and its elements in 'game_state'.")

    # --- BASIC DUNGEON SIMULATION FOR THE SKELETON ---
    # This simulates a linear dungeon so the skeleton is executable.
    # Later, this will be generated and managed by the AI.
    game_state["simulated_dungeon_layout"] = get_simulated_dungeon_layout()
    # End of simulation. The real AI would replace this.
    # --- END SIMULATION ---

    return game_state
