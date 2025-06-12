# src/aimaze/dungeon.py

def get_simulated_dungeon_layout():
    """
    Returns a basic, linear simulated dungeon layout for the skeleton.
    This will be replaced by AI-generated dungeon logic later.
    """
    return {
        "inicio": {
            "description_id": "inicio_desc",
            "options": {
                "1": "pasillo_oscuro",
                "2": "mirar_alrededor_inicio" # Option that does not advance, just simulates an action
            }
        },
        "pasillo_oscuro": {
            "description_id": "pasillo_desc",
            "options": {
                "1": "sala_misteriosa",
                "2": "retroceder_al_inicio" # Option to go back
            }
        },
        "sala_misteriosa": {
            "description_id": "sala_desc",
            "options": {
                "1": "puerta_final",
                "2": "examinar_sala" # Another option that does not advance
            }
        },
        "puerta_final": {
            "description_id": "final_desc",
            "options": {
                "1": "salir_mazmorra", # This will lead to victory
                "2": "volver_sala_anterior"
            }
        }
    }
