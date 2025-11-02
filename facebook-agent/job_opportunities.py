"""
Job Opportunities Module

Handles fetching and matching job opportunities from various sources.
"""

import json
import csv
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import os


@dataclass
class JobOpportunity:
    """Represents a job opportunity."""
    title: str
    location: str
    city: str
    requirements: List[str]
    description: str
    url: str
    salary: Optional[str] = None
    job_type: Optional[str] = None  # Full-time, Part-time, Contract, etc.
    experience_level: Optional[str] = None  # Entry, Mid, Senior, etc.

    def to_comment_text(self) -> str:
        """Format job details for a comment."""
        text = f"**{self.title}** in {self.location}"

        if self.job_type:
            text += f" ({self.job_type})"

        text += "\n\n"

        if self.requirements:
            text += "Key requirements:\n"
            for req in self.requirements[:3]:  # Limit to top 3
                text += f"• {req}\n"

        if self.salary:
            text += f"\nSalary: {self.salary}"

        text += f"\n\nApply here: {self.url}"

        return text


class JobSource:
    """Base class for job sources."""

    def fetch_jobs(self) -> List[JobOpportunity]:
        """Fetch jobs from the source."""
        raise NotImplementedError


class JSONFileJobSource(JobSource):
    """Load jobs from a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_jobs(self) -> List[JobOpportunity]:
        """Load jobs from JSON file."""
        if not os.path.exists(self.file_path):
            print(f"Warning: Jobs file not found at {self.file_path}")
            return []

        with open(self.file_path, 'r') as f:
            data = json.load(f)

        jobs = []
        for job_data in data:
            job = JobOpportunity(
                title=job_data['title'],
                location=job_data['location'],
                city=job_data.get('city', ''),
                requirements=job_data.get('requirements', []),
                description=job_data.get('description', ''),
                url=job_data['url'],
                salary=job_data.get('salary'),
                job_type=job_data.get('job_type'),
                experience_level=job_data.get('experience_level')
            )
            jobs.append(job)

        return jobs


class CSVFileJobSource(JobSource):
    """Load jobs from a CSV file."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def fetch_jobs(self) -> List[JobOpportunity]:
        """Load jobs from CSV file."""
        if not os.path.exists(self.file_path):
            print(f"Warning: Jobs file not found at {self.file_path}")
            return []

        jobs = []
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse requirements from comma-separated string
                requirements = []
                if 'requirements' in row and row['requirements']:
                    requirements = [req.strip() for req in row['requirements'].split(',')]

                job = JobOpportunity(
                    title=row['title'],
                    location=row['location'],
                    city=row.get('city', ''),
                    requirements=requirements,
                    description=row.get('description', ''),
                    url=row['url'],
                    salary=row.get('salary'),
                    job_type=row.get('job_type'),
                    experience_level=row.get('experience_level')
                )
                jobs.append(job)

        return jobs


