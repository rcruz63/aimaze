"""Fachada de funciones de IA y generación.

Este módulo re-exporta funciones desde submódulos especializados para mantener
una interfaz estable y un tamaño manejable.
"""

from aimaze.ai.descriptions import (
    LocationDescription as LocationDescription,
    generate_location_description as _generate_location_description,
)
from aimaze.events_generator import (
    generate_random_event as _generate_random_event,
)
from aimaze.generation.dungeon_generator import (
    generate_random_start_exit_points as _gen_start_exit,
    generate_advanced_main_path as _gen_main_path,
    generate_simple_direct_path as _gen_simple_path,
    add_connected_additional_rooms as _gen_add_rooms,
    get_direction as _gen_direction,
    get_adjacent_coordinates as _gen_adjacent,
    create_dungeon_from_rooms as _gen_create_dungeon,
    calculate_minimum_distance as _gen_min_dist,
    calculate_smart_path_length as _gen_smart_len,
    generate_dungeon_layout as _gen_dungeon_layout,
)


def generate_location_description(location_context: str) -> LocationDescription:
    return _generate_location_description(location_context)


def generate_random_event(location_context: str):
    return _generate_random_event(location_context)


def generate_random_start_exit_points(width: int, height: int):
    return _gen_start_exit(width, height)


def generate_advanced_main_path(start: tuple, end: tuple, width: int, height: int, target_length: int):
    return _gen_main_path(start, end, width, height, target_length)


def generate_simple_direct_path(start: tuple, end: tuple):
    return _gen_simple_path(start, end)


def add_connected_additional_rooms(path_rooms: list, width: int, height: int):
    return _gen_add_rooms(path_rooms, width, height)


def get_direction(from_coord: tuple, to_coord: tuple) -> str:
    return _gen_direction(from_coord, to_coord)


def get_adjacent_coordinates(coord: tuple, width: int, height: int) -> list:
    return _gen_adjacent(coord, width, height)


def create_dungeon_from_rooms(rooms: dict, width: int, height: int, start_coords: tuple, exit_coords: tuple):
    return _gen_create_dungeon(rooms, width, height, start_coords, exit_coords)


def calculate_minimum_distance(start: tuple, end: tuple) -> int:
    return _gen_min_dist(start, end)


def calculate_smart_path_length(start: tuple, end: tuple, width: int, height: int) -> int:
    return _gen_smart_len(start, end, width, height)


def generate_dungeon_layout():
    return _gen_dungeon_layout()


if __name__ == "__main__":
    # Prueba rápida de fachada
    from aimaze.config import load_config

    load_config()

    print("=== PRUEBA DE GENERACIÓN DE UBICACIÓN ===")
    location = generate_location_description("inicio - entrada de la mazmorra")
    print(location.description)

    print("\n=== PRUEBA DE GENERACIÓN DE MAZMORRA DETERMINISTA ===")
    dungeon = generate_dungeon_layout()
    print(f"Niveles totales: {dungeon.total_levels}")
    level = dungeon.levels[dungeon.current_level]
    print(f"Dimensiones: {level.width}x{level.height}")
