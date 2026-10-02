from datetime import date
import requests
import streamlit as st
from document_service import export_filename, format_docx, format_pdf, format_txt
from config import get_settings
from text_utils import html_preview

settings = get_settings()
st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown("""<style>.legal-preview{background:#171717;color:#f5f5f5;padding:1.25rem;border-radius:8px;}</style>""", unsafe_allow_html=True)
st.title("⚖️ LegalEase")
st.caption("AI-Powered Legal Document Generator")
st.markdown('<div class="notice"><b>Important:</b> LegalEase creates AI-assisted drafts. Please review with a legal professional.</div>', unsafe_allow_html=True)

with st.sidebar:
    backend_url = st.text_input("Backend URL", settings.backend_url if hasattr(settings, 'backend_url') else "http://127.0.0.1:8000").rstrip("/")

if "document" not in st.session_state:
    st.session_state.document = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = "Legal Document"

a, b = st.columns([1, 1.2])

with a:
    st.subheader("Document details")
    document_type = st.text_input("Document type", placeholder="Freelance Work Contract")
    parties = st.text_area("Parties involved", placeholder="Jane Doe (Service Provider), John Smith (Client)")
    terms = st.text_area("Terms & conditions", placeholder="Payment within 30 days; Confidentiality...")
    effective_date = st.date_input("Effective date", date.today())
    
    if st.button("Generate Document", type="primary", use_container_width=True):
        if not all([document_type.strip(), parties.strip(), terms.strip()]):
            st.error("Please fill all fields")
        else:
            try:
                with st.spinner("Generating your draft..."):
                    r = requests.post(f"{backend_url}/generate", json={"document_type": document_type, "parties": parties, "terms": terms, "effective_date": str(effective_date)})
                    data = r.json()
                    st.session_state.document = data.get("content", "") or data.get("document", "")
                    st.session_state.generated_type = document_type
            except Exception as e:
                st.error(f"Could not reach FastAPI at {backend_url}: {e}")
                # Fallback local draft
                st.session_state.document = f"{document_type}\n\nParties: {parties}\n\nTerms: {terms}\n\nEffective Date: {effective_date}"
                st.session_state.generated_type = document_type

with b:
    st.subheader("Document preview")
    if st.session_state.document:
        st.markdown(html_preview(st.session_state.document), unsafe_allow_html=True)
        edited = st.text_area("Editable content", st.session_state.document, height=420)
        if st.button("Save edits", use_container_width=True):
            st.session_state.document = edited
        
        st.subheader("Download")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("Download TXT", format_txt(st.session_state.document), file_name=export_filename(st.session_state.generated_type, "txt"))
        with c2:
            st.download_button("Download DOCX", format_docx(st.session_state.document, st.session_state.generated_type), file_name=export_filename(st.session_state.generated_type, "docx"))
        with c3:
            st.download_button("Download PDF", format_pdf(st.session_state.document), file_name=export_filename(st.session_state.generated_type, "pdf"))
    else:
        st.info("Your generated document will appear here.")
