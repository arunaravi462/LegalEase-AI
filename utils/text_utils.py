import html, re, unicodedata
def sanitize_text(text: str) -> str:
    if not text: return ""
    for old,new in {"“":"\"","”":"\"","‘":"'","’":"'","–":"-","—":"-","\u00a0":" ","•":"-"}.items(): text=text.replace(old,new)
    text=unicodedata.normalize("NFKC",text)
    text="".join(c for c in text if c in "\n\r\t" or ord(c)>=32)
    text=re.sub(r"[ \t]+"," ",text); text=re.sub(r"\n{3,}","\n\n",text)
    return text.strip()
def parse_terms(terms: str) -> list[str]: return [x.strip() for x in terms.split(";") if x.strip()]
def html_preview(text: str) -> str:
    safe=html.escape(sanitize_text(text)).replace("\n\n","<br><br>").replace("\n","<br>")
    return f'<div class="legal-preview">{safe}</div>'
