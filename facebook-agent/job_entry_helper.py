"""
Job Entry Helper - Easy way to add jobs to the Facebook agent

This script helps you quickly add jobs from your Correct Tech website
to the Facebook agent's jobs.json file.
"""

import json
import os
from typing import List, Dict


class JobEntryHelper:
    """Helper to easily add and manage jobs."""

    def __init__(self, output_file: str = "jobs.json"):
        self.output_file = output_file
        self.jobs = self._load_existing_jobs()

    def _load_existing_jobs(self) -> List[Dict]:
        """Load existing jobs if file exists."""
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def add_job_interactive(self):
        """Add a job through interactive prompts."""
        print("\n" + "=" * 60)
        print("Add New Job")
        print("=" * 60)

        job = {}

        # Basic info
        job['title'] = input("Job Title: ").strip()
        job['location'] = input("Location (e.g., 'Tel Aviv, Israel'): ").strip()
        job['city'] = input("City: ").strip()

        # Requirements
        print("\nJob Requirements (one per line, press Enter twice when done):")
        requirements = []
        while True:
            req = input("  - ").strip()
            if not req:
                break
            requirements.append(req)
        job['requirements'] = requirements

        # Description
        job['description'] = input("\nJob Description: ").strip()

        # URL
        job['url'] = input("Job URL/Application Link: ").strip()

        # Optional fields
        job['salary'] = input("Salary (optional, press Enter to skip): ").strip() or None
        job['job_type'] = input("Job Type (Full-time/Part-time/Contract, press Enter to skip): ").strip() or None
        job['experience_level'] = input("Experience Level (Entry/Mid/Senior, press Enter to skip): ").strip() or None

        self.jobs.append(job)
        print("\n✓ Job added successfully!")

        return job

    def add_job_from_dict(self, job_data: Dict):
        """Add a job from a dictionary."""
        required_fields = ['title', 'location', 'city', 'requirements', 'description', 'url']

        for field in required_fields:
            if field not in job_data:
                raise ValueError(f"Missing required field: {field}")

        self.jobs.append(job_data)
        print(f"✓ Added: {job_data['title']}")

    def add_jobs_from_text(self, text: str):
        """
        Add jobs from formatted text.

        Expected format:
        ---
        Title: Software Engineer
        Location: Tel Aviv, Israel
        City: Tel Aviv
        Requirements: Python, React, 3+ years experience
        Description: Join our team...
        URL: https://example.com/apply
        Salary: ₪15,000 - ₪20,000
        Job Type: Full-time
        Experience Level: Mid
        ---
        """
        job_blocks = text.strip().split('---')

        for block in job_blocks:
            if not block.strip():
                continue

            job = {}
            lines = block.strip().split('\n')

            for line in lines:
                if ':' not in line:
                    continue

                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()

                if key == 'requirements':
                    # Split by comma
                    job['requirements'] = [req.strip() for req in value.split(',')]
                else:
                    job[key] = value if value else None

            if job.get('title'):
                self.add_job_from_dict(job)

    def remove_job(self, index: int):
        """Remove a job by index."""
        if 0 <= index < len(self.jobs):
            removed = self.jobs.pop(index)
            print(f"✓ Removed: {removed['title']}")
        else:
            print("✗ Invalid index")

    def list_jobs(self):
        """List all jobs."""
        if not self.jobs:
            print("\nNo jobs found.")
            return

        print("\n" + "=" * 60)
        print(f"Current Jobs ({len(self.jobs)} total)")
        print("=" * 60)

        for i, job in enumerate(self.jobs):
            print(f"\n{i+1}. {job['title']}")
            print(f"   Location: {job['location']}")
            print(f"   City: {job['city']}")
            print(f"   Requirements: {', '.join(job['requirements'][:3])}{'...' if len(job['requirements']) > 3 else ''}")
            print(f"   URL: {job['url']}")

    def save(self):
        """Save jobs to file."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Saved {len(self.jobs)} jobs to {self.output_file}")

    def export_to_csv(self, output_file: str = "jobs.csv"):
        """Export jobs to CSV format."""
        import csv

        if not self.jobs:
            print("No jobs to export")
            return

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'location', 'city', 'requirements', 'description', 'url', 'salary', 'job_type', 'experience_level']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            for job in self.jobs:
                # Convert requirements list to comma-separated string
                job_copy = job.copy()
                if isinstance(job_copy.get('requirements'), list):
                    job_copy['requirements'] = ', '.join(job_copy['requirements'])
                writer.writerow(job_copy)

        print(f"✓ Exported to {output_file}")

    def interactive_menu(self):
        """Run interactive menu."""
        while True:
            print("\n" + "=" * 60)
            print("Job Entry Helper")
            print("=" * 60)
            print("1. Add new job (interactive)")
            print("2. Add jobs from text (paste formatted text)")
            print("3. List all jobs")
            print("4. Remove a job")
            print("5. Save to jobs.json")
            print("6. Export to CSV")
            print("7. Exit")
            print("=" * 60)

            choice = input("\nChoose an option (1-7): ").strip()

            if choice == '1':
                self.add_job_interactive()

            elif choice == '2':
                print("\nPaste your formatted text (press Ctrl+D or Ctrl+Z when done):")
                print("Expected format:")
                print("---")
                print("Title: Job Title")
                print("Location: City, Country")
                print("City: City")
                print("Requirements: Req1, Req2, Req3")
                print("Description: Job description")
                print("URL: https://...")
                print("---\n")

                try:
                    import sys
                    text = sys.stdin.read()
                    self.add_jobs_from_text(text)
                except KeyboardInterrupt:
                    print("\nCancelled")

            elif choice == '3':
                self.list_jobs()

            elif choice == '4':
                self.list_jobs()
                try:
                    index = int(input("\nEnter job number to remove: ")) - 1
                    self.remove_job(index)
                except ValueError:
                    print("Invalid number")

            elif choice == '5':
                self.save()

            elif choice == '6':
                self.export_to_csv()

            elif choice == '7':
                print("\nGoodbye!")
                break

            else:
                print("Invalid choice")


def quick_add_jobs():
    """Quick function to add multiple jobs at once."""
    helper = JobEntryHelper()

    # Example: Add jobs quickly with dictionaries
    jobs_data = [
        {
            "title": "Senior Full Stack Developer",
            "location": "Tel Aviv, Israel",
            "city": "Tel Aviv",
            "requirements": [
                "5+ years experience in web development",
                "Strong knowledge of React and Node.js",
                "Experience with TypeScript",
                "Familiarity with AWS or Azure"
            ],
            "description": "We're looking for a Senior Full Stack Developer to join our growing team in Tel Aviv.",
            "url": "https://www.correct-tech.co.il/apply/senior-fullstack",
            "salary": "₪25,000 - ₪35,000",
            "job_type": "Full-time",
            "experience_level": "Senior"
        },
        # Add more jobs here...
    ]

    for job in jobs_data:
        helper.add_job_from_dict(job)

    helper.save()


def main():
    """Main function - run interactive menu."""
    print("Welcome to Job Entry Helper!")
    print("This tool helps you add jobs from Correct Tech to your Facebook agent.")

    helper = JobEntryHelper()
    helper.interactive_menu()


if __name__ == "__main__":
    main()
