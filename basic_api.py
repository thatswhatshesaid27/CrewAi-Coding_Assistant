from github import Github
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API keys from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Initialize GitHub client
g = Github(GITHUB_TOKEN)

# List repositories (to check token access)
for repo in g.get_user().get_repos():
    print(repo.full_name)
