import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field
from langfuse.langchain import CallbackHandler


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
- La descripción debe ser inmersiva y apropiada para una mazmorra misteriosa
- Describe el entorno, la iluminación, los sonidos ambiente, olores, y sensaciones generales

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
