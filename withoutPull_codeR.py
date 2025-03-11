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

# Initialize OpenAI client
client = openai.Client(api_key=OPENAI_API_KEY)

# JSON storage for review results
review_results = []

def get_repo_files(directory=""):
    """Recursively fetch all file paths from the repository."""
    contents = repo.get_contents(directory)
    # print('############ FILE CONTENT BEFORE WHILE LOOP #################:', contents)

    files = []
    
    while contents:
        file_content = contents.pop(0)
        # print('############ FILE CONTENT inside get_repo_files function #################:', file_content)
        if file_content.type == "dir":
            # print('############ FILE CONTENT INSIDE DIR FOLDER #################: ', file_content)

            contents.extend(repo.get_contents(file_content.path))  #Recursively get subdirectory files
        else:
            # print('############### files ###############', files)
            files.append(file_content.path)
    
    return files

def get_file_content(file_path):
    """Retrieve the content of a file from the repository."""
    
    file_content = repo.get_contents(file_path)
    # print('################ FILE CONTENT ############', file_content)
    print(type(file_content))
    return file_content.decoded_content.decode("utf-8")

def review_code(file_content):
    print('file content in review_code function', file_content)
    """Use AI models to review different aspects of the code."""
    prompts = {
        "syntax": f"Check for syntax errors:\n{file_content}",
        "performance": f"Analyze performance:\n{file_content}",
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
repo_files = get_repo_files()
print(f"🔍 Found {len(repo_files)} files in the repository.")

# Loop through each file and review
for file_path in repo_files:
    print("file path is", file_path)
    print(f"📂 Reviewing: {file_path}")
    try:
        file_content = get_file_content(file_path)
        reviews = review_code(file_content)
        review_results.append({"filename": file_path, "reviews": reviews})
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")

# Store the results in a JSON file
with open("code_review.json", "w") as json_file:
    json.dump(review_results, json_file, indent=4)

print(f"✅ AI Code Review Completed. {len(review_results)} files reviewed. Results saved in code_review.json.")
