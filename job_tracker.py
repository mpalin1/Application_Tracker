import json
import os
from datetime import datetime

DATA_FILE = "job_applications.json"

VALID_STATUSES = [
    "interested",
    "applied",
    "waiting",
    "interview",
    "rejected",
    "offer",
    "no response",
    "closed"
]


def load_jobs():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_jobs(jobs):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=4)


def get_multiline_input():
    print("\nPaste the job application information below.")
    print("Use this format: field: value")
    print("When finished, type DONE on a new line.\n")

    lines = []

    while True:
        line = input()
        if line.strip().lower() == "done":
            break
        lines.append(line)

    return "\n".join(lines)


def parse_application(text):
    job = {
        "date_applied": "",
        "company": "",
        "title": "",
        "salary": "",
        "location": "",
        "status": "waiting",
        "link": "",
        "resume": "",
        "notes": ""
    }

    field_map = {
        "date applied": "date_applied",
        "date": "date_applied",
        "company": "company",
        "company name": "company",
        "title": "title",
        "job title": "title",
        "salary": "salary",
        "location": "location",
        "status": "status",
        "link": "link",
        "job link": "link",
        "resume": "resume",
        "resume used": "resume",
        "notes": "notes",
        "note": "notes"
    }

    for line in text.splitlines():
        if ":" not in line:
            continue

        field, value = line.split(":", 1)
        field = field.strip().lower()
        value = value.strip()

        if field in field_map:
            job[field_map[field]] = value

    if job["date_applied"] == "":
        job["date_applied"] = datetime.today().strftime("%Y-%m-%d")

    job["status"] = job["status"].lower()

    if job["status"] not in VALID_STATUSES:
        print(f"\nStatus '{job['status']}' is not recognized.")
        print("Status was changed to 'waiting'.")
        job["status"] = "waiting"

    return job


def add_application():
    text = get_multiline_input()
    job = parse_application(text)

    if job["company"] == "" or job["title"] == "":
        print("\nError: company and title are required.")
        return

    jobs = load_jobs()
    jobs.append(job)

    jobs.sort(key=lambda x: x["date_applied"])

    save_jobs(jobs)

    print("\nApplication saved successfully.")


def view_all_applications():
    jobs = load_jobs()

    if not jobs:
        print("\nNo applications saved yet.")
        return

    print("\n==== All Job Applications ====\n")

    for index, job in enumerate(jobs, start=1):
        print(f"{index}. {job['date_applied']} - {job['company']} - {job['title']}")
        print(f"   Status: {job['status']}")
        print(f"   Location: {job['location']}")
        print(f"   Salary: {job['salary']}")
        print()


def search_applications():
    jobs = load_jobs()

    if not jobs:
        print("\nNo applications saved yet.")
        return []

    search_term = input("\nEnter company or title to search: ").strip().lower()

    results = []

    for index, job in enumerate(jobs):
        company = job["company"].lower()
        title = job["title"].lower()

        if search_term in company or search_term in title:
            results.append((index, job))

    if not results:
        print("\nNo matching applications found.")
        return []

    print("\n==== Search Results ====\n")

    for result_number, (index, job) in enumerate(results, start=1):
        print(f"{result_number}. {job['date_applied']} - {job['company']} - {job['title']}")
        print(f"   Status: {job['status']}")
        print(f"   Location: {job['location']}")
        print(f"   Salary: {job['salary']}")
        print()

    return results


def update_status():
    jobs = load_jobs()
    results = search_applications()

    if not results:
        return

    try:
        choice = int(input("Choose the number to update: "))
    except ValueError:
        print("\nInvalid number.")
        return

    if choice < 1 or choice > len(results):
        print("\nInvalid choice.")
        return

    job_index = results[choice - 1][0]
    selected_job = jobs[job_index]

    print("\nValid statuses:")
    for status in VALID_STATUSES:
        print(f"- {status}")

    new_status = input("\nEnter new status: ").strip().lower()

    if new_status not in VALID_STATUSES:
        print("\nInvalid status. No changes made.")
        return

    selected_job["status"] = new_status
    save_jobs(jobs)

    print("\nStatus updated successfully.")


def export_txt_report():
    jobs = load_jobs()

    if not jobs:
        print("\nNo applications to export.")
        return

    jobs.sort(key=lambda x: x["date_applied"])

    report_file = "job_applications_report.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        current_date = None

        for job in jobs:
            if job["date_applied"] != current_date:
                current_date = job["date_applied"]
                file.write("\n")
                file.write("=" * 40 + "\n")
                file.write(f"{current_date}\n")
                file.write("=" * 40 + "\n\n")

            file.write(f"Company: {job['company']}\n")
            file.write(f"Title: {job['title']}\n")
            file.write(f"Salary: {job['salary']}\n")
            file.write(f"Location: {job['location']}\n")
            file.write(f"Status: {job['status']}\n")
            file.write(f"Link: {job['link']}\n")
            file.write(f"Resume Used: {job['resume']}\n")
            file.write(f"Notes: {job['notes']}\n")
            file.write("-" * 40 + "\n\n")

    print(f"\nReport exported to {report_file}.")


def main():
    while True:
        print("\n==== Job Application Tracker ====")
        print("1. Add new application")
        print("2. View all applications")
        print("3. Search applications")
        print("4. Update application status")
        print("5. Export TXT report")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_application()
        elif choice == "2":
            view_all_applications()
        elif choice == "3":
            search_applications()
        elif choice == "4":
            update_status()
        elif choice == "5":
            export_txt_report()
        elif choice == "6":
            print("\nGoodbye.")
            break
        else:
            print("\nInvalid choice. Try again.")


if __name__ == "__main__":
    main()