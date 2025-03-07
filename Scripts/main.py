import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from elasticsearch import Elasticsearch
import json

app = FastAPI()

# Elasticsearch Configuration
ES_HOST = "http://localhost:9200"
es = Elasticsearch(ES_HOST)

# Ollama API for Summarization
OLLAMA_API_URL = "http://localhost:11434/api/generate"

class SearchQuery(BaseModel):
    query: str

class SummaryRequest(BaseModel):
    paper_title: str

@app.get("/")
def home():
    return {"message": "Welcome to the Intelligent Research Assistant API"}

@app.get("/search/")
def search_papers(query: str):
    """Search for research papers using Elasticsearch"""
    try:
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "abstract", "keywords"]
                }
            }
        }
        response = es.search(index="research_papers", body=search_body)

        if not response["hits"]["hits"]:
            return {"message": "No papers found", "papers": []}

        papers = [
            {
                "title": hit["_source"]["title"],
                "authors": hit["_source"]["authors"],
                "publication_date": hit["_source"]["publication_date"],
                "abstract": hit["_source"]["abstract"],
                "pdf_url": hit["_source"]["pdf_url"]
            }
            for hit in response["hits"]["hits"]
        ]

        return {"papers": papers}

    except Exception as e:
        print(f"❌ Search Error: {str(e)}")  # Debugging log
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")

@app.get("/summarize/")
def summarize_paper(paper_title: str):
    """Summarize a research paper using its abstract."""
    try:
        search_body = {"query": {"match_phrase": {"title": paper_title}}}
        response = es.search(index="research_papers", body=search_body)

        if not response["hits"]["hits"]:
            print(f"⚠️ Paper '{paper_title}' not found.")  # Debugging log
            raise HTTPException(status_code=404, detail=f"Paper '{paper_title}' not found.")

        full_text = response["hits"]["hits"][0]["_source"]["abstract"]

        # Debugging Logs
        print(f"🔍 Paper Found: {paper_title}")
        print(f"📜 Full Text (First 200 chars): {full_text[:200]}...")

        # Call Ollama API for Summarization
        data = {"model": "mistral", "prompt": f"Summarize this research paper:\n\n{full_text}"}
        
        try:
            summary_response = requests.post(OLLAMA_API_URL, json=data, timeout=30, stream=True)  # Enable streaming
            summary_response.raise_for_status()  # Raise error if response is not 200
        except requests.exceptions.RequestException as e:
            print(f"❌ Ollama API Connection Error: {str(e)}")  # Debugging log
            raise HTTPException(status_code=500, detail="Failed to connect to Ollama API")

        print(f"📡 Ollama API Request Sent: {OLLAMA_API_URL}")

        # **Fix: Handle Streamed Response from Ollama API**
        summary_text = ""
        try:
            for line in summary_response.iter_lines():
                if line:
                    try:
                        json_chunk = json.loads(line.decode("utf-8"))
                        summary_text += json_chunk.get("response", "")
                    except json.JSONDecodeError:
                        print(f"⚠️ Skipping invalid JSON chunk: {line.decode('utf-8')}")  # Debugging
                        continue

            print(f"✅ Ollama Response: {summary_text.strip()}")  # Debugging
            return {"summary": summary_text.strip()}

        except Exception as e:
            print(f"⚠️ JSON Parsing Error: {str(e)}")
            print(f"🔍 Raw Response: {summary_response.text}")  # Debugging raw output
            raise HTTPException(status_code=500, detail="Ollama API returned invalid JSON.")

    except Exception as e:
        print(f"🚨 Summarization Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization Error: {str(e)}")