import re
from io import BytesIO
from typing import List, Dict, Any, Union
from pypdf import PdfReader

class DocumentProcessor:
    """
    Parses PDFs, Markdown, and text files into semantically meaningful chunks
    tailored for accessibility and audio narration.
    """

    @staticmethod
    def parse_pdf(source: Union[str, BytesIO]) -> List[Dict[str, Any]]:
        reader = PdfReader(source)
        chunks = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = DocumentProcessor._clean_text(text)
            if text:
                chunks.append({
                    "page": idx + 1,
                    "content": text,
                    "type": "text"
                })
        return chunks

    @staticmethod
    def parse_markdown(content: str) -> List[Dict[str, Any]]:
        """
        Splits markdown by headings to maintain logical structural units.
        """
        sections = re.split(r'\n(?=##?\s)', content)
        chunks = []
        for idx, sec in enumerate(sections):
            clean_sec = DocumentProcessor._clean_text(sec)
            if clean_sec:
                # Detect if the section contains tables
                has_table = "|" in clean_sec and "-|-" in clean_sec
                chunks.append({
                    "section_index": idx + 1,
                    "content": clean_sec,
                    "type": "table" if has_table else "text"
                })
        return chunks

    @staticmethod
    def _clean_text(text: str) -> str:
        # Normalize whitespace while preserving line structure
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

document_processor = DocumentProcessor()
