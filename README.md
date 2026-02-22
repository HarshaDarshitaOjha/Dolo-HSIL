# 🏥 Dolo — AI-Powered Medical Report Analyzer

An AI middleware backend that accepts medical report images, analyzes them using Google Gemini 2.5 Flash, maintains multi-turn conversation memory, and returns structured JSON responses with findings, severity levels, and recommendations.

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| **Backend** | FastAPI |
| **Database** | PostgreSQL (Neon) |
| **ORM** | SQLAlchemy |
| **AI Model** | Google Gemini 2.5 Flash (Vision + Text) |
| **Image Handling** | base64 encoding |
| **Env Config** | python-dotenv |

## 🏗️ Architecture
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

## 📁 Project Structure
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


## 📡 API Endpoints

### Health Check
GET /health

```

```

{ "status": "ok", "service": "Dolo AI Backend", "version": "1.0.0" }

```

### Create Conversation
```

POST /conversation/

Content-Type: application/json

{ "title": "Blood Test Analysis" }

```

```

{ "id": 1, "title": "Blood Test Analysis", "created_at": "...", "messages": [] }

```

### Get Conversation
```

GET /conversation/{conversation_id}

```

### Text Chat (with memory)
```

POST /chat/{conversation_id}

Content-Type: application/json

{ "message": "My hemoglobin is 10.2 g/dL and WBC is 12,500. Is this normal?" }

```

```

{

"conversation_id": 1,

"response": {

"summary": "Mildly low hemoglobin with elevated WBC count",

"abnormal_findings": [

{ "parameter": "Hemoglobin", "value": "10.2 g/dL", "normal_range": "12-16 g/dL", "severity": "medium" },

{ "parameter": "WBC", "value": "12,500", "normal_range": "4,500-11,000", "severity": "low" }

],

"recommended_tests": ["Iron studies", "Peripheral blood smear"],

"lifestyle_suggestions": ["Increase iron-rich foods", "Follow up in 2 weeks"],

"urgency": "medium"

}

}

```

### Image Analysis
```

POST /analyze-report/{conversation_id}

Content-Type: multipart/form-data

file: <medical_report_image>

message: "Analyze this blood test report"

```

```

{

"conversation_id": 1,

"report_id": 1,

"filename": "blood_test.jpg",

"file_url": "/uploads/1708123456_blood_test.jpg",

"response": { "summary": "...", "abnormal_findings": [...], ... }

}

```

### Get Reports for a Conversation
```

GET /conversation/{conversation_id}/reports

```

## 🚀 Run Locally

### Prerequisites
- Python 3.10+
- PostgreSQL database (e.g., [Neon](https://neon.tech))
- Google Gemini API key

### Setup
```
↓

Returns structured JSON to client
