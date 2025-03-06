import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Intelligent Research Assistant", layout="wide")

# Center the title
st.markdown(
    "<h1 style='text-align: center;'>📚 Intelligent Research Assistant</h1>",
    unsafe_allow_html=True
)

# Add some spacing after the title
st.markdown("<br>", unsafe_allow_html=True)

# User input for query
query = st.text_input(
    "🔍 Enter your search query",
    "",
    placeholder="Type a research topic...",
    label_visibility="collapsed",
)

# Add some space for UI
st.markdown("<br>", unsafe_allow_html=True)

# Search button
if st.button("Search"):
    if query:
        with st.spinner("🔎 Searching for papers... Please wait."):
            api_url = f"http://127.0.0.1:8000/search/?query={query}"
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                st.subheader("📄 Search Results")

                # Display papers with styled containers
                for paper in data.get("papers", []):
                    with st.expander(f"📄 {paper['title']}", expanded=True):
                        st.write(f"**Authors:** {paper['authors']}")
                        st.write(f"📅 Published: {paper['publication_date']}")
                        st.write(f"**Summary:** {paper['summary']}")
                        st.markdown(f"🔗 [Read Paper]({paper['pdf_url']})", unsafe_allow_html=True)

            else:
                st.error("⚠️ Error fetching data. Check the API.")
    else:
        st.warning("❗ Please enter a search query.")