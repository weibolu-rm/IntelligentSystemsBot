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
        self.vocabulary = {}
        self.knowledge_base = Graph()
        self._initialize_dirs()

    def _initialize_dirs(self):
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.rdf_dir, exist_ok=True)


    def download_concordia_course_data(self):
        print("Downloading Concordia courses data..")
        subprocess.call(["sh", "scripts/download-concordia-data.sh", str(self.data_dir)])


    def load_data(self):
        VIVO = Namespace('http://vivoweb.org/ontology/core#')
        g = self.knowledge_base
        self._define_vocabulary()

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

       
        for course_id, row in course_data.iterrows():
            #COURSE DATA
            # obviously don't use FOAF person but rather a custom class for course
            _course = URIRef(f"http://example.org/course/{course_id}")

            g.add((_course, RDF.type, VIVO.Course))
            g.add((_course, VIVO.Title, Literal(row["Long Title"])))
            g.add((_course, RDFS.label, Literal(row["Long Title"])))
            g.add((_course, FOAF.name, Literal(row["Long Title"])))
            g.add((_course, VIVO.Uid, Literal(course_id)))
            g.add((_course, VIVO.Credits, Literal(int(row["Class Units"]))))
            g.add((_course, VIVO.subjectAreaOf, Literal(row["Subject"])))
            g.add((_course, self.vocabulary["component_description_property"], Literal(row["Component Descr"])))
            g.add((_course, self.vocabulary["catalog_property"], Literal(row["Catalog"])))
            g.add((_course, self.vocabulary["offered_at"], URIRef("https://dbpedia.org/resource/Concordia_University")))
            if str(row["Pre Requisite Description"]) != "nan":
                g.add((_course, self.vocabulary["prerequisites_property"], Literal(row["Pre Requisite Description"])))
            g.add((_course, self.vocabulary["degree_type_property"], Literal(row["Career"])))
            if str(row["Equivalent Courses"]) != "nan":
                g.add((_course, self.vocabulary["equivalent_courses_property"], Literal(row["Equivalent Courses"])))

            #COURSE DESC
            desc = course_desc.loc[course_id]["Descr"]
            if str(desc) != "nan":
                g.add((_course, VIVO.description, Literal(desc)))

        g.serialize(destination = self.rdf_dir / "courses.ttl")

        #UNIVERSITIES
        g = g + self._fetch_all_universities()


    def serialize_knowledge_base(self):
        print("Serializing knowledge base..")
        self.knowledge_base.serialize(destination=self.rdf_dir / "knowledge_base.ttl")
        print(f"Knowledge base serialized to {(self.rdf_dir / 'knowledge_base.ttl').resolve()}")
            
    def _define_vocabulary(self):
        g = self.knowledge_base
        #custom properties
        #Custom property for Component Description
        _component_desc_property = URIRef(f"http://example.org/property/componentDesc")
        self.vocabulary["component_description_property"] = _component_desc_property
        g.add((_component_desc_property, RDF.type, RDF.Property))
        g.add((_component_desc_property, RDFS.label, Literal("component description property")))
        g.add((_component_desc_property, RDFS.comment, Literal("this property is used to describe whether a course is a lab, lecture or a studio session")))

        #Custom property for Catalogue
        _catalog_property = URIRef(f"http://example.org/property/catalog")
        self.vocabulary["catalog_property"] = _catalog_property
        g.add((_catalog_property, RDF.type, RDF.Property))
        g.add((_catalog_property, RDFS.label, Literal("Catalog property")))
        g.add((_catalog_property, RDFS.comment, Literal("this property is used to describe what the course number is for a course")))

        #Custom property for prerequisites
        _prerequisites_property = URIRef(f"http://example.org/property/prerequisites")
        self.vocabulary["prerequisites_property"] =_prerequisites_property 
        g.add((_prerequisites_property, RDF.type, RDF.Property))
        g.add((_prerequisites_property, RDFS.label, Literal("prerequisites property")))
        g.add((_prerequisites_property, RDFS.comment, Literal("this property is used to describe what the prerequisites are for a course")))

        #Custom property for prerequisites
        _degree_type_property = URIRef(f"http://example.org/property/degreeType")
        self.vocabulary["degree_type_property"] = _degree_type_property
        g.add((_degree_type_property, RDF.type, RDF.Property))
        g.add((_degree_type_property, RDFS.label, Literal("degree type property")))
        g.add((_degree_type_property, RDFS.comment, Literal("this property is used to describe what type of degree the course is offered for")))

        #Custom property for prerequisites
        _equivalent_courses_property = URIRef(f"http://example.org/property/equivalentCourses")
        self.vocabulary["equivalent_courses_property"] = _equivalent_courses_property 
        g.add((_equivalent_courses_property, RDF.type, RDF.Property))
        g.add((_equivalent_courses_property, RDFS.label, Literal("equivalent courses property")))
        g.add((_equivalent_courses_property, RDFS.comment, Literal("this property is used to describe what courses are equivalent to the subject course")))

        #Custom property for Offered at university
        _offered_at = URIRef(f"http://example.org/property/offeredAt")
        self.vocabulary["offered_at"] = _offered_at 
        g.add((_offered_at, RDF.type, RDF.Property))
        g.add((_offered_at, RDFS.label, Literal("Offered at property")))
        g.add((_offered_at, RDFS.comment, Literal("this property is used to indicate a relationship between a university and a course being offered at that university")))

       


    def _fetch_all_universities(self):
        """
        Update our local data on universities

        unfortunately this is limited by the fact that this is a public endpoint
        """
        DBO = Namespace("https://dbpedia.org/ontology/")
        g = Graph()
        print("Fetching universities..")
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

        # special case let's make sure Concordia is here
        print("Fetching data on Concordia University..")
        g.parse("http://dbpedia.org/resource/Concordia_University")

        unis = pd.DataFrame(qres, columns=["University", "Name"])
        # result.to_json(self.data_dir / "dbpedia_universities.json", indent=2, force_ascii=False)
        for _, row in unis.iterrows():
            g.add((row["University"], RDF.type, DBO.University))
            g.add((row["University"], FOAF.name, row["Name"]))
            g.add((row["University"], RDFS.label, row["Name"]))
            
        return g




if __name__ == "__main__":
    
    data_builder = DataBuilder()

    data_builder.download_concordia_course_data()
    data_builder.load_data()
    data_builder.serialize_knowledge_base()
