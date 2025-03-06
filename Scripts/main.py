import requests
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI()

# Function to fetch papers from the API
def fetch_papers_from_api(query, top_n=5):
    api_url = f"http://127.0.0.1:8000/search/?query={query}&top_n={top_n}"
    print(f"Fetching papers from: {api_url}")  # Debugging: Print the URL
    try:
        response = requests.get(api_url)
        print(f"Response status code: {response.status_code}")  # Debugging: Check the response status
        if response.status_code == 200:
            return response.json()['papers']
        else:
            raise Exception(f"Error fetching data from API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred: {e}")  # Debugging: Print the error if any
        raise e  # Reraise the exception after logging it

# Search endpoint to search for papers
@app.get("/search/", response_class=ORJSONResponse)
async def search(query: str, top_n: int = 5):
    print(f"Searching for: {query}")  # Debugging: Print the search query
    try:
        papers = fetch_papers_from_api(query, top_n)
        return {"papers": papers}
    except Exception as e:
        return {"error": str(e)}

# Example endpoint for summarizing papers
@app.get("/summarize/", response_class=ORJSONResponse)
def summarize(paper_title: str):
    """API endpoint to summarize a research paper."""
    summary = f"Summary of the paper '{paper_title}' will be here."
    return {"title": paper_title, "summary": summary}

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Intelligent Research Assistant API!"}