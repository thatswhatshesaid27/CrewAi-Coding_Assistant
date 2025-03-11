from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API keys from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# Fetch open PRs
pulls = repo.get_pulls(state='open')

# Print PRs
if pulls.totalCount == 0:
    print("⚠️ No open pull requests found. Check your repository name and permissions.")
else:
    print(f"✅ Found {pulls.totalCount} open pull requests:")
    for pr in pulls:
        print(f"- #{pr.number}: {pr.title}")
