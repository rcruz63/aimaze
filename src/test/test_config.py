import os
from aimaze.config import load_config


def test_load_config():
    load_config()
    assert os.getenv("OPENAI_API_KEY") is not None
    
# supabase
    assert os.getenv("SUPABASE_URL") is not None
    assert os.getenv("SUPABASE_KEY") is not None
# langfuse
    assert os.getenv("LANGFUSE_SECRET_KEY") is not None
    assert os.getenv("LANGFUSE_PUBLIC_KEY") is not None
    assert os.getenv("LANGFUSE_HOST") is not None