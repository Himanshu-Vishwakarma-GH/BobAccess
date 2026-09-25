import os
from .rag_engine import rag_engine

def seed_sample_documents():
    sample_file = os.path.join(
        os.path.dirname(__file__), "..", "..", "sample-docs", "enterprise-architecture-spec.md"
    )
    sample_file = os.path.abspath(sample_file)

    if os.path.exists(sample_file):
        with open(sample_file, "r", encoding="utf-8") as f:
            content = f.read()

        rag_engine.index_document(
            doc_id="arch-spec-42",
            title="Global Logistics Platform: Enterprise System Architecture (v4.2)",
            content=content,
            doc_type="markdown"
        )
        print(f"[Seed] Successfully indexed: {sample_file} into ChromaDB")
    else:
        print(f"[Seed] Sample file not found at: {sample_file}")

if __name__ == "__main__":
    seed_sample_documents()
