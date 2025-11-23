import json
from pathlib import Path

import pytest

from scheduler import generator, helpers


def _write_inputs(tmp_path: Path, catalog, plan, student):
    cat_path = tmp_path / "catalog.json"
    plan_path = tmp_path / "plan.json"
    student_path = tmp_path / "student.json"
    cat_path.write_text(json.dumps(catalog), encoding="utf-8")
    plan_path.write_text(json.dumps(plan), encoding="utf-8")
    student_path.write_text(json.dumps(student), encoding="utf-8")
    return cat_path, plan_path, student_path


def _run_scheduler(tmp_path, monkeypatch, catalog, plan, student):
    cat_path, plan_path, student_path = _write_inputs(tmp_path, catalog, plan, student)
    monkeypatch.setattr(generator, "CATALOG_FILE", str(cat_path))
    monkeypatch.setattr(generator, "PLAN_FILE", str(plan_path))
    return generator.generate_schedules(str(student_path), num_schedules=1)


def test_respects_credit_limits_and_no_overlaps(tmp_path, monkeypatch):
    catalog = [
        {"course": "CIS 1001 (001)", "day_time": "M 09:00-10:00", "credits": 3, "category": "major", "prerequisites": []},
        {"course": "CIS 2001 (001)", "day_time": "M 09:30-10:30", "credits": 3, "category": "major", "prerequisites": []},
        {"course": "CIS 3001 (001)", "day_time": "T 14:00-15:00", "credits": 3, "category": "major", "prerequisites": []},
    ]
    plan = {}
    student = {
        "min_credits": 6,
        "max_credits": 6,
        "current_semester": 1,
        "taken_courses": [],
        "taken_geneds": [],
    }
    schedules = _run_scheduler(tmp_path, monkeypatch, catalog, plan, student)
    assert schedules, "Scheduler returned no solutions"
    sched = schedules[0]
    assert 6 <= sched["total_credits"] <= 6

    slots = [helpers.parse_daytime_slots(c["day_time"]) for c in sched["courses"]]
    for i in range(len(slots)):
        for j in range(i + 1, len(slots)):
            assert not helpers.slots_overlap(slots[i], slots[j])


def test_avoids_listed_professors_when_alternative_exists(tmp_path, monkeypatch):
    catalog = [
        {"course": "CIS 1100 (001)", "day_time": "T 10:00-11:15", "credits": 3, "category": "major", "prerequisites": [], "instructor": "Bad Prof"},
        {"course": "CIS 1100 (002)", "day_time": "W 10:00-11:15", "credits": 3, "category": "major", "prerequisites": [], "instructor": "Good Prof"},
    ]
    plan = {}
    student = {
        "min_credits": 3,
        "max_credits": 3,
        "current_semester": 1,
        "taken_courses": [],
        "taken_geneds": [],
        "avoid_professors": ["Bad Prof"],
    }
    schedules = _run_scheduler(tmp_path, monkeypatch, catalog, plan, student)
    assert schedules
    instructors = [c.get("instructor") for c in schedules[0]["courses"]]
    assert "Bad Prof" not in instructors
    assert "Good Prof" in instructors


def test_prefers_online_and_penalizes_mornings(tmp_path, monkeypatch):
    catalog = [
        {"course": "CIS 1200 (online)", "day_time": "M 14:00-15:15", "credits": 3, "category": "major", "prerequisites": [], "mode": "online"},
        {"course": "CIS 1200 (offline)", "day_time": "T 09:00-10:15", "credits": 3, "category": "major", "prerequisites": [], "mode": "offline"},
    ]
    plan = {}
    student = {
        "min_credits": 3,
        "max_credits": 3,
        "current_semester": 1,
        "taken_courses": [],
        "taken_geneds": [],
        "prefer_mode": "online",
        "no_mornings": True,
    }
    schedules = _run_scheduler(tmp_path, monkeypatch, catalog, plan, student)
    assert schedules
    course = schedules[0]["courses"][0]
    assert course["mode"] == "online"
    slots = helpers.parse_daytime_slots(course["day_time"])
    assert not helpers.class_starts_before(slots, 10 * 60)


def test_gened_uniqueness_and_prereq_filtering(tmp_path, monkeypatch):
    catalog = [
        {"course": "ART 1001 (001)", "day_time": "M 12:00-13:15", "credits": 3, "category": "gened", "gened_type": "GA", "prerequisites": []},
        {"course": "ART 1001 (002)", "day_time": "W 12:00-13:15", "credits": 3, "category": "gened", "gened_type": "GA", "prerequisites": []},
        {"course": "CIS 2100 (001)", "day_time": "F 09:00-10:15", "credits": 3, "category": "major", "prerequisites": ["CIS 1001"]},
        {"course": "CIS 1001 (001)", "day_time": "Th 14:00-15:15", "credits": 3, "category": "major", "prerequisites": []},
        {"course": "FREE 101 (001)", "day_time": "T 10:00-11:15", "credits": 3, "category": "elective", "prerequisites": []},
        {"course": "FREE 102 (001)", "day_time": "W 10:00-11:15", "credits": 3, "category": "elective", "prerequisites": []},
        {"course": "FREE 103 (001)", "day_time": "F 12:00-13:15", "credits": 3, "category": "elective", "prerequisites": []},
    ]
    plan = {}
    student = {
        "min_credits": 12,
        "max_credits": 12,
        "current_semester": 1,
        "taken_courses": [],
        "taken_geneds": [],
        "gened_preference": ["GA"],
    }
    schedules = _run_scheduler(tmp_path, monkeypatch, catalog, plan, student)
    assert schedules
    sched_courses = schedules[0]["courses"]
    gened_types = [c.get("gened_type") for c in sched_courses if c.get("gened_type")]
    assert gened_types.count("GA") == 1

    codes = [helpers.extract_course_code(c["course"]) for c in sched_courses]
    assert "CIS 2100" not in codes  # prereq missing, should be excluded
    assert sum(c["credits"] for c in sched_courses) == 12
