# app/routes_supabase.py
# REST endpoints for your Supabase tables

from fastapi import APIRouter, HTTPException
from .supabase_client import supabase

router = APIRouter(
    prefix="/supabase",
    tags=["supabase"],
)

# ----- classrooms ------------------------------------------------
@router.get("/classrooms")
def list_classrooms():
    # get all classrooms
    res = supabase.table("classrooms").select("*").order("created_at", desc=True).execute()
    return res.data


@router.post("/classrooms")
def create_classroom(payload: dict):
    # payload example:
    # { "invite_code": "ABC123", "students": 10, "teacher": "Ms. Lee", "title": "Math", "description": "Grade 1" }
    res = supabase.table("classrooms").insert(payload).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data[0]


@router.get("/classrooms/{classroom_id}")
def get_classroom(classroom_id: int):
    res = supabase.table("classrooms").select("*").eq("id", classroom_id).single().execute()
    if res.error:
        raise HTTPException(status_code=404, detail=res.error.message)
    return res.data


# ----- classroom_game_metadata -----------------------------------
@router.get("/classrooms/{classroom_id}/games")
def list_classroom_games(classroom_id: int):
    res = (
        supabase.table("classroom_game_metadata")
        .select("*")
        .eq("classroom_id", classroom_id)
        .order("uploaded", desc=True)
        .execute()
    )
    return res.data


@router.post("/classrooms/{classroom_id}/games")
def add_classroom_game(classroom_id: int, payload: dict):
    # payload example: { "author": "Kaen", "description": "Math game" }
    payload["classroom_id"] = classroom_id
    res = supabase.table("classroom_game_metadata").insert(payload).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data[0]


# ----- game_metadata (public games) ------------------------------
@router.get("/games")
def list_games():
    res = supabase.table("game_metadata").select("*").order("uploaded", desc=True).execute()
    return res.data


@router.post("/games")
def create_game(payload: dict):
    # payload example: { "author": "Kaen", "description": "Public game" }
    res = supabase.table("game_metadata").insert(payload).execute()
    if res.error:
        raise HTTPException(status_code=400, detail=res.error.message)
    return res.data[0]
