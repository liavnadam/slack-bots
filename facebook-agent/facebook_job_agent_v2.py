"""
Facebook Job Search Agent V2 - Enhanced with Job Opportunities

This agent searches for job-related posts on Facebook and comments with:
- Empathy and support
- Actionable career advice
- Relevant job opportunities from your company
"""

import os
import requests
from typing import List, Dict, Optional
from dotenv import find_dotenv, load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import time
import json
import random
from datetime import datetime
from job_opportunities import (
    JobOpportunity,
    JobSource,
    JSONFileJobSource,
    CSVFileJobSource,
    APIJobSource,
    JobMatcher
)

# Load environment variables
load_dotenv(find_dotenv())


class RateLimiter:
    """Smart rate limiter to avoid Facebook blocks."""

    def __init__(
        self,
        min_delay: float = 3.0,
        max_delay: float = 10.0,
        posts_per_group: int = 3,
        max_posts_per_run: int = 10
    ):
        """
        Initialize rate limiter.

        Args:
            min_delay: Minimum delay between comments (seconds)
            max_delay: Maximum delay between comments (seconds)
            posts_per_group: Max comments per group per run
            max_posts_per_run: Total max comments per run
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.posts_per_group = posts_per_group
        self.max_posts_per_run = max_posts_per_run
        self.comments_this_run = 0
        self.comments_per_group = {}

    def can_comment_in_group(self, group_id: str) -> bool:
        """Check if we can comment in this group."""
        group_count = self.comments_per_group.get(group_id, 0)
        return group_count < self.posts_per_group

    def can_comment_overall(self) -> bool:
        """Check if we can comment at all."""
        return self.comments_this_run < self.max_posts_per_run

    def record_comment(self, group_id: Optional[str] = None):
        """Record a comment was posted."""
        self.comments_this_run += 1
        if group_id:
            self.comments_per_group[group_id] = self.comments_per_group.get(group_id, 0) + 1

    def wait(self):
        """Wait with random delay to appear more human."""
        # Random delay with slight variation
        delay = random.uniform(self.min_delay, self.max_delay)
        print(f"⏳ Waiting {delay:.1f} seconds before next action...")
        time.sleep(delay)


class EnhancedFacebookJobAgent:
    """Enhanced agent with job opportunity matching."""

    def __init__(
        self,
        access_token: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        job_source: Optional[JobSource] = None,
        jobs_file: str = "jobs.json",
        groups_file: str = "groups.json",
        dry_run: bool = True,
        include_job_opportunities: bool = True,
        min_delay: float = 3.0,
        max_delay: float = 10.0,
        posts_per_group: int = 3,
        max_posts_per_run: int = 10
    ):
        """
        Initialize the Enhanced Facebook Job Agent.

        Args:
            access_token: Facebook Graph API access token
            openai_api_key: OpenAI API key
            job_source: Custom job source (optional)
            jobs_file: Path to jobs JSON file
            groups_file: Path to groups JSON file
            dry_run: If True, only preview comments
            include_job_opportunities: Include job matches in comments
            min_delay: Minimum delay between comments (seconds)
            max_delay: Maximum delay between comments (seconds)
            posts_per_group: Max comments per group per run
            max_posts_per_run: Total max comments per run
        """
        self.access_token = access_token or os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.dry_run = dry_run
        self.include_job_opportunities = include_job_opportunities

        if not self.access_token:
            raise ValueError("Facebook access token is required")

        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            min_delay=min_delay,
            max_delay=max_delay,
            posts_per_group=posts_per_group,
            max_posts_per_run=max_posts_per_run
        )

        # Load jobs
        if job_source:
            self.job_source = job_source
        else:
            self.job_source = JSONFileJobSource(jobs_file)

        self.jobs = self.job_source.fetch_jobs()
        self.job_matcher = JobMatcher(self.jobs) if self.jobs else None

        # Load groups configuration
        self.groups_config = self._load_groups_config(groups_file)

        print(f"✓ Loaded {len(self.jobs)} job opportunities")
        print(f"✓ Loaded {len(self.groups_config)} group configurations")

        # Initialize LangChain
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,
            openai_api_key=self.openai_api_key
        )

        # Comment generation prompts
        self._setup_prompts()

        # Job search keywords
        self.job_keywords = [
            "job search", "looking for work", "hiring", "job hunting",
            "need a job", "seeking employment", "open to work",
            "unemployed", "career change", "job opportunity",
            "resume tips", "interview", "job application",
            "looking for opportunities", "seeking a position"
        ]

    def _setup_prompts(self):
        """Setup LangChain prompts."""
        # Prompt without job opportunity
        self.comment_prompt_no_job = ChatPromptTemplate.from_template(
            """You are a helpful career advisor providing supportive advice to job seekers.

