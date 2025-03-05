# index_paper.py

from elasticsearch import Elasticsearch
from datetime import datetime
from extract_text import extract_text_from_pdf

es = Elasticsearch("http://localhost:9200")
index_name = "research_papers"

def index_paper(pdf_path, title, authors, publication_date):
    content = extract_text_from_pdf(pdf_path)

    document = {
        "title": title,
        "authors": authors,
        "abstract": content[:1000],  # Store first 1000 chars as abstract
        "content": content,
        "publication_date": datetime.strptime(publication_date, "%Y-%m-%d")
    }

    es.index(index=index_name, document=document)
    print(f"Indexed paper: {title}")

# Example usage
if __name__ == "__main__":
    index_paper("example.pdf", "Deep Learning in NLP", "John Doe, Jane Smith", "2023-06-15")