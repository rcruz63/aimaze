import os
from dotenv import load_dotenv


def load_config():
    """
    Carga la configuración del juego.

    - Carga .env si existe (no sobrescribe variables ya definidas)
    - Si se está ejecutando pytest o AIMAZE_USE_ENV_TEST=1, carga env.test
      para completar variables faltantes (sin sobrescribir las ya definidas)
    """
    # 1) Cargar .env si existe, sin sobrescribir
    load_dotenv(dotenv_path=".env", override=False)

    # 2) Cargar env.test bajo condiciones de test o flag explícito
    if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("AIMAZE_USE_ENV_TEST") == "1":
        load_dotenv(dotenv_path="env.test", override=False)
