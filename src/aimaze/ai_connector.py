import os
import random
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field
from langfuse.langchain import CallbackHandler
from aimaze.dungeon import Dungeon, Level, Room


class LocationDescription(BaseModel):
    """Modelo para la descripción de una ubicación generada por IA"""
    description: str = Field(
        description="Detailed textual description of the location, describing the environment and any general atmospheric elements. DO NOT include ASCII art or specific event details in this description."
    )


def generate_location_description(location_context: str) -> LocationDescription:
    """
    Genera una descripción detallada textual para una ubicación específica.
    
    Args:
        location_context: Contexto de la ubicación (ID, estado del juego, etc.)
        
    Returns:
        LocationDescription: Objeto con descripción textual detallada
    """
    # Configurar el modelo de IA
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Configurar el parser de salida
    parser = PydanticOutputParser(pydantic_object=LocationDescription)
    fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm)
    
    # Configurar Langfuse callback para monitoreo
    langfuse_handler = None
    try:
        if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
            langfuse_handler = CallbackHandler()
    except Exception as e:
        print(f"Warning: No se pudo configurar Langfuse: {e}")
    
    # Crear el prompt
    prompt_template = PromptTemplate(
        template="""Eres un maestro de mazmorras experto en crear descripciones inmersivas para ubicaciones.

Contexto de la ubicación: {location_context}

Tu tarea es generar una descripción detallada y atmosférica de esta ubicación de mazmorra.

REQUISITOS IMPORTANTES:
- Genera SOLO una descripción textual detallada
- NO incluyas ASCII art en la descripción
- NO incluyas detalles específicos de eventos, monstruos o trampas
- Enfócate en el ambiente general, la atmósfera y elementos visuales permanentes
- La descripción debe ser apropiada para una mazmorra misteriosa, centrate en el terror y el humor.
- Describe el entorno, la iluminación, los sonidos ambiente, olores, o sensaciones generales.
- Utiliza 3 frases como máximo.

{format_instructions}""",
        input_variables=["location_context"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Ejecutar la cadena
    callbacks = [langfuse_handler] if langfuse_handler else []
    
    try:
        # Formatear el prompt
        formatted_prompt = prompt_template.format(location_context=location_context)
        
        # Generar respuesta (sin callbacks para evitar conflictos)
        if callbacks:
            # Usar configuración para callbacks
            config = {"callbacks": callbacks}
            response = llm.invoke(formatted_prompt, config=config)
        else:
            response = llm.invoke(formatted_prompt)
        
        # Parsear la respuesta
        result = fixing_parser.parse(response.content)
        
        return result
        
    except Exception as e:
        print(f"Error generando descripción de ubicación: {e}")
        # Fallback en caso de error
        return LocationDescription(
            description=f"Te encuentras en {location_context}. La atmósfera es misteriosa, con piedras húmedas y ecos lejanos que resuenan en la oscuridad."
        )


def generate_random_start_exit_points(width: int, height: int) -> tuple:
    """
    Genera puntos de inicio y salida aleatorios para la mazmorra.
    
    Args:
        width: Ancho del nivel
        height: Alto del nivel
        
    Returns:
        tuple: (start_coords, exit_coords) donde ambos son tuplas (x, y)
    """
    # Generar punto de inicio aleatorio
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    start_coords = (start_x, start_y)
    
    # Generar punto de salida aleatorio, asegurándonos de que no coincida con el inicio
    exit_coords = start_coords  # Inicializar para entrar al bucle
    
    while exit_coords == start_coords:
        exit_x = random.randint(0, width - 1)
        exit_y = random.randint(0, height - 1)
        exit_coords = (exit_x, exit_y)
    
    return start_coords, exit_coords


def generate_advanced_main_path(start: tuple, end: tuple, width: int, height: int, target_length: int) -> list:
    """
    Genera un camino principal de longitud específica desde start hasta end.
    
    Args:
        start: Coordenadas de inicio (x, y)
        end: Coordenadas de fin (x, y)
        width: Ancho del nivel
        height: Alto del nivel
        target_length: Longitud objetivo del camino (número de habitaciones)
        
    Returns:
        Lista de coordenadas que forman el camino principal
    """
    def get_neighbors(pos):
        """Obtiene las coordenadas vecinas válidas (sin movimientos oblicuos)"""
        x, y = pos
        neighbors = []
        # Norte, Sur, Este, Oeste (sin oblicuas)
        for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
        return neighbors
    
    def dfs_find_paths(current_path, current_pos, target_pos, max_paths=50):
        """
        DFS para encontrar caminos desde current_pos hasta target_pos.
        Limita el número de caminos para eficiencia.
        """
        if len(paths_found) >= max_paths:
            return
            
        if current_pos == target_pos:
            paths_found.append(current_path[:])
            return
        
        # Evitar caminos excesivamente largos
        if len(current_path) > target_length + 5:
            return
            
        neighbors = get_neighbors(current_pos)
        random.shuffle(neighbors)  # Aleatorizar para diversidad
        
        for next_pos in neighbors:
            if next_pos not in current_path:  # Evitar repeticiones
                current_path.append(next_pos)
                dfs_find_paths(current_path, next_pos, target_pos, max_paths)
                current_path.pop()
    
    # Buscar múltiples caminos posibles
    paths_found = []
    initial_path = [start]
    dfs_find_paths(initial_path, start, end)
    
    if not paths_found:
        # Fallback: usar camino directo simple si no se encuentra ninguno
        print(f"Warning: No se encontraron caminos, usando camino directo")
        return generate_simple_direct_path(start, end)
    
    # Filtrar caminos por longitud objetivo
    target_paths = [path for path in paths_found if len(path) == target_length]
    
    if target_paths:
        # Si encontramos caminos de la longitud objetivo, elegir uno aleatoriamente
        selected_path = random.choice(target_paths)
        print(f"Camino seleccionado: longitud {len(selected_path)}/{target_length} (objetivo)")
    else:
        # Fallback: usar el camino más largo disponible cerca del objetivo
        paths_found.sort(key=len, reverse=True)
        selected_path = paths_found[0]
        print(f"Fallback: camino más largo encontrado: longitud {len(selected_path)}/{target_length} (objetivo)")
    
    return selected_path


def generate_simple_direct_path(start: tuple, end: tuple) -> list:
    """
    Genera un camino directo simple desde start hasta end.
    Usado como fallback cuando no se encuentran otros caminos.
    """
    path = [start]
    current_x, current_y = start
    
    # Primero moverse horizontalmente hacia el objetivo
    while current_x != end[0]:
        if current_x < end[0]:
            current_x += 1
        else:
            current_x -= 1
        path.append((current_x, current_y))
    
    # Luego moverse verticalmente hacia el objetivo
    while current_y != end[1]:
        if current_y < end[1]:
            current_y += 1
        else:
            current_y -= 1
        path.append((current_x, current_y))
    
    return path


def add_connected_additional_rooms(path_rooms: list, width: int, height: int) -> dict:
    """
    Añade habitaciones adicionales garantizando conectividad al camino principal.
    Evita crear secciones aisladas.
    
    Args:
        path_rooms: Lista de coordenadas del camino principal
        width: Ancho del nivel
        height: Alto del nivel
        
    Returns:
        Diccionario de habitaciones con sus conexiones
    """
    rooms = {}
    
    # Crear habitaciones del camino principal
    for i, coords in enumerate(path_rooms):
        room_id = f"main_path_{i+1}"
        connections = {}
        
        # Conectar con habitaciones adyacentes del camino principal
        if i > 0:  # Conectar con la anterior
            prev_coords = path_rooms[i-1]
            direction = get_direction(coords, prev_coords)
            if direction:
                connections[direction] = prev_coords
        
        if i < len(path_rooms) - 1:  # Conectar with la siguiente
            next_coords = path_rooms[i+1]
            direction = get_direction(coords, next_coords)
            if direction:
                connections[direction] = next_coords
        
        rooms[f"{coords[0]},{coords[1]}"] = Room(
            id=room_id,
            coordinates=coords,
            connections=connections
        )
    
    # Identificar celdas disponibles para habitaciones adicionales
    all_coords = [(x, y) for x in range(width) for y in range(height)]
    available_coords = [coord for coord in all_coords if coord not in path_rooms]
    
    print(f"Habitaciones disponibles para añadir: {len(available_coords)}")
    
    if not available_coords:
        print("No hay celdas disponibles para habitaciones adicionales")
        return rooms
    
    # Añadir habitaciones adicionales de forma progresiva garantizando conectividad
    connected_coords = set(path_rooms)  # Coordenadas ya conectadas al grafo principal
    added_rooms = 0
    
    # Usar un enfoque iterativo para añadir habitaciones conectadas
    max_iterations = len(available_coords)
    for iteration in range(max_iterations):
        added_in_iteration = False
        
        # Buscar coordenadas disponibles que tengan al menos un vecino conectado
        for coords in available_coords[:]:  # Copia de la lista para poder modificarla
            if coords in connected_coords:
                continue
                
            # Verificar si tiene vecinos ya conectados
            neighbors = get_adjacent_coordinates(coords, width, height)
            connected_neighbors = [n for n in neighbors if n in connected_coords]
            
            if connected_neighbors:
                # Añadir esta habitación
                room_id = f"additional_{added_rooms + 1}"
                connections = {}
                
                # Conectar con vecinos ya conectados (máximo 2 conexiones para evitar complejidad)
                selected_neighbors = connected_neighbors[:2]
                for neighbor in selected_neighbors:
                    direction = get_direction(coords, neighbor)
                    if direction:
                        connections[direction] = neighbor
                        
                        # También añadir la conexión bidireccional
                        neighbor_key = f"{neighbor[0]},{neighbor[1]}" 
                        if neighbor_key in rooms:
                            reverse_direction = get_direction(neighbor, coords)
                            if reverse_direction:
                                rooms[neighbor_key].connections[reverse_direction] = coords
                
                rooms[f"{coords[0]},{coords[1]}"] = Room(
                    id=room_id,
                    coordinates=coords,
                    connections=connections
                )
                
                # Marcar como conectada y remover de disponibles
                connected_coords.add(coords)
                available_coords.remove(coords)
                added_rooms += 1
                added_in_iteration = True
        
        # Si no se añadió ninguna habitación en esta iteración, terminar
        if not added_in_iteration:
            break
    
    print(f"Habitaciones adicionales añadidas: {added_rooms}")
    print(f"Total habitaciones en la mazmorra: {len(rooms)}")
    
    return rooms


def get_direction(from_coord: tuple, to_coord: tuple) -> str:
    """
    Calcula la dirección desde from_coord hacia to_coord.
    
    Args:
        from_coord: Coordenada origen (x, y)
        to_coord: Coordenada destino (x, y)
        
    Returns:
        str: Dirección ('north', 'south', 'east', 'west') o '' si no son adyacentes
    """
    dx = to_coord[0] - from_coord[0]
    dy = to_coord[1] - from_coord[1]
    
    # Solo permitir movimientos adyacentes (no oblicuos)
    if abs(dx) + abs(dy) != 1:
        return ''
    
    if dx == 1:
        return 'east'
    elif dx == -1:
        return 'west'
    elif dy == 1:
        return 'south'
    elif dy == -1:
        return 'north'
    else:
        return ''


def get_adjacent_coordinates(coord: tuple, width: int, height: int) -> list:
    """
    Obtiene las coordenadas adyacentes válidas (sin movimientos oblicuos).
    
    Args:
        coord: Coordenada central (x, y)
        width: Ancho del nivel
        height: Alto del nivel
        
    Returns:
        list: Lista de coordenadas adyacentes válidas
    """
    x, y = coord
    adjacent = []
    
    # Norte, Sur, Este, Oeste (sin oblicuas)
    for dx, dy in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            adjacent.append((nx, ny))
    
    return adjacent


def create_dungeon_from_rooms(rooms: dict, width: int, height: int, 
                             start_coords: tuple, exit_coords: tuple) -> Dungeon:
    """
    Crea un objeto Dungeon a partir de las habitaciones generadas.
    
    Args:
        rooms: Diccionario de habitaciones
        width: Ancho del nivel
        height: Alto del nivel
        start_coords: Coordenadas de inicio
        exit_coords: Coordenadas de salida
        
    Returns:
        Objeto Dungeon completo
    """
    level_1 = Level(
        id=1,
        width=width,
        height=height,
        start_coords=start_coords,
        exit_coords=exit_coords,
        rooms=rooms
    )
    
    dungeon = Dungeon(
        total_levels=1,
        current_level=1,
        levels={1: level_1}
    )
    
    return dungeon


def calculate_minimum_distance(start: tuple, end: tuple) -> int:
    """
    Calcula la distancia mínima (Manhattan) entre dos puntos.
    Representa el camino más directo posible.
    
    Args:
        start: Coordenadas de inicio (x, y)
        end: Coordenadas de fin (x, y)
        
    Returns:
        int: Número mínimo de habitaciones en el camino más directo
    """
    manhattan_distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return manhattan_distance + 1  # +1 porque incluimos la habitación de inicio


def calculate_smart_path_length(start: tuple, end: tuple, width: int, height: int) -> int:
    """
    Calcula una longitud de camino inteligente usando distribución normalizada.
    
    Rango: [distancia_mínima, total_celdas]
    Distribución: Favorece valores intermedios, extremos menos probables
    
    Args:
        start: Coordenadas de inicio
        end: Coordenadas de fin
        width: Ancho del nivel
        height: Alto del nivel
        
    Returns:
        int: Longitud objetivo del camino
    """
    import numpy as np
    
    # Calcular límites
    min_length = calculate_minimum_distance(start, end)
    max_length = width * height
    
    # Si el mínimo es igual al máximo (matriz muy pequeña), usar el mínimo
    if min_length >= max_length:
        return min_length
    
    # Usar distribución beta para favorece valores intermedios
    # Beta(2, 2) da una distribución en forma de campana centrada en 0.5
    beta_sample = np.random.beta(2, 2)
    
    # Mapear el valor beta [0,1] al rango [min_length, max_length]
    target_length = int(min_length + beta_sample * (max_length - min_length))
    
    # Asegurar límites
    target_length = max(min_length, min(target_length, max_length))
    
    return target_length


def generate_dungeon_layout() -> Dungeon:
    """
    Genera el layout de una mazmorra usando enfoque determinista.
    Inicialmente genera UN SOLO NIVEL pequeño con estructura garantizada.
    
    Returns:
        Dungeon: Objeto con la estructura completa de la mazmorra
    """
    # Parámetros aleatorios controlados
    width = random.randint(3, 5)
    height = random.randint(3, 5)
    
    # Puntos fijos: generar inicio y salida aleatorios (no pueden coincidir)
    start_coords, exit_coords = generate_random_start_exit_points(width, height)
    
    # Calcular longitud objetivo del camino usando distribución inteligente
    total_cells = width * height
    min_distance = calculate_minimum_distance(start_coords, exit_coords)
    target_path_length = calculate_smart_path_length(start_coords, exit_coords, width, height)
    
    print(f"Generando mazmorra determinista: {width}x{height} ({total_cells} celdas totales)")
    print(f"Entrada: {start_coords}, Salida: {exit_coords}")
    print(f"Distancia mínima: {min_distance}, Máximo posible: {total_cells}")
    print(f"Longitud objetivo del camino: {target_path_length} habitaciones ({target_path_length/total_cells*100:.1f}%)")
    
    # Generar camino principal con longitud objetivo
    path_rooms = generate_advanced_main_path(start_coords, exit_coords, width, height, target_path_length)
    print(f"Camino principal generado: {len(path_rooms)} habitaciones")
    
    # Añadir habitaciones adicionales conectadas (evita secciones aisladas)
    all_rooms = add_connected_additional_rooms(path_rooms, width, height)
    print(f"Total habitaciones: {len(all_rooms)}")
    
    # Crear y retornar la mazmorra
    dungeon = create_dungeon_from_rooms(all_rooms, width, height, start_coords, exit_coords)
    
    return dungeon


def _create_fallback_dungeon() -> Dungeon:
    """
    Crea una mazmorra simple hardcodeada como fallback en caso de error.
    """
    # Crear habitaciones
    rooms = {}
    
    # Habitación inicial (0,0)
    rooms['0,0'] = Room(
        id="start_room",
        coordinates=(0, 0),
        connections={'east': (1, 0)}
    )
    
    # Habitación central (1,0)
    rooms['1,0'] = Room(
        id="middle_room",
        coordinates=(1, 0),
        connections={'west': (0, 0), 'east': (2, 0)}
    )
    
    # Habitación final (2,0)
    rooms['2,0'] = Room(
        id="exit_room",
        coordinates=(2, 0),
        connections={'west': (1, 0)}
    )
    
    # Crear nivel
    level_1 = Level(
        id=1,
        width=3,
        height=1,
        start_coords=(0, 0),
        exit_coords=(2, 0),
        rooms=rooms
    )
    
    # Crear mazmorra
    dungeon = Dungeon(
        total_levels=1,
        current_level=1,
        levels={1: level_1}
    )
    
    return dungeon


if __name__ == "__main__":
    # Prueba de la función
    print("=== PRUEBA DE GENERACIÓN DE UBICACIÓN ===")
    
    # Cargar configuración
    from aimaze.config import load_config
    load_config()
    
    # Generar descripción de prueba
    test_context = "inicio - entrada de la mazmorra"
    try:
        location = generate_location_description(test_context)
        print("\nDESCRIPCIÓN GENERADA:")
        print(location.description)
    except Exception as e:
        print(f"Error en la prueba: {e}")
    
    print("\n=== PRUEBA DE GENERACIÓN DE MAZMORRA DETERMINISTA ===")
    try:
        dungeon = generate_dungeon_layout()
        print("\nMAZMORRA GENERADA:")
        print(f"Niveles totales: {dungeon.total_levels}")
        print(f"Nivel actual: {dungeon.current_level}")
        
        for level_id, level in dungeon.levels.items():
            print(f"\nNivel {level_id}:")
            print(f"  Dimensiones: {level.width}x{level.height}")
            print(f"  Inicio: {level.start_coords}")
            print(f"  Salida: {level.exit_coords}")
            print(f"  Habitaciones: {len(level.rooms)}")
            
            for room_key, room in level.rooms.items():
                print(f"    {room_key}: {room.id} -> {room.connections}")
                
    except Exception as e:
        print(f"Error en la prueba de mazmorra: {e}")
