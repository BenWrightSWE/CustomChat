import os
from supabase import Client, create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Default client (uses the key from .env)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

APP_ENCRYPTION_KEY = os.getenv("APP_ENCRYPTION_KEY")

# Service role client for admin operations (uses the key from .env)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
