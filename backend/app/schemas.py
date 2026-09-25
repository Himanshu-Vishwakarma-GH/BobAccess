from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DocumentMetadata(BaseModel):
    document_id: str
    filename: str
    page_count: int = 1
    total_characters: int = 0
    diagram_count: int = 0
    table_count: int = 0
    created_at: str

class DocumentUploadResponse(BaseModel):
    status: str
    document: DocumentMetadata
    audio_narrative_summary: str
    audio_url: Optional[str] = None

class QueryRequest(BaseModel):
    query_text: str = Field(..., description="Voice-transcribed or text query from user")
    document_id: Optional[str] = Field(None, description="Optional target document id to scope query")
    mode: str = Field("audio_summary", description="Mode: 'audio_summary' | 'detailed' | 'diagram_explanation'")

class QueryResponse(BaseModel):
    spoken_answer: str = Field(..., description="Natural spoken language answer crafted for audio narration")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Grounding passages and page numbers")
    audio_base64: Optional[str] = Field(None, description="Pre-synthesized speech audio in base64")
    suggested_followups: List[str] = Field(default_factory=list, description="Verbal suggestions for next questions")

class DiagramExplanationRequest(BaseModel):
    image_url_or_base64: str
    context: Optional[str] = None

class DiagramExplanationResponse(BaseModel):
    diagram_type: str = Field(..., description="e.g. Cloud Architecture, Sequence Flow, Database Schema")
    semantic_narration: str = Field(..., description="Conversational verbal walkthrough of the diagram")
    key_entities: List[str] = Field(default_factory=list)
