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


def generate_main_path(start: tuple, end: tuple, width: int, height: int) -> list:
    """
    Genera un camino principal desde start hasta end usando un algoritmo simple.
    
    Args:
        start: Coordenadas de inicio (x, y)
        end: Coordenadas de fin (x, y)
        width: Ancho del nivel
        height: Alto del nivel
        
    Returns:
        Lista de coordenadas que forman el camino principal
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


def add_extra_rooms_and_connect(path_rooms: list, width: int, height: int) -> dict:
    """
    Añade habitaciones adicionales y las conecta al camino principal.
    
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
        room_id = f"room_{i+1}"
        connections = {}
        
        # Conectar con habitaciones adyacentes del camino
        if i > 0:  # Conectar con la anterior
            prev_coords = path_rooms[i-1]
            if prev_coords[0] < coords[0]:
                connections['west'] = prev_coords
            elif prev_coords[0] > coords[0]:
                connections['east'] = prev_coords
            elif prev_coords[1] < coords[1]:
                connections['north'] = prev_coords
            elif prev_coords[1] > coords[1]:
                connections['south'] = prev_coords
        
        if i < len(path_rooms) - 1:  # Conectar con la siguiente
            next_coords = path_rooms[i+1]
            if next_coords[0] > coords[0]:
                connections['east'] = next_coords
            elif next_coords[0] < coords[0]:
                connections['west'] = next_coords
            elif next_coords[1] > coords[1]:
                connections['south'] = next_coords
            elif next_coords[1] < coords[1]:
                connections['north'] = next_coords
        
        rooms[f"{coords[0]},{coords[1]}"] = Room(
            id=room_id,
            coordinates=coords,
            connections=connections
        )
    
    # Añadir habitaciones adicionales (80-100% del total de coordenadas posibles)
    total_possible = width * height
    target_rooms = random.randint(int(total_possible * 0.8), total_possible)
    current_rooms = len(rooms)
    
    # Generar coordenadas adicionales
    all_coords = [(x, y) for x in range(width) for y in range(height)]
    available_coords = [coord for coord in all_coords if coord not in path_rooms]
    
    # Añadir habitaciones adicionales hasta alcanzar el objetivo
    extra_rooms_needed = min(target_rooms - current_rooms, len(available_coords))
    extra_coords = random.sample(available_coords, extra_rooms_needed)
    
    for i, coords in enumerate(extra_coords):
        room_id = f"extra_room_{i+1}"
        connections = {}
        
        # Conectar con habitaciones adyacentes existentes
        x, y = coords
        adjacent_coords = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1)
        ]
        
        for adj_x, adj_y in adjacent_coords:
            if (0 <= adj_x < width and 0 <= adj_y < height and 
                f"{adj_x},{adj_y}" in rooms):
                # Determinar dirección
                if adj_x > x:
                    connections['east'] = (adj_x, adj_y)
                elif adj_x < x:
                    connections['west'] = (adj_x, adj_y)
                elif adj_y > y:
                    connections['south'] = (adj_x, adj_y)
                elif adj_y < y:
                    connections['north'] = (adj_x, adj_y)
        
        # Si no tiene conexiones, conectar con la habitación más cercana del camino
        if not connections and path_rooms:
            closest = min(path_rooms, key=lambda p: abs(p[0]-x) + abs(p[1]-y))
            if closest[0] > x:
                connections['east'] = closest
            elif closest[0] < x:
                connections['west'] = closest
            elif closest[1] > y:
                connections['south'] = closest
            elif closest[1] < y:
                connections['north'] = closest
        
        rooms[f"{coords[0]},{coords[1]}"] = Room(
            id=room_id,
            coordinates=coords,
            connections=connections
        )
    
    return rooms


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
    
    # Puntos fijos: entrada en (0,0), salida en esquina opuesta
    start_coords = (0, 0)
    exit_coords = (width - 1, height - 1)
    
    print(f"Generando mazmorra determinista: {width}x{height}")
    print(f"Entrada: {start_coords}, Salida: {exit_coords}")
    
    # Generar camino principal
    path_rooms = generate_main_path(start_coords, exit_coords, width, height)
    print(f"Camino principal: {len(path_rooms)} habitaciones")
    
    # Añadir habitaciones adicionales y conectarlas
    all_rooms = add_extra_rooms_and_connect(path_rooms, width, height)
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
