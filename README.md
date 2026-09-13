# NemoTheFinder

NemoTheFinder is a rental-listing prescreening workflow. It loads listings, lets a renter define preferences in a Streamlit dashboard, uses CALL-E to prescreen landlords, stores structured results in SQLite, and displays matching properties and scheduled tours.

## Prerequisites

Install these before starting:

- Python 3.10 or newer
- Git
- A CALL-E API key for live calls
- Google Calendar OAuth credentials for calendar availability and tour creation

The project has been tested with a local Python virtual environment on Windows.

## 1. Get the Project

```powershell
git clone <repository-url>
cd NemoTheFinder
```

On macOS or Linux:

```bash
git clone <repository-url>
cd NemoTheFinder
```

## 2. Create and Activate a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Use the same commands after activating the environment on macOS or Linux.

## 4. Configure Credentials

### CALL-E

Set the API key only in the current terminal session:

Windows PowerShell:

```powershell
$env:CALLE_API_KEY="your-calle-api-key"
```

macOS or Linux:

```bash
export CALLE_API_KEY="your-calle-api-key"
```

Do not commit API keys. The repository ignores `.env`, but environment variables are preferred for local development.

### Google Calendar

Place the Google OAuth client file at the repository root with this exact name:

```text
credentials.json
```

The first calendar operation opens a browser for authorization and creates:

```text
token.json
```

Both files are ignored by Git. Never commit them or share them publicly.

Calendar access is needed when the workflow fetches available slots or creates a confirmed viewing event.

## 5. Seed Demo Data

From the repository root, create the demo SQLite table and sample listings:

```powershell
python src\database\seed_demo.py
```

macOS or Linux:

```bash
python src/database/seed_demo.py
```

This recreates the `listings` table in `listings.db`. Run it only when you want to reset the local demo database.

## 6. Start the Dashboard

```powershell
streamlit run src\ui\app.py
```

macOS or Linux:

```bash
streamlit run src/ui/app.py
```

Open the URL shown by Streamlit, normally:

```text
http://localhost:8501
```

### Dashboard workflow

1. Review the loaded property cards.
2. Select renter must-haves and negotiables.
3. Click the save preferences control if you want to persist the selections.
4. Start the prescreening flow to process the input listings.
5. Watch the status output while calls are running.
6. Review property statuses, structured results, and confirmed tours.

Preferences are stored in `data/user/renter_prefs.json`.

## 7. Run Batch Prescreening Directly

The batch command reads a CSV, processes each row, and writes structured results to JSON:

```powershell
python -m src.domain.batch_prescreen `
  --input data\raw\listings.csv `
  --output data\raw\batch_results.json
```

macOS or Linux:

```bash
python -m src.domain.batch_prescreen \
  --input data/raw/listings.csv \
  --output data/raw/batch_results.json
```

Optional custom viewing slots can be supplied after `--slots`:

```powershell
python -m src.domain.batch_prescreen `
  --input data\raw\listings.csv `
  --output data\raw\batch_results.json `
  --slots "Saturday at 2:00 PM" "Saturday at 4:30 PM"
```

Input rows need at least:

- `phone`: an E.164 phone number such as `+14155552671`
- `address`: the listing address

Live batch processing requires `CALLE_API_KEY`. Use valid, authorized contact data and follow applicable telephony consent and operating-hour requirements.

## 8. Useful Checks

Compile the Python source:

```powershell
python -m compileall -q src tests
```

Verify the dashboard imports:

```powershell
python -c "import src.ui.app; print('dashboard import passed')"
```

Show batch command options:

```powershell
python -m src.domain.batch_prescreen --help
```

## Project Layout

```text
NemoTheFinder/
├── data/
│   ├── raw/                  # CSV inputs and generated batch results
│   └── user/                 # Renter preferences
├── src/
│   ├── config/               # Prompts and response schemas
│   ├── database/             # SQLite access and demo seed data
│   ├── domain/               # CALL-E workflow, batch execution, scoring
│   ├── ui/                   # Streamlit app, components, and assets
│   └── utils/                # Calendar, prompt, and mock-data helpers
├── tests/
│   └── fixtures/             # Mock CALL-E responses
├── credentials.json          # Local Google OAuth client; ignored by Git
├── token.json                # Local Google OAuth token; ignored by Git
├── listings.db               # Local SQLite database
├── requirements.txt
└── README.md
```

## Important Files

- `src/ui/app.py`: Streamlit entry point
- `src/domain/agent_runner.py`: Single landlord prescreen workflow
- `src/domain/batch_prescreen.py`: CSV batch entry point
- `src/domain/scoring.py`: Listing status and budget evaluation
- `src/database/db_manager.py`: SQLite persistence
- `src/config/prompts/prescreen_task_en.txt`: CALL-E conversation prompt
- `src/config/schemas/prescreen_schema.py`: Structured CALL-E response schema
- `data/raw/listings.csv`: Batch input listings
- `data/user/renter_prefs.json`: Saved renter preferences

## Troubleshooting

### `ModuleNotFoundError`

Confirm the virtual environment is active and install dependencies again:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### `CALLE_API_KEY environment variable missing`

Set the key in the same terminal where you run Streamlit or the batch command.

### No listings appear

Run the demo seed command, then restart or refresh Streamlit:

```powershell
python src\database\seed_demo.py
streamlit run src\ui\app.py
```

### Google authentication fails

Confirm `credentials.json` is at the repository root. Delete the local `token.json` only if you need to repeat OAuth authorization.

### Port 8501 is already in use

Start Streamlit on another port:

```powershell
streamlit run src\ui\app.py --server.port 8502
```
