# src/aimaze/game_state.py

from aimaze.dungeon import PlayerLocation, Dungeon
from aimaze.ai_connector import generate_dungeon_layout
from aimaze.config import load_config
from aimaze.player import Player


def initialize_game_state():
    """
    Initializes the global game state and player data.
    This is where the AI would start preparing the environment.
    """
    print("--- INICIALIZANDO JUEGO ---")
    load_config()

    game_state = {
        "player_location": None,  # Will be initialized with PlayerLocation
        "game_over": False,
        "objective_achieved": False,
        "player": Player()               # Initialize Player model
    }

    print("Here the AI will be asked to: ")
    print("  - Generate the initial dungeon and its characteristics (rooms, corridors).")
    print("  - Populate the dungeon with events, monsters, traps, treasures, puzzles.")
    print("  - Define the main objective of the game for this specific run.")
    print("  - Store the dungeon structure and its elements in 'game_state'.")

    # --- GENERATE DUNGEON USING AI ---
    # Generate dungeon layout using AI
    game_state["dungeon"] = generate_dungeon_layout()
    
    # Initialize player location with start coordinates of level 1
    level_1 = game_state["dungeon"].levels[1]
    start_x, start_y = level_1.start_coords
    game_state["player_location"] = PlayerLocation(level=1, x=start_x, y=start_y)
    # --- END AI GENERATION ---

    return game_state


def check_game_over(game_state):
    """
    Checks if the game should end based on current game state.
    Returns True if the player has died (health <= 0) or other game over conditions.
    
    Args:
        game_state: The current game state dictionary
        
    Returns:
        bool: True if game should end, False otherwise
    """
    player = game_state.get("player")
    
    if player and player.health <= 0:
        return True
    
    # Otras condiciones de game over pueden añadirse aquí en el futuro
    # Por ejemplo: tiempo límite, condiciones especiales de la mazmorra, etc.
    
    return False
