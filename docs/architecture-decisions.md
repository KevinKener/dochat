# Decisiones de arquitectura — DocChat

Registro de decisiones técnicas importantes con su razonamiento.
Formato: contexto → decisión → consecuencias.

---

## ADR-001 — ChromaDB para MVP, pgvector para producción

**Fecha:** Junio 2025  
**Estado:** Activo

### Contexto
Necesitamos un vector store para guardar embeddings y hacer búsqueda semántica. Las opciones principales son: Pinecone (managed), Weaviate (self-hosted), ChromaDB (embeddable), y pgvector (extensión de PostgreSQL).

### Decisión
- **MVP:** ChromaDB corriendo local con persistencia en disco
- **Producción / Fase 2:** pgvector dentro del mismo PostgreSQL que ya usamos para el resto de los datos

### Razonamiento
ChromaDB para MVP porque no requiere cuenta en ningún servicio externo, arranca en dos líneas de Python, y permite iterar rápido. La migración a pgvector para producción simplifica la infraestructura (una sola DB en lugar de dos servicios) y hace más simple el multi-tenancy (RLS nativa de PostgreSQL).

Pinecone fue descartado porque introduce una dependencia externa de pago y complica el desarrollo local.

### Consecuencias
- La interfaz de `VectorStore` en `services/rag_service.py` está abstraída detrás de un wrapper — cambiar de Chroma a pgvector requiere solo cambiar el provider, no la lógica de negocio.
- Los embeddings generados son compatibles entre ambos stores (mismo modelo → mismo vector space).

---

## ADR-002 — Claude API como LLM principal

**Fecha:** Junio 2025  
**Estado:** Activo

### Contexto
Opciones principales: Claude (Anthropic), GPT-4o (OpenAI), Gemini (Google), modelos locales (Ollama).

### Decisión
Claude API con modelo `claude-3-haiku-20240307` para el MVP. Claude Sonnet para queries que requieran más razonamiento.

### Razonamiento
- Context window grande (200k tokens) — relevante para RAG con documentos largos
- Buena relación calidad/precio en Haiku
- Demostrar manejo de la Anthropic API suma al portfolio de AI Engineering
- El sistema está abstraído para poder swappear el LLM si se necesita

### Consecuencias
- Se necesita `ANTHROPIC_API_KEY` para correr el sistema
- Se implementa fallback básico a GPT-4o-mini si hay error en la API de Anthropic

---

## ADR-003 — Embeddings con OpenAI text-embedding-3-small

**Fecha:** Junio 2025  
**Estado:** Activo

### Contexto
Los embeddings son el corazón del RAG — afectan directamente la calidad del retrieval.

### Decisión
`text-embedding-3-small` de OpenAI como default. `sentence-transformers/all-MiniLM-L6-v2` como fallback local cuando no hay `OPENAI_API_KEY`.

### Razonamiento
`text-embedding-3-small` ofrece excelente calidad a bajo costo ($0.02/1M tokens). El modelo local de sentence-transformers permite desarrollar y testear sin costo y sin conexión, pero con menor calidad de retrieval.

**Importante:** si se cambia el modelo de embeddings en producción, todos los documentos indexados deben re-procesarse. Los vectores generados por modelos distintos no son comparables.

### Consecuencias
- Config `EMBEDDING_MODEL` en `.env` controla qué modelo se usa
- El `VectorStore` guarda junto a cada chunk el modelo con que fue embeddado
- Breaking change si se cambia el modelo con índices existentes

---

## ADR-004 — FastAPI sobre Flask/Django

**Fecha:** Junio 2025  
**Estado:** Activo

### Contexto
El backend necesita manejar requests asincrónicos (llamadas a LLMs que pueden tardar varios segundos) y eventualmente streaming (SSE).

### Decisión
FastAPI con Uvicorn.

### Razonamiento
- Async nativo — fundamental para no bloquear el server mientras espera la respuesta del LLM
- Swagger/OpenAPI auto-generado — documentación gratis
- Pydantic para validación — type safety en los schemas
- Más fácil de escalar horizontalmente que Django para este caso de uso

### Consecuencias
- Toda la lógica de IO (LLM calls, DB queries) debe ser `async def`
- Los servicios sincrónicos (como algunos de LangChain) se ejecutan en `run_in_executor`

---

## ADR-006 — Whisper + yt-dlp para soporte de audio, video y YouTube

**Fecha:** Junio 2025  
**Estado:** Planeado (Fase 2)

### Contexto
La mayoría de proyectos RAG solo soportan texto (PDF, DOCX). El mundo real tiene mucha información en audio y video: grabaciones de reuniones, podcasts, videos de capacitación, charlas de YouTube.

### Decisión
- **Transcripción:** OpenAI Whisper corriendo local (`whisper` Python package, modelo `base` o `small`)
- **Extracción de audio:** `ffmpeg` para video, `yt-dlp` para YouTube
- **OCR:** `easyocr` para imágenes escaneadas

### Razonamiento
Whisper corre completamente offline — no necesita API key, no tiene costo por uso, y la calidad es excelente. Esto es importante para la narrativa del portfolio: "transcripción local y privada". `yt-dlp` es el estándar de facto para bajar audio de YouTube y es trivial de integrar.

El pipeline es simple: cualquier fuente de medios → audio WAV → Whisper → texto → mismo pipeline de chunking + embeddings que el resto de documentos. La abstracción es tan limpia que agregar un nuevo tipo de fuente es cuestión de agregar un loader.

### Consecuencias
- Whisper `small` pesa ~460MB — se descarga la primera vez que se usa, no va en la imagen Docker
- En máquinas sin GPU la transcripción es más lenta (1-2 minutos para un audio de 10 min con `base`)
- Se agrega `ffmpeg` como dependencia del sistema (va en el Dockerfile)
- El response de `/ingest` incluye metadata de transcripción: modelo usado, duración del audio, idioma detectado

## ADR-005 — Source highlighting como feature core

**Fecha:** Junio 2025  
**Estado:** Activo

### Contexto
La mayoría de implementaciones de RAG devuelven solo la respuesta generada. El usuario no puede verificar de dónde viene la información.

### Decisión
Cada respuesta incluye los chunks del documento que se usaron como contexto, con metadata (número de página si aplica, posición en el documento).

### Razonamiento
- Aumenta la confianza del usuario en la respuesta
- Hace que el sistema sea verificable (el usuario puede ir al documento original)
- Diferenciador visual fuerte para demos y entrevistas
- No agrega costo (los chunks ya están disponibles en el proceso de retrieval)

### Consecuencias
- El response schema de `/query` incluye `answer` + `sources: [{content, document_id, metadata}]`
- El frontend renderiza los chunks usados debajo de cada respuesta
- Los chunks deben preservar metadata de posición durante el ingest
