import json
from pathlib import Path
from typing import List, Set
from fastapi import APIRouter, HTTPException
from .models import (
    ScheduleRequest, GenerateResponse, Schedule, ScheduledSection, CatalogItem
)
from .utils_schedule import (
    normalize_course, base_code, expand_meetings, check_conflict, add_to_timetable,
    prereq_satisfied, hhmm_to_time
)

router = APIRouter(tags=["Schedules"])

# Read catalog directly from data/course_catalog.json at repo root
ROOT_DIR = Path(__file__).resolve().parents[1]
CATALOG_FILE = ROOT_DIR / "data" / "course_catalog.json"

def get_catalog_items() -> List[CatalogItem]:
    if not CATALOG_FILE.exists():
        raise HTTPException(status_code=500, detail=f"Missing catalog file: {CATALOG_FILE}")
    try:
        raw = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
        return [CatalogItem(**r) for r in raw]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse course_catalog.json: {e}")

@router.post("/api/schedules/generate", response_model=GenerateResponse)
def generate_schedules(req: ScheduleRequest) -> GenerateResponse:
    catalog: List[CatalogItem] = get_catalog_items()

    taken_set = {normalize_course(c) for c in req.taken_courses}
    must_include_set = {normalize_course(c) for c in req.must_include}
    must_exclude_set = {normalize_course(c) for c in req.must_exclude}
    include_categories = req.include_categories

    window_start = hhmm_to_time(req.time_window_start) if req.time_window_start else None
    window_end   = hhmm_to_time(req.time_window_end)   if req.time_window_end   else None
    days_off_set = set(req.days_off)

    # Pre-filter by category/exclusion/prerequisites
    filtered: List[CatalogItem] = []
    for it in catalog:
        code = base_code(it.course)
        if include_categories and it.category not in include_categories:
            continue
        if code in must_exclude_set:
            continue
        if not prereq_satisfied(it, taken_set):
            continue
        filtered.append(it)

    # Sort: must_include first, prefer_modes second, then category (major->gened->elective), then credits desc
    cat_score = {"major": 0, "gened": 1, "elective": 2}
    prefer_modes = req.prefer_modes or []
    def key(it: CatalogItem):
        code = base_code(it.course)
        prefer_bonus = -1 if it.mode in prefer_modes else 0
        must_bonus = -2 if code in must_include_set else 0
        return (must_bonus, prefer_bonus, cat_score.get(it.category, 9), -it.credits)
    filtered.sort(key=key)

    results: List[Schedule] = []
    timetable = {}  # day -> [(start,end)]
    picked: List[CatalogItem] = []
    picked_codes: Set[str] = set()
    total_credits = 0

    def can_take(it: CatalogItem) -> bool:
        if req.one_section_per_course and base_code(it.course) in picked_codes:
            return False
        return not check_conflict(timetable, it, days_off_set, window_start, window_end)

    must_targets = {c for c in must_include_set}

    def rebuild_timetable():
        """Rebuild 'timetable' from 'picked' to keep it canonical."""
        timetable.clear()
        for p in picked:
            for d, s, e in expand_meetings(p.day_time):
                timetable.setdefault(d, []).append((s, e))

    def backtrack(start_idx: int) -> bool:
        nonlocal total_credits

        # Record a valid schedule once min credits are satisfied and all must_include are covered
        if total_credits >= req.desired_credits_min:
            if all(any(base_code(p.course) == m for p in picked) for m in must_targets):
                results.append(Schedule(
                    total_credits=total_credits,
                    sections=[ScheduledSection(
                        course=p.course, section=p.section, instructor=p.instructor,
                        day_time=p.day_time, credits=p.credits, mode=p.mode
                    ) for p in picked],
                    violations=[]
                ))
                return len(results) >= req.num_schedules

        # Prune on max credits or if enough schedules collected
        if total_credits > req.desired_credits_max or len(results) >= req.num_schedules:
            return False

        i = start_idx
        while i < len(filtered):
            it = filtered[i]
            i += 1
            if not can_take(it):
                continue

            # Choose
            picked.append(it)
            picked_codes.add(base_code(it.course))
            total_credits += it.credits
            rebuild_timetable()

            stop = backtrack(i)

            # Backtrack
            picked.pop()
            picked_codes.discard(base_code(it.course))
            total_credits -= it.credits
            rebuild_timetable()

            if stop:
                return True
        return False

    backtrack(0)

    if not results:
        violations = []
        if must_targets:
            remaining = [m for m in sorted(must_targets) if all(base_code(x.course) != m for x in picked)]
            if remaining:
                violations.append(f"Unable to satisfy must_include: {', '.join(remaining)}")
        if not violations:
            violations.append("No schedules found satisfying the constraints")
        return GenerateResponse(schedules=[
            Schedule(total_credits=0, sections=[], violations=violations)
        ])

    results.sort(key=lambda s: (-s.total_credits, len(s.sections)))
    return GenerateResponse(schedules=results[:req.num_schedules])
