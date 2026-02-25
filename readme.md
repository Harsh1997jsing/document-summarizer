# 📄 Document Summarizer

A FastAPI-based application that connects to Google Drive, fetches documents (PDF, DOCX, TXT), extracts text, and summarizes each document using OpenAI GPT.

---

## 🏗️ Project Structure

```
doc_summarizer/
│
├── app/
│   ├── api/
│   │   ├── __init__.py              # Registers all routers
│   │   ├── drive_routes.py          # Google Drive API routes
│   │   └── summarize_routes.py      # Summarization API routes
│   │
│   ├── auth/
│   │   └── google_auth.py           # Google OAuth2 authentication
│   │
│   ├── clients/
│   │   ├── drive_client.py          # Google Drive client
│   │   └── llm_client.py            # OpenAI API client
│   │
│   ├── output/
│   │   ├── csv_exporter.py          # Export summaries to CSV
│   │   └── pdf_exporter.py          # Export summaries to PDF
│   │
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── parser_factory.py        # Auto-detects file type and parses
│   │   ├── pdf_parser.py            # PDF text extraction
│   │   ├── docx_parser.py           # DOCX text extraction
│   │   └── txt_parser.py            # TXT text extraction
│   │
│   ├── services/
│   │   ├── pipeline.py              # Main orchestration (Drive → Parse → Summarize)
|   |
│   │
│   ├── utils/                       # Helper/utility functions
│   │
│   ├── __init__.py
│   ├── config.py                    # App configuration from .env
│   └── main.py                      # FastAPI entry point
│
├── credentials/
│   └── credentials.json             # Google OAuth2 credentials (gitignored)
│
├── downloads/                       # Downloaded files from Drive (gitignored)
├── .env                             # Environment variables (gitignored)
├── .env.example                     # Example env file
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Harsh1997jsing/document-summarizer.git
cd doc_summarizer
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Then open `.env` and fill in your values:

```env
OPENAI_API_KEY=your-openai-api-key
DRIVE_FOLDER_ID=your-google-drive-folder-id
```

### 5. Setup Google Drive Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Google Drive API**
4. Go to **APIs & Services → Credentials**
5. Create **OAuth 2.0 Client ID** → Desktop App
6. Download the JSON file
7. Rename it to `credentials.json`
8. Place it inside the `credentials/` folder

### 6. Run the Application

```bash
python app/main.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/drive/connect` | Test Google Drive connection |
| `GET` | `/drive/files?folder_id=<id>` | List files in a Drive folder |
| `POST` | `/summarize` | Run full summarization pipeline |
| `GET` | `/summarize/status` | Summarizer health check |

### POST /summarize — Request Body

```json
{
  "folder_id": "your_google_drive_folder_id",
  "download_dir": "downloads"
}
```

### POST /summarize — Response

```json
{
  "status": "success",
  "folder_id": "your_folder_id",
  "total": 3,
  "success_count": 3,
  "failed_count": 0,
  "results": [
    {
      "file_name": "report.pdf",
      "summary": "This document discusses...",
      "status": "success",
      "error": null
    }
  ]
}
```

---

## 📖 Swagger Docs

Once the server is running, visit:

- **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📦 Requirements

- Python 3.9+
- OpenAI API Key
- Google Cloud OAuth2 Credentials

---

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `OPENAI_API_KEY` | Your OpenAI API key | required |
| `OPENAI_MODEL` | GPT model to use | `gpt-4o-mini` |
| `GOOGLE_CREDENTIALS_PATH` | Path to credentials.json | `credentials/credentials.json` |
| `GOOGLE_TOKEN_PATH` | Path to save token.json | `credentials/token.json` |
| `DRIVE_FOLDER_ID` | Default Drive folder ID | optional |
| `DOWNLOAD_DIR` | Local folder for downloads | `downloads` |

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI |
| AI Summarization | OpenAI GPT |
| Google Drive | Google Drive API v3 + OAuth2 |
| PDF Parsing | PyMuPDF (fitz) |
| DOCX Parsing | python-docx |
| Server | Uvicorn |
| Config | python-dotenv |

---

## 📝 License

MIT License