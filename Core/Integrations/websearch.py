import requests
import os
from dotenv import load_dotenv

class WebSearchIntegration:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("SERPAPI_KEY")  # You need to set this in your .env
        self.base_url = "https://serpapi.com/search"

    def search(self, query: str, num_results: int = 5):
        """Perform a web search and return the top results as a list of dicts."""
        if not self.api_key:
            return {"error": "Missing SERPAPI_KEY in environment."}
        params = {
            "q": query,
            "api_key": self.api_key,
            "num": num_results,
            "engine": "google"
        }
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get("organic_results", [])
            return results[:num_results]
        except Exception as e:
            return {"error": str(e)}
