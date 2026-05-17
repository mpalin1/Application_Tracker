import json
from playwright.sync_api import sync_playwright

PROFILE_FILE = "autofill_profile.json"


def load_profile():
    with open(PROFILE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def try_fill_by_label(page, label_text, value):
    try:
        page.get_by_label(label_text, exact=False).fill(value, timeout=800)
        print(f"Filled by label: {label_text}")
        return True
    except Exception:
        return False


def try_fill_by_placeholder(page, placeholder_text, value):
    try:
        page.get_by_placeholder(placeholder_text, exact=False).fill(value, timeout=800)
        print(f"Filled by placeholder: {placeholder_text}")
        return True
    except Exception:
        return False


def safe_fill(page, possible_labels, possible_placeholders, value):
    if not value:
        return

    for label in possible_labels:
        if try_fill_by_label(page, label, value):
            return

    for placeholder in possible_placeholders:
        if try_fill_by_placeholder(page, placeholder, value):
            return

    print(f"Could not auto-fill: {possible_labels[0] if possible_labels else 'unknown field'}")



def fill_current_page(page, profile):
    safe_fill(page, ["First Name", "Given Name"], ["First Name", "Given Name"], profile.get("first_name", ""))
    safe_fill(page, ["Middle Name"], ["Middle Name"], profile.get("middle_name", ""))
    safe_fill(page, ["Last Name", "Family Name", "Surname"], ["Last Name", "Family Name", "Surname"], profile.get("last_name", ""))
    safe_fill(page, ["Full Name", "Name"], ["Full Name", "Name"], profile.get("full_name", ""))

    safe_fill(page, ["Email", "Email Address"], ["Email", "Email Address"], profile.get("email", ""))
    safe_fill(page, ["Phone", "Phone Number", "Mobile Phone"], ["Phone", "Phone Number", "Mobile Phone"], profile.get("phone", ""))

    safe_fill(
        page,
        ["Address", "Address Line 1", "Street Address", "Street Address 1", "Address 1"],
        ["Address", "Address Line 1", "Street Address", "Street Address 1", "Address 1"],
        profile.get("address", "")
    )

    safe_fill(page, ["City", "Town"], ["City", "Town"], profile.get("city", ""))

    safe_fill(
        page,
        ["State", "Province", "State/Province", "Region"],
        ["State", "Province", "State/Province", "Region"],
        profile.get("state", "")
    )

    safe_fill(
        page,
        ["Postal Code", "Zip", "ZIP", "ZIP Code", "Zip Code"],
        ["Postal Code", "Zip", "ZIP", "ZIP Code", "Zip Code"],
        profile.get("zip", "")
    )

    safe_fill(page, ["Country"], ["Country"], profile.get("country", ""))

    safe_fill(page, ["School", "University", "College"], ["School", "University", "College"], profile.get("school", ""))
    safe_fill(page, ["Degree"], ["Degree"], profile.get("degree", ""))
    safe_fill(page, ["Graduation Date", "Graduation"], ["Graduation Date", "Graduation"], profile.get("graduation_date", ""))

    safe_fill(page, ["LinkedIn", "LinkedIn Profile"], ["LinkedIn", "LinkedIn Profile"], profile.get("linkedin", ""))
    safe_fill(page, ["GitHub", "Portfolio"], ["GitHub", "Portfolio"], profile.get("github", ""))

    safe_fill(page, ["Job Title"], ["Job Title"], profile.get("work_experience_1_title", ""))
    safe_fill(page, ["Company"], ["Company"], profile.get("work_experience_1_company", ""))
    safe_fill(page, ["Location"], ["Location"], profile.get("work_experience_1_location", ""))
    safe_fill(page, ["From"], ["MM/YYYY"], profile.get("work_experience_1_from", ""))
    safe_fill(page, ["To"], ["MM/YYYY"], profile.get("work_experience_1_to", ""))
    safe_fill(page, ["Role Description"], ["Role Description"], profile.get("work_experience_1_description", ""))

    safe_fill(page, ["School or University"], ["School or University"], profile.get("school", ""))
    safe_fill(page, ["Field of Study"], ["Field of Study"], profile.get("field_of_study", ""))
    safe_fill(page, ["Overall Result (GPA)"], ["Overall Result (GPA)"], profile.get("gpa", ""))
    safe_fill(page, ["Type to Add Skills"], ["Type to Add Skills"], profile.get("skills", ""))




def main():
    profile = load_profile()

    url = input("Paste the job application URL: ").strip()

    with sync_playwright() as p:
        user_data_dir = "playwright_chrome_profile"

        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            slow_mo=150
        )

        page = browser.new_page()

        # Give Workday enough time to load the page
        page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # After the page loads, use a short timeout for autofill attempts
        page.set_default_timeout(1000)


        print("\nPage opened.")
        print("If the website requires login, log in manually first.")
        print("When a form page is visible, come back here.")

        while True:
            choice = input("\nPress ENTER to autofill the current page, or type q to quit: ").strip().lower()

            if choice == "q":
                break

            fill_current_page(page, profile)

            print("\nAutofill attempt finished for this page.")
            print("Review the page carefully.")
            print("Click Next / Save and Continue manually, then press ENTER here again for the next page.")

        browser.close()



if __name__ == "__main__":
    main()