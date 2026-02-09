"""
Module: scanner.py
Description: OSINT Search with reliable "Dev Mode" Mocking.
"""
from duckduckgo_search import DDGS

# MOCK DATABASE: The "Golden Path" for your demo.
# keys must be lowercase.
MOCK_DB = {
    # BRANCH A TEST CASE (Website Exists)
    "persona": "https://withpersona.com",
    "accenture": "https://www.accenture.com",
    "microsoft": "https://www.microsoft.com",
    
    # BRANCH B TEST CASE (No Website)
    "lopez farm": None, 
    "my local bakery": None
}

def find_business_url(name, location):
    """
    1. Checks MOCK_DB for a guaranteed match.
    2. Searches DuckDuckGo if not in DB.
    """
    
    # Standardize input to lowercase for key matching
    key = name.lower().strip()
    
    # Check our internal database first
    if key in MOCK_DB:
        print(f"[DEBUG] Found '{name}' in Internal Database.")
        return MOCK_DB[key]

    # REAL SEARCH FALLBACK
    print(f"[-] '{name}' not in database. Searching web...")
    query = f"{name} {location} official site"
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            if results:
                # Return the first result
                return results[0]['href']
    except Exception as e:
        print(f"Search Error: {e}")
        return None

    return None