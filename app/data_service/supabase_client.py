import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load .env from root
BASE = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE / ".env")

def get_supabase() -> Client:
    """
    Create a Supabase client using the PUBLIC ANON KEY.
    Safe for server-side RPC/DB operations as long as RLS is disabled or policies allow access.
    """

    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")

    print("DEBUG: Using ANON KEY for data-service")

    if not url or not anon_key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_ANON_KEY in .env")

    # Create client with anon key
    client: Client = create_client(url, anon_key)

    # No storage/postgrest auth needed when using anon key
    return client
