# Application Tracker

Application Tracker is a Python-based job application helper that helps organize job applications and speed up repetitive application form filling.

The project includes a local job tracker, an autofill profile system, and a simple web-based tracker option.

## Features

- Track job applications in one place
- Store reusable application information in a JSON profile
- Autofill common job application fields
- Keep track of companies, job titles, links, dates, and application status
- Use a web-based tracker interface
- Maintain a local resume/profile setup for faster applications

## Project Files

```text
Application_Tracker/
│
├── autofill_job_application.py   # Script for autofilling job application fields
├── autofill_profile.json         # Local profile data used by the autofill script
├── job_tracker.py                # Main job tracker program
├── web_job_tracker.py            # Web-based job tracker version
├── requirements.txt              # Python package requirements
├── README.md                     # Project documentation
└── .gitignore                    # Files that should not be uploaded to GitHub