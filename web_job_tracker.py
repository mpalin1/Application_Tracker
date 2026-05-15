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
    :root {
        --bg: #f4f6f8;
        --card: #ffffff;
        --text: #111827;
        --muted: #555;
        --border: #ddd;
        --table-header: #e5e7eb;
        --input-bg: #ffffff;
        --input-text: #111827;
        --button-blue: #2563eb;
        --button-red: #dc2626;
        --button-green: #059669;
        --shadow: rgba(0,0,0,0.12);
    }

    body.dark-mode {
        --bg: #1c1f20;
        --card: #171a1b;
        --text: #f3f4f6;
        --muted: #c7c7c7;
        --border: #33383b;
        --table-header: #25292b;
        --input-bg: #3a3a3a;
        --input-text: #f3f4f6;
        --button-blue: #0f4fc4;
        --button-red: #b91c1c;
        --button-green: #047857;
        --shadow: rgba(0,0,0,0.35);
    }

	

    body {
        font-family: Arial, sans-serif;
        background: var(--bg);
        color: var(--text);
        margin: 0;
        padding: 20px;
    }

    h1 {
        text-align: center;
        font-size: 34px;
        margin-bottom: 25px;
    }

    h2 {
        margin-top: 0;
    }

    .top-bar {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 10px;
}

.theme-toggle {
    cursor: pointer;
    border: none;
    border-radius: 50%;
    background: var(--card);
    color: var(--text);
    width: 44px;
    height: 44px;
    font-size: 22px;
    box-shadow: 0 2px 8px var(--shadow);
    border: 1px solid var(--border);
}

    .container {
        display: grid;
        grid-template-columns: 1fr 1.5fr;
        gap: 20px;
    }

    .card {
        background: var(--card);
        color: var(--text);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px var(--shadow);
    }

    textarea {
        width: 100%;
        height: 330px;
        font-family: Consolas, monospace;
        font-size: 14px;
        background: var(--input-bg);
        color: var(--input-text);
        border: 1px solid var(--border);
    }

    input, select, button {
        padding: 8px;
        margin: 4px 0;
        background: var(--input-bg);
        color: var(--input-text);
        border: 1px solid var(--border);
    }

    button {
        cursor: pointer;
        border: none;
        border-radius: 6px;
        background: var(--button-blue);
        color: white;
    }

    button.delete {
        background: var(--button-red);
    }

    button.export {
        background: var(--button-green);
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: var(--card);
        color: var(--text);
    }

    body.dark-mode tr.date-group-even td {
        background: #15191a;
    }

    body.dark-mode tr.date-group-odd td {
        background: #202526;
    }

    body:not(.dark-mode) tr.date-group-even td {
        background: #ffffff;
    }

    body:not(.dark-mode) tr.date-group-odd td {
        background: #eef2f7;
    }

    tr.date-group-even td,
    tr.date-group-odd td {
        transition: background 0.2s ease;
    }

    th, td {
        border-bottom: 1px solid var(--border);
        padding: 8px;
        text-align: left;
        font-size: 14px;
    }

    th {
        background: var(--table-header);
    }

    a {
        color: #3b82f6;
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
        color: var(--muted);
        font-size: 13px;
    }

    .status {
        font-weight: bold;
    }

    .title-link {
        color: #3b82f6;
        text-decoration: underline;
        cursor: pointer;
        background: none;
        border: none;
        padding: 0;
        font-size: 14px;
    }

    .modal {
        display: none;
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.65);
    }

    .modal-content {
        background: var(--card);
        color: var(--text);
        margin: 8% auto;
        padding: 20px;
        border-radius: 12px;
        width: 55%;
        box-shadow: 0 4px 12px var(--shadow);
        border: 1px solid var(--border);
    }

    .close {
        float: right;
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
    }

    .detail-line {
        margin: 8px 0;
    }
</style>
</head>

<body class="dark-mode">
    <h1>Job Application Tracker</h1>

    <div class="top-bar">
    <button id="themeButton" class="theme-toggle" type="button" onclick="toggleTheme()" title="Toggle theme">
        🌙
    </button>
</div>

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
                <tr class="{{ job.date_group_class }}">
                    <td>{{ job.date_applied }}</td>
                    <td>{{ job.company }}</td>
                                        <td>
                        <button class="title-link" type="button" onclick="openModal('modal-{{ loop.index0 }}')">
                            {{ job.title }}
                        </button>

                        <div id="modal-{{ loop.index0 }}" class="modal">
                            <div class="modal-content">
                                <span class="close" onclick="closeModal('modal-{{ loop.index0 }}')">&times;</span>

                                <h2>{{ job.title }}</h2>

                                <p class="detail-line"><strong>Date Applied:</strong> {{ job.date_applied }}</p>
                                <p class="detail-line"><strong>Company:</strong> {{ job.company }}</p>
                                <p class="detail-line"><strong>Salary:</strong> {{ job.salary }}</p>
                                <p class="detail-line"><strong>Location:</strong> {{ job.location }}</p>
                                <p class="detail-line"><strong>Status:</strong> {{ job.status }}</p>
                                <p class="detail-line"><strong>Resume Used:</strong> {{ job.resume }}</p>

                                {% if job.link %}
                                    <p class="detail-line">
                                        <strong>Job Link:</strong>
                                        <a href="{{ job.link }}" target="_blank">Open job posting</a>
                                    </p>
                                {% endif %}

                                <p class="detail-line"><strong>Notes:</strong></p>
                                <p>{{ job.notes }}</p>
                            </div>
                        </div>
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
    <script>
    function openModal(id) {
        document.getElementById(id).style.display = "block";
    }

    function closeModal(id) {
        document.getElementById(id).style.display = "none";
    }

    function updateThemeButton() {
    let themeButton = document.getElementById("themeButton");

    if (document.body.classList.contains("dark-mode")) {
        themeButton.textContent = "☀️";
        themeButton.title = "Switch to light mode";
    } else {
        themeButton.textContent = "🌙";
        themeButton.title = "Switch to dark mode";
    }
}

function toggleTheme() {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }

    updateThemeButton();
}

window.onload = function() {
    let savedTheme = localStorage.getItem("theme");

    if (savedTheme === "light") {
        document.body.classList.remove("dark-mode");
    } else {
        document.body.classList.add("dark-mode");
    }

    updateThemeButton();
};

    window.onclick = function(event) {
        let modals = document.getElementsByClassName("modal");

        for (let i = 0; i < modals.length; i++) {
            if (event.target === modals[i]) {
                modals[i].style.display = "none";
            }
        }
    };
</script>
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

    current_date = None
    group_number = -1

    for job in jobs:
        job_date = job.get("date_applied", "")

        if job_date != current_date:
            current_date = job_date
            group_number += 1

        if group_number % 2 == 0:
            job["date_group_class"] = "date-group-even"
        else:
            job["date_group_class"] = "date-group-odd"

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