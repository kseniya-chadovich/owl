import os
from pathlib import Path

from supabase import create_client, Client
from dotenv import load_dotenv


# Always load .env from project root (the folder that contains "app" and ".env")
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(env_path)


def get_supabase() -> Client:
    """
    Create and return a Supabase client using env vars.

    Required in .env:
      SUPABASE_URL=...
      SUPABASE_ANON_KEY=...
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")

    if not url or not key:
        # Print to server log to help debugging
        print("DEBUG Supabase URL:", url)
        print("DEBUG Supabase ANON KEY exists:", bool(key))

        raise RuntimeError(
            "Supabase URL or key not set. Please check your .env file."
        )

    return create_client(url, key)
