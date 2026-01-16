# 🧹 Safe Gmail Cleaner & Insights

<div align="center">

A high-performance, security-focused Python tool designed to automate the cleanup of old, unread emails while providing deep insights into your inbox storage and subscription habits. 

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Gmail API](https://img.shields.io/badge/Gmail-API-red.svg)](https://developers.google.com/gmail/api)
[![Pandas](https://img.shields.io/badge/Pandas-Powered-150458.svg?logo=pandas)](https://pandas.pydata.org/)

</div>

---

## ✨ Key Features

- 💾 **Storage Savings Calculator** - See exactly how many MB/GB of space you'll reclaim before deleting anything
- 📊 **Pandas-Powered Analysis** - Advanced data processing and insights using Pandas for efficient email categorization and reporting
- 🏷️ **Automatic Categorization** - Uses Gmail's internal AI to identify if your junk mail is `Promotions`, `Social`, or `Updates`
- ✉️ **Unsubscribe Assistant** - Extracts hidden `List-Unsubscribe` links so you can get off mailing lists permanently
- 🛡️ **Safety-First Logic** - Automatically protects emails that are **Starred**, marked as **Important**, or contain specific labels (e.g., `Tax`, `Work`, `Banking`)
- 🔍 **Dry Run Mode** - Scans and summarizes candidates for review. Action only happens after your explicit `PROCEED` confirmation
- ⚡ **Real-Time Progress** - Live counter during the cleanup process

---

## 📋 Prerequisites

Before you begin, ensure you have the following: 

- **Python 3.10+** installed on your system
- A **Google Cloud Project** with the Gmail API enabled
- **OAuth 2.0 Credentials** (`credentials.json`)

---

## 🚀 Setup

### 1️⃣ Google Cloud Configuration

1. **Create a Project**
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one

2. **Enable Gmail API**
   - Go to the API Library
   - Search for "Gmail API" and enable it

3. **Configure OAuth Consent Screen**
   - Set the user type to **External**
   - Add your email address as a **Test User**

4. **Create OAuth Credentials**
   - Go to **Credentials** → **Create Credentials** → **OAuth client ID**
   - Select **Desktop app** as the application type
   - Download the credentials file and save it as `credentials.json` in the project root

### 2️⃣ Local Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ChrisAnghel1/Gmail-Cleanup-Automation.git
   cd Gmail-Cleanup-Automation
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv .venv
   ```
   
   **Activate the environment:**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux: 
     ```bash
     source .venv/bin/activate
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### Running the Tool

Start the dry run analysis with: 

```bash
python gmail_cleanup.py
```

> **Note:** On Windows, use `python` after activating your virtual environment to ensure it uses the correct interpreter.

### 🔄 The Workflow

1. **🔐 Authentication**
   - Secure Google Login via your browser on first run
   - Credentials are saved locally for future use

2. **📊 Inbox Analysis**
   - Scans your unread emails older than 1 year
   - Identifies safe candidates for deletion

3. **📈 Review Dashboard**
   - **Total Storage**: Shows potential space to be reclaimed
   - **Category Breakdown**: View percentage distribution (Promotions, Social, Updates)
   - **Sample List**:  Preview email subjects with direct **Unsubscribe links**

4. **🗑️ Cleanup**
   - Review the summary carefully
   - Type `PROCEED` to move the emails to Trash
   - Cancel anytime without making changes

---

## ⚙️ Customization

You can customize the behavior by modifying `gmail_cleanup.py`:

| Configuration | Description | Default |
|--------------|-------------|---------|
| `PROTECTED_LABELS` | Labels that should never be touched | `['Tax', 'Work', 'Banking']` |
| `SEARCH_QUERY` | Email filter criteria | `older_than:1y` |

### Example Modifications

```python
# Change the age threshold to 2 years
SEARCH_QUERY = "is:unread older_than:2y"

# Add more protected labels
PROTECTED_LABELS = ['Tax', 'Work', 'Banking', 'Legal', 'Important']
```

---

## 🔒 Security & Privacy

- ✅ **`credentials.json`** and **`token.json`** are automatically excluded via `.gitignore`
- ✅ All authentication happens locally on your machine
- ✅ No third-party servers process your data
- ⚠️ **NEVER** commit credential files to public repositories as they grant access to your email

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  Feel free to check the [issues page](https://github.com/ChrisAnghel1/Gmail-Cleanup-Automation/issues).

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ChrisAnghel1/Gmail-Cleanup-Automation/blob/main/LICENSE) file for details.

---

<div align="center">

**⭐ If you find this tool helpful, please consider giving it a star! **

</div>
