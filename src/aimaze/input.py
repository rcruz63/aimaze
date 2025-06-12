# src/aimaze/input.py

def get_player_input(game_state):
    """
    Gets player input (option number, free text).
    """
    # Here the blinking prompt would visually appear
    choice = input("\n> What do you want to do? (Enter the number): ").strip()
    return choice
