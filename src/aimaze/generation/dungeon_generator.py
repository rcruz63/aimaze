import random
from typing import Dict, Tuple, Optional, List

from aimaze.dungeon import Dungeon, Level, Room


def generate_random_start_exit_points(width: int, height: int) -> tuple:
    """Genera puntos de inicio y salida aleatorios para la mazmorra."""
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    start_coords = (start_x, start_y)

    exit_coords = start_coords
    while exit_coords == start_coords:
        exit_x = random.randint(0, width - 1)
        exit_y = random.randint(0, height - 1)
        exit_coords = (exit_x, exit_y)

    return start_coords, exit_coords


def generate_advanced_main_path(start: tuple, end: tuple, width: int, height: int, target_length: int) -> list:
    """Genera un camino principal de longitud específica desde start hasta end."""

    def get_neighbors(pos):
        x, y = pos
        neighbors = []
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
        return neighbors

    def dfs_find_paths(current_path, current_pos, target_pos, max_paths=50):
        if len(paths_found) >= max_paths:
            return
        if current_pos == target_pos:
            paths_found.append(current_path[:])
            return
        if len(current_path) > target_length + 5:
            return
        neighbors = get_neighbors(current_pos)
        random.shuffle(neighbors)
        for next_pos in neighbors:
            if next_pos not in current_path:
                current_path.append(next_pos)
                dfs_find_paths(current_path, next_pos, target_pos, max_paths)
                current_path.pop()

    paths_found = []
    initial_path = [start]
    dfs_find_paths(initial_path, start, end)

    if not paths_found:
        return generate_simple_direct_path(start, end)

    target_paths = [path for path in paths_found if len(path) == target_length]

    if target_paths:
        selected_path = random.choice(target_paths)
    else:
        paths_found.sort(key=len, reverse=True)
        selected_path = paths_found[0]

    return selected_path


def generate_simple_direct_path(start: tuple, end: tuple) -> list:
    """Genera un camino directo simple desde start hasta end."""
    path = [start]
    current_x, current_y = start

    while current_x != end[0]:
        current_x += 1 if current_x < end[0] else -1
        path.append((current_x, current_y))

    while current_y != end[1]:
        current_y += 1 if current_y < end[1] else -1
        path.append((current_x, current_y))

    return path


def add_connected_additional_rooms(path_rooms: list, width: int, height: int) -> dict:
    """Añade habitaciones adicionales garantizando conectividad al camino principal."""
    rooms: Dict[str, Room] = {}

    for i, coords in enumerate(path_rooms):
        room_id = f"main_path_{i + 1}"
        connections: Dict[str, Tuple[int, int]] = {}
        if i > 0:
            prev_coords = path_rooms[i - 1]
            direction = get_direction(coords, prev_coords)
            if direction:
                connections[direction] = prev_coords
        if i < len(path_rooms) - 1:
            next_coords = path_rooms[i + 1]
            direction = get_direction(coords, next_coords)
            if direction:
                connections[direction] = next_coords
        rooms[f"{coords[0]},{coords[1]}"] = Room(
            id=room_id, coordinates=coords, connections=connections
        )

    all_coords = [(x, y) for x in range(width) for y in range(height)]
    available_coords = [coord for coord in all_coords if coord not in path_rooms]

    connected_coords = set(path_rooms)
    added_rooms = 0

    max_iterations = len(available_coords)
    for _ in range(max_iterations):
        added_in_iteration = False
        for coords in available_coords[:]:
            if coords in connected_coords:
                continue
            neighbors = get_adjacent_coordinates(coords, width, height)
            connected_neighbors = [n for n in neighbors if n in connected_coords]
            if connected_neighbors:
                room_id = f"additional_{added_rooms + 1}"
                connections = {}
                selected_neighbors = connected_neighbors[:2]
                for neighbor in selected_neighbors:
                    direction = get_direction(coords, neighbor)
                    if direction:
                        connections[direction] = neighbor
                        neighbor_key = f"{neighbor[0]},{neighbor[1]}"
                        if neighbor_key in rooms:
                            reverse_direction = get_direction(neighbor, coords)
                            if reverse_direction:
                                rooms[neighbor_key].connections[reverse_direction] = coords
                rooms[f"{coords[0]},{coords[1]}"] = Room(
                    id=room_id, coordinates=coords, connections=connections
                )
                connected_coords.add(coords)
                available_coords.remove(coords)
                added_rooms += 1
                added_in_iteration = True
        if not added_in_iteration:
            break

    return rooms


