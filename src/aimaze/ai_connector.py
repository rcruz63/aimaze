import os
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


def generate_dungeon_layout() -> Dungeon:
    """
    Genera el layout de una mazmorra usando IA con la nueva arquitectura de coordenadas.
    Inicialmente genera UN SOLO NIVEL pequeño (3x3 o 4x3).
    
    Returns:
        Dungeon: Objeto con la estructura completa de la mazmorra
    """
    # Configurar el modelo de IA
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Configurar el parser de salida
    parser = PydanticOutputParser(pydantic_object=Dungeon)
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
        template="""Eres un maestro de mazmorras experto en diseñar layouts de mazmorras.

Tu tarea es generar una pequeña mazmorra de UN SOLO NIVEL usando coordenadas específicas.

ESPECIFICACIONES REQUERIDAS:
- Crear un único nivel (id: 1) con dimensiones pequeñas (3x3 o 4x3)
- Definir claramente start_coords y exit_coords para el nivel
- Cada habitación debe tener coordenadas válidas dentro de los límites del nivel
- Las connections de cada habitación deben referenciar coordenadas válidas de habitaciones adyacentes
- Usar direcciones cardinales: 'north', 'south', 'east', 'west'
- Asegurar que hay un camino válido desde start_coords hasta exit_coords
- Los rooms deben usar la clave 'x,y' (ejemplo: '0,0', '1,2')

EJEMPLO DE ESTRUCTURA:
- Level 1: width=3, height=3, start_coords=(0,0), exit_coords=(2,2)
- Room en (0,0): connections={'east': (1,0), 'south': (0,1)}
- Room en (1,0): connections={'west': (0,0), 'east': (2,0)}
- ... y así sucesivamente

IMPORTANTE:
- Todas las coordenadas deben estar dentro de los límites (0 <= x < width, 0 <= y < height)
- Solo conectar habitaciones adyacentes (no conexiones en diagonal)
- Crear un layout interesante pero simple para el MVP

{format_instructions}""",
        input_variables=[],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Ejecutar la cadena
    callbacks = [langfuse_handler] if langfuse_handler else []
    
    try:
        # Formatear el prompt
        formatted_prompt = prompt_template.format()
        
        # Generar respuesta
        if callbacks:
            config = {"callbacks": callbacks}
            response = llm.invoke(formatted_prompt, config=config)
        else:
            response = llm.invoke(formatted_prompt)
        
        # Parsear la respuesta
        result = fixing_parser.parse(response.content)
        
        return result
        
    except Exception as e:
        print(f"Error generando layout de mazmorra: {e}")
        # Fallback en caso de error - crear una mazmorra simple hardcodeada
        return _create_fallback_dungeon()


def _create_fallback_dungeon() -> Dungeon:
    """
    Crea una mazmorra simple hardcodeada como fallback en caso de error de IA.
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
    
    print("\n=== PRUEBA DE GENERACIÓN DE MAZMORRA ===")
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
