# CLAUDE.md — DocChat RAG

## Proyecto
RAG system: pregunta sobre docs. Stack: Python + FastAPI + LangChain + ChromaDB + Claude API | React + Vite + TS.
Portfolio AI Engineering. Arquitectura lista para SaaS.

---

## Reglas de output (token efficiency)

- Respuesta en linea 1. Sin preambulo.
- Sin "Claro!", "Excelente!", "Por supuesto!". Ejecutar directo.
- Sin explicar lo que vas a hacer. Hacerlo.
- Sin sugerencias no pedidas. Scope exacto.
- Sin closings: "Avisa si necesitas algo", "Espero que ayude".
- Respuestas cortas por defecto. Profundidad solo si se pide explicitamente.
- Sin repetir contexto ya establecido en la sesion.
- Si no sabes: "No se." Nunca inventar paths, nombres de funcion, firmas de API.
- No leas el mismo archivo dos veces. Leer antes de editar, nunca editar a ciegas.
- No toques codigo fuera del scope del pedido.
- No refactorices lo que no se pidio.
- No crees archivos nuevos si no es estrictamente necesario.

---

## Esfuerzo por defecto

- Esfuerzo medio. Preguntar antes de encarar algo grande.
- No corras tests automaticamente salvo que se pida.
- No hagas PRs automaticos.
- Preguntar antes de correr cualquier script que tarde mas de lo esperado.

---

## Reglas de codigo

### Backend (Python/FastAPI)
- Type hints obligatorios en firmas.
- Docstring de una linea en funciones publicas.
- Config siempre desde `core/config.py`. Nunca hardcodear.
- Errores HTTP: `HTTPException`. Nunca `raise` generico en routers.
- Logging: `structlog`. Nunca `print()`.
- IO asincrono: todo debe ser `async def`. LangChain sync va en `run_in_executor`.

### Frontend (React/TS)
- Componentes: PascalCase. Hooks: camelCase con prefijo `use`.
- Sin `any` en TypeScript.
- Fetch al backend solo via `src/utils/api.ts`.
- Loading/error siempre manejados visualmente.

### LangChain / RAG
- `chunk_size` y `chunk_overlap` viven en config, nunca hardcodeados.
- Embeddings fallback: si no hay `OPENAI_API_KEY`, usar `sentence-transformers` local.
- Vector store: inicializar una sola vez al arrancar, nunca por request.
- Cada doc procesado: loggear `doc_id` + cantidad de chunks.

---

## Estructura

```
dochat/
├── backend/
│   ├── api/routes/     # endpoints FastAPI
│   ├── core/           # config, logging, vector store init
│   ├── services/       # logica RAG, ingest, query
│   ├── models/         # Pydantic schemas
│   └── utils/          # file parsing, helpers
├── frontend/src/
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   └── utils/          # api.ts y helpers
├── docs/               # ADRs
└── scripts/            # seed, dev helpers
```

---

## Comandos

```bash
cd backend && uvicorn main:app --reload
cd frontend && npm run dev
cd backend && pytest -v
cd frontend && npm run test
chroma run --path ./chroma_data
```

---

## Prohibido

- Modificar `services/rag_service.py` sin leer `docs/architecture-decisions.md`.
- Cambiar modelo de embeddings con indices existentes (breaking change).
- Exponer `ANTHROPIC_API_KEY` en logs o responses de error.
- Skipear validacion de tipo de archivo en ingest.
- Comentarios en codigo que no cambio.
- Over-engineering: la solucion mas simple que funciona.

---

## Override

Instrucciones del usuario siempre ganan sobre este archivo.
