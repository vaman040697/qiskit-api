from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# List of main Qiskit documentation URLs
qiskit_main_pages = [
    "https://docs.quantum.ibm.com/api/qiskit",
    "https://docs.quantum.ibm.com/api/qiskit-ibm-runtime",
    "https://docs.quantum.ibm.com/api/qiskit-ibm-transpiler"
]

# Function to extract all subpage links
def get_all_subpage_links(main_url):
    response = requests.get(main_url)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    
    for a_tag in soup.find_all("a", href=True):  # Find all <a> links
        href = a_tag["href"]
        if href.startswith("/") or main_url in href:  # Internal links only
            full_url = href if href.startswith("http") else main_url + href
            links.append(full_url)

    return list(set(links))  # Remove duplicates

# Function to scrape content from a given URL
def scrape_page_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator="\n")[:2000]  # Return first 2000 characters

# Function to search through Qiskit docs dynamically
def fetch_relevant_docs(query):
    results = []
    
    # Go through each main documentation page
    for main_page in qiskit_main_pages:
        subpages = get_all_subpage_links(main_page)  # Get subpage links
        for subpage in subpages:
            text_content = scrape_page_content(subpage)
            if query.lower() in text_content.lower():
                snippet = text_content[:1000]  # Limit snippet size
                results.append({"url": subpage, "snippet": snippet})

    return results

@app.get("/search_qiskit")
async def search_qiskit(query: str = Query(...)):
    results = fetch_relevant_docs(query)
    return {"query": query, "results": results}
