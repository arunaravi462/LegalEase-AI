from datetime import date
import requests, streamlit as st
from services.document_service import export_filename,format_docx,format_pdf,format_txt
from utils.config import get_settings
from utils.text_utils import html_preview
settings=get_settings(); st.set_page_config(page_title="LegalEase",page_icon="⚖️",layout="wide")
st.markdown('''<style>.legal-preview{background:#171717;color:#f5f5f5;padding:1.25rem;border-radius:12px;border:1px solid #333;min-height:300px;max-height:650px;overflow-y:auto;line-height:1.6;font-family:Georgia,serif}.notice{padding:.8rem 1rem;border-left:4px solid #777;background:#f6f6f6;border-radius:4px}</style>''',unsafe_allow_html=True)
st.title("⚖️ LegalEase"); st.caption("AI-Powered Legal Document Generator")
st.markdown('<div class="notice"><b>Important:</b> LegalEase creates AI-assisted drafts. Review documents for your jurisdiction and circumstances before relying on them.</div>',unsafe_allow_html=True)
with st.sidebar: backend_url=st.text_input("Backend URL",settings.backend_url).rstrip("/")
if "document" not in st.session_state: st.session_state.document=""
if "generated_type" not in st.session_state: st.session_state.generated_type="Legal Document"
a,b=st.columns([1,1.2])
with a:
    st.subheader("Document details")
    document_type=st.text_input("Document type",placeholder="Freelance Work Contract")
    parties=st.text_area("Parties involved",placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",height=120)
    terms=st.text_area("Terms & conditions",placeholder="Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",height=180)
    effective_date=st.date_input("Effective date",date.today())
    if st.button("Generate Document",type="primary",use_container_width=True):
        if not all([document_type.strip(),parties.strip(),terms.strip()]): st.error("Please complete document type, parties, and terms.")
        else:
            try:
                with st.spinner("Generating your draft..."):
                    r=requests.post(f"{backend_url}/generate",json={"document_type":document_type,"parties":parties,"terms":terms,"effective_date":effective_date.isoformat()},timeout=settings.request_timeout_seconds); r.raise_for_status(); data=r.json()
                st.session_state.document=data["content"]; st.session_state.generated_type=data["document_type"]; st.success("Document generated successfully." if not data.get("demo_mode") else "Demo draft generated.")
            except requests.RequestException as e: st.error(f"Could not reach FastAPI at {backend_url}: {e}")
with b:
    st.subheader("Document preview")
    if st.session_state.document:
        st.markdown(html_preview(st.session_state.document),unsafe_allow_html=True); st.divider(); st.subheader("Edit document")
        edited=st.text_area("Editable content",st.session_state.document,height=420,label_visibility="collapsed")
        if st.button("Save edits",use_container_width=True): st.session_state.document=edited; st.rerun()
        st.subheader("Download"); c1,c2,c3=st.columns(3)
        with c1: st.download_button("Download TXT",format_txt(st.session_state.document),export_filename(st.session_state.generated_type,"txt"),"text/plain",use_container_width=True)
        with c2: st.download_button("Download DOCX",format_docx(st.session_state.document,st.session_state.generated_type),export_filename(st.session_state.generated_type,"docx"),"application/vnd.openxmlformats-officedocument.wordprocessingml.document",use_container_width=True)
        with c3: st.download_button("Download PDF",format_pdf(st.session_state.document,st.session_state.generated_type),export_filename(st.session_state.generated_type,"pdf"),"application/pdf",use_container_width=True)
    else: st.info("Your generated document will appear here.")
