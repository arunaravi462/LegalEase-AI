from fastapi import APIRouter, HTTPException
from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest, DocumentResponse
from utils.config import get_settings
router=APIRouter(); settings=get_settings(); generator=GeminiDocumentGenerator(settings)
@router.post("/generate",response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        content=generator.generate_document(request)
        if len(content)>settings.max_document_chars: raise HTTPException(422,f"Generated document exceeds {settings.max_document_chars} characters.")
        return DocumentResponse(document_type=request.document_type,content=content,model="demo" if settings.demo_mode else settings.gemini_model,demo_mode=settings.demo_mode)
    except HTTPException: raise
    except Exception as exc: raise HTTPException(502,str(exc)) from exc