A person posted this on Facebook about their job search:

"{post_content}"

Generate a brief, friendly, helpful comment (2-3 sentences) that:
- Shows empathy and encouragement
- Provides ONE specific, actionable tip
- Feels natural and human (not robotic or formal)
- Is specific to their situation
- Avoids being salesy

Comment:"""
        )

        # Prompt with job opportunity
        self.comment_prompt_with_job = ChatPromptTemplate.from_template(
            """You are a helpful career advisor providing supportive advice to job seekers.

A person posted this on Facebook about their job search:

"{post_content}"

You have a relevant job opportunity to share:

Job Title: {job_title}
Location: {job_location}
Key Requirements: {job_requirements}
URL: {job_url}

Generate a brief, friendly comment (3-4 sentences) that:
- Shows empathy and encouragement
- Provides ONE actionable tip related to their search
- Naturally mentions you saw a relevant opportunity that might interest them
- Briefly highlights why it could be a good fit (1 sentence max)
- Includes the job URL
- Feels personal, not like a job board spam
- Doesn't sound overly promotional

Comment:"""
        )

        self.comment_chain_no_job = LLMChain(
            llm=self.llm,
            prompt=self.comment_prompt_no_job,
            verbose=False
        )

        self.comment_chain_with_job = LLMChain(
            llm=self.llm,
            prompt=self.comment_prompt_with_job,
            verbose=False
        )

    def _load_groups_config(self, groups_file: str) -> List[Dict]:
        """Load groups configuration from JSON file."""
        if not os.path.exists(groups_file):
            print(f"Warning: Groups file not found at {groups_file}")
            return []

        with open(groups_file, 'r') as f:
            return json.load(f)

    def is_job_related_post(self, post_text: str) -> bool:
        """Check if post is job-related."""
        if not post_text:
            return False

        post_lower = post_text.lower()
        return any(keyword in post_lower for keyword in self.job_keywords)

    def search_group_posts(self, group_id: str, limit: int = 20) -> List[Dict]:
        """Fetch posts from a Facebook group."""
        url = f"https://graph.facebook.com/v18.0/{group_id}/feed"

        params = {
            "access_token": self.access_token,
            "fields": "id,message,created_time,from",
            "limit": limit
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error fetching posts: {e}")
            return []

    def generate_comment(
        self,
        post_content: str,
        matched_job: Optional[JobOpportunity] = None
    ) -> str:
        """Generate a comment with optional job opportunity."""
        try:
            if matched_job and self.include_job_opportunities:
                # Generate comment with job opportunity
                comment = self.comment_chain_with_job.run(
                    post_content=post_content,
                    job_title=matched_job.title,
                    job_location=matched_job.location,
                    job_requirements=", ".join(matched_job.requirements[:3]),
                    job_url=matched_job.url
                )
            else:
                # Generate general supportive comment
                comment = self.comment_chain_no_job.run(
                    post_content=post_content
                )

            return comment.strip()
        except Exception as e:
            print(f"  ✗ Error generating comment: {e}")
            return ""

    def post_comment(self, post_id: str, comment_text: str) -> bool:
        """Post a comment to Facebook."""
        if self.dry_run:
            print(f"\n  [DRY RUN] Would post:")
            print(f"  '{comment_text}'\n")
            return True

        url = f"https://graph.facebook.com/v18.0/{post_id}/comments"

        params = {
            "access_token": self.access_token,
            "message": comment_text
        }

        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            print(f"  ✓ Successfully posted comment")
            return True
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error posting comment: {e}")
            return False

    def run_on_groups(self, city_filter: Optional[List[str]] = None):
        """
        Run agent on configured groups.

        Args:
            city_filter: Only run on groups in these cities (optional)
        """
        print("=" * 70)
        print("Enhanced Facebook Job Search Agent V2")
        print("=" * 70)
        print(f"Mode: {'🔍 DRY RUN (preview only)' if self.dry_run else '🚀 LIVE'}")
        print(f"Job Opportunities: {'✓ Enabled' if self.include_job_opportunities else '✗ Disabled'}")
        print(f"Rate Limit: {self.rate_limiter.posts_per_group} per group, {self.rate_limiter.max_posts_per_run} total")
        print(f"Delay: {self.rate_limiter.min_delay}s - {self.rate_limiter.max_delay}s between comments")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()

        # Filter groups by city if specified
        target_groups = self.groups_config
        if city_filter:
            target_groups = [
                g for g in self.groups_config
                if g.get('city', '').lower() in [c.lower() for c in city_filter]
            ]
            print(f"🎯 Filtering to cities: {', '.join(city_filter)}")

        if not target_groups:
            print("❌ No groups to search. Check your groups.json configuration.")
            return

        print(f"📍 Targeting {len(target_groups)} group(s):\n")
        for group in target_groups:
            print(f"   • {group['name']} ({group['city']})")
        print()

        total_processed = 0
        total_commented = 0

        # Process each group
        for group in target_groups:
            if not self.rate_limiter.can_comment_overall():
                print(f"\n⚠️  Reached maximum comments per run ({self.rate_limiter.max_posts_per_run})")
                break

            group_id = group['group_id']
            group_name = group['name']
            group_city = group.get('city', 'Unknown')

            print(f"\n{'─' * 70}")
            print(f"📍 Processing: {group_name} ({group_city})")
            print(f"{'─' * 70}")

            # Fetch posts
            posts = self.search_group_posts(group_id, limit=30)

            if not posts:
                print(f"  ℹ️  No posts found or unable to access group")
                continue

            print(f"  ✓ Found {len(posts)} posts")

            # Filter job-related posts
            job_posts = [p for p in posts if self.is_job_related_post(p.get('message', ''))]
            print(f"  ✓ Identified {len(job_posts)} job-related posts")

            # Comment on posts
            group_comments = 0

            for post in job_posts:
                if not self.rate_limiter.can_comment_in_group(group_id):
                    print(f"  ⚠️  Reached limit for this group ({self.rate_limiter.posts_per_group} comments)")
                    break

                if not self.rate_limiter.can_comment_overall():
                    break

                post_id = post.get('id')
                message = post.get('message', '')
                author = post.get('from', {}).get('name', 'Unknown')

                print(f"\n  📝 Post by: {author}")
                print(f"  Content: {message[:80]}...")

                # Try to match a job
                matched_job = None
                if self.job_matcher and self.include_job_opportunities:
                    matched_job = self.job_matcher.find_best_match(message, group_city)

                    if matched_job:
                        print(f"  ✨ Matched job: {matched_job.title} ({matched_job.city})")
                    else:
                        print(f"  ℹ️  No specific job match found")

                # Generate comment
                comment = self.generate_comment(message, matched_job)

                if comment:
                    # Post comment
                    success = self.post_comment(post_id, comment)

                    if success:
                        self.rate_limiter.record_comment(group_id)
                        group_comments += 1
                        total_commented += 1

                        # Wait before next comment (unless last comment)
                        if self.rate_limiter.can_comment_overall():
                            self.rate_limiter.wait()

                total_processed += 1

            print(f"\n  ✓ Posted {group_comments} comment(s) in this group")

        # Final summary
        print(f"\n{'=' * 70}")
        print(f"✅ COMPLETED")
        print(f"{'=' * 70}")
        print(f"Posts processed: {total_processed}")
        print(f"Comments posted: {total_commented}")
        print(f"Groups processed: {len(target_groups)}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 70}\n")


def main():
    """Main function."""
    # Initialize agent
    agent = EnhancedFacebookJobAgent(
        jobs_file="jobs.json",
        groups_file="groups.json",
        dry_run=True,  # Set to False for live posting
        include_job_opportunities=True,
        min_delay=3.0,
        max_delay=8.0,
        posts_per_group=3,
        max_posts_per_run=10
    )

    # Run on all configured groups
    agent.run_on_groups()

    # Or run only on specific cities
    # agent.run_on_groups(city_filter=["San Francisco", "New York"])


if __name__ == "__main__":
    main()
