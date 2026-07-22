# SelfGPT

> **Every conversation. A new perspective.**

An AI Identity Platform where you talk to different AI identities — famous personalities, legendary books, fictional characters, historical figures, cartoon characters, and your own custom persona — each powered by open-source multimodal LLMs.

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- MongoDB (local)
- Redis (local)
- Ollama (for local LLM inference)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Optional: ChromaDB (for RAG)
```bash
docker-compose up -d chromadb
```

## Architecture

```
Frontend (Next.js 15) → FastAPI Backend → MongoDB + Redis
                                       → Ollama (LLM)
                                       → ChromaDB (RAG vectors)
```

## License

MIT © Shivansh Rana
