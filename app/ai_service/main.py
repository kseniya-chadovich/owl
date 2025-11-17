# ai_service/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION

# IMPORTANT: import your supabase client from data_service
# Adjust path if needed
from app.data_service.supabase_client import get_supabase


app = FastAPI(title="Scheduling Assistant AI Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini client
client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# Fallback in-memory (only used if DB not reachable)
memory_cache: Dict[str, Dict[str, Any]] = {}


# -------------------------------------------------------------------
# 🧠 CONVERSATION PERSISTENCE HELPERS (Supabase)
# -------------------------------------------------------------------

def load_conversation(user_id: str) -> List[Dict[str, Any]]:
    """Load conversation history for user from Supabase, fallback to memory."""
    try:
        supabase = get_supabase()
        res = supabase.table("dialog_state").select("*").eq("user_id", user_id).execute()
        if res.data:
            return res.data[0]["conversation"]
    except Exception as e:
        print("WARNING: Failed loading conversation from DB → using memory. Error:", e)

    # fallback
    return memory_cache.get(user_id, {}).get("conversation", [SCHEMA_DESCRIPTION])


def save_conversation(user_id: str, conversation: List[Dict[str, Any]]):
    """Save conversation history to Supabase + local fallback."""
    try:
        supabase = get_supabase()
        supabase.table("dialog_state").upsert({
            "user_id": user_id,
            "conversation": conversation
        }).execute()
    except Exception as e:
        print("WARNING: Failed saving conversation to DB → storing in memory. Error:", e)

    # fallback
    memory_cache[user_id] = memory_cache.get(user_id, {})
    memory_cache[user_id]["conversation"] = conversation


# -------------------------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "AI Parser & Scheduler is running!"}


# -------------------------------------------------------------------
# /dialog — MAIN AI ENDPOINT
# -------------------------------------------------------------------

@app.post("/dialog")
async def dialog(request: Request):
    data = await request.json()

    user_id = data.get("user_id")
    message = data.get("message", "").strip()
    new_student_data = data.get("student_data", {})
    num_schedules = data.get("num_schedules", 3)
    temperature = data.get("temperature", 0.2)

    if not user_id:
        return {"error": "Missing 'user_id'."}
    if not message:
        return {"error": "Missing 'message'."}

    # Determine what is academic
    academic_fields = {"taken_courses", "taken_geneds", "current_semester"}
    academic_data = {k: v for k, v in new_student_data.items() if k in academic_fields}

    # Load conversation*
    conversation = load_conversation(user_id)

    # Load per-user academic prefs (stored in fallback memory only)
    user_mem = memory_cache.get(user_id, {"student_data": {}})
    if academic_data:
        user_mem["student_data"].update(academic_data)
    memory_cache[user_id] = user_mem

    try:
        result = handle_request(
            client=client,
            model_name=MODEL_NAME,
            message=message,
            student_data=user_mem["student_data"],
            conversation_history=conversation,
            num_schedules=num_schedules,
            temperature=temperature,
        )
    except Exception as e:
        return {"error": str(e)}

    # Save new conversation (persistent)
    save_conversation(user_id, result["conversation"])

    return {
        "user_id": user_id,
        "payload": result["payload"],
        "schedules": result["schedules"],
        "conversation_length": len(result["conversation"]),
    }


# -------------------------------------------------------------------
# RESET USER
# -------------------------------------------------------------------

@app.post("/reset")
async def reset_user(request: Request):
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        return {"error": "Missing 'user_id'."}

    # Reset DB
    try:
        supabase = get_supabase()
        supabase.table("dialog_state").delete().eq("user_id", user_id).execute()
    except Exception as e:
        print("WARNING: reset failed for DB:", e)

    # Reset fallback memory
    memory_cache.pop(user_id, None)

    return {"message": f"Conversation reset for '{user_id}'."}
