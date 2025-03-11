import json
import openai
from github import Github
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Format: "owner/repo"

# Initialize GitHub client (No Token Needed for Public Repos)
g = Github()  
repo = g.get_repo(GITHUB_REPO)

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# JSON storage
review_results = []

def get_file_content(file):
    """Fetch file content from GitHub"""
    try:
        content = repo.get_contents(file.path).decoded_content.decode("utf-8")
        return content
    except Exception as e:
        print(f"❌ Error fetching {file.path}: {e}")
        return None

def review_code(file_content):
    """Use AI models to review code"""
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
            reviews[model_name] = f"❌ OpenAI API Error: {e}"

    return reviews

# Fetch all files from the repository
def get_all_files(repo, path=""):
    """Recursively get all files in a repository"""
    files = []
    contents = repo.get_contents(path)
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            files.append(file_content)
    
    return files

files = get_all_files(repo)

# Review each file
for file in files:
    print(f"📂 Reviewing: {file.path}")
    content = get_file_content(file)
    if content:
        reviews = review_code(content)
        review_results.append({"filename": file.path, "reviews": reviews})

# Store the results in a JSON file
with open("wt_code_review.json", "w") as json_file:
    json.dump(review_results, json_file, indent=4)

# Final output message
if review_results:
    print(f"✅ AI Code Review Completed. {len(review_results)} files reviewed. Results saved in code_review.json.")
else:
    print("⚠️ No reviews generated. Check if the repository has files or if OpenAI API is responding.")
