from scheduler.generator import generate_schedules

def main():
    schedules = generate_schedules("data/student_progress.json", num_schedules=3)
    for idx, sched in enumerate(schedules, start=1):
        print(f"\n--- Schedule {idx} ---")
        for c in sched["courses"]:
            print(f"{c['course']} | {c['day_time']} | {c['credits']}cr | "
                  f"{c['category']} | gened={c['gened_type']} | mode={c['mode']} | prof={c['instructor']}")
        print(f"Total credits: {sched['total_credits']}")
        print("Progress report:", sched["progress_report"])

if __name__ == "__main__":
    main()