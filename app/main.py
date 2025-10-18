# app/main.py
import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ---------- file paths ----------
CATALOG_FILE = os.getenv("CATALOG_FILE", "data/course_catalog.json")
PLAN_FILE    = os.getenv("PLAN_FILE",    "data/plan.json")
PROGRESS_FILE= os.getenv("PROGRESS_FILE","data/student_progress.json")

# ---------- import your generator ----------
try:
    from scheduler.generator import generate_schedules
except Exception:
    from generator import generate_schedules

app = FastAPI(title="Scheduling Assistant Backend", version="0.1.0")

# allow CORS for dev; narrow it later if you know the exact frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/api/catalog")
def get_catalog():
    p = Path(CATALOG_FILE)
    if not p.exists():
        raise HTTPException(500, f"catalog file missing: {CATALOG_FILE}")
    return json.loads(p.read_text(encoding="utf-8"))

@app.post("/api/student-progress")
def save_student_progress(student_progress: Dict[str, Any] = Body(...)):
    Path(PROGRESS_FILE).write_text(
        json.dumps(student_progress, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return {"ok": True, "path": PROGRESS_FILE}

@app.post("/api/schedules/generate")
def generate(
    num_schedules: int = Body(3, embed=True),
    student_progress: Optional[Dict[str, Any]] = Body(None)
):
    if student_progress is not None:
        Path(PROGRESS_FILE).write_text(
            json.dumps(student_progress, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    for f in [CATALOG_FILE, PLAN_FILE, PROGRESS_FILE]:
        if not Path(f).exists():
            raise HTTPException(500, f"required file missing: {f}")

    try:
        schedules = generate_schedules(PROGRESS_FILE, num_schedules=num_schedules)
        return {"ok": True, "count": len(schedules), "schedules": schedules}
    except Exception as e:
        raise HTTPException(500, f"generator failed: {e}")