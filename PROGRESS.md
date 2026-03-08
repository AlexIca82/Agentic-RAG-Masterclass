# Progress

Track your progress through the masterclass. Update this file as you complete modules - Claude Code reads this to understand where you are in the project.

## Convention
- `[ ]` = Not started
- `[-]` = In progress
- `[x]` = Completed

## Modules

### Module 1: App Shell + Observability
- [x] Backend setup (FastAPI + venv structure)
- [x] Frontend setup (Vite + React + TypeScript + Tailwind v4 + shadcn/ui)
- [x] Supabase client configuration
- [x] Auth context and login/signup pages
- [x] Chat UI with streaming SSE
- [x] Ollama integration via OpenAI-compatible API (remote ollama.com)
- [x] RAGAS observability setup
- [x] CORS configuration for multiple ports
- [x] Dev mode bypass for testing

### Module 2: BYO Retrieval + Memory
- [x] Database schema with pgvector (threads, messages, documents, chunks)
- [x] Supabase project setup and configuration
- [x] Document upload and storage via Supabase Storage
- [x] Text chunking service (512 chars, 50 overlap)
- [x] Embeddings via local Ollama (nomic-embed-text:v1.5)
- [x] Vector similarity search with pgvector
- [x] Documents page UI with drag-and-drop upload
- [x] RAG integration in chat endpoint
- [x] Frontend auth token passing to backend
- [x] Storage policies for service role access
- [x] End-to-end RAG pipeline tested and verified
- [x] Similarity threshold tuning (0.3)

### Module 3: Record Manager
- [x] Content hashing (SHA-256) for documents
- [x] Deduplication - check existing documents before processing
- [x] Incremental updates - reprocess modified documents
- [x] Database migration for content_hash column
- [x] Unique index on user_id + content_hash

### Module 4: Metadata Extraction
- [ ] Not started

### Module 5: Multi-Format Support
- [ ] Not started

### Module 6: Hybrid Search & Reranking
- [ ] Not started

### Module 7: Additional Tools
- [ ] Not started

### Module 8: Sub-Agents
- [ ] Not started

## Current Status
- **Backend**: Running on http://localhost:8000
- **Frontend**: Running on http://localhost:5174
- **Database**: Supabase (jyftyhppffrfgpvgghzm.supabase.co)
- **LLM**: Remote Ollama (ollama.com) - ministral-3:8b
- **Embeddings**: Local Ollama - nomic-embed-text:v1.5
- **Auth**: Supabase Auth with RLS policies

## Next Steps
Continue with Module 4: Metadata Extraction to add:
- LLM-based metadata extraction from documents
- Structured metadata schema
- Metadata-filtered retrieval
- Enhanced search capabilities
