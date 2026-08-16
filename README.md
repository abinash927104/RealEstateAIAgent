# 🏠 RealEstateAI — AI-Powered Real Estate Assistant

An intelligent real estate platform combining **Next.js 15**, **FastAPI**, **LangGraph AI Agent**, **ChromaDB RAG**, and **PostgreSQL** to provide property search, mortgage calculations, ROI analysis, and market insights through natural conversation.

## 🏗️ Architecture

```
User (Browser) → Next.js Frontend → FastAPI Backend → Query Analyzer
                                                         ├── GREETING → Direct Response
                                                         ├── SIMPLE → RAG Pipeline (ChromaDB)
                                                         └── COMPLEX → AI Agent (LangGraph)
                                                                         ├── Property Search
                                                                         ├── Mortgage Calculator
                                                                         ├── ROI Analysis
                                                                         └── Market Analysis
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- OpenAI API key

### 1. Clone & Configure
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Start Infrastructure (PostgreSQL + Redis)
```bash
docker-compose up -d postgres redis
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Seed the database with sample data
python -m app.db.seed

# Start the backend
uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Open
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🧠 AI Features

| Feature | Description |
|---------|-------------|
| **Property Search** | Natural language search with semantic matching (ChromaDB) |
| **Mortgage Calculator** | Deterministic monthly payment breakdown with taxes/insurance |
| **ROI Analysis** | Cap rate, cash-on-cash return, 5-year projection with grading |
| **Market Analysis** | Aggregate stats, property type distribution, price ranges |
| **Query Routing** | Automatic classification to RAG (simple) or Agent (complex) |

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, React 19, Tailwind CSS |
| Backend | FastAPI, Python 3.12 |
| AI Agent | LangChain + LangGraph |
| Vector DB | ChromaDB |
| Database | PostgreSQL 16 + SQLAlchemy 2.0 |
| LLM | OpenAI GPT-4o |
| Auth | JWT (bcrypt + python-jose) |
| Maps | Leaflet.js + OpenStreetMap |
| Cache | Redis |
| Infra | Docker Compose |

## 📁 Project Structure

```
RealEstateAI/
├── frontend/         # Next.js 15 App (React)
│   ├── src/app/      # App Router pages
│   ├── src/components/  # Reusable components
│   └── src/lib/      # API client, utilities
├── backend/          # FastAPI Backend
│   ├── app/api/      # REST endpoints
│   ├── app/core/     # AI Agent, RAG, Query Analyzer
│   ├── app/models/   # SQLAlchemy ORM models
│   ├── app/services/ # Business logic
│   └── app/utils/    # Auth, embeddings
├── docker-compose.yml
└── .env.example
```

## 📝 License

MIT
