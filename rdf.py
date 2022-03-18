import os
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import FOAF, RDF
from pathlib import Path
import pandas as pd
import subprocess



class DataBuilder:
    def __init__(
        self,
        data_dir: Path = "data",
        rdf_dir: Path = "rdf",
    ):
        self.data_dir = Path(data_dir)
        self.rdf_dir = Path(rdf_dir)

    def download_data(self):
        print(self.data_dir)
        subprocess.call(["sh", "scripts/download-concordia-data.sh", str(self.data_dir)])
        

    def serialize_data(self):
        # EXAMPLE OF SERIALIZING EXISTING DATA
        g = Graph()
        g.parse("http://dbpedia.org/resource/Concordia_University")
        g.serialize(destination = self.rdf_dir / "concordia.ttl")

    def load_data(self):
        # THIS IS AN EXAMPLE, A BETTER THING TO DO WOULD BE TO POPULATE A GRAPH
        g = Graph()

        # only reading first file for now
        for f in os.listdir("data")[:-1]:
            print(f"DATA FROM {f}")

            data = pd.read_csv(self.data_dir / f"{f}", encoding="unicode_escape")
            print(data.head())

            for _, row in data.iterrows():
                # obviously don't use FOAF person but rather a custom class for course
                _course = URIRef(f"http://example.org/people/{row['Course ID']}")
                g.add((_course, RDF.type, FOAF.Person))
                g.add((_course, FOAF.name, Literal(row["Long Title"])))
                
            g.serialize(destination = self.rdf_dir / "courses.ttl")
            




if __name__ == "__main__":
    data_builder = DataBuilder()
    print("DOWNLOAD CONCORDIA CSV DATA")
    data_builder.download_data()
    data_builder.load_data()

    # serialize dbpedia data
    print("SERIALIZING CONCORDIA DBPEDIA ENTRY")
    data_builder.serialize_data()
