import streamlit as st
import requests

# FastAPI Backend URL
FASTAPI_BASE_URL = "http://127.0.0.1:8000"

# Streamlit App Configuration
st.set_page_config(page_title="Research Assistant", layout="wide")

# App Title
st.title("📚 Intelligent Research Assistant")

# User Input for Search Query
query = st.text_input("🔍 Enter a topic to search for research papers:", "")

# State variables to store search results and summaries
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = {}

if st.button("Search"):
    if query:
        st.write("🔄 Searching for papers... Please wait.")
        try:
            response = requests.get(f"{FASTAPI_BASE_URL}/search/?query={query}")
            if response.status_code == 200:
                papers = response.json().get("papers", [])

                # Store papers in session state and reset summaries
                st.session_state.papers = papers
                st.session_state.summaries = {}  

                if not papers:
                    st.warning("⚠️ No papers found. Try a different search term.")
            else:
                st.error("❌ Error fetching papers. Please check the API.")
        except Exception as e:
            st.error(f"🚨 An error occurred: {str(e)}")

# Display papers and add a button to generate summaries
for i, paper in enumerate(st.session_state.papers):
    st.subheader(f"📄 {paper['title']}")

    # ✅ **Fix Author Formatting**
    authors = paper["authors"]
    if isinstance(authors, list):
        authors = ", ".join(authors)  # Convert list to a comma-separated string
    
    st.write(f"**Authors:** {authors}")
    st.write(f"**Published on:** {paper['publication_date']}")
    st.write(f"**Abstract:** {paper['abstract']}")
    st.write(f"[📄 Read Full Paper]({paper['pdf_url']})")

    # Summarization button
    if st.button(f"Summarize Paper {i+1}", key=f"summary_btn_{i}"):
        st.write("⏳ Generating summary... Please wait.")
        try:
            summary_url = f"{FASTAPI_BASE_URL}/summarize/?paper_title={paper['title']}"
            summary_response = requests.get(summary_url)

            if summary_response.status_code == 200:
                summary_data = summary_response.json()
                st.session_state.summaries[paper["title"]] = summary_data.get("summary", "No summary available.")
            else:
                st.session_state.summaries[paper["title"]] = f"❌ Error fetching summary. API returned {summary_response.status_code}"
        except Exception as e:
            st.session_state.summaries[paper["title"]] = f"🚨 An error occurred: {str(e)}"

    # Show the summary if it exists
    if paper["title"] in st.session_state.summaries:
        st.write(f"**Summary:** {st.session_state.summaries[paper['title']]}")

    st.divider()  # Adds a horizontal line between papers

# Footer
st.markdown("---")
st.markdown("👨‍💻 Built by **Durgesh** | Powered by **FastAPI & Streamlit**")