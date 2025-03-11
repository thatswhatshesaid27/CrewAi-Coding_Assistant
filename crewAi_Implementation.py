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
FUNCTIONALITY_DOC_PATH = "functionality_doc.txt"  # Local path to the functionality document
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

# Define CrewAI Agents
potential_tester = Agent(
    role="Potential Tester",
    goal="Perform an initial check for syntax errors, code structure, and formatting across all Python files in the repository.",
    backstory="A meticulous tester specializing in identifying syntax errors, indentation issues, and PEP8 violations in Python code.",
    model="gpt-4-turbo"
)

senior_tester = Agent(
    role="Senior Tester",
    goal="Analyze the performance and security vulnerabilities of the Python files based on the functionality document.",
    backstory="A performance and security expert with a focus on optimizing Python scripts, preventing vulnerabilities like SQL injection, and ensuring efficient memory usage.",
    model="gpt-4-turbo"
)

senior_fullstack_tester = Agent(
    role="Senior Full Stack Tester",
    goal="Validate business logic, API endpoints, and code architecture of the Python scripts based on the provided functionality document.",
    backstory="An experienced software architect with a deep understanding of Python backend workflows, API integrations, and error handling mechanisms.",
    model="gpt-4-turbo"
)

# Get repository files
repo_files = get_repo_files(GITHUB_REPO)
print("Type of repo_files variables", type(repo_files))
functionality_description = read_functionality_doc()
review_results = []

for file in repo_files:
    if file['type'] == 'file' and file['name'].endswith('.py'):  # Only process Python files
        file_url = file['download_url']
        file_response = requests.get(file_url)
        
        if file_response.status_code == 200:
            file_content = file_response.text  # Get actual Python code

            # Assign tasks with actual file content
            task_1 = Task(
                description=f"Analyze the following Python code for syntax errors:\n\n{file_content}",
                agent=potential_tester,
                expected_output="List of syntax errors with file name and line numbers."
            )

            task_2 = Task(
                description=f"Review this Python file for performance and security issues:\n\n{file_content}",
                agent=senior_tester,
                expected_output="Identified performance bottlenecks and security risks."
            )

            task_3 = Task(
                description=f"Check if this Python file aligns with the functionality document:\n\n{functionality_description}\n\nCode:\n{file_content}",
                agent=senior_fullstack_tester,
                expected_output="Detailed report on whether the file meets functionality requirements."
            )

            # Create crew
            crew = Crew(
                agents=[potential_tester, senior_tester, senior_fullstack_tester],
                tasks=[task_1, task_2, task_3]
            )

           

            # Run tasks and collect responses
            results = crew.kickoff()
            # review_results.append({
            #     "filename": file['name'],
            #     "reviews": results
            # })



            # for output in review_results:
            #     serialized_results.append({
            #         "filename": output["filename"],
            #         "reviews": str(output["reviews"])  # Convert CrewOutput object to a string
            #     })


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



# Store results in a text file
# with open("crewAi_output.json", "w", encoding="utf-8") as json_file:
#     json.dump(review_results, json_file, indent=4, ensure_ascii=False)

# print("✅ AI Code Review Completed. Results saved in crewAi_output.json.")

# print("✅ AI Code Review Completed. Results saved in crewAi_output.txt.")
