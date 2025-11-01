# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# ✅ add this: use our Supabase endpoints
from .routes_supabase import router as supabase_router

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

# ✅ mount Supabase routes
# this will give you:
# GET  /supabase/classrooms
# POST /supabase/classrooms
# GET  /supabase/games
# ...
app.include_router(supabase_router)

client = build_client()
MODEL_NAME = "models/gemini-2.5-flash-lite"

# Stores per-user conversation + academic info
user_state = {}


@app.get("/")
def root():
    return {"message": "Scheduling Assistant API is running!"}


@app.post("/dialog")
async def dialog(request: Request):
    """
    Main dialog endpoint.
    - Academic records are fixed for one session.
    - Preferences (gened_preference, days, etc.) are updated dynamically through AI.
    """
    data = await request.json()
    user_id = data.get("user_id", "default")
    message = data.get("message", "").strip()
    new_student_data = data.get("student_data", {})
    num_schedules = data.get("num_schedules", 3)
    temperature = data.get("temperature", 0.2)

    if not message:
        return {"error": "Missing 'message' field in request."}

    # Split academic data (static) from preferences (handled by AI)
    academic_fields = {"taken_courses", "taken_geneds", "current_semester"}
    academic_data = {k: v for k, v in new_student_data.items() if k in academic_fields}

    # Initialize user if new
    if user_id not in user_state:
        user_state[user_id] = {
            "conversation": [SCHEMA_DESCRIPTION],
            "student_data": academic_data,
        }
    else:
        # Update academic data if new info provided
        if academic_data:
            user_state[user_id]["student_data"].update(academic_data)

    student_data = user_state[user_id]["student_data"]
    conversation = user_state[user_id]["conversation"]

    try:
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
        return {"error": str(e)}

    # Save conversation state for context
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
    Fully resets user's data and conversation.
    Called when the student finalizes a semester and starts a new one.
    """
    data = await request.json()
    user_id = data.get("user_id")

    if not user_id:
        return {"error": "Missing user_id."}

    if user_id in user_state:
        del user_state[user_id]

    return {"message": f"All data reset for user '{user_id}'. New session ready."}
