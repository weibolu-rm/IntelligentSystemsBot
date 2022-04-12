import rdflib
import requests
from .api import ApiClient
from pathlib import Path

class Sparql:
    def __init__(self, base_url: str = "http://localhost:3030/idk/") -> None:
        self.base_url = base_url
        self.graph = rdflib.Graph()
        self.api = ApiClient(base_url)
        self.init()

    def init(self):
        self.check_if_server_is_running()
        self.graph.parse(self.api.base_url)

    def check_if_server_is_running(self):

        print("Checking is fuseki server is running..")
        try:
            self.api.get('', status=[200])
            print(f"Server running @ {self.base_url}.")
        except requests.exceptions.ConnectionError:
            print("ERROR: Start the fuseki server!")
            exit()

    def query(self, query: str):
        qres = self.graph.query(query)
        for row in qres:
            print(row)
        return qres
        



