import fitz  # PyMuPDF
import sys
from pathlib import Path

def extract_pdf_text(pdf_path: Path, txt_path: Path):
    print(f"Extracting {pdf_path.name}...")
    doc = fitz.open(pdf_path)
    text = []
    for page in doc:
        text.append(page.get_text())
    
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n--- PAGE BREAK ---\n".join(text))
    print(f"Saved to {txt_path.name}")

if __name__ == "__main__":
    downloads = Path(r"C:\Users\Deving-1\Downloads")
    output_dir = Path(r"C:\Users\Deving-1\welly_db_4budZ\docs\extracted")
    
    # We will extract text from the smaller/critical documents first
    files_to_extract = [
        "Action Plan From Research Documents.pdf",
        "ZuluYokohama_Protocol_Feature_Compute_Hardening_Request_Package-1.pdf",
        "Review and Suggestion Layer Development.pdf",
        "ZuluYokohama Protocol refactoring- .pdf",
        "LLM V&V Toolchain Optimization Strategies.pdf",
        "OFFICE365-VEP-OILFIELDoPS-WELLBORE-&-STANDALONE-DATABASE-SOFTWARE-OBJECT-PLAN-CONCEPT-1.pdf"
    ]
    
    for f in files_to_extract:
        pdf_path = downloads / f
        txt_path = output_dir / f.replace(".pdf", ".txt")
        extract_pdf_text(pdf_path, txt_path)
