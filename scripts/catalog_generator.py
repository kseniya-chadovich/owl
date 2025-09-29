import csv
import json
import re

classes = []

def get_course_number(course_name):
    """
    Extracts the numeric part of a course code.
    e.g., "ART 1010" -> 1010
    Returns None if not found.
    """
    match = re.search(r'(\d{3,4})', course_name)
    if match:
        return int(match.group(1))
    return None

with open("schedule.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if len(row) < 9:
            continue
        if row[0].startswith("web-scraper-order"):
            continue

        course = row[2]        # e.g., "CIS 1000 (801)"
        instructor = row[5]
        day_time = row[6]
        credits = int(row[8])

        section = course.split("(")[-1].strip(")")
        mode = "online" if section.startswith("7") else "offline"

        # ------------------- Metadata -------------------
        course_number = get_course_number(course)

        if course.startswith("CIS"):
            category = "major"
            gened_type = None
            prerequisites = []  # manually fill later for major courses
        else:
            if course_number is not None and course_number < 2000:
                category = "gened"
            else:
                category = "elective"
            gened_type = None
            prerequisites = []

        semester_recommended = None

        course_dict = {
            "course": course,
            "section": section,
            "instructor": instructor,
            "day_time": day_time,
            "credits": credits,
            "mode": mode,
            "category": category,
            "gened_type": gened_type,
            "prerequisites": prerequisites,
            "semester_recommended": semester_recommended
        }

        classes.append(course_dict)

# ------------------- Print summary -------------------
print(f"Total courses parsed: {len(classes)}\n")
for i, c in enumerate(classes, 1):
    print(f"{i}. {c['course']} | {c['category']} | "
          f"GenEd Type: {c['gened_type']} | Credits: {c['credits']} | "
          f"Mode: {c['mode']} | Section: {c['section']} | Instructor: {c['instructor']} | Time: {c['day_time']}")

# Save to JSON
with open("course_catalog.json", "w", encoding="utf-8") as f:
    json.dump(classes, f, indent=4)

print("\nSaved all courses to course_catalog.json")
