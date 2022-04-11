from .base import Base
import requests
import json
import xmltodict

class Spotlight(Base):
    def __init__(self) -> None:
        self.api = ApiClient()

    def fetch_spotlight_entry(self, text: set):
        params = {
            "text": text,
            "confidence": 0.4,
            "support": 20,
        }
        response = self.api.get("annotate?", params)
        content = xmltodict.parse(response.text)
        data = json.dumps(content, indent=2)

        print(data)

    def run(self, texts: list):
        for t in texts:
            self.fetch_spotlight_entry(t)


class ApiClient():
    def __init__(self) -> None:
        self.base_url = "https://api.dbpedia-spotlight.org/en/"

    @staticmethod
    def handle_response(response, status):
        if (len(status) == 0 and 100 < response.status_code < 400) or (
                len(status) > 0 and response.status_code in status
            ):
            return response
        else:
            try:
                response = response.json()
            except Exception:
                pass
            raise requests.HTTPError(response)


    def get(self, url, *args, **kwargs):
        status = kwargs.pop("status", {})
        response = requests.get(self.base_url + url, *args, **kwargs)
        return self.handle_response(response, set() if status is None else status)
