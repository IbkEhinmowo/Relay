
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
                    "count": "10"
                    
                },
            ).json()
            print(response)
            return response
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
                    "count": "10"
                },
            ).json()
            return response
        except Exception as e:
            return {"error": str(e)}
