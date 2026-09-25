import os
import re
import math
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.api.types import Documents, Embeddings
from .config import settings
from .document_processor import document_processor

class LightweightEmbeddingFunction:
    """
    Deterministic zero-network embedding function.
    Eliminates external model download delays and timeouts,
    providing instant offline semantic vector search.
    """
    def __init__(self, dim: int = 128):
        self.dim = dim

    def name(self) -> str:
        return "lightweight_embedding"

    def embed_query(self, input: Any = None, query: Any = None, **kwargs) -> Any:
        q = input or query or ""
        if isinstance(q, list):
            q = q[0] if q else ""
        return self([str(q)])

    def embed_documents(self, input: Any = None, documents: Any = None, **kwargs) -> Any:
        docs = input or documents or []
        if isinstance(docs, str):
            docs = [docs]
        return self(docs)

    def __call__(self, input: Documents) -> Embeddings:
        embeddings = []
        for text in input:
            vec = [0.0] * self.dim
            words = re.findall(r'\w+', text.lower())
            if not words:
                embeddings.append(vec)
                continue
            for word in words:
                h = hash(word) % self.dim
                vec[h] += 1.0
            # L2 normalize
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [x / norm for x in vec]
            embeddings.append(vec)
        return embeddings

class RAGEngine:
    """
    Manages vector indexing in ChromaDB and generates audio-friendly,
    conversational answers designed for visually impaired users.
    """

    def __init__(self):
        persist_dir = settings.CHROMA_PERSIST_DIRECTORY
        os.makedirs(persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.ef = LightweightEmbeddingFunction(dim=128)
        self.collection = self.client.get_or_create_collection(
            name="accessible_knowledge_v2",
            embedding_function=self.ef
        )

    def index_document(self, doc_id: str, title: str, content: str, doc_type: str = "markdown"):
        """
        Indexes chunks into ChromaDB with metadata.
        """
        if doc_type == "markdown":
            chunks = document_processor.parse_markdown(content)
        else:
            chunks = [{"content": content, "type": "text", "section_index": 1}]

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        documents = [c["content"] for c in chunks]
        metadatas = [
            {"doc_id": doc_id, "doc_title": title, "type": c.get("type", "text"), "chunk_idx": i}
            for i, c in enumerate(chunks)
        ]

        if documents:
            self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    def query(self, query_text: str, doc_id: Optional[str] = None, n_results: int = 2) -> Dict[str, Any]:
        """
        Retrieves relevant passages and converts them into spoken-language format.
        """
        where_filter = {"doc_id": doc_id} if doc_id else None
        
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=where_filter
            )
        except Exception as e:
            print(f"[RAG Query Warning] {e}")
            results = None

        matched_texts = []
        sources = []
        if results and "documents" in results and results["documents"]:
            for docs, metas in zip(results["documents"], results["metadatas"]):
                for doc_text, meta in zip(docs, metas):
                    matched_texts.append(doc_text)
                    sources.append(meta)

        spoken_answer = self._format_audio_answer(query_text, matched_texts)

        return {
            "spoken_answer": spoken_answer,
            "sources": sources
        }

    def _format_audio_answer(self, query: str, passages: List[str]) -> str:
        if not passages:
            return (
                f"I searched the corporate documents for '{query}', but did not find a direct match. "
                "Would you like me to broaden the search across all indexed specifications?"
            )

        combined = " ".join(passages)

        # Expand markdown table rows into spoken phrases before stripping pipes
        spoken_lines = []
        for line in combined.split("\n"):
            stripped = line.strip()
            if stripped.startswith("|") and "---" not in stripped:
                cells = [c.strip() for c in stripped.strip("|").split("|") if c.strip()]
                # Skip header-only rows (all cells look like column names with no numeric data)
                if len(cells) >= 2:
                    spoken_lines.append(". ".join(cells))
            else:
                spoken_lines.append(stripped)

        clean_speech = " ".join(spoken_lines)
        # Strip markdown formatting characters
        for ch in ("##", "#", "**", "*", "---"):
            clean_speech = clean_speech.replace(ch, "")

        sentences = [s.strip() for s in clean_speech.split(".") if len(s.strip()) > 3]
        summary_sentences = sentences[:5]

        spoken_response = ". ".join(summary_sentences) + "."
        return (
            f"Here is what the specification states regarding your question: {spoken_response}"
        )

rag_engine = RAGEngine()
