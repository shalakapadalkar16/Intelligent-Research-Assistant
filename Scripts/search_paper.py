# search_paper.py - Searches for research papers in Elasticsearch

from elasticsearch import Elasticsearch

# Initialize Elasticsearch
es = Elasticsearch("http://localhost:9200")
index_name = "research_papers"

def search_papers(query, top_n=5):
    """Search for research papers in Elasticsearch and remove duplicates."""
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "abstract", "content"]
            }
        },
        "size": top_n
    }

    results = es.search(index=index_name, body=search_body)

    # Remove duplicates using a dictionary (key = title)
    unique_papers = {}
    for hit in results["hits"]["hits"]:
        paper = hit["_source"]
        if paper["title"] not in unique_papers:
            unique_papers[paper["title"]] = paper  # Store only unique titles

    return list(unique_papers.values())

# Example usage
if __name__ == "__main__":
    papers = search_papers("machine learning", top_n=5)
    for paper in papers:
        print(f"\nTitle: {paper['title']}\nAuthors: {paper['authors']}\nPDF: {paper['pdf_url']}\n")