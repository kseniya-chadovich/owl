# app/main.py
import os
import json
from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ---------- file paths (override via env if needed) ----------
CATALOG_FILE  = os.getenv("CATALOG_FILE",  "data/course_catalog.json")
PLAN_FILE     = os.getenv("PLAN_FILE",     "data/plan.json")
PROGRESS_FILE = os.getenv("PROGRESS_FILE", "data/student_progress.json")

# ---------- import schedules router (provides POST /api/schedules/generate) ----------
try:
    from scheduler.routes_generate import router as schedules_router
except Exception as e:
    schedules_router = None
    # Do not crash startup if the router cannot be imported
    import logging
    logging.getLogger(__name__).warning("Failed to import schedules router: %s", e)

app = FastAPI(title="Scheduling Assistant Backend", version="0.1.0")

# ---------- CORS (open for dev; restrict in prod with ALLOW_ORIGINS) ----------
origins_env = os.getenv("ALLOW_ORIGINS", "*")
allow_origins = [o.strip() for o in origins_env.split(",")] if origins_env else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount schedules router if available
if schedules_router:
    app.include_router(schedules_router)

@app.get("/healthz")
def healthz():
    """Liveness endpoint."""
    return {"ok": True}

@app.get("/api/catalog")
def get_catalog():
    """Return the raw course catalog JSON."""
    p = Path(CATALOG_FILE)
    if not p.exists():
        raise HTTPException(500, f"catalog file missing: {CATALOG_FILE}")
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(500, f"failed to parse catalog: {e}")

@app.post("/api/student-progress")
def save_student_progress(student_progress: Dict[str, Any] = Body(...)):
    """
    Persist student progress/preferences as-is.
    The frontend can POST any structure; we simply store it.
    """
    try:
        Path(PROGRESS_FILE).write_text(
            json.dumps(student_progress, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        raise HTTPException(500, f"failed to store student progress: {e}")
    return {"ok": True, "path": PROGRESS_FILE}

# Note:
# - The schedules generation endpoint is provided by scheduler/routes_generate.py:
#   POST /api/schedules/generate
# - Keep PLAN_FILE here in case other routes use it later.
