import requests

class Web:
    def __init__(self, query):
        self.query = query

    def search(self):
        response = requests.get(
          "https://api.search.brave.com/res/v1/web/search",
          headers={
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "x-subscription-token": "BSA0WHajgTIvUQ_wfFDQoHKawYDfSK-"
          },
          params={
            "q": self.query,
            "offset": "1",
            "summary": "true"
          },
        ).json()
        return response