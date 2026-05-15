# Application Tracker

A Python job application tracking tool that helps organize job applications during the job search process.

The project includes both a terminal version and a web browser version.

## Features

- Add job applications using one pasted text block
- Save application data locally
- Search applications by company or job title
- Update application status
- Export a TXT report
- Web interface that opens in Google Chrome
- Job details pop-up when clicking the job title
- Light mode / dark mode toggle

## Application Fields

Each application can include:

- Date applied
- Company name
- Job title
- Salary
- Location
- Status
- Job link
- Resume used
- Notes

## Status Options

- interested
- applied
- waiting
- interview
- rejected
- offer
- no response
- closed

## Example Input

Paste the job application using this format:

```text
date applied: 2026-05-15
company: Lockheed Martin
title: Embedded Software Engineer
salary: 78000
location: Orlando, FL
status: waiting
link: https://example.com/job
resume: embedded resume
notes: Entry level role, matches C, hardware, and defense experience.