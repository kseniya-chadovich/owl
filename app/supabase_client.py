# app/supabase_client.py
# Simple helper to create and reuse a Supabase client.
# Uses SUPABASE_URL and SUPABASE_ANON_KEY / SERVICE_ROLE_KEY from .env

import os
from supabase import create_client, Client
from dotenv import load_dotenv

_client: Client | None = None

def get_supabase() -> Client:
    """Return a singleton Supabase client."""
    global _client
    if _client is None:
        load_dotenv()
        url = os.getenv("SUPABASE_URL")
        key = (
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            or os.getenv("SUPABASE_ANON_KEY")
        )
        if not url or not key:
            raise RuntimeError(
                "Supabase URL or key not set. Please check your .env file."
            )
        _client = create_client(url, key)
    return _client
