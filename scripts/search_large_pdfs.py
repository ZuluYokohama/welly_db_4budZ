import fitz  # PyMuPDF
from pathlib import Path

def search_pdf_for_keywords(pdf_path: Path, keywords: list):
    doc = fitz.open(pdf_path)
    found_any = False
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        for kw in keywords:
            if kw.lower() in text.lower():
                print(f"[{pdf_path.name}] Page {page_num + 1} matches key: '{kw}'")
                # print some lines surrounding the match
                lines = text.split("\n")
                for line in lines:
                    if kw.lower() in line.lower():
                        print(f"  Line: {line.strip()}")
                found_any = True
    return found_any

if __name__ == "__main__":
    downloads = Path(r"C:\Users\Deving-1\Downloads")
    keywords = ["compute sequencing", "sw:hw", "sequencing", "sw/hw"]
    
    pdfs = list(downloads.glob("*.pdf"))
    for pdf in pdfs:
        try:
            search_pdf_for_keywords(pdf, keywords)
        except Exception as e:
            print(f"Error reading {pdf.name}: {e}")
