from utils.text_utils import sanitize_text,parse_terms,html_preview
def test_sanitize_text(): assert sanitize_text('“Hello” — world')=='"Hello" - world'
def test_parse_terms(): assert parse_terms('First; Second; Third')==['First','Second','Third']
def test_html_preview(): assert '<script>' not in html_preview('<script>alert(1)</script>')
