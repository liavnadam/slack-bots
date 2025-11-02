# Facebook Job Search Agent

An intelligent agent that finds Facebook posts about job searching and automatically generates helpful, supportive comments using LangChain and GPT.

## Features

- 🔍 **Smart Post Detection**: Identifies job-related posts using keyword matching
- 🤖 **AI-Powered Comments**: Generates personalized, helpful comments using GPT-3.5
- 🛡️ **Safe by Default**: Runs in dry-run mode to preview comments before posting
- ⚙️ **Configurable**: Control comment limits, targeting, and behavior
- 📊 **Multiple Sources**: Search your feed or specific Facebook groups

## How It Works

1. **Search**: Finds posts in your feed or specified Facebook groups
2. **Filter**: Identifies posts related to job searching using keywords
3. **Analyze**: Uses LangChain + GPT to understand the post context
4. **Generate**: Creates empathetic, actionable advice tailored to the post
5. **Comment**: Posts the comment (or shows preview in dry-run mode)

## Setup

### 1. Install Dependencies

```bash
cd facebook-agent
pip install -r requirements.txt
```

### 2. Get Facebook Access Token

You need a Facebook User Access Token with these permissions:
- `user_posts` - Read posts from your feed
- `publish_actions` or `pages_manage_posts` - Post comments
- `groups_access_member_info` - Access group posts (if targeting groups)

**How to get an access token:**

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or use an existing one
3. Go to **Tools** → **Graph API Explorer**
4. Select your app from the dropdown
5. Click **Generate Access Token**
6. Grant the required permissions
7. Copy the token

**Important Notes:**
- User tokens expire after 1-2 hours by default
- For long-lived tokens (60 days), exchange your short-lived token using the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- For production use, consider implementing proper OAuth flow

### 3. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **Create new secret key**
5. Copy the key

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Basic Usage (Dry Run)

```bash
python facebook_job_agent.py
```

This runs in **dry-run mode** by default, which means it will:
- Find job-related posts
- Generate comments
- Show you what it would post
- **NOT actually post** anything

### Live Mode (Actually Post Comments)

Edit `facebook_job_agent.py` and change:

```python
agent = FacebookJobAgent(
    max_comments_per_run=5,
    dry_run=False  # Set to False to actually post
)
```

Then run:

```bash
python facebook_job_agent.py
```

### Target Specific Groups

If you want to comment on posts in specific Facebook groups:

```python
from facebook_job_agent import FacebookJobAgent

agent = FacebookJobAgent(
    max_comments_per_run=5,
    dry_run=True
)

# Add your group IDs
group_ids = [
    "123456789",  # Replace with actual group IDs
    "987654321"
]

agent.run(group_ids=group_ids)
```

**How to find group IDs:**
1. Go to the Facebook group
2. Look at the URL: `facebook.com/groups/{GROUP_ID}/`
3. Copy the GROUP_ID

### Custom Configuration

```python
agent = FacebookJobAgent(
    access_token="your_token",  # Or use env var
    openai_api_key="your_key",  # Or use env var
    max_comments_per_run=10,    # Limit comments per run
    dry_run=True                # Preview mode
)
```

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `access_token` | From `.env` | Facebook Graph API access token |
| `openai_api_key` | From `.env` | OpenAI API key |
| `max_comments_per_run` | 5 | Maximum comments to post per run |
| `dry_run` | True | If True, only shows previews without posting |

## Job Search Keywords

The agent identifies posts containing these keywords:
- job search
- looking for work
- hiring
- job hunting
- need a job
- seeking employment
- open to work
- unemployed
- career change
- job opportunity
- resume tips
- interview
- job application

You can customize these in the `job_keywords` list in `facebook_job_agent.py`.

## Comment Style

The agent generates comments that are:
- **Empathetic**: Shows understanding and support
- **Actionable**: Provides specific tips or advice
- **Natural**: Feels human, not robotic
- **Brief**: 2-3 sentences
- **Context-aware**: Tailored to the specific post

Example generated comments:
- "Hang in there! The job search can be tough, but staying consistent with applications and networking often pays off. Have you tried reaching out directly to hiring managers on LinkedIn?"
- "Great that you're being proactive! One tip that helped me: tailor your resume for each position by matching keywords from the job description. It really improves your chances of getting past ATS systems."

## Safety & Best Practices

⚠️ **Important Considerations:**

1. **Start with Dry Run**: Always test in dry-run mode first
2. **Limit Comments**: Don't spam - keep `max_comments_per_run` low (5-10)
3. **Wait Between Runs**: Don't run the agent too frequently
4. **Respect Privacy**: Only comment on public posts or groups you're a member of
5. **Facebook Policies**: Review [Facebook's Platform Policies](https://developers.facebook.com/policy) to ensure compliance
6. **Rate Limits**: Facebook has API rate limits - space out your requests
7. **Monitor Comments**: Check the comments being posted and adjust prompts if needed

## Facebook API Limitations

As of 2024, Facebook has restricted many public search capabilities:
- Public post search is no longer available for privacy reasons
- You can only access posts from:
  - Your own feed
  - Groups you're a member of
  - Pages you manage

This agent focuses on commenting in groups you belong to or on posts in your feed.

## Troubleshooting

### "Facebook access token is required"
- Make sure your `.env` file exists and contains `FACEBOOK_ACCESS_TOKEN`
- Check that the token hasn't expired

### "Error fetching posts: 403"
- Your token may not have the required permissions
- Regenerate with `user_posts` and `groups_access_member_info` permissions

### "Error posting comment: 403"
- You need `publish_actions` or `pages_manage_posts` permission
- You may not have permission to comment on that post

### No job-related posts found
- Try adjusting the `job_keywords` list
- Check if posts in your feed/groups contain these keywords

## Customization

### Modify Comment Prompt

Edit the `comment_prompt` in `facebook_job_agent.py`:

```python
self.comment_prompt = ChatPromptTemplate.from_template(
    """Your custom prompt here...

    Post: {post_content}

    Generate a comment that..."""
)
```

### Change GPT Model

```python
self.llm = ChatOpenAI(
    model_name="gpt-4",  # Use GPT-4 for better quality
    temperature=0.7,
    openai_api_key=self.openai_api_key
)
```

### Add More Keywords

```python
self.job_keywords = [
    "job search",
    "your custom keywords",
    # ... add more
]
```

## License

Part of the LangChain Experiments repository.

## Disclaimer

This tool is for educational and helpful purposes. Please use responsibly and in accordance with Facebook's terms of service and community standards. Always prioritize being genuinely helpful to job seekers.
