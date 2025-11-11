# 🤖 סוכן פייסבוק אוטומטי - מדריך בעברית

סוכן חכם שמוצא אנשים שמחפשים עבודה בפייסבוק ומגיב להם עם עצות מועילות + הצעות עבודה רלוונטיות מהחברה שלך!

---

## 🎯 למה Playwright?

❌ **Facebook Graph API חסום** - הרבה פעמים לא עובד
✅ **Playwright תמיד עובד** - מדמה משתמש אמיתי בדפדפן

### היתרונות:
- ✅ לא צריך Facebook Developer Account
- ✅ לא צריך API Token
- ✅ עובד גם כשה-API חסום
- ✅ נראה כמו משתמש אמיתי
- ✅ תמיכה מלאה בעברית
- ✅ שומר session (לא צריך להתחבר כל פעם)

---

## 🚀 התחלה מהירה

### שלב 1: התקנה

```bash
cd facebook-agent
pip install -r requirements.txt
playwright install chromium
```

### שלב 2: הגדרת פרטים

```bash
cp .env.example .env
nano .env  # או כל עורך שאתה אוהב
```

הכנס:
```
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password
OPENAI_API_KEY=sk-your-key-here
```

### שלב 3: הגדר קבוצות

ערוך `groups.json`:
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

איך למצוא group_id? תסתכל על ה-URL:
```
facebook.com/groups/123456789/  <-- זה ה-ID
```

### שלב 4: הגדר משרות

ערוך `jobs.json`:
```json
[
  {
    "title": "מפתח Full Stack",
    "location": "פתח תקווה, ישראל",
    "city": "Petah Tikva",
    "requirements": ["React", "Node.js", "עברית"],
    "description": "מפתח מנוסה לצוות שלנו",
    "url": "https://example.com/jobs/fullstack",
    "salary": "₪15,000-25,000",
    "job_type": "משרה מלאה",
    "experience_level": "בכיר"
  }
]
```

**עזרה מהירה:**
```bash
python job_entry_helper.py  # כלי אינטראקטיבי
```

### שלב 5: בדיקה

```bash
python test_playwright.py
```

זה יבדוק:
- ✅ Playwright מותקן
- ✅ הדפדפן עובד
- ✅ ההתחברות לפייסבוק עובדת

### שלב 6: הרצה (Dry Run)

```bash
python facebook_playwright_agent.py
```

הסוכן יפתח דפדפן ויראה לך בדיוק מה הוא עושה **בלי לפרסם תגובות באמת!**

### שלב 7: הפעלה אמיתית 🚀

ערוך `facebook_playwright_agent.py` (שורה 656):

```python
dry_run=False,  # שנה ל-False!
```

והרץ שוב:
```bash
python facebook_playwright_agent.py
```

---

## 📖 מה הסוכן עושה?

1. **מתחבר לפייסבוק** - עם האימייל והסיסמה שלך
2. **נכנס לקבוצות** - שהגדרת ב-groups.json
3. **סורק פוסטים** - מחפש אנשים שמחפשים עבודה
4. **מתאים משרות** - משווה בין הפוסט למשרות שלך
5. **מגיב** - תגובה מועילת + לינק למשרה רלוונטית

### דוגמה לתגובה:

**ללא משרה מתאימה:**
> "אני מבין כמה זה מאתגר לחפש עבודה, תמשיך ככה! 💪
> טיפ אחד שעזר לי - נסה לפנות ישירות למנהלי גיוס בלינקדאין,
> לפעמים זה עובד יותר טוב מאשר רק לשלוח קורות חיים."

**עם משרה מתאימה:**
> "אני מבין כמה זה מאתגר לחפש עבודה, תמשיך ככה! 💪
> ראיתי שיש לך ניסיון ב-React - נתקלתי במשרה של מפתח Full Stack
> בפתח תקווה שאולי מעניינת אותך. הם מחפשים מישהו עם React ו-Node.js.
> אולי כדאי להסתכל: https://example.com/jobs/fullstack"

---

## ⚙️ הגדרות חשובות

### Rate Limiting (למניעת חסימה!)

```python
FacebookPlaywrightAgent(
    min_delay=5.0,       # עיכוב מינימלי בין תגובות (שניות)
    max_delay=15.0,      # עיכוב מקסימלי
    posts_per_group=2,   # כמה תגובות לקבוצה בהרצה
    max_posts_per_run=5  # כמה תגובות סה"כ בהרצה
)
```

**המלצות:**

🐢 **זהיר (מומלץ בהתחלה):**
```python
min_delay=10, max_delay=20, posts_per_group=1, max_posts_per_run=3
```

⚡ **בינוני:**
```python
min_delay=5, max_delay=15, posts_per_group=2, max_posts_per_run=5
```

🚀 **אגרסיבי (לא מומלץ!):**
```python
min_delay=3, max_delay=8, posts_per_group=3, max_posts_per_run=10
```

### דפדפן נסתר

```python
headless=True  # הדפדפן לא יופיע על המסך
```

מתי להשתמש?
- ✅ בשרתים מרוחקים
- ✅ בהרצות אוטומטיות (cron)
- ❌ לא מומלץ בהתחלה (תרצה לראות מה קורה!)

