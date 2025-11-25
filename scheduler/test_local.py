import json
from scheduler.generator import generate_schedules

def print_schedule(idx, sched):
    print(f"\n=== Schedule {idx} ===")
    for c in sched["courses"]:
        print(
            f"{c['course']} | {c['day_time']} | {c['credits']}cr | "
            f"{c['category']} | gened={c['gened_type']} | mode={c['mode']} | prof={c['instructor']}"
        )
    print(f"Total credits: {sched['total_credits']}")
    print("Progress report:", json.dumps(sched["progress_report"], indent=2))


def main():
    print("Running scheduler locally...\n")

    schedules = generate_schedules("scheduler/mock_student.json", num_schedules=7)

    if not schedules:
        print("❌ No schedules returned!")
        return

    for idx, sched in enumerate(schedules, start=1):
        print_schedule(idx, sched)


if __name__ == "__main__":
    main()
