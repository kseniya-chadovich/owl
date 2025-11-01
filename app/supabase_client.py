# app/supabase_client.py
import os
from supabase import create_client, Client

def get_supabase() -> Client:
    """
    Return a Supabase client using env vars.
    This will raise an error if env vars are missing.
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        # Keep message simple so students can understand
        raise RuntimeError("Supabase URL or KEY is missing. Check your .env file.")
    client: Client = create_client(url, key)
    return client
