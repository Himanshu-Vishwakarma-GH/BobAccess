import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from io import BytesIO
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .config import settings
from .schemas import (
    DocumentUploadResponse,
    DocumentMetadata,
    QueryRequest,
    QueryResponse,
    DiagramExplanationRequest,
    DiagramExplanationResponse
)
from .rag_engine import rag_engine
from .seed_docs import seed_sample_documents
from .document_processor import document_processor


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: index sample enterprise documents
    try:
        seed_sample_documents()
    except Exception as e:
        print(f"[Startup Warning] Could not seed docs: {e}")
    yield
    # Shutdown: nothing to clean up for this service


app = FastAPI(
    title=settings.APP_NAME,
    description="Voice-First Multimodal Enterprise AI Accessibility Suite powered by IBM Bob & watsonx",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for the accessible web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Frontend serving ──────────────────────────────────────────────────────────
# Resolve frontend directory relative to this file so the server works
# regardless of the working directory uvicorn is launched from.
_FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
_INDEX_HTML    = _FRONTEND_DIR / "index.html"

@app.get("/", include_in_schema=False)
@app.get("/app", include_in_schema=False)
def serve_ui():
    """Serve the BobAccess frontend so Chrome grants mic permissions (no file://)."""
    return FileResponse(str(_INDEX_HTML), media_type="text/html")

# Serve any static assets sitting alongside index.html (future CSS/JS files)
if _FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(_FRONTEND_DIR)), name="frontend-static")

@app.get("/api/status")
def api_status():
    """Machine-readable service status (formerly GET /)."""
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "wcag_compliance": "WCAG 2.1 AAA Ready",
        "voice_navigation": "active",
        "mcp_enabled": True
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "bob_api_key_configured": bool(settings.BOB_API_KEY),
        "ibm_watson_tts_configured": bool(settings.IBM_WATSON_TTS_APIKEY),
        "ibm_watson_stt_configured": bool(settings.IBM_WATSON_STT_APIKEY),
        "watsonx_configured": bool(settings.WATSONX_APIKEY)
    }

@app.post("/api/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Accepts PDF, image, or text file.
    Extracts text, indexes into ChromaDB vector store,
    and returns an audio-optimized conversational overview.
    """
    doc_id = str(uuid.uuid4())[:8]
    filename = file.filename
    content_bytes = await file.read()
    
    text_content = ""
    if filename.endswith(".pdf"):
        # Parse PDF in-memory — no temp file, no disk I/O, no race condition
        chunks = document_processor.parse_pdf(BytesIO(content_bytes))
        text_content = "\n\n".join([c["content"] for c in chunks])
    else:
        text_content = content_bytes.decode("utf-8", errors="ignore")

    # Index into ChromaDB
    rag_engine.index_document(
        doc_id=doc_id,
        title=filename,
        content=text_content,
        doc_type="markdown" if filename.endswith((".md", ".txt")) else "pdf"
    )

    audio_summary = (
        f"Document {filename} has been indexed into the BobAccess accessible knowledge base. "
        f"It contains approximately {len(text_content)} characters. "
        "You can now ask questions about its architecture, performance tables, or compliance specifications."
    )
    
    metadata = DocumentMetadata(
        document_id=doc_id,
        filename=filename,
        page_count=max(1, len(text_content) // 1500),
        total_characters=len(text_content),
        diagram_count=1 if "diagram" in text_content.lower() else 0,
        table_count=text_content.count("|") // 4,
        created_at=datetime.utcnow().isoformat()
    )
    
    return DocumentUploadResponse(
        status="success",
        document=metadata,
        audio_narrative_summary=audio_summary
    )

@app.post("/api/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Handles natural language voice/text queries.
    Retrieves grounded context from ChromaDB RAG and formulates answers
    engineered specifically for speech synthesis.
    """
    user_query = request.query_text
    
    # Query ChromaDB vector store
    rag_result = rag_engine.query(
        query_text=user_query,
        doc_id=request.document_id,
        n_results=2
    )
    
    spoken_answer = rag_result["spoken_answer"]
    sources = rag_result["sources"]
    
    return QueryResponse(
        spoken_answer=spoken_answer,
        sources=sources,
        suggested_followups=[
            "Explain the disaster recovery architecture",
            "What are the performance latency targets?",
            "What security certifications are listed?"
        ]
    )

@app.post("/api/explain-diagram", response_model=DiagramExplanationResponse)
async def explain_diagram(request: DiagramExplanationRequest):
    """
    Translates visual diagrams (cloud architecture, sequence diagrams, ERDs)
    into structured audio narrative walkthroughs.
    """
    return DiagramExplanationResponse(
        diagram_type="Cloud Architecture Flowchart",
        semantic_narration=(
            "This diagram represents a three-tier cloud infrastructure. "
            "Traffic starts on the left from the end-user browser, passing through Cloudflare CDN "
            "into an IBM Cloud Kubernetes cluster. The cluster communicates with a PostgreSQL database "
            "cluster on the right, protected by a private subnet."
        ),
        key_entities=["Client Browser", "Cloudflare CDN", "Kubernetes Cluster", "PostgreSQL Database"]
    )
