# Roadmap — DocChat

Sistema RAG (Retrieval-Augmented Generation) para hacer preguntas sobre tus documentos.
Proyecto de portfolio con arquitectura preparada para SaaS.

---

## Estado actual
**Fase:** Setup inicial  
**Última actualización:** Junio 2025

---

## Fase 1 — MVP funcional
> Objetivo: sistema que funciona end-to-end, deployable, demostrable en entrevistas.

### Backend
- [ ] Setup FastAPI + estructura de carpetas
- [ ] Config centralizada con `pydantic-settings`
- [ ] `POST /ingest` — recibe PDF, lo procesa y guarda en Chroma
- [ ] `POST /query` — recibe pregunta, hace retrieval + genera respuesta con Claude
- [ ] `GET /documents` — lista documentos indexados
- [ ] `DELETE /documents/{id}` — elimina un documento del índice
- [ ] Chunking con `RecursiveCharacterTextSplitter` (configurable)
- [ ] Embeddings con `text-embedding-3-small` de OpenAI
- [ ] Vector store con ChromaDB (local, persistente)
- [ ] Source highlighting — devolver los chunks usados en la respuesta
- [ ] Manejo de errores y logging estructurado
- [ ] Tests de integración para `/ingest` y `/query`

### Frontend
- [ ] Setup React + Vite + TypeScript
- [ ] Upload de PDFs con drag & drop
- [ ] Chat interface — pregunta y respuesta
- [ ] Source highlighting visual — resaltar el fragmento del doc usado
- [ ] Estados de loading y error
- [ ] Lista de documentos indexados

### Infraestructura
- [ ] `Dockerfile` para el backend
- [ ] `docker-compose.yml` para dev (backend + chroma)
- [ ] Deploy backend en Railway o Render
- [ ] Deploy frontend en Vercel
- [ ] Variables de entorno documentadas en `.env.example`
- [ ] CI con GitHub Actions (lint + tests)

---

## Fase 2 — Diferenciadores técnicos
> Objetivo: features que aparecen en el 20% de los proyectos. Para destacar en el portfolio.

### Multi-formato y medios
> "RAG sobre cualquier fuente de información" — no solo PDFs.

- [ ] **DOCX, PPTX, Excel** — loaders nativos de LangChain (`Docx2txtLoader`, `UnstructuredPowerPointLoader`, `UnstructuredExcelLoader`)
- [ ] **OCR en imágenes** — subís una foto de un documento escaneado y funciona igual (`easyocr` o `pytesseract`)
- [ ] **Audio → texto** — transcripción local offline con OpenAI Whisper (`whisper` python package, corre sin API key)
- [ ] **Video → texto** — mismo pipeline que audio, extrae el audio primero con `ffmpeg`
- [ ] **YouTube URL** — pegás un link, `yt-dlp` baja el audio, Whisper transcribe, se indexa como cualquier doc

### RAG avanzado
- [ ] **Streaming con SSE** — respuesta token a token en el frontend
- [ ] **Reranking** — usar `cross-encoder` para reordenar chunks antes de generar
- [ ] **Hybrid search** — combinar búsqueda semántica + BM25 (keyword)
- [ ] **Evaluación automática** — score de calidad por respuesta (llamada secundaria a Claude)
- [ ] **Historial de conversación** — contexto multi-turno dentro de una sesión

### Observabilidad
- [ ] Dashboard de métricas — latencia, tokens usados, queries por doc
- [ ] Logging de cada query con su score de evaluación
- [ ] Endpoint `GET /analytics` para métricas agregadas

### Dev experience
- [ ] Migrar vector store a `pgvector` (consolidar en una sola DB)
- [ ] Agregar `pytest-asyncio` y aumentar cobertura de tests
- [ ] Documentación de API con Swagger enriquecido

---

## Fase 3 — Visión SaaS
> Objetivo: arquitectura multi-tenant. Para mostrar pensamiento de producto en entrevistas senior.

- [ ] Auth con JWT — registro, login, refresh tokens
- [ ] Multi-tenancy — cada usuario tiene su espacio de documentos aislado
- [ ] Row-level security en la DB
- [ ] Planes de uso — límite de documentos y queries por plan
- [ ] Integración con Stripe para pagos
- [ ] Panel de admin — gestión de usuarios y uso
- [ ] Rate limiting por usuario
- [ ] Onboarding flow en el frontend

---

## Decisiones técnicas clave

| Decisión | Elegida | Alternativa | Razón |
|---|---|---|---|
| Vector store (MVP) | ChromaDB local | Pinecone | Sin costo, sin cuenta externa |
| Vector store (Fase 2+) | pgvector | Pinecone / Weaviate | Consolida en una DB, más simple en prod |
| Embeddings | OpenAI text-embedding-3-small | Sentence-transformers local | Calidad/precio óptimo para MVP |
| LLM | Claude API (claude-3-haiku) | GPT-4o-mini | Portfolio + mejor context window |
| Framework API | FastAPI | Flask / Django | Async nativo, tipado, Swagger auto |
| Deploy backend | Railway | Fly.io / AWS | Free tier generoso, fácil de usar |

---

## Métricas de éxito

- **MVP:** responde preguntas sobre un PDF con source highlighting en < 5 segundos
- **Fase 2:** soporta PDF, DOCX, PPTX, Excel, imágenes, audio, video y YouTube — latencia < 2s con streaming — score de eval > 7/10 promedio
- **SaaS:** capaz de manejar 10 usuarios concurrentes sin degradación

---

## Recursos y referencias

- [LangChain Docs](https://python.langchain.com/docs)
- [ChromaDB Docs](https://docs.trychroma.com)
- [Anthropic API](https://docs.anthropic.com)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [RAG from scratch — LangChain YouTube](https://youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)
- [OpenAI Whisper](https://github.com/openai/whisper) — transcripción local de audio/video
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — descarga audio de YouTube
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — OCR en imágenes
