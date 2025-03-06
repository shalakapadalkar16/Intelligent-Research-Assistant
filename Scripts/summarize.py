# summarize.py - Summarizing research papers using Ollama
import ollama
from search_paper import search_papers

def summarize_text(text):
    """Summarizes a research paper using Ollama LLM."""
    model = "mistral"  # Change to another model if needed (e.g., llama3, gemma)
    prompt = f"Summarize the following academic text:\n\n{text[:3000]}"  # Limit input size

    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

# Example usage
if __name__ == "__main__":
    papers = search_papers("deep learning", top_n=1)  # Get one most relevant paper
    if papers:
        summary = summarize_text(papers[0]["abstract"])
        print("\nTitle:", papers[0]["title"])
        print("\nSummary:", summary)
    else:
        print("No papers found.")