from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)

# Get open PRs
pulls = repo.get_pulls(state='open')
print(f"🔍 Found {pulls.totalCount} open pull requests.")

# List PRs
for pr in pulls:
    print(f"PR #{pr.number} - {pr.title}")
