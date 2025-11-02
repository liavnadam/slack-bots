"""
Facebook Job Search Agent

This agent searches for job-related posts on Facebook and generates
helpful, supportive comments using LangChain and GPT.
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

# Load environment variables
load_dotenv(find_dotenv())


class FacebookJobAgent:
    """Agent that finds job search posts and comments with helpful advice."""

    def __init__(
        self,
        access_token: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        max_comments_per_run: int = 5,
        dry_run: bool = True
    ):
        """
        Initialize the Facebook Job Agent.

        Args:
            access_token: Facebook Graph API access token
            openai_api_key: OpenAI API key for LangChain
            max_comments_per_run: Maximum number of comments to post per run
            dry_run: If True, only print comments without posting
        """
        self.access_token = access_token or os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.max_comments = max_comments_per_run
        self.dry_run = dry_run

        if not self.access_token:
            raise ValueError("Facebook access token is required")

        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")

        # Initialize LangChain
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.7,  # Slightly creative but still helpful
            openai_api_key=self.openai_api_key
        )

        # Comment generation prompt
        self.comment_prompt = ChatPromptTemplate.from_template(
            """You are a helpful career advisor who provides supportive, actionable advice to job seekers.

A person has posted the following on Facebook about their job search:

"{post_content}"

Generate a brief, friendly, and genuinely helpful comment (2-3 sentences) that:
- Shows empathy and encouragement
- Provides actionable advice or tips
- Feels natural and human (not overly formal)
- Is specific to their situation if details are provided
- Avoids being salesy or promotional

Comment:"""
        )

        self.comment_chain = LLMChain(
            llm=self.llm,
            prompt=self.comment_prompt,
            verbose=True
        )

        # Job search keywords to identify relevant posts
        self.job_keywords = [
            "job search", "looking for work", "hiring", "job hunting",
            "need a job", "seeking employment", "open to work",
            "unemployed", "career change", "job opportunity",
            "resume tips", "interview", "job application"
        ]

    def is_job_related_post(self, post_text: str) -> bool:
        """
        Check if a post is related to job searching.

        Args:
            post_text: The text content of the post

        Returns:
            True if the post appears to be about job searching
        """
        if not post_text:
            return False

        post_lower = post_text.lower()
        return any(keyword in post_lower for keyword in self.job_keywords)

    def search_public_posts(self, query: str = "job search", limit: int = 10) -> List[Dict]:
        """
        Search for public posts using Facebook Graph API.

        Note: As of 2024, public post search is limited. This method searches
        for posts in groups you're a member of or on pages you manage.

        Args:
            query: Search query
            limit: Maximum number of posts to retrieve

        Returns:
            List of post dictionaries
        """
        # Note: Facebook deprecated public post search for privacy reasons
        # This will search your own feed instead
        url = f"https://graph.facebook.com/v18.0/me/feed"

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
            print(f"Error fetching posts: {e}")
            return []

    def search_group_posts(self, group_id: str, limit: int = 10) -> List[Dict]:
        """
        Search for posts in a specific Facebook group.

        Args:
            group_id: The Facebook group ID
            limit: Maximum number of posts to retrieve

        Returns:
            List of post dictionaries
        """
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
            print(f"Error fetching group posts: {e}")
            return []

    def generate_comment(self, post_content: str) -> str:
        """
        Generate a helpful comment using LangChain and GPT.

        Args:
            post_content: The content of the job search post

        Returns:
            Generated comment text
        """
        try:
            comment = self.comment_chain.run(post_content=post_content)
            return comment.strip()
        except Exception as e:
            print(f"Error generating comment: {e}")
            return ""

    def post_comment(self, post_id: str, comment_text: str) -> bool:
        """
        Post a comment to a Facebook post.

        Args:
            post_id: The ID of the post to comment on
            comment_text: The comment text to post

        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            print(f"\n[DRY RUN] Would post comment to {post_id}:")
            print(f"'{comment_text}'")
            return True

        url = f"https://graph.facebook.com/v18.0/{post_id}/comments"

        params = {
            "access_token": self.access_token,
            "message": comment_text
        }

        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            print(f"✓ Successfully posted comment to {post_id}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Error posting comment: {e}")
            return False

    def run(self, group_ids: Optional[List[str]] = None):
        """
        Run the agent to find and comment on job search posts.

        Args:
            group_ids: List of Facebook group IDs to search (optional)
        """
        print("=" * 60)
        print("Facebook Job Search Agent")
        print("=" * 60)
        print(f"Mode: {'DRY RUN (no actual comments)' if self.dry_run else 'LIVE'}")
        print(f"Max comments per run: {self.max_comments}")
        print()

        all_posts = []

        # Search in groups if provided
        if group_ids:
            for group_id in group_ids:
                print(f"Searching group {group_id}...")
                posts = self.search_group_posts(group_id, limit=20)
                all_posts.extend(posts)
        else:
            # Search user's feed
            print("Searching your feed...")
            posts = self.search_public_posts(limit=20)
            all_posts.extend(posts)

        print(f"Found {len(all_posts)} total posts")
        print()

        # Filter for job-related posts
        job_posts = []
        for post in all_posts:
            message = post.get("message", "")
            if self.is_job_related_post(message):
                job_posts.append(post)

        print(f"Found {len(job_posts)} job-related posts")
        print()

        # Comment on job posts (up to max_comments)
        comments_posted = 0

        for post in job_posts[:self.max_comments]:
            if comments_posted >= self.max_comments:
                break

            post_id = post.get("id")
            message = post.get("message", "")
            author = post.get("from", {}).get("name", "Unknown")

            print("-" * 60)
            print(f"Post by: {author}")
            print(f"Content: {message[:100]}...")
            print()

            # Generate comment
            print("Generating comment...")
            comment = self.generate_comment(message)

            if comment:
                # Post comment
                success = self.post_comment(post_id, comment)
                if success:
                    comments_posted += 1
                    # Be respectful - wait between comments
                    time.sleep(2)

            print()

        print("=" * 60)
        print(f"Completed! Posted {comments_posted} comments.")
        print("=" * 60)


def main():
    """Main function to run the agent."""
    # Initialize agent in dry run mode by default
    agent = FacebookJobAgent(
        max_comments_per_run=5,
        dry_run=True  # Set to False to actually post comments
    )

    # Example: Run on your feed
    agent.run()

    # Example: Run on specific groups (uncomment and add your group IDs)
    # group_ids = ["123456789", "987654321"]
    # agent.run(group_ids=group_ids)


if __name__ == "__main__":
    main()
