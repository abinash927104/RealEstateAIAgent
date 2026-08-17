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

## 🧠 AI Features & Capabilities

| Feature | Description |
|---------|-------------|
| **Stateful Conversations** | The agent persists financial context (prices, rent, loan terms) across turns, allowing dynamic "what if" recalculations. |
| **Strict Tool Grounding** | Prevents LLM hallucinations; the agent strictly relies on deterministic tools and live databases rather than inventing properties. |
| **Advanced Property Search** | Combines SQL filtering for exact matches (beds, baths, price) with ChromaDB semantic search for soft constraints ("quiet neighborhood"). |
| **Mortgage Calculator** | Accurately calculates EMI (Principal + Interest) while explicitly separating taxes, insurance, and HOA fees into a Total Monthly Cost. |
| **ROI Analysis** | Calculates precise Cap Rate (NOI / Price), Cash-on-Cash Return accounting for actual capital invested, and 5-year equity projections. |
| **Market Analysis** | Provides aggregate stats, property type distribution, and price ranges with full data-source transparency (live scrape vs. local DB). |
| **Query Routing** | Automatically classifies queries into RAG (simple FAQs) or Agent (complex calculations). |

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
