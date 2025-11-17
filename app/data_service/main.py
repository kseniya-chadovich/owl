from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from app.data_service.supabase_client import get_supabase

app = FastAPI(title="Student Data API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========= MODELS ========= #

class PersonalInfo(BaseModel):
    user_id: str
    full_name: str
    age: int
    is_international: bool

class AcademicInfo(BaseModel):
    user_id: str
    current_semester: int
    taken_courses: List[str]
    taken_geneds: List[str]

class RegisterStudentPayload(BaseModel):
    personal: PersonalInfo
    academic: AcademicInfo

class SchedulePayload(BaseModel):
    user_id: str
    schedule: Dict[str, Any]

class ChatPayload(BaseModel):
    user_id: str
    conversation: List[Dict[str, Any]]

# ========= ROUTES ========= #

@app.get("/")
def root():
    return {"message": "Student Data API running!"}

# ---- Student CRUD ---- #

@app.post("/register-student")
def register_student(payload: RegisterStudentPayload):
    supabase = get_supabase()

    supabase.table("student_personal").upsert(payload.personal.model_dump()).execute()
    supabase.table("student_academic").upsert(payload.academic.model_dump()).execute()

    return {"message": "Saved student", "user_id": payload.personal.user_id}


@app.get("/students/{user_id}")
def get_student(user_id: str):
    supabase = get_supabase()

    personal = supabase.table("student_personal").select("*").eq("user_id", user_id).execute().data
    academic = supabase.table("student_academic").select("*").eq("user_id", user_id).execute().data

    if not personal and not academic:
        raise HTTPException(status_code=404, detail="Not found")

    return {
        "personal": personal[0] if personal else None,
        "academic": academic[0] if academic else None,
    }

# ---- Schedules ---- #

@app.post("/students/schedules")
def save_schedule(payload: SchedulePayload):
    supabase = get_supabase()
    supabase.table("student_schedules").upsert(payload.model_dump()).execute()
    return {"message": "Schedule saved"}


@app.get("/students/schedules/{user_id}")
def get_schedule(user_id: str):
    supabase = get_supabase()
    res = supabase.table("student_schedules").select("*").eq("user_id", user_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="No schedule")
    return res.data[0]


@app.delete("/students/{user_id}")
def delete_student(user_id: str):
    supabase = get_supabase()
    supabase.table("student_personal").delete().eq("user_id", user_id).execute()
    supabase.table("student_academic").delete().eq("user_id", user_id).execute()
    supabase.table("student_schedules").delete().eq("user_id", user_id).execute()
    supabase.table("chat_history").delete().eq("user_id", user_id).execute()
    return {"message": f"Deleted {user_id}"}

# ---- CHAT HISTORY ---- #

@app.post("/chat/save")
def save_chat(payload: ChatPayload):
    supabase = get_supabase()

    supabase.table("chat_history").upsert({
        "user_id": payload.user_id,
        "conversation": payload.conversation
    }).execute()

    return {"message": "Chat saved"}

@app.get("/chat/load/{user_id}")
def load_chat(user_id: str):
    supabase = get_supabase()

    res = supabase.table("chat_history").select("*").eq("user_id", user_id).execute()

    if not res.data:
        return {"conversation": []}

    return res.data[0]

@app.post("/chat/reset")
def reset_chat(payload: ChatPayload):
    supabase = get_supabase()
    supabase.table("chat_history").delete().eq("user_id", payload.user_id).execute()
    return {"message": "Chat reset"}
