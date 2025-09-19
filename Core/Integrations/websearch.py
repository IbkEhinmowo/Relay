import os
import requests




class Web:
    def __init__(self):
        self.BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")

    def search_result(self, query):
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "x-subscription-token": self.BRAVE_SEARCH_API_KEY
                },
                params={
                    "q": query,
                    "offset": "1",
                    "summary": "true",
                    "count": "3"
                    
                },
            ).json()

            results = []
            if "web" in response and "results" in response["web"]:
                results.extend(response["web"]["results"])
            if "videos" in response and "results" in response["videos"]:
                results.extend(response["videos"]["results"])
            
            return results if results else response
        except Exception as e:
            return {"error": str(e)}

    def news_result(self, query):
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/news/search",
                headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "gzip",
                    "x-subscription-token": self.BRAVE_SEARCH_API_KEY
                },
                params={
                    "q": query,
                    "offset": "1",
                    "summary": "true",
                    "count": "9"
                },
            ).json()
            if "news" in response:
                return response["news"].get("results", [])
            return response
        except Exception as e:
            return {"error": str(e)}
