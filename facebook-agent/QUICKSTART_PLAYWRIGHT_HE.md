# 🚀 מדריך התחלה מהירה - סוכן פייסבוק עם Playwright

## למה Playwright?

✅ **עובד תמיד** - לא תלוי ב-Facebook Graph API שיכול להיחסם
✅ **אוטומציה מלאה** - מדמה משתמש אמיתי בדפדפן
✅ **תמיכה מלאה בעברית** - זיהוי ותגובות בעברית
✅ **שמירת Session** - לא צריך להתחבר בכל פעם

---

## 📋 שלב 1: הכנה

### התקנת התלויות

```bash
cd facebook-agent
pip install -r requirements.txt
playwright install chromium
```

---

## 🔐 שלב 2: הגדרת פרטי התחברות

העתק את קובץ ההגדרות לדוגמה:

```bash
cp .env.example .env
```

ערוך את הקובץ `.env`:

```bash
# פרטי התחברות לפייסבוק (חשוב!)
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password_here

# מפתח OpenAI
OPENAI_API_KEY=sk-your-openai-key-here
```

⚠️ **אבטחה**: אל תשתף את קובץ `.env` עם אף אחד! הוא מכיל את הסיסמה שלך.

---

## 📍 שלב 3: הגדרת קבוצות פייסבוק

ערוך את `groups.json` עם הקבוצות שלך:

```json
[
  {
    "group_id": "123456789",
    "name": "פורום דרושים פתח תקווה",
    "city": "Petah Tikva",
    "description": "קבוצת דרושים מקומית"
  }
]
```

### איך למצוא את ה-`group_id`?

1. היכנס לקבוצה בפייסבוק
2. תסתכל על ה-URL: `facebook.com/groups/{GROUP_ID}/`
3. העתק את המספר (GROUP_ID)

---

## 💼 שלב 4: הגדרת משרות

ערוך את `jobs.json` עם המשרות שלך:

```json
[
  {
    "title": "מפתח Full Stack",
    "location": "פתח תקווה, ישראל",
    "city": "Petah Tikva",
    "requirements": [
      "ניסיון ב-React",
      "ניסיון ב-Node.js",
      "עברית ברמת שפת אם"
    ],
    "description": "מפתח מנוסה לצוות שלנו",
    "url": "https://example.com/jobs/fullstack",
    "salary": "₪15,000-25,000",
    "job_type": "משרה מלאה",
    "experience_level": "בכיר"
  }
]
```

**רעיונות מהירים:**
- משתמש ב-Correct Tech? ראה `setup_petah_tikva_jobs.py`
- צריך עזרה? הרץ `python job_entry_helper.py`

---

## 🧪 שלב 5: בדיקה (Dry Run)

בואו ננסה בלי לפרסם תגובות אמיתיות:

```bash
python facebook_playwright_agent.py
```

זה יעשה:
- ✅ יפתח דפדפן (תוכל לראות מה קורה!)
- ✅ יתחבר לפייסבוק
- ✅ יסרוק את הקבוצות
- ✅ ימצא פוסטים רלוונטיים
- ✅ יציג לך מה הוא **היה** מגיב (אבל לא באמת מגיב)

### מה אתה אמור לראות:

```
══════════════════════════════════════════════════════════════════════
Facebook Job Search Agent - Playwright Edition
══════════════════════════════════════════════════════════════════════
Mode: 🔍 DRY RUN (preview only)
Browser: 👀 Visible
Job Opportunities: ✓ Enabled
Rate Limit: 2 per group, 5 total
...

🔐 Logging in to Facebook...
✓ Successfully logged in!

📍 Processing: פורום דרושים פתח תקווה (Petah Tikva)
────────────────────────────────────────────────────────────────────
  ✓ Found 15 posts on page
  ✓ Successfully scraped 15 posts
  ✓ Identified 5 job-related posts

  📝 Post preview: מחפש עבודה כמפתח...
  ✨ Matched job: מפתח Full Stack (Petah Tikva)

  [DRY RUN] Would post:
  'אני מבין כמה זה מאתגר לחפש עבודה, תמשיך ככה!
   ראיתי משרה שאולי מעניינת אותך - מפתח Full Stack בפתח תקווה...'

⏳ Waiting 7.3 seconds before next comment...
...
```

