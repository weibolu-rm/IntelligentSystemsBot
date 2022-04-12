from .base import Base
import os
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm


class Spotlight(Base):
    def __init__(
        self,
        data_dir: Path = "data",
        res_dir: Path = "resources",
        rdf_dir: Path = "rdf",
        is_init: bool = True,
    ):
        super().__init__(
            data_dir=data_dir, res_dir=res_dir, rdf_dir=rdf_dir, is_init=is_init
        )
        self.api = ApiClient()
        self.entities = []

    def fetch_spotlight_entries(self, texts: set) -> list:
        """
        Use the dbpedia spotlight API to fetch entries in dbpedia.
        We limit the amount of texts passed to the endpoint due to 414 limitations.
        """
        
        TEXTS_PER_LOOP = 500
        start = end = 0

        _entities = []
        with tqdm(total=len(texts), desc="Fetching dbpedia entries with spotlight..") as pbar:
            while start <= len(texts):
                end = end + TEXTS_PER_LOOP if end + TEXTS_PER_LOOP < len(texts) else len(texts)
                diff = end - start

                _text = ""
                for t in list(texts)[start:end]:
                    _text += f"{t},"

                headers = {"Accept": "application/json"}
                params = {
                    "text": _text,
                    "confidence": 0.4,
                    "support": 20,
                }
                response = self.api.get("annotate?", params, headers=headers).json()
                _entities.extend(self.process_entries(response))
                start += TEXTS_PER_LOOP
                pbar.update(diff)
        return _entities

    @staticmethod
    def process_entries(data):
        return [
            {
                "surfaceForm": r["@surfaceForm"],
                "uri": r["@URI"],
            }
            for r in data["Resources"]
        ]

    def run(self, texts: set) -> None:
        data = self.fetch_spotlight_entries(texts)

        self.entities = data
            
        self.dump()

    def dump(self):
        os.makedirs(self.data_dir / "processed", exist_ok=True)
        entities = pd.DataFrame(self.entities)
        file_path = self.data_dir / "processed" / "entities.pkl"
        entities.to_pickle(file_path)
        print(entities)
        print(f"{len(entities)} entities saved to {file_path}.")


class ApiClient:
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
