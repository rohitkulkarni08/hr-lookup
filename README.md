# HR Employee Lookup

##Overview

The HR Employee Lookup tool simplifies retrieving employee information through a chatbot interface, reducing manual lookups and improving accessibility for HR, managers, and third-party background checks.

##Key Benefits

1. Minimizes manual effort by eliminating reliance on multiple systems.
2. Provides easy access for non-technical users to retrieve structured data.
3. Useful for HR processes, background checks, and onboarding.

## Tech Stack

1. Python – Backend logic.
2. OpenAI (GPT-4o) – Natural language processing.
3. MongoDB & AWS/Azure (Future Scope) – Scalability and data storage.

## How It Works

1. Loads employee, progress, and project data from CSV files.
2. Processes user queries via a chatbot-style interface.
3. Uses GPT-4o to identify relevant fields.
4. Retrieves and merges relevant employee data.
5. Returns structured responses to the user.

## Running the Application

Prerequisites

1. Python installed.
2. OpenAI API Key (OPENAI_API_KEY set as an environment variable).
3. Required files: employee_fact_table.csv, progress_table.csv, project_table.csv, and database_schema.txt. (These files were added as a demo, future scope is to integrate with company database tables)

Steps to Run

```ts
# Clone the repository
git clone https://github.com/rohitkulkarni08//hr-lookup.git
cd hr-employee-lookup

# Install dependencies
pip install pandas openai

# Run the script
python employee_lookup.py

Ask employee-related questions interactively. Type stop to exit.
```

## Future Enhancements

1. Database integration for direct connection to internal employee databases.
2. PII protection and role-based access for secure authentication.
3. Cloud scalability for faster lookups with cloud storage.