class APIJobSource(JobSource):
    """Load jobs from an API endpoint."""

    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url
        self.api_key = api_key

    def fetch_jobs(self) -> List[JobOpportunity]:
        """Fetch jobs from API."""
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        try:
            response = requests.get(self.api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            jobs = []
            # Assuming API returns list of jobs
            job_list = data if isinstance(data, list) else data.get('jobs', [])

            for job_data in job_list:
                job = JobOpportunity(
                    title=job_data['title'],
                    location=job_data['location'],
                    city=job_data.get('city', ''),
                    requirements=job_data.get('requirements', []),
                    description=job_data.get('description', ''),
                    url=job_data['url'],
                    salary=job_data.get('salary'),
                    job_type=job_data.get('job_type'),
                    experience_level=job_data.get('experience_level')
                )
                jobs.append(job)

            return jobs

        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs from API: {e}")
            return []


class WebScraperJobSource(JobSource):
    """Scrape jobs from a website (requires BeautifulSoup)."""

    def __init__(self, url: str, selectors: Dict[str, str]):
        """
        Initialize web scraper.

        Args:
            url: URL to scrape
            selectors: CSS selectors for job elements
                      e.g., {'container': '.job-listing', 'title': '.job-title', ...}
        """
        self.url = url
        self.selectors = selectors

    def fetch_jobs(self) -> List[JobOpportunity]:
        """Scrape jobs from website."""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            print("Error: BeautifulSoup not installed. Run: pip install beautifulsoup4")
            return []

        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            jobs = []
            job_containers = soup.select(self.selectors.get('container', '.job'))

            for container in job_containers:
                title_elem = container.select_one(self.selectors.get('title', '.title'))
                location_elem = container.select_one(self.selectors.get('location', '.location'))
                url_elem = container.select_one(self.selectors.get('url', 'a'))

                if not (title_elem and location_elem and url_elem):
                    continue

                # Extract requirements if available
                requirements = []
                req_elem = container.select_one(self.selectors.get('requirements', '.requirements'))
                if req_elem:
                    requirements = [li.text.strip() for li in req_elem.find_all('li')]

                job = JobOpportunity(
                    title=title_elem.text.strip(),
                    location=location_elem.text.strip(),
                    city=location_elem.text.strip().split(',')[0],  # Extract city
                    requirements=requirements,
                    description='',
                    url=url_elem.get('href', ''),
                    salary=None,
                    job_type=None,
                    experience_level=None
                )
                jobs.append(job)

            return jobs

        except Exception as e:
            print(f"Error scraping jobs: {e}")
            return []


class JobMatcher:
    """Match jobs to user requirements and locations."""

    def __init__(self, jobs: List[JobOpportunity]):
        self.jobs = jobs

    def find_by_city(self, city: str, limit: int = 5) -> List[JobOpportunity]:
        """Find jobs in a specific city."""
        city_lower = city.lower()
        matching_jobs = [
            job for job in self.jobs
            if city_lower in job.city.lower() or city_lower in job.location.lower()
        ]
        return matching_jobs[:limit]

    def find_by_keywords(self, keywords: List[str], limit: int = 5) -> List[JobOpportunity]:
        """Find jobs matching keywords."""
        keywords_lower = [k.lower() for k in keywords]
        matching_jobs = []

        for job in self.jobs:
            # Check title, description, and requirements
            searchable_text = f"{job.title} {job.description} {' '.join(job.requirements)}".lower()

            if any(keyword in searchable_text for keyword in keywords_lower):
                matching_jobs.append(job)

                if len(matching_jobs) >= limit:
                    break

        return matching_jobs

    def find_best_match(self, post_content: str, city: Optional[str] = None) -> Optional[JobOpportunity]:
        """
        Find the best matching job for a post.

        Args:
            post_content: The Facebook post content
            city: Optional city to filter by

        Returns:
            Best matching job or None
        """
        # Extract keywords from post
        post_lower = post_content.lower()

        # Common job-related keywords
        tech_keywords = ['python', 'javascript', 'java', 'react', 'node', 'developer',
                        'engineer', 'software', 'frontend', 'backend', 'fullstack',
                        'data', 'analyst', 'scientist', 'devops', 'cloud', 'aws']

        business_keywords = ['marketing', 'sales', 'manager', 'accountant', 'hr',
                            'customer service', 'support', 'operations', 'analyst']

        # Find mentioned keywords in post
        mentioned_keywords = []
        for keyword in tech_keywords + business_keywords:
            if keyword in post_lower:
                mentioned_keywords.append(keyword)

        # Filter by city if provided
        candidate_jobs = self.jobs
        if city:
            candidate_jobs = self.find_by_city(city, limit=len(self.jobs))

        # Score jobs based on keyword matches
        scored_jobs = []
        for job in candidate_jobs:
            score = 0
            job_text = f"{job.title} {job.description} {' '.join(job.requirements)}".lower()

            for keyword in mentioned_keywords:
                if keyword in job_text:
                    score += 1

            if score > 0:
                scored_jobs.append((score, job))

        # Return highest scoring job
        if scored_jobs:
            scored_jobs.sort(key=lambda x: x[0], reverse=True)
            return scored_jobs[0][1]

        # If no keyword matches, return first job in the city
        if candidate_jobs:
            return candidate_jobs[0]

        return None

    def get_all_cities(self) -> List[str]:
        """Get list of all cities with job openings."""
        cities = set()
        for job in self.jobs:
            if job.city:
                cities.add(job.city)
        return sorted(list(cities))
