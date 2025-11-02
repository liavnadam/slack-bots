"""
Setup Script for Petah Tikva Jobs

This script helps you quickly set up all 10 jobs in Petah Tikva.
First job (AIG Sales) is already filled in as an example.
"""

import json
import os


def setup_petah_tikva_jobs():
    """Set up jobs for Petah Tikva, Israel."""

    jobs = [
        # Job 1 - AIG Health Insurance Sales (from your example)
        {
            "title": "תותחי מכירות למוקד ביטוחי בריאות - AIG",
            "location": "פתח תקווה, ישראל",
            "city": "Petah Tikva",
            "requirements": [
                "ניסיון במכירות - חובה",
                "כושר שכנוע וכריזמה",
                "יכולת עמידה ביעדים ומוטיבציה להצלחה",
                "מוסר עבודה גבוה, חוסן נפשי וטמפו גבוה"
            ],
            "description": """דרושים/ות תותחי מכירות למוקד ביטוחי הבריאות של AIG!

מה תעשו אצלנו?
📞 שיחות יוצאות ללקוחות החברה וללקוחות פוטנציאליים
💡 מכירת מוצרי ביטוח בריאות, חיים ותאונות אישיות
🚀 עבודה עצמאית בסביבה דינמית עם אווירה אנרגטית

מה תקבלו?
💰 שכר בסיס + בונוסים - ממוצע של 15,000 ש"ח בחודש
📅 5 ימים בשבוע + שישי לסירוגין
🎯 הכשרה מקיפה על חשבון החברה
🔝 הזדמנות לפיתוח קריירה בתחום הביטוח
📅 עד יומיים עבודה מהבית
⭐️ נופש חברה ועוד מגוון תנאים מעולים""",
            "url": "https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba",
            "salary": "₪15,000 ממוצע (בסיס + בונוסים)",
            "job_type": "Full-time",
            "experience_level": "Entry"
        },

        # Jobs 2-10: TODO - Add your remaining jobs here
        # Copy this template for each job:

        # {
        #     "title": "שם התפקיד",
        #     "location": "פתח תקווה, ישראל",
        #     "city": "Petah Tikva",
        #     "requirements": [
        #         "דרישה 1",
        #         "דרישה 2",
        #         "דרישה 3"
        #     ],
        #     "description": "תיאור מלא של התפקיד...",
        #     "url": "https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba",
        #     "salary": "₪10,000 - ₪20,000",
        #     "job_type": "Full-time",
        #     "experience_level": "Mid"
        # },
    ]

    # Save to jobs.json
    output_file = "jobs.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print("✓ נשמר בהצלחה!")
    print(f"✓ {len(jobs)} משרות נוספו לקובץ {output_file}")
    print()
    print("שלבים הבאים:")
    print("1. ערוך את הקובץ setup_petah_tikva_jobs.py")
    print("2. הוסף את 9 המשרות הנוספות שלך")
    print("3. הרץ שוב: python setup_petah_tikva_jobs.py")
    print()
    print("או השתמש בכלי האינטראקטיבי:")
    print("python job_entry_helper.py")


def setup_petah_tikva_groups():
    """Set up Facebook groups for Petah Tikva area."""

    groups = [
        {
            "group_id": "REPLACE_WITH_REAL_GROUP_ID_1",
            "name": "דרושים פתח תקווה",
            "city": "Petah Tikva",
            "description": "Job opportunities in Petah Tikva"
        },
        {
            "group_id": "REPLACE_WITH_REAL_GROUP_ID_2",
            "name": "משרות מרכז - פתח תקווה ואזור",
            "city": "Petah Tikva",
            "description": "Jobs in center area - Petah Tikva and surroundings"
        },
        {
            "group_id": "REPLACE_WITH_REAL_GROUP_ID_3",
            "name": "דרושים ישראל - מרכז",
            "city": "Petah Tikva",
            "description": "Jobs in Israel - Central region"
        },
        # Add more groups as you find them
    ]

    output_file = "groups.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(groups, f, indent=2, ensure_ascii=False)

    print()
    print("✓ קבוצות נשמרו ל-groups.json")
    print()
    print("כדי למצוא קבוצות:")
    print("1. חפש בפייסבוק: 'דרושים פתח תקווה'")
    print("2. הצטרף לקבוצות")
    print("3. העתק את מספר הקבוצה מה-URL")
    print("   (facebook.com/groups/123456789/ - 123456789 זה המספר)")
    print("4. החלף את REPLACE_WITH_REAL_GROUP_ID ב-groups.json")


