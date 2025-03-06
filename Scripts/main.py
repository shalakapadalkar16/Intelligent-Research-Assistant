from fastapi import FastAPI
from fastapi.responses import Response
from search_paper import search_papers
from summarize import summarize_text
import json

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Research Assistant API!"}

@app.get("/search/")
def search(query: str, top_n: int = 5):
    """API endpoint to search for research papers."""
    results = search_papers(query, top_n)

    # Always pretty-print the response
    formatted_results = json.dumps({"papers": results}, indent=4)
    return Response(content=formatted_results, media_type="application/json")

@app.get("/summarize/")
def summarize(paper_title: str):
    """API endpoint to summarize a research paper."""
    results = search_papers(paper_title, top_n=1)

    if not results:
        return Response(content=json.dumps({"error": "Paper not found"}, indent=4), media_type="application/json")

    summary = summarize_text(results[0]["abstract"])
    formatted_summary = json.dumps({"title": results[0]["title"], "summary": summary}, indent=4)
    return Response(content=formatted_summary, media_type="application/json")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)