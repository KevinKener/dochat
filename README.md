# DocChat — RAG sobre tus documentos

Subís un PDF. Le hacés preguntas. Te responde citando exactamente de dónde sacó la información.

Sistema RAG (Retrieval-Augmented Generation) construido con FastAPI, LangChain y Claude API. Arquitectura preparada para escalar a SaaS multi-tenant.

---

## Demo

> Screenshot / GIF acá cuando esté deployado

---

## ¿Qué hace?

- **Indexás cualquier fuente** — PDF, Word, Excel, PowerPoint, imágenes escaneadas (OCR), archivos de audio, videos, o directamente una URL de YouTube.
- **Hacés preguntas en lenguaje natural** — el sistema busca los fragmentos más relevantes y los usa como contexto para que Claude genere una respuesta precisa.
- **Ves exactamente de dónde viene cada respuesta** — source highlighting que resalta el fragmento del documento usado.
- **Transcripción local y offline** — el audio y video se procesan con Whisper corriendo en tu máquina, sin APIs externas.

### Formatos soportados

| Tipo | Formatos |
|---|---|
| Documentos | PDF, DOCX, PPTX, XLSX, TXT |
| Imágenes | JPG, PNG, TIFF — con OCR automático |
| Audio | MP3, WAV, M4A — transcripción con Whisper |
| Video | MP4, MKV, AVI — extrae y transcribe el audio |
| Web | YouTube URL — descarga y transcribe automáticamente |

---

## Stack técnico

| Capa | Tecnología |
|---|---|
| API | Python + FastAPI |
| RAG pipeline | LangChain |
| Vector store | ChromaDB (dev) → pgvector (prod) |
| LLM | Claude API (Anthropic) |
| Embeddings | OpenAI text-embedding-3-small |
| Transcripción | OpenAI Whisper (local, offline) |
| OCR | EasyOCR |
| YouTube | yt-dlp |
| Frontend | React + Vite + TypeScript |
| Deploy | Railway (backend) + Vercel (frontend) |
| CI/CD | GitHub Actions |

---

## Arquitectura

```
Usuario
  │
  ▼
React (Vite)
  │  POST /query
  ▼
FastAPI
  │
  ├── /ingest ──► LangChain Loader
  │                    │
  │              TextSplitter (chunks)
  │                    │
  │              Embeddings (OpenAI)
  │                    │
  │              ChromaDB ◄─────────────────┐
  │                                         │
  └── /query ──► Retrieval (top-k chunks) ──┘
                      │
                 Claude API (genera respuesta)
                      │
                 Response + source chunks
```

---

## Setup local

### Requisitos
- Python 3.11+
- Node.js 18+
- Cuenta Anthropic (para la Claude API)
- Cuenta OpenAI (para embeddings — opcional, hay fallback local)

### 1. Clonar y configurar

```bash
git clone https://github.com/KevinKener/dochat.git
cd dochat
cp .env.example .env
# Completar variables en .env
```

### 2. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

API disponible en `http://localhost:8000` — docs en `/docs`.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App disponible en `http://localhost:5173`.

### 4. Con Docker (recomendado)

```bash
docker-compose up
```

---

## Variables de entorno

```env
# .env.example

# LLM
ANTHROPIC_API_KEY=sk-ant-...

# Embeddings
OPENAI_API_KEY=sk-...           # opcional, hay fallback local

# Vector store
CHROMA_PERSIST_PATH=./chroma_data

# RAG config
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_TOP_K=4

# App
ENVIRONMENT=development
LOG_LEVEL=INFO
```

---

## Endpoints principales

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/ingest` | Procesa y guarda un documento |
| `POST` | `/query` | Pregunta sobre los documentos |
| `GET` | `/documents` | Lista documentos indexados |
| `DELETE` | `/documents/{id}` | Elimina un documento |
| `GET` | `/health` | Health check |

Documentación interactiva: `http://localhost:8000/docs`

---

## Decisiones de diseño

Ver [docs/architecture-decisions.md](docs/architecture-decisions.md) para el razonamiento detrás de cada decisión técnica.

Ver [ROADMAP.md](ROADMAP.md) para el plan de fases MVP → Fase 2 → SaaS.

---

## Tests

```bash
cd backend
pytest -v

cd frontend
npm run test
```

---

## Roadmap

- [x] Setup inicial y estructura del proyecto
- [ ] MVP funcional (ingest + query + source highlighting)
- [ ] Streaming de respuestas con SSE
- [ ] Evaluación automática de calidad
- [ ] Multi-formato (DOCX, URL scraping)
- [ ] Arquitectura SaaS multi-tenant

Ver [ROADMAP.md](ROADMAP.md) para el detalle completo.

---

## Autor

**Kevin Kener** — Técnico Universitario en Programación (UTN Rosario)  
Orientado a AI Engineering.

[GitHub](https://github.com/KevinKener) · [LinkedIn](https://linkedin.com/in/kevinkener)

---

## Licencia

MIT
