# Safe Gmail Cleaner & Insights 

A high-performance, security-focused Python tool designed to automate the cleanup of old, unread emails while providing deep insights into your inbox storage and subscription habits.

## Key Features
- **Storage Savings Calculator**: See exactly how many **MB/GB** of space you'll reclaim before deleting anything.
- **Automatic categorization**: Uses Gmail's internal AI to identify if your junk mail is `Promotions`, `Social`, or `Updates`.
- **Unsubscribe Assistant**: Extracts hidden `List-Unsubscribe` links so you can get off mailing lists permanently while cleaning up.
- **Safety-First Logic**: Automatically protects emails that are **Starred**, marked as **Important**, or contain specific labels (e.g., `Tax`, `Work`, `Banking`).
- **Dry Run Mode**: Scans and summarizes candidates for review. Action only happens after your explicit `PROCEED` confirmation.
- **Real-Time Progress**: Live counter during the cleanup process.

## Prerequisites
- Python 3.10+
- A Google Cloud Project with the **Gmail API** enabled.
- OAuth 2.0 Credentials (`credentials.json`).

## Setup

### 1. Google Cloud Configuration
1.  **Create a Project**: Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  **Enable Gmail API**: Enable it in the API Library.
3.  **OAuth Consent Screen**: Set to **External** and add your email as a **Test User**.
4.  **Create Credentials**: Create an **OAuth client ID** (Desktop app) and download it as `credentials.json` in the project root.

### 2. Local Installation
1.  **Clone & Navigate**:
    ```bash
    git clone https://github.com/ChrisAnghel1/gmail-cleanup-automation.git
    cd gmail-cleanup-automation
    ```
2.  **Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the script to start the dry run analysis:
```bash
python gmail_cleanup.py
```
*(Note: On Windows, use `python` after activating your virtual environment to ensure it uses the correct interpreter.)*

### The Insights Flow:
1.  **Authentication**: Secure Google Login via your browser.
2.  **Inbox Analysis**: Scans your unread emails older than 1 year.
3.  **Review Dashboard**:
    - **Total Storage**: Shows potential space reclaimed.
    - **Category Breakdown**: See the percentage of Promotions vs Social.
    - **Sample List**: View subjects and direct **Unsubscribe links**.
4.  **Cleanup**: Type `PROCEED` to move the emails to the Trash.

## Customization
Modify `gmail_cleanup.py` to tune:
- **`PROTECTED_LABELS`**: List labels that should never be touched.
- **`SEARCH_QUERY`**: Change the filter (e.g., `older_than:2y`).

## Security Note
- **`credentials.json`** and **`token.json`** are blocked by `.gitignore`. 
- **NEVER** commit these to a public repository as they grant access to your email.
