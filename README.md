# CrewAI GitHub Repository Validator

## 🚀 Overview
This application leverages **CrewAI** to analyze, review, and validate Python repositories hosted on GitHub. It utilizes AI-powered agents to identify syntax errors, review code performance, and validate functionality against a predefined document. The results are stored in both **TXT** and **JSON** formats for easy reference.

## 🛠 Features
- 📌 **Automated Code Review**: Detects syntax errors, inefficiencies, and best practices violations.
- 🔍 **Functionality Validation**: Ensures code meets the expected functionality described in `functionality_doc.txt`.
- ⚡ **Performance Optimization Suggestions**: Identifies performance bottlenecks and suggests improvements.
- 🔐 **Security Checks**: Highlights potential security vulnerabilities.
- 📜 **Structured Output**: Results are stored in `crewAi_output.txt` and `crewAi_output.json`.

## 🤖 AI Agents
This application uses three specialized AI agents:
1. **Potential Tester**: Performs an initial review of syntax errors, code structure, and formatting.
2. **Senior Tester**: Focuses on performance optimizations, security vulnerabilities, and efficient coding practices.
3. **Senior Full-Stack Tester**: Validates business logic, API endpoints, and overall code architecture.

## 📝 Prerequisites
Before running the application, create a `.env` file and add the following details:

```
OPENAI_API_KEY=your_openai_api_key
GITHUB_REPO=your_github_repository
```

Also, define the expected functionality of your repository in `functionality_doc.txt`. This document should outline what the code is supposed to do, providing a reference for validation.

## 📌 Setup & Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```
2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your OpenAI API key and GitHub repository name.
4. Run the script:
   ```sh
   python crewAi_Implementation.py
   ```
5. The validation results will be available in:
   - `crewAi_output.txt`
   - `crewAi_output.json`

## 📊 Expected Output
The output includes:
- **Syntax error reports** (line numbers & issues found)
- **Performance analysis** (loop optimizations, memory efficiency, etc.)
- **Functionality validation** (comparison with `functionality_doc.txt`)
- **Improvement suggestions**

## 🛠 Example Functionality Document (functionality_doc.txt)
```
This repository contains Python scripts for:
1. Counting occurrences of numbers in a list (frequency.py)
2. Finding the maximum number in a list (max.py)
3. Checking if a number is prime (prime.py)

Each script should correctly implement the described functionality without logical or performance issues.
```

## 🎯 Future Enhancements
- Extend support for more programming languages.
- Add additional AI agents for in-depth security analysis.
- Implement GitHub Actions for automated validation on every commit.



