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
        VIVO = Namespace('http://vivoweb.org/ontology/core#')
        g = Graph()

        #COURSES:
        #COURSE DATA
        course_data = pd.read_csv(
            self.data_dir / f"CU_SR_OPEN_DATA_CATALOG.csv",
            encoding="unicode_escape",
            index_col = "Course ID",
        )
        # COURSE DESC
        course_desc = pd.read_csv(
            self.data_dir / f"CU_SR_OPEN_DATA_CATALOG_DESC.csv",
            encoding="unicode_escape",
            index_col = "Course ID",
        )

        #custom properties
        #Custom property for Component Description
        _component_desc_property = URIRef(f"http://example.org/property/componentdesc")
        g.add((_component_desc_property, RDF.type, RDF.Property))
        g.add((_component_desc_property, RDFS.label, Literal("component description property")))
        g.add((_component_desc_property, RDFS.comment, Literal("this property is used to describe whether a course is a lab, lecture or a studio session")))

        #Custom property for Catalogue
        _catalog_property = URIRef(f"http://example.org/property/catalog")
        g.add((_catalog_property, RDF.type, RDF.Property))
        g.add((_catalog_property, RDFS.label, Literal("Catalog property")))
        g.add((_catalog_property, RDFS.comment, Literal("this property is used to describe what the course number is for a course")))

        #Custom property for prerequisites
        _prerequisites_property = URIRef(f"http://example.org/property/prerequisites")
        g.add((_prerequisites_property, RDF.type, RDF.Property))
        g.add((_prerequisites_property, RDFS.label, Literal("prerequisites property")))
        g.add((_prerequisites_property, RDFS.comment, Literal("this property is used to describe what the prerequisites are for a course")))

        #Custom property for prerequisites
        _degree_type_property= URIRef(f"http://example.org/property/degreetype")
        g.add((_degree_type_property, RDF.type, RDF.Property))
        g.add((_degree_type_property, RDFS.label, Literal("degree type property")))
        g.add((_degree_type_property, RDFS.comment, Literal("this property is used to describe what type of degree the course is offered for")))

        #Custom property for prerequisites
        _equivalent_courses_property= URIRef(f"http://example.org/property/equivalentcourses")
        g.add((_equivalent_courses_property, RDF.type, RDF.Property))
        g.add((_equivalent_courses_property, RDFS.label, Literal("equivalent courses property")))
        g.add((_equivalent_courses_property, RDFS.comment, Literal("this property is used to describe what courses are equivalent to the subject course")))

        #Custom property for Offered at university
        _offered_at = URIRef(f"http://example.org/property/offeredat")
        g.add((_offered_at, RDF.type, RDF.Property))
        g.add((_offered_at, RDFS.label, Literal("Offered at property")))
        g.add((_offered_at, RDFS.comment, Literal("this property is used to indicate a relationship between a university and a course being offered at that university")))

        for course_id, row in course_data.iterrows():
            #COURSE DATA
            # obviously don't use FOAF person but rather a custom class for course
            _course = URIRef(f"http://example.org/course/{course_id}")

            g.add((_course, RDF.type, VIVO.Course))
            g.add((_course, VIVO.Title, Literal(row["Long Title"])))
            g.add((_course, RDFS.label, Literal(row["Long Title"])))
            g.add((_course, VIVO.Uid, Literal(course_id)))
            g.add((_course, VIVO.Credits, Literal(int(row["Class Units"]))))
            g.add((_course, VIVO.subjectAreaOf, Literal(row["Subject"])))
            g.add((_course, _component_desc_property, Literal(row["Component Descr"])))
            g.add((_course, _catalog_property, Literal(row["Catalog"])))
            g.add((_course, _offered_at, URIRef("https://dbpedia.org/resource/Concordia_University")))
            g.add((_course, _prerequisites_property, Literal(row["Pre Requisite Description"])))
            g.add((_course, _degree_type_property, Literal(row["Career"])))
            g.add((_course, _equivalent_courses_property, Literal(row["Equivalent Courses"])))

            #COURSE DESC
            desc = course_desc.loc[course_id]["Descr"]
            g.add((_course, VIVO.description, Literal(desc)))

        g.serialize(destination = self.rdf_dir / "courses.ttl")


        #UNIVERSITIES

        #fetch_all_universities()
            

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

    print("DOWNLOAD CONCORDIA CSV DATA")
    data_builder.download_data()
    data_builder.load_data()

    # # serialize dbpedia data
    # print("SERIALIZING CONCORDIA DBPEDIA ENTRY")
    # data_builder.serialize_data()
