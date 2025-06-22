# src/aimaze/actions.py

def process_player_action(game_state, raw_input):
    """
    Processes the player's action using the new coordinate-based system.
    """
    valid_options = game_state.get("current_options_map", {})
    player_location = game_state["player_location"]
    dungeon = game_state["dungeon"]
    current_level = dungeon.levels[player_location.level]

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
            else:
                # Movimiento a una nueva habitación
                direction = action_type
                new_x, new_y = target_coords
                
                # Validar que las coordenadas están dentro de los límites
                if 0 <= new_x < current_level.width and 0 <= new_y < current_level.height:
                    # Actualizar la ubicación del jugador
                    player_location.x = new_x
                    player_location.y = new_y
                    
                    # Traducir dirección a texto
                    direction_text = {
                        'north': 'Norte',
                        'south': 'Sur', 
                        'east': 'Este',
                        'west': 'Oeste'
                    }.get(direction, direction)
                    
                    print(f"\nTe mueves hacia el {direction_text}.")
                    print(f"Ahora estás en la posición ({new_x}, {new_y}).")
                    
                    # Verificar si llegamos a la salida del nivel
                    if (new_x, new_y) == current_level.exit_coords:
                        print("¡Has encontrado la salida del nivel!")
                    
                    # Aquí se podría generar un evento aleatorio
                    print("Aquí la IA podría generar un evento aleatorio para la nueva ubicación.")
                    print("Aquí se verificarían las características del jugador y tiradas de dados para posibles eventos/trampas.")
                    print("Aquí se actualizaría el estado del jugador (consumo de recursos, daño, etc.).")
                else:
                    print(f"\nError: Coordenadas ({new_x}, {new_y}) fuera de los límites del nivel.")
        else:
            print(f"\nAcción no reconocida: {chosen_action}")
    else:
        print("Opción inválida. Por favor ingresa el número de una de las opciones disponibles.")

    # Verificar condiciones de fin de juego
    if game_state["objective_achieved"]:
        game_state["game_over"] = True

    return game_state