---

## 🚀 שלב 6: הפעלה אמיתית (LIVE MODE)

אם הכל נראה טוב, בואו נפעיל באמת!

ערוך את `facebook_playwright_agent.py` (שורה 656):

```python
def main():
    agent = FacebookPlaywrightAgent(
        jobs_file="jobs.json",
        groups_file="groups.json",
        dry_run=False,  # ⚠️ שנה ל-False להפעלה אמיתית!
        include_job_opportunities=True,
        headless=False,  # True = דפדפן נסתר
        min_delay=5.0,
        max_delay=15.0,
        posts_per_group=2,  # מקסימום 2 תגובות לקבוצה
        max_posts_per_run=5,  # מקסימום 5 תגובות סה"כ
        save_session=True
    )
```

הרץ:

```bash
python facebook_playwright_agent.py
```

---

## ⚙️ הגדרות מתקדמות

### Rate Limiting (חשוב למניעת חסימה!)

| פרמטר | ברירת מחדל | תיאור |
|-------|-----------|-------|
| `min_delay` | 5.0 | עיכוב מינימלי בין תגובות (שניות) |
| `max_delay` | 15.0 | עיכוב מקסימלי בין תגובות (שניות) |
| `posts_per_group` | 2 | מקס' תגובות לקבוצה בהרצה |
| `max_posts_per_run` | 5 | מקס' תגובות כולל בהרצה |

**המלצות:**

🐢 **זהיר (מומלץ!):**
```python
min_delay=10.0, max_delay=20.0, posts_per_group=1, max_posts_per_run=3
```

⚡ **בינוני:**
```python
min_delay=5.0, max_delay=15.0, posts_per_group=2, max_posts_per_run=5
```

🚀 **אגרסיבי (לא מומלץ!):**
```python
min_delay=3.0, max_delay=8.0, posts_per_group=3, max_posts_per_run=10
```

### דפדפן נסתר (Headless)

```python
headless=True  # הדפדפן לא יופיע על המסך
```

שימושי ל:
- ✅ הרצה אוטומטית (cron jobs)
- ✅ שרתים מרוחקים
- ✅ חיסכון במשאבים

### פילטור לפי ערים

רוצה לרוץ רק על קבוצות מפתח תקווה?

```python
agent.run_on_groups(city_filter=["Petah Tikva"])
```

או על מספר ערים:

```python
agent.run_on_groups(city_filter=["Petah Tikva", "Tel Aviv", "Jerusalem"])
```

---

## 🔒 אבטחה והימנעות מחסימות

### DO ✅

- **התחל עם Dry Run** - תמיד בדוק לפני
- **השתמש בעיכובים גדולים** - ככל שיותר - יותר בטוח
- **הרץ פעם-פעמיים ביום** - אל תגזים
- **עקוב אחרי התגובות** - בדוק שהן מתקבלות טוב
- **היה אותנטי** - תגובות שמושיות באמת

### DON'T ❌

- **אל תריץ כל שעה** - פייסבוק יזהה
- **אל תשתמש בעיכובים קצרים מדי** - נראה רובוטי
- **אל תפרסם תגובות זהות** - כל תגובה ייחודית (GPT עושה את זה)
- **אל תתעלם מאזהרות** - אם פייסבוק מזהיר - עצור

### שמירת Session

הסוכן שומר cookies ב-`fb_session.json`:
- ✅ לא צריך להתחבר בכל פעם
- ✅ נראה יותר טבעי לפייסבוק
- ✅ מהיר יותר

אם יש בעיות:
```bash
rm fb_session.json
```

---

## 📅 לוח זמנים מומלץ

| תדירות | מתי | הגדרות |
|---------|-----|--------|
| **יומי** | 10:00 בבוקר | `posts_per_group=1, max_posts_per_run=3` |
| **פעמיים ביום** | 10:00, 16:00 | `posts_per_group=1, max_posts_per_run=2` |
| **3 פעמים בשבוע** | א', ג', ה' בבוקר | `posts_per_group=2, max_posts_per_run=5` |

