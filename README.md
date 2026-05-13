# Google Drive AI Agent

A conversational AI assistant that helps users search, filter, and discover files from Google Drive using natural language.

Built using:
- FastAPI
- Streamlit
- LangChain
- Groq LLM
- Google Drive API

---

# Features

- Conversational file search
- Exact filename search
- Partial filename search
- File type filtering
- PDF, Docs, Sheets, Image support
- Full text document search
- Date-based filtering
- Conversational memory
- Clickable Google Drive links

---

# Tech Stack

## Backend
- FastAPI
- LangChain
- Groq API

## Frontend
- Streamlit

## APIs
- Google Drive API

---

# Architecture

User Query
↓
LangChain Conversational Agent
↓
DriveSearchTool
↓
Google Drive API (`files.list` + `q`)
↓
Results Returned to Streamlit UI

---

# Google Drive Search Features

The agent supports:
- `name='file.pdf'` → exact search
- `name contains 'report'` → partial search
- `mimeType='application/pdf'` → file type filtering
- `fullText contains 'marketing'` → content search
- `modifiedTime > 'timestamp'` → date filtering

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_LINK
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\\Scripts\\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key
```

---

## 5. Add Google Service Account

Place:

```text
service_account.json
```

inside:

```text
backend/app/
```

---

# Run Backend

```bash
cd backend/app
uvicorn main:app --reload
```

---

# Run Frontend

```bash
cd frontend
streamlit run streamlit_app.py
```

---

# Deployment

## Backend
- Railway

## Frontend
- Streamlit Cloud

---

# Future Improvements

- Semantic search
- Better ranking
- Pagination
- LangGraph migration
- Vector search support

---

# Author

Aradhya Gupta