#

import json
import os
from typing import Dict, Any
from aimaze.player import Player
from aimaze.dungeon import Dungeon, PlayerLocation


def save_game(game_state: Dict[str, Any], filename: str = 'savegame.json') -> None:
    """
    Saves the current game state to a JSON file.

    Args:
        game_state: The current game state dictionary
        filename: Name of the file to save to (default: 'savegame.json')
    """
    # Preparar el estado para serialización
    serializable_state = {}

    for key, value in game_state.items():
        if hasattr(value, 'model_dump'):
            # Es un modelo Pydantic, convertir a dict
            serializable_state[key] = value.model_dump()
        elif key.startswith('location_description_'):
            # Descripción de ubicación, también puede ser un modelo Pydantic
            if hasattr(value, 'model_dump'):
                serializable_state[key] = value.model_dump()
            else:
                serializable_state[key] = value
        else:
            # Tipos básicos (str, int, bool, dict, list)
            serializable_state[key] = value

    # Guardar en archivo JSON
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_state, f, indent=2, ensure_ascii=False)
        print(f"Partida guardada en {filename}")
    except Exception as e:
        raise Exception(f"Error al guardar partida: {e}")


def load_game(filename: str = 'savegame.json') -> Dict[str, Any]:
    """
    Loads game state from a JSON file.

    Args:
        filename: Name of the file to load from (default: 'savegame.json')

    Returns:
        Dict containing the loaded game state

    Raises:
        FileNotFoundError: If the save file doesn't exist
        Exception: If there's an error loading or parsing the file
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No se encontró el archivo de guardado: {filename}")

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            raw_state = json.load(f)

        # Reconstruir objetos Pydantic desde los dicts
        game_state = {}

        for key, value in raw_state.items():
            if key == 'player' and isinstance(value, dict):
                # Reconstruir Player
                game_state[key] = Player(**value)
            elif key == 'player_location' and isinstance(value, dict):
                # Reconstruir PlayerLocation
                game_state[key] = PlayerLocation(**value)
            elif key == 'dungeon' and isinstance(value, dict):
                # Reconstruir Dungeon
                game_state[key] = Dungeon(**value)
            elif key.startswith('location_description_') and isinstance(value, dict):
                # Reconstruir LocationDescription
                from aimaze.ai_connector import LocationDescription
                game_state[key] = LocationDescription(**value)
            else:
                # Tipos básicos
                game_state[key] = value

        print(f"Partida cargada desde {filename}")
        return game_state

    except json.JSONDecodeError as e:
        raise Exception(f"Error al parsear el archivo de guardado: {e}")
    except Exception as e:
        raise Exception(f"Error al cargar partida: {e}")


def save_exists(filename: str = 'savegame.json') -> bool:
    """
    Check if a save file exists.

    Args:
        filename: Name of the file to check (default: 'savegame.json')

    Returns:
        bool: True if save file exists, False otherwise
    """
    return os.path.exists(filename)


def delete_save(filename: str = 'savegame.json') -> bool:
    """
    Delete a save file.

    Args:
        filename: Name of the file to delete (default: 'savegame.json')

    Returns:
        bool: True if file was deleted successfully, False if file didn't exist

    Raises:
        Exception: If there's an error deleting the file
    """
    if not os.path.exists(filename):
        return False

    try:
        os.remove(filename)
        print(f"Archivo de guardado {filename} eliminado")
        return True
    except Exception as e:
        raise Exception(f"Error al eliminar archivo de guardado: {e}")
