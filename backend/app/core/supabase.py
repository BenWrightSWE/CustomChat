import os
from supabase import Client, create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Default client (uses the key from .env)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Service role client for admin operations (uses the key from .env)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
