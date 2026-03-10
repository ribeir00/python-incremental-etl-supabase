# Incremental Data Extraction Pipeline: Supabase to JSON

This project is a Python-based data pipeline designed for the automated and efficient extraction of tables from **Supabase** to local storage in **JSON** format. The script utilizes an incremental load architecture, ensuring that only new records are processed, optimizing bandwidth consumption and computational resources.

## Features

*   **Incremental Extraction (Delta Load):** Synchronizes only the data created after the last successful execution.
*   **Smart Reset:** Automatically detects the absence of local files and triggers a full historical load.
*   **Environment Management:** Configured via environment variables (`.env`) for credential security and directory flexibility.
*   **Path Resilience:** Automatic folder creation and cross-platform compatibility (Windows/Linux) using `os.path`.
*   **Data Governance:** Pre-configured Git exclusion rules to prevent versioning sensitive data or high-volume files.

##  Technologies Used

| Technology | Function |
| :--- | :--- |
| **Python 3.x** | Core processing pipeline. |
| **Supabase SDK** | Interface for communication with the PostgreSQL database. |
| **Pandas** | Dataframe manipulation and metadata identification. |
| **Dotenv** | Management of secrets and environment variables. |

##  Configuration and Installation

### 1. Prerequisites

Ensure you have the required libraries installed:

```bash
pip install supabase pandas python-dotenv

##Create a .env file in the project root and configure the variables as shown below:
SUPABASE_URL=[https://your-project.supabase.co] (https://your-project.supabase.co)
SUPABASE_KEY=your-service-role-admin-key
PATH_DATA=C:/path/to/store/your/data

###[!IMPORTANT]###
The service_role key must be used to ensure the bypass of RLS (Row Level Security) policies and administrative access during extraction.

Decision Logic (Data Flow)
The script operates under a robust decision logic for each processed table:

File Verification: The script checks for the existence of the *_historico.json file in the directory defined in PATH_DATA.

Reference Date Definition:

If the file DOES NOT exist: The starting date is set to 1900-01-01T00:00:00+00 (Full Load).

If the file EXISTS: The script queries the controle_extracao table in the database to retrieve the timestamp of the last processed record (Incremental Load).

Delta Filtering: Only records with a created_at strictly greater than the reference date are downloaded.

Persistence and Upsert: New data is appended to the local JSON file, and the control table is updated with the new maximum identified timestamp.

Troubleshooting
Scenario: State Desynchronization (Data Gap)
Problem: The control table in the database shows a date more recent than the actual data in the local file (e.g., after a manual deletion of records in the JSON). The script will not download the missing data because those records are not "greater than" the record stored in the database.

Solution (Recommended Action):
Due to the implemented Smart Reset logic, simply delete the .json file from your local folder and run the script again. The system will detect the absence of the physical file and automatically rebuild the entire history.

###   Project structure
├── main.py              # Main execution script
├── .env                 # Credentials and paths (not versioned)
├── .gitignore           # Git exclusion rules
└── [PATH_DATA]/         # Destination directory for JSON files