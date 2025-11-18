# app/data_service/main.py
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

# -------- Models ----------

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

class SaveConversationPayload(BaseModel):
    user_id: str
    conversation: List[str]

# -------- Health Check ------
@app.get("/")
def root():
    return {"message": "Student Data API running!"}

# -------- Register Student ----------
@app.post("/register-student")
def register_student(payload: RegisterStudentPayload):
    db = get_supabase()

    db.table("student_personal").upsert(payload.personal.model_dump()).execute()
    db.table("student_academic").upsert(payload.academic.model_dump()).execute()

    return {"message": "Student saved", "user_id": payload.personal.user_id}

# -------- Get Student ----------
@app.get("/students/{user_id}")
def get_student(user_id: str):
    db = get_supabase()

    personal = db.table("student_personal").select("*").eq("user_id", user_id).execute().data
    academic = db.table("student_academic").select("*").eq("user_id", user_id).execute().data

    return {
        "personal": personal[0] if personal else None,
        "academic": academic[0] if academic else None,
    }

# -------- Schedules ----------
@app.post("/students/schedules")
def save_schedule(payload: SchedulePayload):
    db = get_supabase()
    db.table("student_schedules").upsert(payload.model_dump()).execute()
    return {"message": "Schedule saved"}

@app.get("/students/schedules/{user_id}")
def get_schedule(user_id: str):
    db = get_supabase()
    res = db.table("student_schedules").select("*").eq("user_id", user_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="No schedule")
    return res.data[0]

# -------- Conversation State (NEW) ----------
@app.post("/students/conversation")
def save_conversation(payload: SaveConversationPayload):
    db = get_supabase()
    db.table("student_conversations").upsert(payload.model_dump()).execute()
    return {"message": "Conversation saved"}

@app.get("/students/conversation/{user_id}")
def get_conversation(user_id: str):
    db = get_supabase()
    res = db.table("student_conversations").select("*").eq("user_id", user_id).execute().data
    return res[0] if res else {"conversation": []}

# -------- Delete ----------
@app.delete("/students/{user_id}")
def delete_student(user_id: str):
    db = get_supabase()
    db.table("student_personal").delete().eq("user_id", user_id).execute()
    db.table("student_academic").delete().eq("user_id", user_id).execute()
    db.table("student_schedules").delete().eq("user_id", user_id).execute()
    db.table("student_conversations").delete().eq("user_id", user_id).execute()

    return {"message": f"Deleted {user_id}"}


@app.delete("/students/conversation/{user_id}")
def delete_conversation(user_id: str):
    db = get_supabase()
    db.table("student_conversations").delete().eq("user_id", user_id).execute()
    return {"message": "Conversation cleared"}