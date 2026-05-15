import json
import os
from datetime import datetime
from flask import Flask, request, redirect, render_template_string, url_for

app = Flask(__name__)

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

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_jobs(jobs):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=4)


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
        job["status"] = "waiting"

    return job


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Job Application Tracker</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        .container {
            display: grid;
            grid-template-columns: 1fr 1.5fr;
            gap: 20px;
        }

        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        }

        textarea {
            width: 100%;
            height: 330px;
            font-family: Consolas, monospace;
            font-size: 14px;
        }

        input, select, button {
            padding: 8px;
            margin: 4px 0;
        }

        button {
            cursor: pointer;
            border: none;
            border-radius: 6px;
            background: #2563eb;
            color: white;
        }

        button.delete {
            background: #dc2626;
        }

        button.export {
            background: #059669;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th, td {
            border-bottom: 1px solid #ddd;
            padding: 8px;
            text-align: left;
            font-size: 14px;
        }

        th {
            background: #e5e7eb;
        }

        .search-box {
            display: flex;
            gap: 6px;
            margin-bottom: 12px;
        }

        .search-box input {
            flex: 1;
        }

        .small-text {
            color: #555;
            font-size: 13px;
        }

        .status {
            font-weight: bold;
        }
    </style>
</head>

<body>
    <h1>Job Application Tracker</h1>

    <div class="container">
        <div class="card">
            <h2>Add Application</h2>

            <p class="small-text">Paste one job application block below.</p>

            <form method="POST" action="/add">
                <textarea name="application_text" placeholder="date applied: 2026-05-15
company: Lockheed Martin
title: Embedded Software Engineer
salary: 75000
location: Orlando, FL
status: waiting
link: https://example.com/job
resume: embedded resume
notes: Entry level role."></textarea>

                <br>
                <button type="submit">Save Application</button>
            </form>

            <br>

            <form method="POST" action="/export">
                <button class="export" type="submit">Export TXT Report</button>
            </form>
        </div>

        <div class="card">
            <h2>Saved Applications</h2>

            <form class="search-box" method="GET" action="/">
                <input type="text" name="search" placeholder="Search company or title" value="{{ search }}">
                <button type="submit">Search</button>
                <a href="/"><button type="button">Show All</button></a>
            </form>

            <table>
                <tr>
                    <th>Date</th>
                    <th>Company</th>
                    <th>Title</th>
                    <th>Salary</th>
                    <th>Location</th>
                    <th>Status</th>
                    <th>Update</th>
                    <th>Delete</th>
                </tr>

                {% for job in jobs %}
                <tr>
                    <td>{{ job.date_applied }}</td>
                    <td>{{ job.company }}</td>
                    <td>
                        {% if job.link %}
                            <a href="{{ job.link }}" target="_blank">{{ job.title }}</a>
                        {% else %}
                            {{ job.title }}
                        {% endif %}
                        <br>
                        <span class="small-text">{{ job.notes }}</span>
                    </td>
                    <td>{{ job.salary }}</td>
                    <td>{{ job.location }}</td>
                    <td class="status">{{ job.status }}</td>
                    <td>
                        <form method="POST" action="/update/{{ loop.index0 }}">
                            <select name="status">
                                {% for status in statuses %}
                                    <option value="{{ status }}" {% if status == job.status %}selected{% endif %}>
                                        {{ status }}
                                    </option>
                                {% endfor %}
                            </select>
                            <button type="submit">Save</button>
                        </form>
                    </td>
                    <td>
                        <form method="POST" action="/delete/{{ loop.index0 }}">
                            <button class="delete" type="submit">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    jobs = load_jobs()
    search = request.args.get("search", "").strip().lower()

    if search:
        jobs = [
            job for job in jobs
            if search in job.get("company", "").lower()
            or search in job.get("title", "").lower()
        ]

    jobs.sort(key=lambda x: x.get("date_applied", ""))

    return render_template_string(
        HTML,
        jobs=jobs,
        statuses=VALID_STATUSES,
        search=search
    )


@app.route("/add", methods=["POST"])
def add_application():
    text = request.form.get("application_text", "").strip()

    if text:
        job = parse_application(text)

        if job["company"] and job["title"]:
            jobs = load_jobs()
            jobs.append(job)
            jobs.sort(key=lambda x: x.get("date_applied", ""))
            save_jobs(jobs)

    return redirect(url_for("home"))


@app.route("/update/<int:index>", methods=["POST"])
def update_status(index):
    jobs = load_jobs()

    if 0 <= index < len(jobs):
        new_status = request.form.get("status", "").strip().lower()

        if new_status in VALID_STATUSES:
            jobs[index]["status"] = new_status
            save_jobs(jobs)

    return redirect(url_for("home"))


@app.route("/delete/<int:index>", methods=["POST"])
def delete_application(index):
    jobs = load_jobs()

    if 0 <= index < len(jobs):
        jobs.pop(index)
        save_jobs(jobs)

    return redirect(url_for("home"))


@app.route("/export", methods=["POST"])
def export_txt_report():
    jobs = load_jobs()
    jobs.sort(key=lambda x: x.get("date_applied", ""))

    report_file = "job_applications_report.txt"

    with open(report_file, "w", encoding="utf-8") as file:
        current_date = None

        for job in jobs:
            if job.get("date_applied", "") != current_date:
                current_date = job.get("date_applied", "")
                file.write("\n")
                file.write("=" * 40 + "\n")
                file.write(f"{current_date}\n")
                file.write("=" * 40 + "\n\n")

            file.write(f"Company: {job.get('company', '')}\n")
            file.write(f"Title: {job.get('title', '')}\n")
            file.write(f"Salary: {job.get('salary', '')}\n")
            file.write(f"Location: {job.get('location', '')}\n")
            file.write(f"Status: {job.get('status', '')}\n")
            file.write(f"Link: {job.get('link', '')}\n")
            file.write(f"Resume Used: {job.get('resume', '')}\n")
            file.write(f"Notes: {job.get('notes', '')}\n")
            file.write("-" * 40 + "\n\n")

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)