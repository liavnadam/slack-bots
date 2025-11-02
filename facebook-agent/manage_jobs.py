"""
מנהל משרות - Job Manager
ממשק פשוט לניהול המשרות שלכם

Simple interface for managing your jobs - add, remove, update jobs easily!
"""

import json
import os
from datetime import datetime
from typing import List, Dict


class JobManager:
    """מנהל משרות פשוט - Simple Job Manager"""

    def __init__(self, jobs_file: str = "jobs.json"):
        self.jobs_file = jobs_file
        self.jobs = self._load_jobs()

    def _load_jobs(self) -> List[Dict]:
        """טען משרות קיימות - Load existing jobs"""
        if os.path.exists(self.jobs_file):
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_jobs(self):
        """שמור משרות - Save jobs"""
        with open(self.jobs_file, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)

        # Create backup
        backup_file = f"{self.jobs_file}.backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, indent=2, ensure_ascii=False)

        print(f"✓ נשמר! Saved to {self.jobs_file}")
        print(f"✓ גיבוי נוצר! Backup created: {backup_file}")

    def list_jobs(self):
        """הצג את כל המשרות - List all jobs"""
        if not self.jobs:
            print("\n❌ אין משרות! No jobs found.")
            print("💡 הוסף משרות עם אפשרות 2")
            return

        print("\n" + "=" * 70)
        print(f"📋 המשרות שלכם - Your Jobs ({len(self.jobs)} total)")
        print("=" * 70)

        for i, job in enumerate(self.jobs, 1):
            print(f"\n{i}. {job['title']}")
            print(f"   📍 מיקום: {job['location']}")
            print(f"   💼 דרישות: {', '.join(job['requirements'][:2])}...")
            print(f"   💰 שכר: {job.get('salary', 'לא צוין')}")
            print(f"   📊 סוג משרה: {job.get('job_type', 'לא צוין')}")

        print("\n" + "=" * 70)

    def add_job(self):
        """הוסף משרה חדשה - Add new job"""
        print("\n" + "=" * 70)
        print("➕ הוספת משרה חדשה - Add New Job")
        print("=" * 70)

        job = {}

        # Basic info
        job['title'] = input("\n🏷️  שם המשרה (Job Title): ").strip()
        if not job['title']:
            print("❌ חובה למלא שם משרה!")
            return

        job['location'] = input("📍 מיקום (Location) [ברירת מחדל: פתח תקווה, ישראל]: ").strip()
        if not job['location']:
            job['location'] = "פתח תקווה, ישראל"

        job['city'] = input("🏙️  עיר (City) [ברירת מחדל: Petah Tikva]: ").strip()
        if not job['city']:
            job['city'] = "Petah Tikva"

        # Requirements
        print("\n📋 דרישות המשרה (Requirements)")
        print("   (כתוב דרישה אחת בכל שורה, Enter פעמיים לסיום)")
        requirements = []
        req_num = 1
        while True:
            req = input(f"   {req_num}. ").strip()
            if not req:
                break
            requirements.append(req)
            req_num += 1

        if not requirements:
            print("⚠️  לא הוספו דרישות - אפשר להוסיף אחר כך")

        job['requirements'] = requirements

        # Description
        print("\n📝 תיאור המשרה (Job Description)")
        print("   (אפשר להדביק טקסט ארוך, Enter פעמיים לסיום)")
        description_lines = []
        while True:
            line = input().strip()
            if not line and description_lines:
                break
            if line:
                description_lines.append(line)

        job['description'] = "\n".join(description_lines)

        # URL - always private_message since we ask candidates to message
        job['url'] = "private_message"

        # Optional fields
        job['salary'] = input("\n💰 שכר (Salary) [אופציונלי, Enter לדילוג]: ").strip() or None

        print("\n💼 סוג משרה (Job Type):")
        print("   1. Full-time")
        print("   2. Part-time")
        print("   3. Contract")
        print("   4. אחר")
        job_type_choice = input("   בחירה [Enter לברירת מחדל: Full-time]: ").strip()
        job_type_map = {"1": "Full-time", "2": "Part-time", "3": "Contract", "4": None}
        job['job_type'] = job_type_map.get(job_type_choice, "Full-time")

        print("\n👔 רמת ניסיון (Experience Level):")
        print("   1. Entry")
        print("   2. Mid")
        print("   3. Senior")
        exp_choice = input("   בחירה [Enter לברירת מחדל: Mid]: ").strip()
        exp_map = {"1": "Entry", "2": "Mid", "3": "Senior"}
        job['experience_level'] = exp_map.get(exp_choice, "Mid")

        # Add job
        self.jobs.append(job)
        print("\n✅ המשרה נוספה בהצלחה! Job added successfully!")

        # Ask to save
        save = input("\n💾 לשמור עכשיו? Save now? (Y/n): ").strip().lower()
        if save != 'n':
            self._save_jobs()

    def remove_job(self):
        """הסר משרה - Remove job"""
        if not self.jobs:
            print("\n❌ אין משרות למחוק!")
            return

        self.list_jobs()

        print("\n" + "=" * 70)
        try:
            choice = input("🗑️  מספר משרה למחיקה (Job number to remove) [0 לביטול]: ")
            index = int(choice) - 1

            if index == -1:
                print("ביטול...")
                return

            if 0 <= index < len(self.jobs):
                removed = self.jobs.pop(index)
                print(f"\n✅ נמחקה: {removed['title']}")
                self._save_jobs()
            else:
                print("❌ מספר לא תקין!")
        except ValueError:
            print("❌ נא להזין מספר!")

    def edit_job(self):
        """ערוך משרה - Edit job"""
        if not self.jobs:
            print("\n❌ אין משרות לעריכה!")
            return

        self.list_jobs()

        print("\n" + "=" * 70)
        try:
            choice = input("✏️  מספר משרה לעריכה (Job number to edit) [0 לביטול]: ")
            index = int(choice) - 1

            if index == -1:
                print("ביטול...")
                return

            if 0 <= index < len(self.jobs):
                job = self.jobs[index]

                print(f"\n📝 עריכת: {job['title']}")
                print("=" * 70)
                print("💡 טיפ: Enter כדי לשמור את הערך הקיים")
                print()

                # Edit fields
                new_title = input(f"🏷️  שם משרה [{job['title']}]: ").strip()
                if new_title:
                    job['title'] = new_title

                new_location = input(f"📍 מיקום [{job['location']}]: ").strip()
                if new_location:
                    job['location'] = new_location

                new_salary = input(f"💰 שכר [{job.get('salary', 'לא צוין')}]: ").strip()
                if new_salary:
                    job['salary'] = new_salary

                edit_reqs = input("📋 לערוך דרישות? Edit requirements? (y/N): ").strip().lower()
                if edit_reqs == 'y':
                    print("   דרישות חדשות (Enter פעמיים לסיום):")
                    requirements = []
                    req_num = 1
                    while True:
                        req = input(f"   {req_num}. ").strip()
                        if not req:
                            break
                        requirements.append(req)
                        req_num += 1
                    if requirements:
                        job['requirements'] = requirements

                print("\n✅ המשרה עודכנה! Job updated!")
                self._save_jobs()
            else:
                print("❌ מספר לא תקין!")
        except ValueError:
            print("❌ נא להזין מספר!")

    def quick_add_from_text(self):
        """הוספה מהירה מטקסט - Quick add from text"""
        print("\n" + "=" * 70)
        print("📋 הוספה מהירה - Quick Add")
        print("=" * 70)
        print("הדבק את פרטי המשרה מה-Correct Tech שלך")
        print("Paste job details from your Correct Tech site")
        print()
        print("פורמט מומלץ:")
        print("שם המשרה בשורה הראשונה")
        print("דרישות ופרטים בשורות הבאות")
        print()
        print("Enter פעמיים לסיום:")
        print()

        lines = []
        while True:
            line = input().strip()
            if not line and lines:
                break
            if line:
                lines.append(line)

        if not lines:
            print("❌ לא הוזן טקסט!")
            return

        # Create basic job from text
        job = {
            "title": lines[0],
            "location": "פתח תקווה, ישראל",
            "city": "Petah Tikva",
            "requirements": lines[1:] if len(lines) > 1 else ["לפי פרטי המשרה"],
            "description": "\n".join(lines),
            "url": "private_message",
            "salary": None,
            "job_type": "Full-time",
            "experience_level": "Mid"
        }

        self.jobs.append(job)
        print("\n✅ נוסף! תוכל לערוך אותו אחר כך.")
        print("   Added! You can edit it later.")

        save = input("\n💾 לשמור? Save? (Y/n): ").strip().lower()
        if save != 'n':
            self._save_jobs()

    def run(self):
        """הרץ את ממשק הניהול - Run management interface"""
        while True:
            print("\n" + "=" * 70)
            print("📋 מנהל משרות - Job Manager")
            print("=" * 70)
            print(f"כרגע יש {len(self.jobs)} משרות במערכת")
            print(f"Currently {len(self.jobs)} jobs in system")
            print()
            print("1. 📋 הצג משרות - List all jobs")
            print("2. ➕ הוסף משרה - Add new job")
            print("3. 🚀 הוספה מהירה (העתק והדבק) - Quick add (copy & paste)")
            print("4. ✏️  ערוך משרה - Edit job")
            print("5. 🗑️  מחק משרה - Remove job")
            print("6. 💾 שמור - Save")
            print("7. 🚪 יציאה - Exit")
            print("=" * 70)

            choice = input("\nבחירה / Choice (1-7): ").strip()

            if choice == '1':
                self.list_jobs()
            elif choice == '2':
                self.add_job()
            elif choice == '3':
                self.quick_add_from_text()
            elif choice == '4':
                self.edit_job()
            elif choice == '5':
                self.remove_job()
            elif choice == '6':
                self._save_jobs()
            elif choice == '7':
                print("\n👋 להתראות! Goodbye!")
                break
            else:
                print("❌ בחירה לא תקינה / Invalid choice")


def main():
    """הפעל את מנהל המשרות - Run job manager"""
    print("=" * 70)
    print("🎯 מנהל משרות - Job Manager")
    print("=" * 70)
    print()
    print("ממשק פשוט לניהול המשרות שלך")
    print("Simple interface to manage your jobs")
    print()
    print("✅ הוסף משרות חדשות")
    print("✅ מחק משרות ישנות")
    print("✅ ערוך משרות קיימות")
    print("✅ גיבוי אוטומטי")
    print()

    manager = JobManager()
    manager.run()


if __name__ == "__main__":
    main()