def add_job_interactively():
    """Add a job interactively in Hebrew."""
    print("\n" + "=" * 60)
    print("הוספת משרה חדשה")
    print("=" * 60)

    job = {}

    job['title'] = input("שם התפקיד: ").strip()
    job['location'] = input("מיקום (למשל: פתח תקווה, ישראל): ").strip()
    job['city'] = "Petah Tikva"  # All jobs are in Petah Tikva

    print("\nדרישות התפקיד (שורה אחת לכל דרישה, Enter פעמיים לסיום):")
    requirements = []
    while True:
        req = input("  - ").strip()
        if not req:
            break
        requirements.append(req)
    job['requirements'] = requirements

    job['description'] = input("\nתיאור התפקיד: ").strip()
    job['url'] = "https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba"
    job['salary'] = input("שכר (אופציונלי, Enter לדילוג): ").strip() or None
    job['job_type'] = input("סוג משרה (Full-time/Part-time, Enter לדילוג): ").strip() or "Full-time"
    job['experience_level'] = input("רמת ניסיון (Entry/Mid/Senior, Enter לדילוג): ").strip() or "Mid"

    return job


def interactive_mode():
    """Interactive mode to add all 10 jobs."""
    print("=" * 60)
    print("הוספת משרות פתח תקווה - מצב אינטראקטיבי")
    print("=" * 60)
    print()
    print("יש לך 10 משרות להוסיף.")
    print("משרה ראשונה (AIG מכירות) כבר מוכנה.")
    print()

    # Load existing job (AIG sales)
    setup_petah_tikva_jobs()

    with open("jobs.json", 'r', encoding='utf-8') as f:
        jobs = json.load(f)

    print(f"\n✓ משרה 1/10 מוכנה: {jobs[0]['title']}")
    print()

    # Add remaining 9 jobs
    for i in range(2, 11):
        print(f"\n{'='*60}")
        print(f"משרה {i}/10")
        print(f"{'='*60}")

        add_more = input(f"\nהאם להוסיף משרה {i}? (y/n, Enter=y): ").strip().lower()
        if add_more == 'n':
            break

        job = add_job_interactively()
        jobs.append(job)

        print(f"\n✓ משרה {i} נוספה!")

    # Save all jobs
    with open("jobs.json", 'w', encoding='utf-8') as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print(f"✓ סה\"כ {len(jobs)} משרות נשמרו!")
    print("=" * 60)
    print()
    print("שלב הבא: הגדר את קבוצות הפייסבוק")
    print("הרץ: python setup_petah_tikva_jobs.py groups")


def main():
    """Main function."""
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "groups":
            setup_petah_tikva_groups()
        elif sys.argv[1] == "interactive":
            interactive_mode()
        else:
            print("שימוש:")
            print("  python setup_petah_tikva_jobs.py           - יצירת jobs.json עם משרת AIG")
            print("  python setup_petah_tikva_jobs.py groups    - יצירת groups.json")
            print("  python setup_petah_tikva_jobs.py interactive - הוספת כל 10 המשרות")
    else:
        print("=" * 60)
        print("הגדרת משרות פתח תקווה")
        print("=" * 60)
        print()
        print("בחר אפשרות:")
        print("1. יצירת jobs.json עם משרת AIG לדוגמה")
        print("2. מצב אינטראקטיבי - הוספת כל 10 המשרות")
        print("3. הגדרת קבוצות פייסבוק")
        print()

        choice = input("בחירה (1-3): ").strip()

        if choice == "1":
            setup_petah_tikva_jobs()
        elif choice == "2":
            interactive_mode()
        elif choice == "3":
            setup_petah_tikva_groups()
        else:
            print("בחירה לא תקינה")


if __name__ == "__main__":
    main()
