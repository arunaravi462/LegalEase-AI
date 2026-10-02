import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = f"""
You are an expert legal AI assistant. Generate a formal, comprehensive, and legally sound {document_type}.

Details:
- Document Type: {document_type}
- Parties Involved: {parties}
- Terms & Conditions: {terms}
- Effective Date: {dates}

Instructions:
1. Include standard legal sections, headings, definitions, and execution blocks.
2. Structure terms clearly.
3. Keep the formatting clean and professional.
"""
        response = self.model.generate_content(prompt)
        return response.text