### Cron Job (לינוקס/Mac)

```bash
# הרצה יומית ב-10:00
0 10 * * * cd /path/to/facebook-agent && python facebook_playwright_agent.py
```

---

## 🛠️ פתרון בעיות

### "Login failed - check credentials"

- ✅ בדוק שהאימייל והסיסמה נכונים ב-`.env`
- ✅ ייתכן ש-CAPTCHA מופיע - הרץ עם `headless=False` ופתור ידנית
- ✅ פייסבוק חשדן? נסה להתחבר ידנית מהדפדפן קודם

### "Could not find comment box"

- ✅ פייסבוק שינה את הממשק - צריך עדכון
- ✅ נסה דפדפן רגיל להבין את המבנה החדש
- ✅ פתח issue ב-GitHub

### "No posts found"

- ✅ בדוק שאתה חבר בקבוצה
- ✅ בדוק ש-group_id נכון
- ✅ אולי הקבוצה פרטית מדי

### תגובות לא מתפרסמות

- ✅ וודא `dry_run=False`
- ✅ בדוק הרשאות בקבוצה
- ✅ אולי יש הגבלה על מספר תגובות ביום

### פייסבוק חוסם אותי

- ✅ הגדל עיכובים: `min_delay=15, max_delay=30`
- ✅ הקטן מספר תגובות: `max_posts_per_run=2`
- ✅ המתן 24 שעות
- ✅ שנה לגישה פחות אגרסיבית

---

## 🎯 דוגמאות שימוש

### דוגמה 1: הרצה בסיסית

```python
from facebook_playwright_agent import FacebookPlaywrightAgent

agent = FacebookPlaywrightAgent(
    jobs_file="jobs.json",
    groups_file="groups.json",
    dry_run=True
)

agent.run_on_groups()
```

### דוגמה 2: ערים ספציפיות

```python
agent = FacebookPlaywrightAgent(
    jobs_file="jobs.json",
    groups_file="groups.json",
    dry_run=False,
    headless=True
)

# רק פתח תקווה
agent.run_on_groups(city_filter=["Petah Tikva"])
```

### דוגמה 3: זהיר מאוד

```python
agent = FacebookPlaywrightAgent(
    jobs_file="jobs.json",
    groups_file="groups.json",
    dry_run=False,
    min_delay=15.0,  # עיכוב ארוך
    max_delay=30.0,
    posts_per_group=1,  # תגובה אחת לקבוצה
    max_posts_per_run=2  # 2 תגובות סה"כ
)

agent.run_on_groups()
```

---

## 📚 קבצים חשובים

| קובץ | תיאור |
|------|-------|
| `facebook_playwright_agent.py` | ⭐ הסוכן הראשי - הרץ את זה! |
| `job_opportunities.py` | אלגוריתם התאמת משרות |
| `jobs.json` | המשרות שלך |
| `groups.json` | הקבוצות שלך |
| `.env` | פרטי התחברות (לא לשתף!) |
| `fb_session.json` | Session שמור (נוצר אוטומטית) |

---

## 💡 טיפים מנצחים

1. **התחל קטן** - קבוצה אחת, תגובה אחת
2. **צפה בדפדפן** - `headless=False` בהתחלה
3. **בדוק התגובות** - הן מועילות? אנשים מגיבים?
4. **התאם את הפרומפט** - ערוך את ה-prompts ב-`_setup_prompts()`
5. **שמור לוגים** - העתק את הפלט לקובץ להתייחסות

---

## 🤝 תמיכה

יש בעיה?

1. בדוק את **פתרון בעיות** למעלה
2. הרץ עם `dry_run=True` לדיבאג
3. בדוק שכל הקבצים מוגדרים נכון

---

## ⚖️ אחריות משפטית

השתמש באחריות:
- ✅ עקוב אחרי תנאי השימוש של פייסבוק
- ✅ היה עוזר ואותנטי
- ✅ אל תספאם
- ✅ כבד פרטיות

---

**בהצלחה! 🎉 עזור לאנשים למצוא עבודה וגם למצוא עובדים מעולים! 💪**
