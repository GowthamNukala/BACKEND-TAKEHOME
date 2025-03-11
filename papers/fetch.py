import requests
import csv
from typing import List, Dict, Optional


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def fetch_paper_ids(query: str) -> List[str]:
    """Fetch paper IDs from PubMed using the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Limit results for testing
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["esearchresult"]["idlist"]


def fetch_paper_details(paper_id: str) -> Optional[Dict]:
    """Fetch paper details from PubMed by ID."""
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "json"
    }
    response = requests.get(DETAILS_URL, params=params)
    response.raise_for_status()
    data = response.json()
    
    try:
        details = data["result"][paper_id]
        return {
            "PubmedID": paper_id,
            "Title": details.get("title", ""),
            "Publication Date": details.get("pubdate", ""),
            "Authors": details.get("authors", []),
            "Company Affiliation(s)": _extract_companies(details.get("authors", [])),
            "Corresponding Author Email": details.get("contactinfo", {}).get("email", "")
        }
    except KeyError:
        return None


def _extract_companies(authors: List[Dict]) -> List[str]:
    """Extract company names from authors' affiliations."""
    companies = []
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if any(kw in affiliation for kw in ["pharma", "biotech", "inc", "ltd", "company"]):
            companies.append(affiliation)
    return companies


def save_to_csv(papers: List[Dict], filename: str) -> None:
    """Save paper details to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

