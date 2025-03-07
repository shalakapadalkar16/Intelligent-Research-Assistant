import arxiv
from elasticsearch import Elasticsearch

# Elasticsearch Connection
ES_URL = "http://localhost:9200"
INDEX_NAME = "research_papers"
es = Elasticsearch(ES_URL)

def fetch_arxiv_papers(query, max_results=50):
    """Fetches research papers from Arxiv and indexes them in Elasticsearch."""

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in search.results():
        title = result.title
        authors = ", ".join([author.name for author in result.authors])
        publication_date = result.published.strftime("%Y-%m-%d")
        abstract = result.summary
        pdf_url = result.pdf_url

        document = {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "content": abstract,  # Storing abstract as content
            "publication_date": publication_date,
            "pdf_url": pdf_url
        }

        es.index(index=INDEX_NAME, document=document)
        print(f"✅ Indexed: {title}")

if __name__ == "__main__":
    fetch_arxiv_papers("deep learning", max_results=50)