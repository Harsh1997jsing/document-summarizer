# 📄 Document Summarizer

A FastAPI-based application that connects to Google Drive, fetches documents (PDF, DOCX, TXT), extracts text, and summarizes each document using OpenAI GPT.

---

## 🏗️ Project Structure

```
doc_summarizer/
│
├── app/
│   ├── api/
│   │   ├── __init__.py              
│   │   ├── drive_routes.py          
│   │   └── summarize_routes.py      
│   │
│   ├── auth/
│   │   └── google_auth.py          
│   │
│   ├── clients/
│   │   ├── drive_client.py        
│   │   └── llm_client.py           
│   │
│   ├── output/
│   │   ├── csv_exporter.py          
│   │   └── pdf_exporter.py          
│   │
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── parser_factory.py        
│   │   ├── pdf_parser.py           
│   │   ├── docx_parser.py          
│   │   └── txt_parser.py            
│   │
│   ├── services/
│   │   ├── pipeline.py              
|   |
│   │
│   ├── utils/                     
│   │
│   ├── __init__.py
│   ├── config.py                   
│   └── main.py                      
│
├── credentials/
│   └── credentials.json            
│
├── downloads/                      
├── .env                            
├── .env.example                     
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Harsh1997jsing/document-summarizer.git
cd document-summarizer
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

7. Create the `credentials` folder in the project root and move the downloaded file there. Example commands:

- Windows (PowerShell / CMD):

  mkdir credentials
  # Rename the downloaded JSON file to credentials.json and place it inside the folder

- macOS / Linux:

  mkdir -p credentials
  mv path/to/downloaded-file.json credentials/credentials.json

8. Ensure the file is located at `credentials/credentials.json`. The application will create `credentials/token.json` automatically after the first OAuth flow when you run the app.

### 6. Run the Application

```bash
python app/main.py
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload 
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



## 📖 Swagger Docs

Once the server is running, visit:

- **Swagger UI** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc** → [http://localhost:8000/redoc](http://localhost:8000/redoc)

- 

## 🖥️ Rendering UI

To view the built-in frontend UI:

1. Start the server (replace host/port if configured in your `.env`):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Open in your browser:

- Main UI: http://localhost:8000/ui
- Swagger UI: http://localhost:8000/docs

3. The UI template is located at `app/templates/index.html` and is served by the `/ui` route.

If you changed `HOST` or `PORT` in `.env`, replace `localhost:8000` with `HOST:PORT`.

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


## 📝 License

MIT License