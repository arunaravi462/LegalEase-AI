import os
import re
from datetime import date
import requests
import streamlit as st
from config import get_settings
from document_service import filename, format_docx, format_pdf, format_txt
from text_utils import html_preview

st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    .legal-preview{background:#f7f7f7;color:#1f2937;padding:1.25rem;border-radius:8px;border:1px solid #e5e7eb;font-family:Georgia,serif;line-height:1.7;white-space:pre-wrap;}
    .notice{background:#eef2ff;border-left:4px solid #6366f1;padding:0.75rem 1rem;border-radius:6px;margin-bottom:1rem;color:#1e293b;}
</style>
""", unsafe_allow_html=True)

st.title("⚖️ LegalEase AI")
st.caption("AI-Powered Legal Document Generator")
st.markdown('<div class="notice"><b>Important:</b> This is AI draft only. Not legal advice. Consult a lawyer.</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    settings = get_settings()
    raw_url = getattr(settings, 'backend_url', getattr(settings, 'backend_uri', ''))
    default_url = str(raw_url) if raw_url else "https://legalease-as-kfrr.onrender.com"
    if "127.0.0.1" in default_url or "localhost" in default_url:
        default_url = "https://legalease-as-kfrr.onrender.com"
    backend_url = st.text_input("Backend URL", value=default_url)
    st.info("Backend must be running on Render")

if "document" not in st.session_state:
    st.session_state.document = ""
if "generated_type" not in st.session_state:
    st.session_state.generated_type = "Legal Document"
if "history" not in st.session_state:
    st.session_state.history = []

# Main Layout
col_left, col_right = st.columns((1, 1.2))

with col_left:
    st.subheader("📝 Document Details")
    document_type = st.text_input("Document Type", value="Freelance Work Contract")
    parties = st.text_area("Parties Involved", placeholder="Ex: Jane Doe (Freelancer), John Smith (Client)", height=120)
    terms = st.text_area("Terms & Conditions", placeholder="Payment: $2000, Deadline: 30 days...", height=140)
    effective_date = st.text_input("Effective Date", value=str(date.today()))

    if st.button("✨ Generate Document", type="primary", use_container_width=True):
        if not document_type.strip() or not parties.strip() or not terms.strip():
            st.error("Please fill all three fields: type, parties, terms")
        else:
            with st.spinner("Generating your legal draft..."):
                try:
                    clean_url = backend_url.strip().rstrip("/")
                    clean_url = re.sub(r"/docs.*$", "", clean_url)
                    clean_url = re.sub(r"/openapi.*$", "", clean_url)
                    if not clean_url.endswith("/generate"):
                        clean_url = clean_url + "/generate"
                    
                    payload = {
                        "document_type": document_type,
                        "parties": parties.strip(),
                        "terms": terms.strip(),
                        "effective_date": effective_date
                    }
                    r = requests.post(clean_url, json=payload, timeout=90)
                    data = r.json()
                    if r.status_code == 200:
                        doc_content = data.get("content", "") or data.get("document", "") or data.get("text", "")
                        st.session_state.document = doc_content
                        st.session_state.generated_type = document_type
                        st.session_state.history.append(document_type)
                        st.success("Generated Successfully!")
                    else:
                        st.error(f"Backend Error: {data}")
                except Exception as e:
                    st.error(f"Could not reach Backend: {e}")
                    st.session_state.document = f"{document_type}\n\nEFFECTIVE DATE: {effective_date}\n\nPARTIES:\n{parties}\n\nTERMS:\n{terms}\n\n1. Parties agree to above.\n2. This is offline draft.\n3. Please consult lawyer."
                    st.session_state.generated_type = document_type

with col_right:
    st.subheader("📄 Document Preview")
    if st.session_state.document:
        st.markdown(html_preview(st.session_state.document), unsafe_allow_html=True)
        
        edited_text = st.text_area("Editable Content", value=st.session_state.document, height=380, label_visibility="collapsed")
        if st.button("💾 Save Edits", use_container_width=True):
            st.session_state.document = edited_text
            st.success("Edits Saved!")

        st.divider()
        st.subheader("⬇️ Download Options")

        def get_bytes(func, content):
            result = func(content)
            if hasattr(result, 'getvalue'):
                return result.getvalue()
            if isinstance(result, str):
                return result.encode('utf-8')
            if isinstance(result, bytes):
                return result
            return result

        c1, c2, c3 = st.columns(3)
        with c1:
            txt_bytes = get_bytes(format_txt, st.session_state.document)
            st.download_button(
                "Download TXT",
                data=txt_bytes,
                file_name=filename("txt"),
                mime="text/plain",
                use_container_width=True
            )
        with c2:
            docx_bytes = get_bytes(format_docx, st.session_state.document)
            st.download_button(
                "Download DOCX",
                data=docx_bytes,
                file_name=filename("docx"),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        with c3:
            pdf_bytes = format_pdf(st.session_state.d_result)
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=filename("pdf"),
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("Your generated document will appear here after generation.")

def validate_inputs(doc_type, parties_text, terms_text):
    if not doc_type or len(doc_type.strip()) < 3:
        return False, "Document type too short"
    if not parties_text or len(parties_text.strip()) < 5:
        return False, "Parties info too short"
    if not terms_text or len(terms_text.strip()) < 10:
        return False, "Terms too short"
    return True, "ok"

def build_offline_document(doc_type, parties_text, terms_text, eff_date):
    header = f"{doc_type.upper()}\n{'='*len(doc_type)}\n\n"
    body = f"Effective Date: {eff_date}\n\nPARTIES:\n{parties_text}\n\nTERMS AND CONDITIONS:\n{terms_text}\n\n"
    clauses = "1. Both parties agree to comply.\n2. This document is AI generated draft.\n3. Consult qualified lawyer before signing.\n"
    return header + body + clauses

def render_footer():
    st.divider()
    st.caption("LegalEase AI v1.0 | Built with Streamlit + FastAPI | For educational purpose only")

if st.session_state.document:
    render_footer()
