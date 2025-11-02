"""
Correct Tech Job Scraper

This script can be used to scrape jobs from your Correct Tech website.
Since the site requires authentication (code 502304544), you'll need to
either run this with Selenium/Playwright or manually copy the data.
"""

import json
from typing import List, Dict, Optional


def scrape_with_selenium(url: str, access_code: str) -> List[Dict]:
    """
    Scrape jobs using Selenium (requires browser automation).

    To use this:
    1. Install Selenium: pip install selenium
    2. Download ChromeDriver: https://chromedriver.chromium.org/
    3. Run this function

    Args:
        url: The Correct Tech URL
        access_code: Your access code (502304544)

    Returns:
        List of job dictionaries
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
    except ImportError:
        print("Error: Selenium not installed. Run: pip install selenium")
        return []

    # Initialize browser
    driver = webdriver.Chrome()
    jobs = []

    try:
        # Go to the URL
        driver.get(url)

        # Wait for page to load
        time.sleep(2)

        # Find and enter access code
        # Note: You'll need to inspect the page to find the correct selectors
        try:
            code_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'], input[type='password'], input"))
            )
            code_input.send_keys(access_code)

            # Find and click submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button")
            submit_button.click()

            time.sleep(3)
        except:
            print("Could not find login form - page might be structured differently")

        # Now scrape the jobs
        # Note: You'll need to customize these selectors based on the actual page structure
        job_elements = driver.find_elements(By.CSS_SELECTOR, ".job-listing, .job-item, .position")

        for job_elem in job_elements:
            try:
                job = {
                    'title': job_elem.find_element(By.CSS_SELECTOR, ".title, h2, h3").text.strip(),
                    'location': job_elem.find_element(By.CSS_SELECTOR, ".location, .city").text.strip(),
                    'city': '',  # Extract from location
                    'requirements': [],
                    'description': job_elem.find_element(By.CSS_SELECTOR, ".description, .details").text.strip(),
                    'url': url,  # Or get specific job URL
                    'salary': None,
                    'job_type': None,
                    'experience_level': None
                }

                # Extract city from location
                if ',' in job['location']:
                    job['city'] = job['location'].split(',')[0].strip()
                else:
                    job['city'] = job['location']

                # Extract requirements if available
                try:
                    req_elements = job_elem.find_elements(By.CSS_SELECTOR, ".requirements li, .skills li")
                    job['requirements'] = [elem.text.strip() for elem in req_elements]
                except:
                    pass

                jobs.append(job)
            except Exception as e:
                print(f"Error parsing job: {e}")
                continue

    finally:
        driver.quit()

    return jobs


def manual_entry_template() -> str:
    """
    Return a template for manually entering jobs.

    Copy this template, fill it out for each job from your Correct Tech site,
    and use the job_entry_helper.py to import it.
    """
    return """
---
Title: [Job Title from Correct Tech]
Location: [Full Location, e.g., Tel Aviv, Israel]
City: [City only, e.g., Tel Aviv]
Requirements: [Requirement 1], [Requirement 2], [Requirement 3]
Description: [Full job description]
URL: https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba
Salary: [Optional - salary range]
Job Type: Full-time
Experience Level: [Entry/Mid/Senior]
---

Example:
---
Title: Senior Python Developer
Location: Tel Aviv, Israel
City: Tel Aviv
Requirements: 5+ years Python, Django/Flask experience, PostgreSQL, RESTful APIs
Description: Join our team as a Senior Python Developer. You'll work on building scalable backend systems for our clients.
URL: https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba
Salary: ₪20,000 - ₪28,000
Job Type: Full-time
Experience Level: Senior
---

Copy this template for each job, then use:
python job_entry_helper.py
Choose option 2 and paste your formatted jobs.
"""


def create_jobs_from_correct_tech_manually():
    """
    Helper function - add your jobs here manually, then run this script.

    This is the EASIEST way to get started!

    Steps:
    1. Go to https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba
    2. Enter code: 502304544
    3. Copy the job information
    4. Fill out the jobs list below
    5. Run: python correct_tech_scraper.py
    """

    jobs = [
        {
            "title": "Example: Senior Full Stack Developer",
            "location": "Tel Aviv, Israel",
            "city": "Tel Aviv",
            "requirements": [
                "5+ years experience in web development",
                "React and Node.js",
                "TypeScript",
                "AWS or Azure experience"
            ],
            "description": "Join our team as a Full Stack Developer...",
            "url": "https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba",
            "salary": "₪25,000 - ₪35,000",
            "job_type": "Full-time",
            "experience_level": "Senior"
        },
        # TODO: Add your real jobs here!
        # Copy the template above for each job from your Correct Tech site
    ]

    # Save to jobs.json
    output_file = "jobs.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print(f"✓ Saved {len(jobs)} jobs to {output_file}")
    print(f"\nNext steps:")
    print(f"1. Edit this file (correct_tech_scraper.py) and add your real jobs")
    print(f"2. Run: python correct_tech_scraper.py")
    print(f"3. Or use the interactive helper: python job_entry_helper.py")


def export_template_for_manual_fill():
    """Create a text file template for easy copy/paste."""
    template = manual_entry_template()

    with open("job_template.txt", "w", encoding='utf-8') as f:
        f.write("CORRECT TECH JOB ENTRY TEMPLATE\n")
        f.write("=" * 60 + "\n\n")
        f.write("Instructions:\n")
        f.write("1. Go to: https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba\n")
        f.write("2. Enter code: 502304544\n")
        f.write("3. For each job, copy this template and fill it out:\n\n")
        f.write(template)
        f.write("\n\n")
        f.write("After filling out your jobs:\n")
        f.write("1. Save this file\n")
        f.write("2. Run: python job_entry_helper.py\n")
        f.write("3. Choose option 2 (Add jobs from text)\n")
        f.write("4. Copy and paste your filled templates\n")

    print("✓ Created job_template.txt")
    print("  Open this file and use it to enter your jobs!")


def main():
    """Main function."""
    print("=" * 60)
    print("Correct Tech Job Scraper")
    print("=" * 60)
    print("\nOptions:")
    print("1. Create manual entry template")
    print("2. Add jobs manually (edit this script)")
    print("3. Use Selenium scraper (advanced - requires setup)")
    print("=" * 60)

    choice = input("\nChoose option (1-3): ").strip()

    if choice == '1':
        export_template_for_manual_fill()
        print("\n✓ Template created! Open job_template.txt to start entering jobs.")

    elif choice == '2':
        print("\n✓ Edit this file (correct_tech_scraper.py)")
        print("  Find the 'create_jobs_from_correct_tech_manually' function")
        print("  Add your jobs to the 'jobs' list")
        print("  Then run this script again")
        create_jobs_from_correct_tech_manually()

    elif choice == '3':
        print("\n⚠️  Selenium scraper requires:")
        print("  1. pip install selenium")
        print("  2. ChromeDriver installed")
        print("  3. Customizing selectors for your site")
        print("\nThis is advanced - consider using option 1 or 2 instead.")

        proceed = input("\nProceed anyway? (y/n): ").lower()
        if proceed == 'y':
            url = "https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba"
            code = "502304544"
            jobs = scrape_with_selenium(url, code)

            if jobs:
                with open("jobs.json", 'w', encoding='utf-8') as f:
                    json.dump(jobs, f, indent=2, ensure_ascii=False)
                print(f"✓ Scraped {len(jobs)} jobs!")
            else:
                print("No jobs found - you may need to customize the scraper")

    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
