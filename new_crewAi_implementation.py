import json
import openai
import requests
from crewai import Crew, Agent, Task
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # Example: "octocat/Hello-World"
FUNCTIONALITY_DOC_PATH = "functionality_doc.txt"
serialized_results = []

# Function to fetch repository files
def get_repo_files(repo_name):
    url = f"https://api.github.com/repos/{repo_name}/contents/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching repo files:", response.json())
        return []

# Read functionality document
def read_functionality_doc():
    with open(FUNCTIONALITY_DOC_PATH, "r") as file:
        return file.read()

# Initialize OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Define CrewAI Agents for Python & Web Files
potential_tester = Agent(
    role="Potential Code Tester",
    goal="Perform an initial check for syntax errors, structure, and formatting across Python, JavaScript, HTML, and CSS files.",
    backstory="An expert at identifying syntax issues, code structure flaws, and formatting inconsistencies in Python and web development files.",
    model="gpt-4-turbo"
)

senior_tester = Agent(
    role="Senior Security & Performance Tester",
    goal="Analyze the performance and security vulnerabilities of Python, JavaScript, HTML, and CSS files.",
    backstory="A security specialist and performance optimizer focusing on preventing vulnerabilities and improving efficiency.",
    model="gpt-4-turbo"
)

senior_fullstack_tester = Agent(
    role="Senior Full Stack Code Reviewer",
    goal="Validate business logic, API integrations, and frontend/backend architecture based on the functionality document.",
    backstory="An experienced software architect who ensures all files meet the required functionality and coding standards.",
    model="gpt-4-turbo"
)

# Get repository files
repo_files = get_repo_files(GITHUB_REPO)
functionality_description = read_functionality_doc()
review_results = []

# Process relevant files
for file in repo_files:
    if file['type'] == 'file' and file['name'].endswith(('.py', '.js', '.html', '.css')):  
        file_url = file['download_url']
        file_response = requests.get(file_url)
        
        if file_response.status_code == 200:
            file_content = file_response.text  # Get actual file content

            # Assign tasks dynamically based on file type
            if file['name'].endswith('.py'):
                task_1 = Task(
                    description=f"Analyze the following Python code for syntax errors:\n\n{file_content}",
                    agent=potential_tester,
                    expected_output="List of syntax errors with file name and line numbers."
                )

                task_2 = Task(
                    description=f"Review this Python file for performance and security issues:\n\n{file_content}",
                    agent=senior_tester,
                    expected_output="Identified performance bottlenecks and security risks and provide list of issues it should be 3, 4 which are severe or which affects the code."
                )

                task_3 = Task(
                    description=f"Check if this Python file aligns with the functionality document:\n\n{functionality_description}\n\nCode:\n{file_content}",
                    agent=senior_fullstack_tester,
                    expected_output="summary report in form of list whether the file meets functionality requirements."
                )

            else:  # JavaScript, HTML, or CSS
                task_1 = Task(
                    description=f"Analyze the following {file['name'].split('.')[-1].upper()} file for syntax errors and best practices:\n\n{file_content}",
                    agent=potential_tester,
                    expected_output="List of syntax errors and structure issues."
                )

                task_2 = Task(
                    description=f"Review this {file['name'].split('.')[-1].upper()} file for performance and security risks:\n\n{file_content}",
                    agent=senior_tester,
                    expected_output="Identified performance bottlenecks and security risks and provide list of issues it should be 3, 4 which are severe or which affects the code."
                )

                task_3 = Task(
                    description=f"Check if this {file['name'].split('.')[-1].upper()} file aligns with the functionality document:\n\n{functionality_description}\n\nCode:\n{file_content}",
                    agent=senior_fullstack_tester,
                    expected_output="summary report in form of list whether the file meets functionality requirements."
                )

            # Create crew
            crew = Crew(
                agents=[potential_tester, senior_tester, senior_fullstack_tester],
                tasks=[task_1, task_2, task_3]
            )
            # Run tasks and collect responses
            results = crew.kickoff()

            review_results.append({
                "filename": file['name'],
                "reviews": str(results)  # Convert CrewOutput object to string
            })

# Save results in JSON format
with open("crewAi_output.json", "w", encoding="utf-8") as json_file:
    json.dump(review_results, json_file, indent=4, ensure_ascii=False)

# Save results in a formatted text file
with open("crewAi_output.txt", "w", encoding="utf-8") as text_file:
    for output in review_results:
        text_file.write(f"Filename: {output['filename']}\n")
        text_file.write(f"Reviews:\n{output['reviews']}\n")
        text_file.write("=" * 80 + "\n\n")  # Add a separator for readability

print("✅ AI Code Review Completed. Results saved in crewAi_output.json & crewAi_output.txt.")
