import os
import fitz  # PyMuPDF
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text() for page in doc])
    return text

def index_paper(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    doc = {"text": text, "file_name": os.path.basename(pdf_path)}
    es.index(index="papers_index", body=doc)

# Process all PDFs in the data folder
pdf_folder = "data"
for pdf_file in os.listdir(pdf_folder):
    if pdf_file.endswith(".pdf"):
        index_paper(os.path.join(pdf_folder, pdf_file))
        print(f"Indexed {pdf_file}")