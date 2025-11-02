# Facebook Job Search Agent V2

An intelligent agent that automatically finds job-seeking posts on Facebook and comments with helpful advice + relevant job opportunities from your company. Built with LangChain, GPT-3.5, and Facebook Graph API.

## 🚀 Key Features

### V2 Enhancements (NEW!)

✨ **Job Opportunity Matching** - Automatically matches job seekers with relevant positions from your company
🎯 **City-Based Targeting** - Target specific Facebook groups in cities where you have job openings
🛡️ **Smart Rate Limiting** - Advanced rate limiting with random delays to avoid Facebook blocks
📊 **Multi-Source Job Loading** - Support for JSON, CSV, API, and web scraping
🤖 **Intelligent Comments** - GPT-powered comments that feel natural and include relevant job links
⚙️ **Production Ready** - Configurable limits, delays, and automatic posting

### Core Features

- 🔍 **Smart Post Detection**: Identifies job-related posts using keyword matching
- 🤖 **AI-Powered Comments**: Personalized, empathetic advice using GPT-3.5
- 🛡️ **Safe by Default**: Dry-run mode to preview before posting
- 📈 **Detailed Reporting**: Real-time progress and summary statistics

## 📋 What It Does

1. **Searches** Facebook groups in cities where you have job openings
2. **Identifies** posts from people looking for work
3. **Matches** them with relevant jobs from your company
4. **Generates** personalized, helpful comments with job recommendations
5. **Posts** comments automatically with smart rate limiting

## 🎯 Example Comments

**Without Job Match:**
> "Hang in there! The job search can be tough, but staying consistent pays off. One tip: reach out directly to hiring managers on LinkedIn - it often gets better response rates than just applying online."

**With Job Match:**
> "I can relate to how challenging the job search can be - keep pushing forward! Since you mentioned experience with React, I came across a Frontend Developer position in New York that might interest you. It requires React, TypeScript, and responsive design skills. Thought it could be a good fit! https://yourcompany.com/jobs/frontend-developer"

## 🚀 Quick Start for Correct Tech Users

**Using Correct Tech for your jobs?** We've got you covered!

See **[QUICKSTART_CORRECT_TECH.md](QUICKSTART_CORRECT_TECH.md)** for a step-by-step guide specific to your platform.

Quick tools available:
- `job_entry_helper.py` - Interactive job entry tool
- `correct_tech_scraper.py` - Job import utilities
- Full Hebrew/UTF-8 support

## 🛠️ Setup

### 1. Install Dependencies

```bash
cd facebook-agent
pip install -r requirements.txt
```

### 2. Get Facebook Access Token

You need a Facebook User Access Token with these permissions:
- `user_posts` - Read posts from feeds
- `groups_access_member_info` - Access group posts
- `publish_actions` or `pages_manage_posts` - Post comments

**How to get a token:**

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use existing
3. Go to **Tools** → **Graph API Explorer**
4. Select your app
5. Add required permissions
6. Click **Generate Access Token**
7. Copy the token

**For long-lived tokens (60 days):**
Use the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/) to exchange short-lived tokens.

