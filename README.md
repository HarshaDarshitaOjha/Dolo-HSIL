# 🩺 Dolo - Medical Report AI Analyzer

Dolo is an AI-powered medical report analysis backend that helps users understand complex medical documents. By leveraging Gemini 2.5 Flash, Dolo extracts key health insights from uploaded reports and maintains a contextual conversation with the user to answer follow-up questions.

![Dolo AI](https://img.shields.io/badge/Dolo-v1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Gemini 2.5](https://img.shields.io/badge/Gemini-2.5_Flash-orange)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

---

## ✨ Features

- **🔍 Intelligent Report Analysis**: Automatically extracts and summarizes data from medical report images (PNG, JPEG, WEBP).
- **💬 Context-Aware Chat**: Remembers previous messages and report contexts within a conversation for specialized follow-up.
- **🖼️ Persistent Storage**: Securely stores uploaded reports and conversation history for longitudinal health tracking.
- **📄 Structured Insights**: Attempts to provide AI responses in structured JSON format for potential frontend integration.
- **🚀 High Performance**: Built with FastAPI for rapid response times and efficient asynchronous handling.

---

## 🎯 How It Works

### 📊 The Analysis Pipeline

Dolo uses a multi-stage process to transform a medical image into a meaningful conversation.

```mermaid
graph TD
    A[Medical Report Image] --> B[Upload & Storage]
    B --> C[Context Extraction]
    C --> D{Gemini Vision Engine}
    D --> E[Structured Analysis]
    E --> F[Conversation Memory]
    F --> G[Health Assistant Response]
    
    subgraph "The Analysis Engine"
    D1["Vision: OCR & Image Interpretation"]
    D2["NLP: Contextual Reasoning"]
    end
```

### 🏗️ Architecture

```mermaid
graph LR
    User((User)) <--> API[FastAPI Backend]
    API <--> AI[Gemini 2.5 Flash]
    API <--> DB[(PostgreSQL Database)]
    API <--> Storage[File System /uploads]
    
    subgraph "Backend Modules"
    API --- R[Analyze & Chat Routers]
    API --- S[AI & Memory Services]
    API --- M[SQLAlchemy Models]
    end
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- A Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### Setup

1. **Clone the repository and navigate to the backend:**

   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Create a `.env` file in the `backend/` directory:

   ```env
   DATABASE_URL=postgresql://user:password@localhost/dolo_db
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the server:**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

---

## 📁 Project Structure

```text
Dolo-HSIL/
├── backend/
│   ├── main.py             # FastAPI entry point & app config
│   ├── database.py         # SQLAlchemy engine & session management
│   ├── config.py           # Environment variable loader
│   ├── models/             # Database models (Conversation, Report, etc.)
│   ├── routers/            # API endpoints (analyze.py, conversation.py)
│   ├── services/           # Business logic (ai_service, memory_service)
│   ├── schemas/            # Pydantic validation schemas
│   └── uploads/            # Local storage for report images
├── README.md               # Current documentation
└── README_INSPIRATION.md   # Structural template
```

---

## 🔌 API Endpoints

### AI Analysis & Chat

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/analyze-report/{id}` | Upload an image for structured AI analysis |
| POST | `/chat/{id}` | Send a text message to continue the conversation |

### Conversations

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| POST | `/conversation/` | Create a new conversation session |
| GET | `/conversation/{id}` | Retrieve history of a specific conversation |
| GET | `/conversation/{id}/reports` | List all reports associated with a session |

### System

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| GET | `/health` | Check service health status |

---

## 💻 Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Engine**: [Google Generative AI (Gemini 2.5 Flash)](https://ai.google.dev/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)

---

## 📝 License

This project is licensed under the MIT License.

---

## 🏥 Medical Disclaimer

**IMPORTANT**: Dolo is a tool for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read through this application.
