import arxiv
import pdfplumber
import requests
import os
from elasticsearch import Elasticsearch
from ollama import chat  # Using Ollama for summarization

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "research_papers"

def fetch_arxiv_papers(query, total_results=10):
    """Fetches and processes research papers from arXiv."""
    search = arxiv.Search(
        query=query,
        max_results=total_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in search.results():
        title = result.title
        authors = ", ".join([author.name for author in result.authors])
        publication_date = result.published.strftime("%Y-%m-%d")
        abstract = result.summary
        pdf_url = result.pdf_url

        # Download and extract full text
        full_text = extract_text_from_pdf(pdf_url)

        # Generate summary using Ollama
        summary = generate_summary(full_text) if full_text else "No summary available."

        # Store in Elasticsearch
        document = {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "full_text": full_text,
            "summary": summary,
            "publication_date": publication_date,
            "pdf_url": pdf_url
        }

        es.index(index=index_name, document=document)
        print(f"✅ Indexed: {title}")

def extract_text_from_pdf(pdf_url):
    """Downloads and extracts text from a research paper PDF."""
    response = requests.get(pdf_url)
    pdf_path = "temp.pdf"

    if response.status_code == 200:
        with open(pdf_path, "wb") as f:
            f.write(response.content)

        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        os.remove(pdf_path)  # Cleanup
        return text
    else:
        print(f"❌ Failed to download PDF: {pdf_url}")
        return ""

def generate_summary(text):
    """Summarizes the extracted text using Ollama."""
    response = chat(model="mistral", messages=[{"role": "user", "content": f"Summarize the following research paper:\n{text}"}])
    return response.get("message", {}).get("content", "No summary generated.")

if __name__ == "__main__":
    fetch_arxiv_papers("deep learning", total_results=10)  # Fetch 10 papers