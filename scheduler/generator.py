import json
from ortools.sat.python import cp_model

from .config import *
from .helpers import (
    extract_course_code, parse_daytime_slots, slots_overlap,
    prereqs_satisfied, lunch_conflict, class_starts_before,
    class_ends_after, days_set, is_cis_3000_plus
)

def generate_schedules(student_progress_file, num_schedules=3):

    # ---------- load ----------
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    with open(PLAN_FILE, "r", encoding="utf-8") as f:
        plan = json.load(f)
    with open(student_progress_file, "r", encoding="utf-8") as f:
        student = json.load(f)

    # ---------- preprocess ----------
    for e in catalog:
        e["course_code"] = extract_course_code(e["course"])
        e["slots"] = parse_daytime_slots(e.get("day_time", ""))

    # ---------- unpack student data ----------
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

    # ---------- plan groups ----------
    plan_groups = []
    electives_seen = set()

    for sem_s, info in plan.items():
        sem = int(sem_s)
        if sem > current_sem:
            continue

        for entry in info.get("major", []):
            if isinstance(entry, list):
                if not any(opt in taken_courses for opt in entry):
                    plan_groups.append(entry[:])

            elif entry == "Comp Sci Elective":
                elective_opts = sorted({
                    sec["course_code"]
                    for sec in catalog
                    if sec.get("category") == "major"
                    and is_cis_3000_plus(sec["course_code"])
                    and sec["course_code"] not in taken_courses
                    and sec["course_code"] not in REQUIRED_MAJOR_SET
                })
                tup = tuple(elective_opts)
                if tup and tup not in electives_seen:
                    electives_seen.add(tup)
                    plan_groups.append(list(elective_opts))

            else:
                if entry not in taken_courses:
                    plan_groups.append([entry])

    # ---------- candidate pool ----------
    candidates = []
    for sec in catalog:
        if sec["course_code"] in taken_courses:
            continue
        if sec.get("category") == "gened" and sec.get("gened_type") in taken_geneds:
            continue
        if not prereqs_satisfied(sec, taken_courses):
            continue
        candidates.append(sec)

    if not candidates:
        return []

    # =============== SOLVER INIT ===============
    schedules = []
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = TIME_LIMIT_SEC

    seen_solutions = []

    # =====================================================
    #                 MAIN LOOP (multiple schedules)
    # =====================================================
    for _ in range(num_schedules):

        model = cp_model.CpModel()
        N = len(candidates)
        x = [model.NewBoolVar(f"x_{i}") for i in range(N)]

        # ---------- hard constraints ----------
        total_credits = sum(x[i] * candidates[i]["credits"] for i in range(N))
        model.Add(total_credits >= min_cr)
        model.Add(total_credits <= max_cr)

        # no overlaps
        for i in range(N):
            for j in range(i+1, N):
                if slots_overlap(candidates[i]["slots"], candidates[j]["slots"]):
                    model.Add(x[i] + x[j] <= 1)

        # one section per course code
        idx_by_code = {}
        for i, c in enumerate(candidates):
            idx_by_code.setdefault(c["course_code"], []).append(i)
        for idxs in idx_by_code.values():
            if len(idxs) > 1:
                model.Add(sum(x[i] for i in idxs) <= 1)

        # one GenEd per type per term
        idxs_by_gt = {}
        for i, c in enumerate(candidates):
            gt = c.get("gened_type")
            if gt:
                idxs_by_gt.setdefault(gt, []).append(i)
        for idxs in idxs_by_gt.values():
            model.Add(sum(x[i] for i in idxs) <= 1)

        # max one 1-credit elective
        one_cr_idxs = [i for i, c in enumerate(candidates)
                       if c.get("category") == "elective" and c["credits"] == 1]
        if one_cr_idxs:
            model.Add(sum(x[i] for i in one_cr_idxs) <= 1)

        # forbid duplicates
        for sol in seen_solutions:
            model.Add(sum(x[i] for i in sol) <= len(sol) - 1)

        # =====================================================
        #                     OBJECTIVE
        # =====================================================
        objective_terms = []

        # 1) Plan groups
        for group in plan_groups:
            idxs = [i for i, c in enumerate(candidates) if c["course_code"] in group]
            if idxs:
                g = model.NewBoolVar("")
                model.AddMaxEquality(g, [x[i] for i in idxs])
                objective_terms.append(PLAN_WEIGHT * g)

        # 2) UNSAT GenEds FIRST
        unsatisfied = ALL_GENED_TYPES - taken_geneds

        for i, c in enumerate(candidates):
            if c.get("category") == "gened":
                gt = c.get("gened_type")
                if gt in unsatisfied:
                    objective_terms.append(UNSAT_GENED_WEIGHT * x[i])
                if gt in gened_pref:
                    objective_terms.append(GENED_WEIGHT * x[i])

        # 3) Day preference
        for i, c in enumerate(candidates):
            ds = days_set(c["slots"])
            if ds:
                if ds.issubset(pref_days):
                    objective_terms.append(DAY_PREF_WEIGHT * x[i])
                if ds & no_days:
                    objective_terms.append(DAY_NO_PENALTY * x[i])

        # 4) Lunch / mornings / evenings
        for i, c in enumerate(candidates):
            if want_lunch and lunch_conflict(c["slots"]):
                objective_terms.append(LUNCH_PENALTY * x[i])
            if no_mornings and class_starts_before(c["slots"], 10*60):
                objective_terms.append(NO_MORN_PENALTY * x[i])
            if no_evenings and class_ends_after(c["slots"], 18*60):
                objective_terms.append(NO_EVEN_PENALTY * x[i])

        # 5) Mode preference
        for i, c in enumerate(candidates):
            if prefer_mode and c.get("mode") == prefer_mode:
                objective_terms.append(MODE_MATCH_REWARD * x[i])

        # 6) Electives logic
        if unsatisfied:
            for i, c in enumerate(candidates):
                if c.get("category") == "elective" and c["credits"] == 1:
                    objective_terms.append(ONE_CREDIT_PENALTY * x[i])
        else:
            for i, c in enumerate(candidates):
                if c.get("category") == "elective":
                    if c["credits"] == 1:
                        objective_terms.append(ONE_CREDIT_PENALTY * x[i])
                    elif 3 <= c["credits"] <= 4:
                        objective_terms.append(NORMAL_ELEC_REWARD * x[i])

        # 7) Avoid professors
        for i, c in enumerate(candidates):
            prof = str(c.get("instructor", "")).split(",")[0].strip()
            if prof in avoid_profs:
                objective_terms.append(AVOID_PROF_PENALTY * x[i])

        # 8) Credit nudge
        objective_terms.append(CREDITS_NUDGE * total_credits)

        model.Maximize(sum(objective_terms))

        # ---------- solve ----------
        status = solver.Solve(model)
        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            break

        # =============== collect solution ===============
        chosen_idxs = [i for i in range(N) if solver.Value(x[i]) == 1]
        seen_solutions.append(chosen_idxs)

        chosen = [candidates[i] for i in chosen_idxs]
        tot = sum(c["credits"] for c in chosen)

        # ---------- progress report ----------
        hist_credits = sum(
            sec.get("credits", 0)
            for sec in catalog
            if sec["course_code"] in taken_courses
        )

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

        geneds_satisfied = taken_geneds | {
            c.get("gened_type")
            for c in chosen
            if c.get("category") == "gened"
        }

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
            "remaining_geneds": sorted(ALL_GENED_TYPES - geneds_satisfied),
        }

        schedules.append({
            "total_credits": tot,
            "courses": [
                {
                    "course": c["course"],
                    "course_code": c["course_code"],
                    "day_time": c.get("day_time", ""),
                    "credits": c["credits"],
                    "category": c.get("category"),
                    "gened_type": c.get("gened_type"),
                    "mode": c.get("mode"),
                    "instructor": c.get("instructor"),
                }
                for c in chosen
            ],
            "progress_report": progress_report
        })

    return schedules