### פילטור ערים

```python
# רק פתח תקווה
agent.run_on_groups(city_filter=["Petah Tikva"])

# כמה ערים
agent.run_on_groups(city_filter=["Petah Tikva", "Tel Aviv"])
```

---

## 🔒 בטיחות

### עשה ✅

- **התחל עם dry_run=True** - תמיד!
- **השתמש בעיכובים גדולים** - 10-20 שניות
- **הרץ פעם-פעמיים ביום** - לא יותר!
- **עקוב אחרי התגובות** - האם הן מועילות?
- **היה אותנטי** - תגובות שמושיות באמת

### אל תעשה ❌

- **אל תריץ כל שעה** - פייסבוק יזהה
- **אל תשתמש בעיכובים קצרים** - (< 5 שניות)
- **אל תספאם** - רק תגובות מועילות!
- **אל תתעלם מאזהרות** - אם פייסבוק מזהיר - עצור

---

## 📅 לוח זמנים מומלץ

| תדירות | מתי | הגדרות |
|---------|-----|--------|
| יומי | 10:00 | `posts=1, total=3` |
| פעמיים ביום | 10:00, 16:00 | `posts=1, total=2` |
| 3 פעמים בשבוע | א', ג', ה' | `posts=2, total=5` |

### Cron Job

```bash
# יומי ב-10:00
0 10 * * * cd /path/to/facebook-agent && python facebook_playwright_agent.py
```

---

## 🛠️ פתרון בעיות

### ❌ "Login failed"

**פתרון:**
- בדוק אימייל/סיסמה ב-`.env`
- יכול להיות CAPTCHA - הרץ עם `headless=False` ופתור ידנית
- פייסבוק חשדן? התחבר ידנית מהדפדפן קודם

### ❌ "Could not find comment box"

**פתרון:**
- פייסבוק שינה את הממשק
- צריך עדכון בקוד
- פתח issue

### ❌ "No posts found"

**פתרון:**
- בדוק שאתה חבר בקבוצה
- בדוק ש-group_id נכון
- הקבוצה פרטית מדי?

### ❌ תגובות לא מתפרסמות

**פתרון:**
- וודא `dry_run=False`
- בדוק הרשאות בקבוצה
- יכול להיות הגבלה יומית

### ⚠️ פייסבוק חוסם

**פתרון:**
- הגדל עיכובים: `min=15, max=30`
- הקטן תגובות: `max_posts_per_run=2`
- המתן 24 שעות
- היה פחות אגרסיבי

---

## 📁 קבצים חשובים

```
facebook-agent/
├── facebook_playwright_agent.py  ⭐ הסוכן הראשי - הרץ את זה!
├── job_opportunities.py          אלגוריתם התאמת משרות
├── test_playwright.py            בדיקת התקנה
├── jobs.json                     המשרות שלך
├── groups.json                   הקבוצות שלך
├── .env                          פרטי התחברות (אל תשתף!)
├── fb_session.json               Session (נוצר אוטומטית)
└── QUICKSTART_PLAYWRIGHT_HE.md   מדריך מפורט בעברית
```

---

## 💡 טיפים

1. **התחל קטן** - קבוצה אחת, תגובה אחת
2. **צפה בדפדפן** - `headless=False` בהתחלה
3. **בדוק תגובות** - האם הן מועילות?
4. **שמור session** - מהיר יותר ובטוח יותר
5. **עקוב אחרי לוגים** - הכל מודפס למסך

---

## 🎯 דוגמאות קוד

### בסיסי
```python
agent = FacebookPlaywrightAgent(
    jobs_file="jobs.json",
    groups_file="groups.json",
    dry_run=True  # תמיד התחל ככה!
)
agent.run_on_groups()
```

### זהיר מאוד
```python
agent = FacebookPlaywrightAgent(
    dry_run=False,
    min_delay=15,
    max_delay=30,
    posts_per_group=1,
    max_posts_per_run=2
)
agent.run_on_groups(city_filter=["Petah Tikva"])
```

### דפדפן נסתר
```python
agent = FacebookPlaywrightAgent(
    dry_run=False,
    headless=True  # רקע, בלי UI
)
agent.run_on_groups()
```

---

## 📚 קישורים שימושיים

- 📖 [מדריך מפורט בעברית](QUICKSTART_PLAYWRIGHT_HE.md)
- 📖 [README באנגלית](README.md)
- 🔧 [אינטגרציה עם Correct Tech](QUICKSTART_CORRECT_TECH.md)
- 🔧 [הגדרת 10 משרות בפתח תקווה](START_HERE_PETAH_TIKVA.md)

---

## ⚖️ אחריות משפטית

השתמש בחוכמה:
- ✅ עקוב אחרי תנאי השימוש של פייסבוק
- ✅ היה מועיל ואותנטי
- ✅ אל תספאם
- ✅ כבד פרטיות

---

**בהצלחה! 🎉**

**עזור לאנשים למצוא עבודה והשתמש בזה כדי למצוא עובדים מעולים! 💪**

יש שאלות? בעיות? פתח issue או בדוק את המדריך המפורט!
