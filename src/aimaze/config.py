import os
from dotenv import load_dotenv


def load_config():
    """
    Carga la configuración del juego
    """
    load_dotenv()
    # Asegurar variables requeridas con valores por defecto para entorno de tests/local
    defaults = {
        "OPENAI_API_KEY": "dummy",
        "SUPABASE_URL": "https://dummy.supabase.co",
        "SUPABASE_KEY": "dummy",
        "LANGFUSE_SECRET_KEY": "dummy",
        "LANGFUSE_PUBLIC_KEY": "dummy",
        "LANGFUSE_HOST": "https://cloud.langfuse.com",
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, value)
