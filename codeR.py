import json
import openai
from github import Github
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# Initialize GitHub client
g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPO)
pulls = repo.get_pulls(state='open')

# Print number of open PRs
print(f"Found {pulls.totalCount} open pull requests.")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# JSON storage
review_results = []

def review_code(file_content):
    """Use AI models to review different aspects of the code."""
    prompts = {
        "syntax": f"Check for syntax errors:\n{file_content}",
        "performance": f"Analyze performance:\n{file_content}",
        "security": f"Find security vulnerabilities:\n{file_content}",
        "best_practices": f"Review best practices:\n{file_content}"
    }

    reviews = {}

    for model_name, prompt in prompts.items():
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": prompt}]
            )
            reviews[model_name] = response.choices[0].message.content
        except Exception as e:
            reviews[model_name] = f"\u274c OpenAI API Error: {e}"

    return reviews

# Loop through open PRs and review files
for pr in pulls:
    print(f" Checking PR #{pr.number}")
    pr_review = {"pull_request": pr.number, "files": []}

    for file in pr.get_files():
        print(f"Reviewing: {file.filename}")
        if file.patch:  # Ensure there is a patch (code change)
            print(f" Patch Found in {file.filename}")
            reviews = review_code(file.patch)
            file_review = {"filename": file.filename, "reviews": reviews}
            pr_review["files"].append(file_review)

    review_results.append(pr_review)

# Store the results in a JSON file
with open("code_review.json", "w") as json_file:
    json.dump(review_results, json_file, indent=4)

# Improved final output message
if review_results:
    print(f" AI Code Review Completed. {len(review_results)} PR(s) reviewed. Results saved in code_review.json.")
else:
    print(" No reviews generated. Check if PRs have changed files or if OpenAI API is responding.")