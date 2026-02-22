🏥 Dolo — AI-Powered Medical Report Analyzer

AI middleware backend that analyzes medical report images + lab values using Google Gemini 2.5 Flash (Vision + Text) and returns structured, clinically readable JSON responses with severity levels and recommendations.

Built with FastAPI + PostgreSQL + SQLAlchemy and designed for clean AI memory handling and production deployment.

✨ Features

🧠 Multi-turn AI conversation memory

🖼️ Medical report image analysis (Vision model)

📊 Structured JSON clinical outputs

⚠️ Severity classification (low / medium / high)

🧪 Recommended follow-up tests

💡 Lifestyle suggestions

🗂️ Conversation + report history storage

🔒 Clean architecture with service layer separation

🛠️ Tech Stack
Layer	Tool
Backend Framework	FastAPI
Database	PostgreSQL (Neon)
ORM	SQLAlchemy
AI Model	Google Gemini 2.5 Flash
Image Handling	Base64 encoding
Environment Config	python-dotenv

🏗️ System Architecture
User uploads image

↓

Backend receives file (FastAPI)

↓

Validates type + size → Saves to disk + DB

↓

Converts to base64 → Builds context:

→ System prompt (guardrails + JSON format)

→ Memory prompt (conversation continuity)

→ Last 10 messages from DB

→ New user message + image

↓

Sends to Google Gemini 2.5 Flash (temp=0.2)

↓

Stores AI response in PostgreSQL

↓

Returns structured JSON to client

📁 Project Structure
backend/

├── [main.py](http://main.py)                 # FastAPI app + CORS + error handling

├── [config.py](http://config.py)               # Environment variable loader

├── [database.py](http://database.py)             # SQLAlchemy engine + session

├── models/

│   ├── [conversation.py](http://conversation.py)     # Conversation model

│   ├── [message.py](http://message.py)          # Message model

│   └── [report.py](http://report.py)           # Report (stored images) model

├── schemas/

│   └── [schemas.py](http://schemas.py)          # Pydantic request/response schemas

├── routers/

│   ├── [conversation.py](http://conversation.py)     # Conversation CRUD endpoints

│   └── [analyze.py](http://analyze.py)          # Text chat + image analysis endpoints

├── services/

│   ├── ai_[service.py](http://service.py)       # Gemini API integration (text + vision)

│   └── memory_[service.py](http://service.py)   # Context builder + message storage

├── utils/

│   └── [prompts.py](http://prompts.py)          # System + memory prompt templates

├── uploads/                # Stored report images

├── requirements.txt

└── .env                    # API keys (not committed)

📡 API Endpoints
🩺 Health Check
GET /health
{
  "status": "ok",
  "service": "Dolo AI Backend",
  "version": "1.0.0"
}
💬 Create Conversation
POST /conversation/
{
  "title": "Blood Test Analysis"
}

Response:

{
  "id": 1,
  "title": "Blood Test Analysis",
  "created_at": "...",
  "messages": []
}
📖 Get Conversation
GET /conversation/{conversation_id}

Returns full conversation history including stored AI responses.

🧠 Text Chat (With Memory)
POST /chat/{conversation_id}
{
  "message": "My hemoglobin is 10.2 g/dL and WBC is 12,500. Is this normal?"
}

Response:

{
  "conversation_id": 1,
  "response": {
    "summary": "Mildly low hemoglobin with elevated WBC count",
    "abnormal_findings": [
      {
        "parameter": "Hemoglobin",
        "value": "10.2 g/dL",
        "normal_range": "12-16 g/dL",
        "severity": "medium"
      },
      {
        "parameter": "WBC",
        "value": "12,500",
        "normal_range": "4,500-11,000",
        "severity": "low"
      }
    ],
    "recommended_tests": [
      "Iron studies",
      "Peripheral blood smear"
    ],
    "lifestyle_suggestions": [
      "Increase iron-rich foods",
      "Follow up in 2 weeks"
    ],
    "urgency": "medium"
  }
}
🖼️ Image Analysis
POST /analyze-report/{conversation_id}

Content-Type: multipart/form-data

file: medical report image

message: optional text prompt

Example:

file: blood_test.jpg
message: "Analyze this blood test report"

Response:

{
  "conversation_id": 1,
  "report_id": 1,
  "filename": "blood_test.jpg",
  "file_url": "/uploads/1708123456_blood_test.jpg",
  "response": {
    "summary": "...",
    "abnormal_findings": [...],
    "recommended_tests": [...],
    "lifestyle_suggestions": [...],
    "urgency": "medium"
  }
}
🗂️ Get Reports for a Conversation
GET /conversation/{conversation_id}/reports

Returns all uploaded medical reports linked to that conversation.

🚀 Run Locally
Prerequisites

Python 3.10+

PostgreSQL database (e.g., Neon)

Google Gemini API key

1️⃣ Clone Repository
git clone https://github.com/your-username/dolo-backend.git
cd dolo-backend/backend
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables

Create a .env file:

DATABASE_URL=postgresql://username:password@host/dbname
GEMINI_API_KEY=your_google_gemini_api_key
5️⃣ Run Server
uvicorn main:app --reload

Server runs at:

http://localhost:8000

Swagger docs available at:

http://localhost:8000/docs
🔐 AI Design Principles

Deterministic output (temperature = 0.2)

Strict JSON schema enforcement

Medical safety guardrails in system prompt

Limited memory window (last 10 messages)

Clean separation between AI service and memory service

📌 Future Improvements

Role-based authentication

PDF report support

Structured lab reference ranges by region

Redis caching for context building

Deployment on Render / Railway

Frontend dashboard (React)

⚠️ Disclaimer

Dolo is an AI-assisted medical interpretation tool.
It does not replace professional medical diagnosis.
Users must consult licensed healthcare providers for medical decisions.

🧑‍💻 Author

Built with precision and structured architecture for production-ready AI middleware.
