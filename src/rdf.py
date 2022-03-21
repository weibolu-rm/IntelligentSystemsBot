import os
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import FOAF, RDF, RDFS
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
        self._initialize_dirs()

    def _initialize_dirs(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.rdf_dir, exist_ok=True)


    def download_data(self):
        subprocess.call(["sh", "scripts/download-concordia-data.sh", str(self.data_dir)])
        

    def serialize_data(self):
        # EXAMPLE OF SERIALIZING EXISTING DATA
        g = Graph()
        g.parse("http://dbpedia.org/resource/Concordia_University")
        g.serialize(destination = self.rdf_dir / "concordia.ttl")

    def load_data(self):
        # THIS IS AN EXAMPLE
        VIVO = Namespace('http://vivoweb.org/ontology/core#')
        g = Graph()

        # only reading first file for now
        # for f in os.listdir("data")[:-1]:


        # COURSE DATA
        course_data = pd.read_csv(
            self.data_dir / f"CU_SR_OPEN_DATA_CATALOG.csv",
            encoding="unicode_escape",
        )
        # COURSE DESC
        course_desc = pd.read_csv(
            self.data_dir / f"CU_SR_OPEN_DATA_CATALOG_DESC.csv",
            encoding="unicode_escape",
        )

        for i, row in course_data.iterrows():
            #COURSE DATA
            # obviously don't use FOAF person but rather a custom class for course
            _course = URIRef(f"http://example.org/course/{row['Course ID']}")

            g.add((_course, RDF.type, VIVO.Course))
            g.add((_course, FOAF.name, Literal(row["Long Title"])))
            g.add((_course, RDFS.label, Literal(row["Long Title"])))
            g.add((_course, VIVO["uid"], Literal(row["Course ID"])))
            g.add((_course, VIVO["credits"], Literal(row["Class Units"])))
            g.add((_course, VIVO["subjectAreaOf"], Literal(row["Subject"])))


            #Custom property for Component Description
            _component_desc_property = URIRef(f"http://example.org/property/componentdesc")
            g.add((_component_desc_property, RDF.type, RDF.Property))
            g.add((_component_desc_property, RDFS.label, Literal("component description property")))
            g.add((_component_desc_property, RDFS.comment, Literal("this property is used to describe whether a course is a lab, lecture or a studio session")))
            g.add((_course, _component_desc_property, Literal(row["Component Descr"])))


            #COURSE DESC
            desc = course_desc.iloc[i]["Descr"]
            g.add((_course, VIVO["description"], Literal(desc)))



        g.serialize(destination = self.rdf_dir / "courses.ttl")
            

    def fetch_all_universities(self):
        """
        Update our local data on universities

        unfortunately this is limited by the fact that this is a public endpoint
        """
        g = Graph()
        qres = g.query(
        """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?university ?name
        WHERE {
            SERVICE <https://dbpedia.org/sparql/> {
                ?university rdf:type dbo:University .
                ?university rdfs:label ?name.
            } 
            FILTER (LANG(?name) = "en")
        }
        LIMIT 10000
        """
        )

        result = pd.DataFrame(qres, columns=["University", "Name"])
        result.to_json(self.data_dir / "temp.json", indent=2, force_ascii=False)




if __name__ == "__main__":
    
    data_builder = DataBuilder()

    # data_builder.fetch_all_universities()

    # print("DOWNLOAD CONCORDIA CSV DATA")
    # data_builder.download_data()
    data_builder.load_data()

    # # serialize dbpedia data
    # print("SERIALIZING CONCORDIA DBPEDIA ENTRY")
    # data_builder.serialize_data()
