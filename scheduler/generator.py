import json
from ortools.sat.python import cp_model

from .config import *
from .helpers import (
    extract_course_code, parse_daytime_slots, slots_overlap,
    prereqs_satisfied, lunch_conflict, class_starts_before,
    class_ends_after, days_set, is_cis_3000_plus
)

def generate_schedules(student_progress_file, num_schedules=3):
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan = json.load(f)
    with open(student_progress_file, "r", encoding="utf-8") as f:
        student = json.load(f)

    # preprocess
    for e in catalog:
        e["course_code"] = extract_course_code(e["course"])
        e["slots"] = parse_daytime_slots(e.get("day_time", ""))

    # unpack student data
    current_sem   = int(student["current_semester"])
    taken_courses = set(student.get("taken_courses", []))
    taken_geneds  = set(student.get("taken_geneds", []))
    gened_pref    = set(student.get("gened_preference", []))
    pref_days     = set(student.get("preferred_days", []))
    no_days       = set(student.get("no_days", []))
    want_lunch    = bool(student.get("lunch_break", False))
    no_mornings   = bool(student.get("no_mornings", False))
    no_evenings   = bool(student.get("no_evenings", False))
    prefer_mode   = student.get("prefer_mode")
    avoid_profs   = set(student.get("avoid_professors", []))
    min_cr        = int(student["min_credits"])
    max_cr        = int(student["max_credits"])

    REQUIRED_MAJOR_SET = {
        "CIS 1001","CIS 1068","CIS 1166","CIS 2107","CIS 2168","CIS 2166",
        "CIS 2033","CIS 3207","CIS 3223","CIS 3296","MATH 1041","MATH 1042",
        "PHYS 1061","PHYS 1062","CIS 1051","CIS 1057","SCTC 1001","SCTC 2001",
        "CIS 4397","CIS 4398"
    }
    ALL_GENED_TYPES = {"GA","GB","GG","GD","GQ","GS","GU","GW","GY","GZ"}

    # plan groups
    plan_groups = []
    electives_seen = set()
    for sem_s, info in plan.items():
        sem = int(sem_s)
        if sem > current_sem: continue
        for entry in info.get("major", []):
            if isinstance(entry, list):
                if any(opt in taken_courses for opt in entry): continue
                plan_groups.append(entry[:])
            elif entry == "Comp Sci Elective":
                elective_opts = sorted({
                    sec["course_code"] for sec in catalog
                    if sec.get("category") == "major"
                    and is_cis_3000_plus(sec["course_code"])
                    and sec["course_code"] not in taken_courses
                    and sec["course_code"] not in REQUIRED_MAJOR_SET
                })
                new_opts = tuple(elective_opts)
                if new_opts and new_opts not in electives_seen:
                    plan_groups.append(list(new_opts))
                    electives_seen.add(new_opts)
            else:
                if entry in taken_courses: continue
                plan_groups.append([entry])

    # candidate pool
    candidates = []
    for sec in catalog:
        if sec["course_code"] in taken_courses: continue
        if sec.get("category") == "gened" and sec.get("gened_type") in taken_geneds: continue
        if not prereqs_satisfied(sec, taken_courses): continue
        candidates.append(sec)
    if not candidates: return []

    schedules = []
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = TIME_LIMIT_SEC

    seen_solutions = []

    for s in range(num_schedules):
        model = cp_model.CpModel()
        N = len(candidates)
        x = [model.NewBoolVar(f"x_{i}") for i in range(N)]

        total_credits = sum(x[i] * candidates[i]["credits"] for i in range(N))
        model.Add(total_credits >= min_cr)
        model.Add(total_credits <= max_cr)

        for i in range(N):
            for j in range(i+1, N):
                if slots_overlap(candidates[i]["slots"], candidates[j]["slots"]):
                    model.Add(x[i] + x[j] <= 1)

        idx_by_code = {}
        for i, c in enumerate(candidates):
            idx_by_code.setdefault(c["course_code"], []).append(i)
        for code, idxs in idx_by_code.items():
            if len(idxs) > 1:
                model.Add(sum(x[i] for i in idxs) <= 1)

        idxs_by_gened_type = {}
        for i, c in enumerate(candidates):
            gt = c.get("gened_type")
            if gt:
                idxs_by_gened_type.setdefault(gt, []).append(i)
        for gt, idxs in idxs_by_gened_type.items():
            model.Add(sum(x[i] for i in idxs) <= 1)

        one_cr_idxs = [i for i, c in enumerate(candidates) if c.get("category")=="elective" and c["credits"]==1]
        if one_cr_idxs:
            model.Add(sum(x[i] for i in one_cr_idxs) <= 1)

        # forbid duplicates
        for chosen_set in seen_solutions:
            model.Add(sum(x[i] for i in chosen_set) <= len(chosen_set) - 1)

        # objective
        objective_terms = []
        for g_idx, group in enumerate(plan_groups):
            group_idxs = [i for i,c in enumerate(candidates) if c["course_code"] in group]
            if group_idxs:
                g = model.NewBoolVar(f"plan_group_{g_idx}")
                model.AddMaxEquality(g, [x[i] for i in group_idxs])
                objective_terms.append(PLAN_WEIGHT * g)

        for i, c in enumerate(candidates):
            if c.get("category")=="gened" and c.get("gened_type") in gened_pref:
                objective_terms.append(GENED_WEIGHT * x[i])

        for i, c in enumerate(candidates):
            ds = days_set(c["slots"])
            if ds:
                if pref_days and ds.issubset(pref_days):
                    objective_terms.append(DAY_PREF_WEIGHT * x[i])
                if no_days and (ds & no_days):
                    objective_terms.append(DAY_NO_PENALTY * x[i])

        if want_lunch:
            for i, c in enumerate(candidates):
                if lunch_conflict(c["slots"]):
                    objective_terms.append(LUNCH_PENALTY * x[i])
        if no_mornings:
            for i, c in enumerate(candidates):
                if class_starts_before(c["slots"], 10*60):
                    objective_terms.append(NO_MORN_PENALTY * x[i])
        if no_evenings:
            for i, c in enumerate(candidates):
                if class_ends_after(c["slots"], 18*60):
                    objective_terms.append(NO_EVEN_PENALTY * x[i])

        if prefer_mode in ("online","offline"):
            for i,c in enumerate(candidates):
                if c.get("mode")==prefer_mode:
                    objective_terms.append(MODE_MATCH_REWARD * x[i])

        for i,c in enumerate(candidates):
            if c.get("category")=="elective":
                if c["credits"]==1:
                    objective_terms.append(ONE_CREDIT_PENALTY * x[i])
                elif 3 <= c["credits"] <= 4:
                    objective_terms.append(NORMAL_ELEC_REWARD * x[i])

        for i,c in enumerate(candidates):
            prof = str(c.get("instructor","")).split(",")[0].strip()
            if any(prof == avoid for avoid in avoid_profs):
                objective_terms.append(AVOID_PROF_PENALTY * x[i])

        objective_terms.append(CREDITS_NUDGE * total_credits)
        model.Maximize(sum(objective_terms))

        status = solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break

        chosen_idxs = [i for i in range(N) if solver.Value(x[i])==1]
        chosen = [candidates[i] for i in chosen_idxs]
        seen_solutions.append(chosen_idxs)

        tot = sum(c["credits"] for c in chosen)

        # Progress report
        hist_credits = 0
        taken_set = set(taken_courses)
        for sec in catalog:
            if sec["course_code"] in taken_set:
                hist_credits += sec.get("credits", 0)

        majors_required = majors_electives = geneds = free_elec = 0
        for c in chosen:
            code = c["course_code"]
            if c.get("category") == "gened":
                geneds += c["credits"]
            elif code in REQUIRED_MAJOR_SET:
                majors_required += c["credits"]
            elif is_cis_3000_plus(code):
                majors_electives += c["credits"]
            else:
                free_elec += c["credits"]

        geneds_satisfied = taken_geneds | {c.get("gened_type") for c in chosen if c.get("category")=="gened"}
        remaining_geneds = ALL_GENED_TYPES - geneds_satisfied

        progress_report = {
            "overall_credits": hist_credits + tot,
            "this_term": {
                "majors_required": majors_required,
                "majors_electives": majors_electives,
                "geneds": geneds,
                "free_electives": free_elec,
            },
            "geneds_satisfied": len(geneds_satisfied),
            "geneds_total": len(ALL_GENED_TYPES),
            "remaining_geneds": sorted(remaining_geneds),
        }

        schedules.append({
            "total_credits": tot,
            "courses": [
                {
                    "course": c["course"],
                    "course_code": c["course_code"],
                    "day_time": c.get("day_time",""),
                    "credits": c["credits"],
                    "category": c.get("category"),
                    "gened_type": c.get("gened_type"),
                    "mode": c.get("mode"),
                    "instructor": c.get("instructor"),
                } for c in chosen
            ],
            "progress_report": progress_report
        })

    return schedules