def get_direction(from_coord: tuple, to_coord: tuple) -> str:
    """Calcula la dirección cardinal entre dos coordenadas adyacentes."""
    dx = to_coord[0] - from_coord[0]
    dy = to_coord[1] - from_coord[1]
    if abs(dx) + abs(dy) != 1:
        return ""
    if dx == 1:
        return "east"
    if dx == -1:
        return "west"
    if dy == 1:
        return "south"
    if dy == -1:
        return "north"
    return ""


def get_adjacent_coordinates(coord: tuple, width: int, height: int) -> list:
    """Obtiene las coordenadas adyacentes válidas (sin movimientos oblicuos)."""
    x, y = coord
    adjacent = []
    for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            adjacent.append((nx, ny))
    return adjacent


def create_dungeon_from_rooms(rooms: dict, width: int, height: int, start_coords: tuple, exit_coords: tuple) -> Dungeon:
    """Crea un objeto Dungeon a partir de habitaciones generadas."""
    level_1 = Level(
        id=1,
        width=width,
        height=height,
        start_coords=start_coords,
        exit_coords=exit_coords,
        rooms=rooms,
    )
    dungeon = Dungeon(total_levels=1, current_level=1, levels={1: level_1})
    return dungeon


def calculate_minimum_distance(start: tuple, end: tuple) -> int:
    """Distancia de Manhattan + 1 (incluye la sala inicial)."""
    manhattan_distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return manhattan_distance + 1


def calculate_smart_path_length(start: tuple, end: tuple, width: int, height: int) -> int:
    """Longitud objetivo usando distribución Beta(2,2) para favorecer valores intermedios."""
    min_length = calculate_minimum_distance(start, end)
    max_length = width * height
    if min_length >= max_length:
        return min_length
    beta_sample = random.betavariate(2, 2)
    target_length = int(min_length + beta_sample * (max_length - min_length))
    target_length = max(min_length, min(target_length, max_length))
    return target_length


def generate_dungeon_layout() -> Dungeon:
    """Genera un layout de mazmorra determinista con un solo nivel pequeño."""
    width = random.randint(3, 5)
    height = random.randint(3, 5)
    start_coords, exit_coords = generate_random_start_exit_points(width, height)
    target_path_length = calculate_smart_path_length(start_coords, exit_coords, width, height)
    path_rooms = generate_advanced_main_path(start_coords, exit_coords, width, height, target_path_length)
    all_rooms = add_connected_additional_rooms(path_rooms, width, height)
    dungeon = create_dungeon_from_rooms(all_rooms, width, height, start_coords, exit_coords)
    return dungeon


def _create_fallback_dungeon() -> Dungeon:
    rooms = {}
    rooms['0,0'] = Room(id="start_room", coordinates=(0, 0), connections={'east': (1, 0)})
    rooms['1,0'] = Room(id="middle_room", coordinates=(1, 0), connections={'west': (0, 0), 'east': (2, 0)})
    rooms['2,0'] = Room(id="exit_room", coordinates=(2, 0), connections={'west': (1, 0)})
    level_1 = Level(id=1, width=3, height=1, start_coords=(0, 0), exit_coords=(2, 0), rooms=rooms)
    dungeon = Dungeon(total_levels=1, current_level=1, levels={1: level_1})
    return dungeon