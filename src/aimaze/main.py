# src/aimaze/main.py

from aimaze.game_state import initialize_game_state
from aimaze.display import display_scenario
from aimaze.input import get_player_input
from aimaze.actions import process_player_action
from . import dungeon # Importamos dungeon aunque solo lo use game_state directamente por ahora

def game_loop():
    """
    Main game loop. Orchestrates calls to other modules.
    """
    game_state_data = initialize_game_state()

    print("\n--- ¡COMIENZA LA AVENTURA! ---")

    while not game_state_data["game_over"]:
        display_scenario(game_state_data)
        player_choice = get_player_input(game_state_data)
        game_state_data = process_player_action(game_state_data, player_choice)

    print("\n--- FIN DEL JUEGO ---")
    if game_state_data["objective_achieved"]:
        print("¡Tu aventura ha terminado con éxito!")
    else:
        print("La aventura ha terminado. (Por ahora, esto solo ocurre al salir con éxito).")
        print("Aquí se mostrarían mensajes de derrota si el juego terminara por otras causas.")

# Entry point of the game
if __name__ == "__main__":
    game_loop()
