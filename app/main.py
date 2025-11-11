# app/main.py

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.supabase_client import get_supabase
from scripts.terminal_chat import build_client, handle_request, SCHEMA_DESCRIPTION

app = FastAPI(title="Scheduling Assistant API")

# Allow frontend access (adjust to your frontend URL later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 1. Lazy AI client (for /dialog)
# =========================

MODEL_NAME = "models/gemini-2.5-flash-lite"
_ai_client = None

def get_ai_client():
    """Create AI client only when needed (avoid crash when GOOGLE_API_KEY is missing)."""
    global _ai_client
    if _ai_client is None:
        _ai_client = build_client()
    return _ai_client

# Stores per-user conversation + academic info (for /dialog)
user_state: Dict[str, Dict[str, Any]] = {}


@app.get("/")
def root():
    return {"message": "Scheduling Assistant API is running!"}


# =========================
# 2. Registration data models
# =========================

class Personal(BaseModel):
    user_id: str
    full_name: str
    age: int
    is_international: bool

class Academic(BaseModel):
    user_id: str
    current_semester: str
    taken_courses: List[str] = []
    taken_geneds: List[str] = []

class StudentRegistrationRequest(BaseModel):
    personal: Personal
    academic: Academic


# =========================
# 3. POST /register-student
# =========================

@app.post("/register-student")
async def register_student(payload: StudentRegistrationRequest):
    """
    Save or update student personal + academic records in Supabase.

    Body format (for frontend):

    {
      "personal": {
        "user_id": "s1234567",
        "full_name": "Kaen Zhang",
        "age": 23,
        "is_international": true
      },
      "academic": {
        "user_id": "s1234567",
        "current_semester": "Fall 2025",
        "taken_courses": ["CIS1001", "ENG1002"],
        "taken_geneds": ["Humanities", "Math"]
      }
    }
    """
    personal = payload.personal
    academic = payload.academic

    if personal.user_id != academic.user_id:
        raise HTTPException(status_code=400, detail="user_id does not match.")

    supabase = get_supabase()

    # Upsert personal info by user_id
    supabase.table("students_personal").upsert(
        {
            "user_id": personal.user_id,
            "full_name": personal.full_name,
            "age": personal.age,
            "is_international": personal.is_international,
        },
        on_conflict="user_id",
    ).execute()

    # Upsert academic info by user_id
    supabase.table("students_academic").upsert(
        {
            "user_id": academic.user_id,
            "current_semester": academic.current_semester,
            "taken_courses": academic.taken_courses,
            "taken_geneds": academic.taken_geneds,
        },
        on_conflict="user_id",
    ).execute()

    return {"message": "Student data saved.", "user_id": personal.user_id}


# =========================
# 4. GET /students/{user_id}
# =========================

@app.get("/students/{user_id}")
async def get_student(user_id: str):
    """
    Return personal + academic info and a ready-to-use scheduler_input object.

    Example:
    GET /students/s1234567
    """
    supabase = get_supabase()

    # personal
    personal_res = (
        supabase.table("students_personal")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    personal = personal_res.data[0] if personal_res.data else None

    # academic
    academic_res = (
        supabase.table("students_academic")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    academic = academic_res.data[0] if academic_res.data else None

    if not personal and not academic:
        raise HTTPException(status_code=404, detail="Student not found.")

    scheduler_input = None
    if personal and academic:
        scheduler_input = {
            "user_id": user_id,
            "current_semester": academic.get("current_semester"),
            "taken_courses": academic.get("taken_courses") or [],
            "taken_geneds": academic.get("taken_geneds") or [],
            "is_international": personal.get("is_international"),
        }

    return {
        "personal": personal,
        "academic": academic,
        "scheduler_input": scheduler_input,
    }


# =========================
# 5. Existing dialog endpoints (unchanged except lazy client)
# =========================

@app.post("/dialog")
async def dialog(request: Request):
    """
    Main dialog endpoint for the scheduler assistant.
    Uses get_ai_client() so it only loads when needed.
    """
    data = await request.json()
    user_id = data.get("user_id", "default")
    message = data.get("message", "").strip()
    new_student_data = data.get("student_data", {})
    num_schedules = data.get("num_schedules", 3)
    temperature = data.get("temperature", 0.2)

    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' field.")

    academic_fields = {"taken_courses", "taken_geneds", "current_semester"}
    academic_data = {k: v for k, v in new_student_data.items() if k in academic_fields}

    if user_id not in user_state:
        user_state[user_id] = {
            "conversation": [SCHEMA_DESCRIPTION],
            "student_data": academic_data,
        }
    else:
        if academic_data:
            user_state[user_id]["student_data"].update(academic_data)

    student_data = user_state[user_id]["student_data"]
    conversation = user_state[user_id]["conversation"]

    try:
        client = get_ai_client()
        result = handle_request(
            client=client,
            model_name=MODEL_NAME,
            message=message,
            student_data=student_data,
            conversation_history=conversation,
            num_schedules=num_schedules,
            temperature=temperature,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    user_state[user_id]["conversation"] = result["conversation"]

    return {
        "user_id": user_id,
        "payload": result["payload"],
        "schedules": result["schedules"],
        "conversation_length": len(result["conversation"]),
    }


@app.post("/reset")
async def reset_user(request: Request):
    """
    Reset user's in-memory data for /dialog.
    """
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user_id.")

    user_state.pop(user_id, None)
    return {"message": f"All data reset for user '{user_id}'."}
