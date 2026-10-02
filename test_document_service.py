from services.document_service import format_txt,format_docx,format_pdf,export_filename
S='''FREELANCE WORK CONTRACT\n\nNOTICE\nThis is an AI-generated draft.\n\n1. PARTIES\nJane Doe (Provider), TechNova Inc. (Client)\n\n5. SIGNATURES\nParty 1: __________'''
def test_txt(): assert b'FREELANCE WORK CONTRACT' in format_txt(S)
def test_docx(): assert format_docx(S,'Freelance Work Contract')[:2]==b'PK'
def test_pdf(): assert format_pdf(S,'Freelance Work Contract').startswith(b'%PDF')


def test_filename(): assert export_filename("NDA", "pdf") == "NDA.pdf"
