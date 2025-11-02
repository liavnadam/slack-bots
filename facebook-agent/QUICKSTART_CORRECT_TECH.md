# Quick Start Guide for Correct Tech

This guide will help you set up the Facebook Job Agent with your Correct Tech job listings.

## 🎯 Your Info

- **Website**: https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba
- **Access Code**: 502304544

## 📝 Step 1: Get Your Jobs into the System

You have **3 easy options**:

### Option A: Interactive Helper (Recommended)

The easiest way - just answer questions:

```bash
python job_entry_helper.py
```

Then:
1. Choose option 1 "Add new job (interactive)"
2. Answer the prompts for each job
3. Repeat for all your jobs
4. Choose option 5 "Save to jobs.json"

### Option B: Copy/Paste Template

Quick for multiple jobs:

```bash
python correct_tech_scraper.py
# Choose option 1
```

This creates `job_template.txt`. Then:

1. Open `job_template.txt`
2. For each job on your Correct Tech site, fill out:
   ```
   ---
   Title: [Copy from site]
   Location: Tel Aviv, Israel
   City: Tel Aviv
   Requirements: [Comma separated requirements]
   Description: [Job description]
   URL: https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba
   ---
   ```
3. Run: `python job_entry_helper.py`
4. Choose option 2, paste your jobs
5. Choose option 5 to save

### Option C: Edit Directly

For programmers:

Edit `correct_tech_scraper.py` and find this section:

```python
jobs = [
    {
        "title": "Your Job Title",
        "location": "Tel Aviv, Israel",
        "city": "Tel Aviv",
        "requirements": ["Requirement 1", "Requirement 2"],
        "description": "Job description",
        "url": "https://www.correct-tech.co.il/sites/4599caa68a/8fbce806ba",
        "salary": "₪20,000 - ₪30,000",
        "job_type": "Full-time",
        "experience_level": "Mid"
    },
    # Add more jobs...
]
```

Then run:
```bash
python correct_tech_scraper.py
# Choose option 2
```

## 🎯 Step 2: Set Up Facebook Groups

Now you need to find Facebook groups in your target cities where job seekers hang out.

### Finding Groups

1. Search Facebook for:
   - "[City] jobs"
   - "[City] employment"
   - "[City] job search"
   - "[City] hiring"
   - "[Industry] jobs [city]"

2. Join relevant groups

3. Get the group IDs:
   - Go to the group
   - Look at the URL: `facebook.com/groups/123456789/`
   - Copy the numbers

### Add Groups to `groups.json`

Edit `groups.json`:

```json
[
  {
    "group_id": "YOUR_GROUP_ID_HERE",
    "name": "Tel Aviv Tech Jobs",
    "city": "Tel Aviv",
    "description": "Tech jobs in Tel Aviv"
  },
  {
    "group_id": "ANOTHER_GROUP_ID",
    "name": "Israel Job Seekers",
    "city": "Tel Aviv",
    "description": "General job search group"
  }
]
```

**Pro tip**: Match the `city` field to the cities in your jobs for better matching!

## 🔑 Step 3: Get API Keys

### Facebook Access Token

1. Go to https://developers.facebook.com/
2. Create an app (or use existing)
3. Go to **Tools** → **Graph API Explorer**
4. Select your app
5. Click "Generate Access Token"
6. Grant permissions:
   - `user_posts`
   - `groups_access_member_info`
   - `publish_actions`
7. Copy the token

**Make it long-lived (60 days):**
- Go to https://developers.facebook.com/tools/debug/accesstoken/
- Paste your token
- Click "Extend Access Token"
- Copy the new token

### OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign in
3. Go to API Keys
4. Create new key
5. Copy it

### Add to `.env`

```bash
cp .env.example .env
```

Edit `.env`:
```
FACEBOOK_ACCESS_TOKEN=your_facebook_token_here
OPENAI_API_KEY=your_openai_key_here
```

## 🧪 Step 4: Test in Dry Run

```bash
python facebook_job_agent_v2.py
```

This will:
- Show you which groups it searches
- Find job-related posts
- Match your jobs to posts
- Show you the comments it WOULD post
- **NOT actually post anything**

Check if:
- ✅ Comments look natural and helpful
- ✅ Job matches make sense
- ✅ No errors appear

## 🚀 Step 5: Go Live!

If dry run looks good:

Edit `facebook_job_agent_v2.py` (line ~442):

```python
agent = EnhancedFacebookJobAgent(
    jobs_file="jobs.json",
    groups_file="groups.json",
    dry_run=False,  # ⚠️ CHANGE THIS TO FALSE
    include_job_opportunities=True,
    min_delay=3.0,
    max_delay=8.0,
    posts_per_group=3,
    max_posts_per_run=10
)
```

Then run:
```bash
python facebook_job_agent_v2.py
```

## ⚙️ Configuration Tips

### For Israel / Hebrew Support

The system already supports Hebrew characters (שָׁלוֹם!) since we use UTF-8 encoding.

Jobs can have Hebrew descriptions:
```json
{
  "title": "מפתח Full Stack",
  "location": "תל אביב, ישראל",
  "requirements": ["React", "Node.js", "5+ שנות ניסיון"],
  ...
}
```

### Recommended Settings for Israel

```python
agent = EnhancedFacebookJobAgent(
    min_delay=5.0,      # Be more conservative
    max_delay=12.0,     # Longer delays
    posts_per_group=2,  # Fewer per group
    max_posts_per_run=8 # Total max
)
```

### Target Specific Cities Only

```python
# Only run in Tel Aviv groups
agent.run_on_groups(city_filter=["Tel Aviv"])

# Or multiple cities
agent.run_on_groups(city_filter=["Tel Aviv", "Jerusalem", "Haifa"])
```

## 📅 Recommended Schedule

- **Daily**: Run once per day in the morning (9-11 AM)
- **3x per week**: Monday, Wednesday, Friday
- **After new jobs posted**: Run when you add new positions

## 🎯 Example Full Workflow

```bash
# 1. Set up (one time)
cd facebook-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys

# 2. Add your jobs (whenever you have new positions)
python job_entry_helper.py
# Add jobs, save

# 3. Test it
python facebook_job_agent_v2.py
# Check the output

# 4. Go live (edit dry_run=False first)
python facebook_job_agent_v2.py

# 5. Check Facebook to see your comments!
```

## 🆘 Common Issues

### "Can't access groups"
- Make sure you're a member of the groups
- Check your Facebook token has `groups_access_member_info` permission

### "No job-related posts found"
- The group might not have recent posts
- Try adding more groups
- Check if the group is active

### "Comments seem generic"
- Jobs might not be matching well
- Add more specific requirements to your jobs
- Adjust the keywords in the agent

### Hebrew characters showing weird
- Make sure your terminal supports UTF-8
- Files should already be UTF-8 encoded

## 📞 Need Help?

1. Check the main README.md for detailed docs
2. Look at example jobs in jobs.json
3. Test in dry run mode first
4. Start with just 1-2 groups

---

**Ready to help people find great jobs!** 🎯🇮🇱