### 3. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Create a new API key
4. Copy the key

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
OPENAI_API_KEY=your_openai_api_key
```

### 5. Configure Your Jobs

Edit `jobs.json` with your actual job openings:

```json
[
  {
    "title": "Senior Software Engineer",
    "location": "San Francisco, CA",
    "city": "San Francisco",
    "requirements": [
      "5+ years Python experience",
      "React and Node.js",
      "Microservices architecture"
    ],
    "description": "Join our team building scalable web apps...",
    "url": "https://yourcompany.com/jobs/senior-engineer",
    "salary": "$150,000 - $200,000",
    "job_type": "Full-time",
    "experience_level": "Senior"
  }
]
```

**Alternative formats supported:**
- CSV files (use `CSVFileJobSource`)
- API endpoint (use `APIJobSource`)
- Web scraping (use `WebScraperJobSource`)

### 6. Configure Facebook Groups

Edit `groups.json` with groups you're a member of:

```json
[
  {
    "group_id": "123456789",
    "name": "San Francisco Bay Area Job Seekers",
    "city": "San Francisco",
    "description": "Job search group for SF Bay Area"
  }
]
```

**How to find group IDs:**
1. Go to the Facebook group
2. Look at URL: `facebook.com/groups/{GROUP_ID}/`
3. Copy the GROUP_ID

## 🚀 Usage

### Quick Start (Dry Run)

Test the agent without posting anything:

```bash
python facebook_job_agent_v2.py
```

This will:
- Search configured groups
- Find job-related posts
- Match jobs to posts
- Generate comments
- Show you what it WOULD post (but not actually post)

### Live Mode (Automatic Posting)

Edit `facebook_job_agent_v2.py`:

```python
agent = EnhancedFacebookJobAgent(
    jobs_file="jobs.json",
    groups_file="groups.json",
    dry_run=False,  # ⚠️ Set to False for live posting
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

### Target Specific Cities

Only comment in groups from specific cities:

```python
# Only run in SF and NY groups
agent.run_on_groups(city_filter=["San Francisco", "New York"])
```

### Advanced Configuration

```python
agent = EnhancedFacebookJobAgent(
    # API Keys (or use .env)
    access_token="your_token",
    openai_api_key="your_key",

    # Job Sources
    jobs_file="jobs.json",
    groups_file="groups.json",

    # Behavior
    dry_run=True,  # False to actually post
    include_job_opportunities=True,  # Include job links

    # Rate Limiting (IMPORTANT for avoiding blocks)
    min_delay=3.0,  # Min seconds between comments
    max_delay=8.0,  # Max seconds between comments
    posts_per_group=3,  # Max comments per group per run
    max_posts_per_run=10  # Total max per run
)
```

## 🔧 Configuration Options

### Rate Limiting (Prevent Blocks)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_delay` | 3.0 | Minimum seconds between comments |
| `max_delay` | 8.0 | Maximum seconds between comments |
| `posts_per_group` | 3 | Max comments per group per run |
| `max_posts_per_run` | 10 | Total max comments per run |

**Recommended settings:**
- **Conservative**: `min_delay=5`, `max_delay=15`, `posts_per_group=2`, `max_posts_per_run=5`
- **Moderate**: `min_delay=3`, `max_delay=10`, `posts_per_group=3`, `max_posts_per_run=10`
- **Aggressive** (not recommended): `min_delay=2`, `max_delay=5`, `posts_per_group=5`, `max_posts_per_run=15`

### Job Sources

**JSON File (default):**
```python
from job_opportunities import JSONFileJobSource
job_source = JSONFileJobSource("jobs.json")
```

**CSV File:**
```python
from job_opportunities import CSVFileJobSource
job_source = CSVFileJobSource("jobs.csv")
```

**API Endpoint:**
```python
from job_opportunities import APIJobSource
job_source = APIJobSource(
    api_url="https://yourcompany.com/api/jobs",
    api_key="your_api_key"
)
```

**Web Scraping:**
```python
from job_opportunities import WebScraperJobSource
job_source = WebScraperJobSource(
    url="https://yourcompany.com/careers",
    selectors={
        'container': '.job-listing',
        'title': '.job-title',
        'location': '.job-location',
        'url': 'a'
    }
)
```

## 📊 Job Matching Algorithm

The agent uses intelligent matching to find relevant jobs:

1. **Keyword Extraction**: Identifies tech/role keywords in posts (e.g., "Python", "React", "marketing")
2. **City Filtering**: Prioritizes jobs in the same city as the group
3. **Scoring**: Ranks jobs based on keyword matches
4. **Best Match**: Selects highest-scoring job or most relevant for the city

## 🔒 Safety & Best Practices

### Avoiding Facebook Blocks

✅ **DO:**
- Start with dry-run mode
- Use conservative rate limits
- Space out your runs (don't run hourly)
- Monitor your comments
- Be genuinely helpful

❌ **DON'T:**
- Post too frequently
- Use aggressive rate limits
- Spam the same groups
- Post generic/salesy comments
- Ignore Facebook policies

### Recommended Schedule

- **Daily**: Run once per day during business hours
- **Multiple times/day**: Wait at least 4-6 hours between runs
- **Weekly**: Run 3-4 times per week

### Monitoring

Check your comments regularly:
- Are they helpful and well-received?
- Any negative feedback?
- Are jobs actually relevant?

Adjust your configuration based on feedback.

## 🛠️ Job Entry Tools

### Interactive Job Entry Helper

The easiest way to add jobs:

```bash
python job_entry_helper.py
```

Features:
- **Interactive mode**: Answer simple questions to add jobs
- **Bulk import**: Paste formatted text for multiple jobs
- **List/edit**: View and manage your jobs
- **Export**: Export to CSV for backup

### Correct Tech Job Import

For Correct Tech users:

```bash
python correct_tech_scraper.py
```

Options:
- **Manual template**: Get a template to fill out
- **Direct entry**: Edit the script to add jobs
- **Selenium scraper**: Advanced automation (requires setup)

See [QUICKSTART_CORRECT_TECH.md](QUICKSTART_CORRECT_TECH.md) for detailed instructions.

## 📝 Customization

### Modify Comment Prompts

Edit prompts in `facebook_job_agent_v2.py`:

```python
self.comment_prompt_with_job = ChatPromptTemplate.from_template(
    """Your custom prompt here...

    Post: {post_content}
    Job: {job_title} in {job_location}

    Generate a comment that..."""
)
```

### Add More Keywords

```python
self.job_keywords = [
    "job search",
    "looking for work",
    "your custom keywords here",
    # ... add more
]
```

### Use GPT-4 for Better Quality

```python
self.llm = ChatOpenAI(
    model_name="gpt-4",  # More expensive but higher quality
    temperature=0.7,
    openai_api_key=self.openai_api_key
)
```

## 📁 File Structure

```
facebook-agent/
├── facebook_job_agent_v2.py        # ⭐ Enhanced version (recommended)
├── job_opportunities.py            # Job loading and matching
├── job_entry_helper.py             # 🆕 Interactive job entry tool
├── correct_tech_scraper.py         # 🆕 Job import utilities
├── jobs.json                       # Your job openings
├── groups.json                     # Target Facebook groups
├── facebook_job_agent.py           # Original simple version
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
└── QUICKSTART_CORRECT_TECH.md      # 🆕 Quick start for Correct Tech
```

## 🆚 Version Comparison

| Feature | V1 (Basic) | V2 (Enhanced) |
|---------|------------|---------------|
| Basic comments | ✓ | ✓ |
| Job matching | ✗ | ✓ |
| City targeting | ✗ | ✓ |
| Advanced rate limiting | ✗ | ✓ |
| Multiple job sources | ✗ | ✓ |
| Production ready | Partial | ✓ |

**Recommendation:** Use V2 (`facebook_job_agent_v2.py`) for production use.

## 🐛 Troubleshooting

### "Facebook access token is required"
- Check `.env` file exists and contains `FACEBOOK_ACCESS_TOKEN`
- Verify token hasn't expired

### "Error fetching posts: 403"
- Token missing required permissions
- Regenerate with correct permissions
- Verify you're a member of the groups

### "Error posting comment: 403"
- Need `publish_actions` permission
- May not have permission to comment in that group
- Token might have expired

### No job-related posts found
- Adjust `job_keywords` list
- Try different groups
- Check if groups are active

### Getting blocked by Facebook
- Reduce rate limits (increase delays, reduce max posts)
- Space out your runs more
- Make comments more natural/varied
- Follow the safety guidelines above

## 📄 License

Part of the LangChain Experiments repository.

## ⚖️ Disclaimer

This tool is for educational and helpful purposes. Use responsibly and in accordance with:
- Facebook's Terms of Service
- Facebook's Community Standards
- Facebook's Platform Policies
- Applicable laws and regulations

Always prioritize being genuinely helpful to job seekers. Don't spam or be overly promotional.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Facebook's API documentation
3. Verify your configuration files
4. Test in dry-run mode first

---

**Happy job matching! Help people find great opportunities while growing your company's talent pipeline.** 🎯
