# index_arxiv.py - Fetches and indexes research papers from arXiv with pagination

import arxiv
from elasticsearch import Elasticsearch
from datetime import datetime

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "research_papers"

def fetch_arxiv_papers_paginated(query, total_results=100):
    """Fetches research papers from arXiv API with pagination."""
    per_page = 50  # Maximum allowed per request by arXiv API
    num_pages = (total_results // per_page) + (1 if total_results % per_page else 0)  # Calculate required pages

    for i in range(num_pages):
        search = arxiv.Search(
            query=query,
            max_results=per_page,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        for result in search.results():
            title = result.title
            authors = ", ".join([author.name for author in result.authors])
            publication_date = result.published.strftime("%Y-%m-%d")
            abstract = result.summary
            pdf_url = result.pdf_url

            # Create document for Elasticsearch
            document = {
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "content": abstract,  # Storing abstract as content
                "publication_date": publication_date,
                "pdf_url": pdf_url
            }

            # Index document into Elasticsearch
            es.index(index=index_name, document=document)
            print(f"Indexed: {title}")

if __name__ == "__main__":
    fetch_arxiv_papers_paginated("deep learning", total_results=100)  # Fetch 100 papers