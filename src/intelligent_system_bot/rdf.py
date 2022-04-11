import os
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import FOAF, RDF, RDFS
from pathlib import Path
import pandas as pd
import subprocess
from .base import Base

VIVO = Namespace("http://vivoweb.org/ontology/core#")
DBO = Namespace("http://dbpedia.org/ontology/")
EXP = Namespace("http://example.org/property/")
EXO = Namespace("http://example.org/ontology/")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class DataBuilder(Base):
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
        self.vocabulary = {}
        self.knowledge_graph = Graph()

    def download_concordia_course_data(self):
        print("Downloading Concordia courses data..")
        subprocess.call(
            ["sh", "scripts/download-concordia-data.sh", str(self.data_dir)]
        )

    def load_data(self):
        self._define_vocabulary()
        self._populate_students_and_grades()
        self._populate_lectures_and_topics()

        g = self.knowledge_graph

        # COURSES:
        # COURSE DATA
        course_data = pd.read_csv(
            self.data_dir / f"CU_SR_OPEN_DATA_CATALOG.csv",
            encoding="unicode_escape",
            index_col="Course ID",
        )
        # COURSE DESC
        course_desc = pd.read_csv(
            self.data_dir / f"CU_SR_OPEN_DATA_CATALOG_DESC.csv",
            encoding="unicode_escape",
            index_col="Course ID",
        )

        for course_id, row in course_data.iterrows():
            # COURSE DATA
            # obviously don't use FOAF person but rather a custom class for course
            _course = URIRef(f"http://example.org/course/{course_id}")

            g.add((_course, RDF.type, VIVO.Course))
            g.add((_course, VIVO.title, Literal(row["Long Title"])))
            g.add((_course, RDFS.label, Literal(row["Long Title"])))
            g.add((_course, FOAF.name, Literal(row["Long Title"])))
            g.add((_course, VIVO.credits, Literal(int(row["Class Units"]))))
            # g.add((_course, VIVO.subjectAreaOf, Literal(row["Subject"])))
            g.add((_course, EXP.subject, Literal(row["Subject"])))
            g.add(
                (
                    _course,
                    self.vocabulary["component_description_property"],
                    Literal(row["Component Descr"]),
                )
            )
            g.add(
                (
                    _course,
                    self.vocabulary["course_number_property"],
                    Literal(row["Catalog"]),
                )
            )
            g.add(
                (
                    _course,
                    self.vocabulary["offered_at"],
                    URIRef("http://dbpedia.org/resource/Concordia_University"),
                )
            )
            if str(row["Pre Requisite Description"]) != "nan":
                g.add(
                    (
                        _course,
                        self.vocabulary["prerequisites_property"],
                        Literal(row["Pre Requisite Description"]),
                    )
                )
            g.add(
                (
                    _course,
                    self.vocabulary["degree_type_property"],
                    Literal(row["Career"]),
                )
            )
            if str(row["Equivalent Courses"]) != "nan":
                g.add(
                    (
                        _course,
                        self.vocabulary["equivalent_courses_property"],
                        Literal(row["Equivalent Courses"]),
                    )
                )

            # COURSE DESC
            desc = course_desc.loc[course_id]["Descr"]
            if str(desc) != "nan":
                g.add((_course, VIVO.description, Literal(desc)))

        # UNIVERSITIES
        g = g + self._fetch_all_universities()

    def serialize_knowledge_graph(self):
        print("Serializing knowledge base..")
        self.knowledge_graph.serialize(destination=self.rdf_dir / "knowledge_base.ttl")
        print(
            f"Knowledge base serialized to {(self.rdf_dir / 'knowledge_base.ttl').resolve()}"
        )

    def _define_vocabulary(self):
        g = Graph()
        # custom properties
        # Custom property for Component Description
        ######
        # COURSES
        #####

        _component_desc_property = URIRef("http://example.org/property/componentDesc")
        self.vocabulary["component_description_property"] = _component_desc_property
        g.add((_component_desc_property, RDF.type, RDF.Property))
        g.add((_component_desc_property, RDFS.domain, VIVO.Course))
        g.add((_component_desc_property, RDFS.range, RDFS.Literal))
        g.add(
            (
                _component_desc_property,
                RDFS.label,
                Literal("component description property"),
            )
        )
        g.add(
            (
                _component_desc_property,
                RDFS.comment,
                Literal(
                    "this property is used to describe whether a course is a lab, lecture or a studio session"
                ),
            )
        )

        # Custom property for Course Numberue
        _course_number_property = URIRef("http://example.org/property/courseNumber")
        self.vocabulary["course_number_property"] = _course_number_property
        g.add((_course_number_property, RDF.type, RDF.Property))
        g.add((_course_number_property, RDFS.domain, VIVO.Course))
        g.add((_course_number_property, RDFS.range, RDFS.Literal))
        g.add((_course_number_property, RDFS.label, Literal("Course Number property")))
        g.add(
            (
                _course_number_property,
                RDFS.comment,
                Literal(
                    "this property is used to describe what the course number is for a course"
                ),
            )
        )

        # Custom property for prerequisites
        _prerequisites_property = URIRef("http://example.org/property/prerequisites")
        self.vocabulary["prerequisites_property"] = _prerequisites_property
        g.add((_prerequisites_property, RDF.type, RDF.Property))
        g.add((_prerequisites_property, RDFS.domain, VIVO.Course))
        g.add((_prerequisites_property, RDFS.range, RDFS.Literal))
        # this is a Description, so not necessarily Range of Course
        g.add((_prerequisites_property, RDFS.label, Literal("prerequisites property")))
        g.add(
            (
                _prerequisites_property,
                RDFS.comment,
                Literal(
                    "this property is used to describe what the prerequisites are for a course"
                ),
            )
        )

        # Custom property for prerequisites
        _degree_type_property = URIRef("http://example.org/property/degreeType")
        self.vocabulary["degree_type_property"] = _degree_type_property
        g.add((_degree_type_property, RDF.type, RDF.Property))
        g.add((_degree_type_property, RDFS.domain, VIVO.Course))
        g.add((_degree_type_property, RDFS.range, RDFS.Literal))
        g.add((_degree_type_property, RDFS.label, Literal("degree type property")))
        g.add(
            (
                _degree_type_property,
                RDFS.comment,
                Literal(
                    "this property is used to describe what type of degree the course is offered for"
                ),
            )
        )

        # Custom property for prerequisites
        _equivalent_courses_property = URIRef(
            "http://example.org/property/equivalentCourses"
        )
        self.vocabulary["equivalent_courses_property"] = _equivalent_courses_property
        g.add((_equivalent_courses_property, RDF.type, RDF.Property))
        g.add((_equivalent_courses_property, RDFS.domain, VIVO.Course))
        # The data is actually a description, not necessarily a course
        g.add((_equivalent_courses_property, RDFS.range, RDFS.Literal))
        g.add(
            (
                _equivalent_courses_property,
                RDFS.label,
                Literal("equivalent courses property"),
            )
        )
        g.add(
            (
                _equivalent_courses_property,
                RDFS.comment,
                Literal(
                    "this property is used to describe what courses are equivalent to the subject course"
                ),
            )
        )

        # Custom property for Offered at university
        _offered_at = URIRef("http://example.org/property/offeredAt")
        self.vocabulary["offered_at"] = _offered_at
        g.add((_offered_at, RDF.type, RDF.Property))
        g.add((_offered_at, RDFS.domain, VIVO.Course))
        g.add((_offered_at, RDFS.range, DBO.University))
        g.add((_offered_at, RDFS.label, Literal("Offered at property")))
        g.add(
            (
                _offered_at,
                RDFS.comment,
                Literal(
                    "this property is used to indicate a relationship between a university and a course being offered at that university"
                ),
            )
        )

        ######
        # STUDENTS
        #####
        _student_id = URIRef("http://example.org/property/studentId")
        self.vocabulary["student_id"] = _student_id
        g.add((_student_id, RDF.type, RDF.Property))
        g.add((_student_id, RDFS.domain, VIVO.Student))
        g.add((_student_id, RDFS.range, RDFS.Literal))
        g.add((_student_id, RDFS.label, Literal("Student Identification Number")))
        g.add(
            (
                _student_id,
                RDFS.comment,
                Literal("Unique identification number associated to a student"),
            )
        )

        _received_grade = URIRef("http://example.org/property/receivedGrade")
        self.vocabulary["received_grade"] = _received_grade
        g.add((_received_grade, RDF.type, RDF.Property))
        g.add((_received_grade, RDFS.domain, VIVO.Student))
        g.add((_received_grade, RDFS.range, EXO.Grade))
        g.add((_received_grade, RDFS.label, Literal("Received Grade Property")))
        g.add(
            (
                _received_grade,
                RDFS.comment,
                Literal("Grade received by a Student in a given Course"),
            )
        )

        _retaken_course = URIRef("http://example.org/property/retakenCourse")
        self.vocabulary["retaken_course"] = _retaken_course
        g.add((_received_grade, RDF.type, RDF.Property))
        g.add((_received_grade, RDFS.domain, VIVO.Student))
        g.add((_received_grade, RDFS.range, VIVO.Course))
        g.add((_received_grade, RDFS.label, Literal("Re-taken Course")))
        g.add(
            (
                _received_grade,
                RDFS.comment,
                Literal(
                    "Student has re-taken a course, perhaps to get a passing grade."
                ),
            )
        )

        _competent_in = URIRef("http://example.org/property/competentIn")
        self.vocabulary["competent_in"] = _competent_in
        g.add((_competent_in, RDF.type, RDF.Property))
        g.add((_competent_in, RDFS.domain, VIVO.Student))
        g.add((_competent_in, RDFS.range, EXO.Topic))
        g.add((_competent_in, RDFS.label, Literal("Competent in Property")))
        g.add(
            (
                _competent_in,
                RDFS.comment,
                Literal("Property describing competency in a given topic."),
            )
        )

        ####
        # GRADE
        ####
        g.add((EXO.Grade, RDF.type, RDFS.Class))

        _from_course = URIRef("http://example.org/property/fromCourse")
        self.vocabulary["from_course"] = _from_course
        g.add((_from_course, RDF.type, RDF.Property))
        g.add((_from_course, RDFS.domain, EXO.Grade))
        g.add((_from_course, RDFS.range, VIVO.Course))
        g.add((_from_course, RDFS.label, Literal("Grade from course property")))
        g.add(
            (
                _from_course,
                RDFS.comment,
                Literal("Property describing grade received from a given course."),
            )
        )

        ####
        # TOPIC
        ####
        g.add((EXO.Topic, RDF.type, RDFS.Class))
        g.add((EXO.Topic, RDFS.subClassOf, VIVO.Concept))
        _provenance = URIRef("http://example.org/property/provenance")
        self.vocabulary["provenance"] = _provenance
        g.add((_provenance, RDF.type, RDF.Property))
        g.add((_provenance, RDFS.domain, EXO.Topic))
        # NO RANGE HERE

        ####
        # SUBJECT
        ####
        g.add((EXO.Subject, RDF.type, RDF.Property))
        _subject = URIRef("http://example.org/property/subject")
        g.add((_subject, RDFS.domain, VIVO.Course))
        g.add((_subject, RDFS.range, RDFS.Literal))
        g.add((_subject, RDFS.label, Literal("Subject")))
        g.add((_subject, RDFS.comment, Literal("Describes the subject of a course")))

        ####
        # LECTURE
        ####
        g.add((EXO.Lecture, RDF.type, VIVO.Event))
        _lecture_number = URIRef("http://example.org/property/lectureNumber")
        self.vocabulary["lecture_number"] = _lecture_number
        g.add((_lecture_number, RDF.type, RDF.Property))
        g.add((_lecture_number, RDFS.domain, EXO.Lecture))
        g.add((_lecture_number, RDFS.range, RDFS.Literal))
        g.add((_lecture_number, RDFS.label, Literal("Lecture Number")))
        g.add(
            (
                _lecture_number,
                RDFS.comment,
                Literal("The number of the lecture in sequence with the course."),
            )
        )

        ####
        # CONTENT
        ####
        _content = URIRef("http://example.org/property/content")
        self.vocabulary["content"] = _content
        g.add((_content, RDF.type, RDF.Property))
        g.add((_content, RDFS.domain, EXO.Lecture))
        g.add((_content, RDFS.label, Literal("Content")))
        g.add((_content, RDFS.comment, Literal("Files or materials for given lecture")))

        _video = URIRef("http://example.org/property/video")
        self.vocabulary["video"] = _video
        g.add((_video, RDFS.subPropertyOf, EXP.content))

        _image = URIRef("http://example.org/property/image")
        self.vocabulary["image"] = _image
        g.add((_image, RDFS.subPropertyOf, EXP.content))

        _document = URIRef("http://example.org/property/document")
        self.vocabulary["document"] = _document
        g.add((_document, RDFS.subPropertyOf, EXP.content))

        _pdf = URIRef("http://example.org/property/pdf")
        self.vocabulary["pdf"] = _pdf
        g.add((_document, RDFS.subPropertyOf, EXP.content))

        # Serialize definitions in a separate turtle file
        print("Serializing RDFS definitions")
        g.serialize(destination=self.rdf_dir / "RDFS.ttl")

        # add it to our knowledge base
        self.knowledge_graph = self.knowledge_graph + g

    def _populate_students_and_grades(self):
        """
        Temporary manual data
        """
        g = self.knowledge_graph

        elijah = URIRef("http://example.org/student/40078229")
        robert = URIRef(f"http://example.org/student/40058095")
        amine = URIRef(f"http://example.org/student/40046046")
        logan = URIRef(f"http://example.org/student/40089767")

        g.add((elijah, RDF.type, VIVO.Student))
        g.add((elijah, VCARD.givenName, Literal("Elijah")))
        g.add((elijah, VCARD.familyName, Literal("Mon")))
        g.add((elijah, VCARD.email, Literal("elijah@email.com")))
        g.add((elijah, self.vocabulary["student_id"], Literal(40078229)))

        g.add((robert, RDF.type, VIVO.Student))
        g.add((robert, VCARD.givenName, Literal("Robert")))
        g.add((robert, VCARD.familyName, Literal("Michad")))
        g.add((robert, VCARD.email, Literal("robert@email.com")))
        g.add((robert, self.vocabulary["student_id"], Literal(40058095)))

        g.add((amine, RDF.type, VIVO.Student))
        g.add((amine, VCARD.givenName, Literal("Mohamed Amine")))
        g.add((amine, VCARD.familyName, Literal("Kihal")))
        g.add((amine, VCARD.email, Literal("momo@email.com")))
        g.add((amine, self.vocabulary["student_id"], Literal(40046046)))

        g.add((logan, RDF.type, VIVO.Student))
        g.add((logan, VCARD.givenName, Literal("Logan")))
        g.add((logan, VCARD.familyName, Literal("Paul")))
        g.add((logan, VCARD.email, Literal("epaul@email.com")))
        g.add((logan, self.vocabulary["student_id"], Literal(40089767)))

        grade01 = URIRef("http://example.org/grade/40078229_F_Intelligent_Systems")
        grade02 = URIRef("http://example.org/grade/40078229_A_Intelligent_Systems")
        course01 = URIRef("http://example.org/course/5484")

        g.add((grade01, RDF.type, EXO.Grade))
        g.add((grade01, RDF.value, Literal("F")))
        g.add((grade01, self.vocabulary["from_course"], course01))

        g.add((grade02, RDF.type, EXO.Grade))
        g.add((grade02, RDF.value, Literal("A")))
        g.add((grade02, self.vocabulary["from_course"], course01))

        g.add((elijah, self.vocabulary["received_grade"], grade01))
        g.add((elijah, self.vocabulary["received_grade"], grade02))

        g.add((elijah, self.vocabulary["retaken_course"], course01))

    def _populate_lectures_and_topics(self):
        """
        Temporary manual data
            TODO: use csv or somethign
        """
        course01 = URIRef("http://example.org/course/049701")
        g = self.knowledge_graph

        lec01 = URIRef("http://example.org/lecture/Bagging_And_Boosting")
        g.add((lec01, RDF.type, EXO.Lecture))
        g.add((lec01, VIVO.title, Literal("Bagging and boosting")))
        g.add((lec01, self.vocabulary["lecture_number"], Literal(1)))
        g.add((lec01, self.vocabulary["provenance"], course01))

        lec02 = URIRef("http://example.org/lecture/Linear_Models")
        g.add((lec02, RDF.type, EXO.Lecture))
        g.add((lec02, VIVO.title, Literal("Linear Models")))
        g.add((lec02, self.vocabulary["lecture_number"], Literal(2)))
        g.add((lec02, self.vocabulary["provenance"], course01))

        lec03 = URIRef("http://example.org/lecture/Clustering_and_Mixture_Models")
        g.add((lec03, RDF.type, EXO.Lecture))
        g.add((lec03, VIVO.title, Literal("Clustering and Mixture Models")))
        g.add((lec03, self.vocabulary["lecture_number"], Literal(3)))
        g.add((lec03, self.vocabulary["provenance"], course01))

        lec04 = URIRef("http://example.org/lecture/Kernel_Density")
        g.add((lec04, RDF.type, EXO.Lecture))
        g.add((lec04, VIVO.title, Literal("Kernel Density")))
        g.add((lec04, self.vocabulary["lecture_number"], Literal(4)))
        g.add((lec04, self.vocabulary["provenance"], course01))

        lec05 = URIRef("http://example.org/lecture/Support_Vector_Machines")
        g.add((lec05, RDF.type, EXO.Lecture))
        g.add((lec05, VIVO.title, Literal("Support Vector Machines")))
        g.add((lec05, self.vocabulary["lecture_number"], Literal(5)))
        g.add((lec05, self.vocabulary["provenance"], course01))

        wiki_page = URIRef("http://dbpedia.org/resource/Support-vector_machine")
        topic = URIRef("http://example.org/topic/Support_Vector_Machines")
        g.add((topic, RDF.type, EXO.Topic))
        g.add((topic, self.vocabulary["provenance"], lec05))
        g.add((topic, RDFS.seeAlso, wiki_page))

    def _fetch_all_universities(self):
        """
        Update our local data on universities

        unfortunately this is limited by the fact that this is a public endpoint
        """
        g = self.knowledge_graph

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
        # print("Fetching data on Concordia University..")
        # g.parse("http://dbpedia.org/resource/Concordia_University")

        unis = pd.DataFrame(qres, columns=["University", "Name"])
        # making sure Concordia is here
        unis.loc[len(unis)] = [
            URIRef("http://dbpedia.org/resource/Concordia_University"),
            Literal("Concordia University"),
        ]
        # result.to_json(self.data_dir / "dbpedia_universities.json", indent=2, force_ascii=False)
        for _, row in unis.iterrows():
            g.add((row["University"], RDF.type, DBO.University))
            g.add((row["University"], FOAF.name, row["Name"]))
            g.add((row["University"], RDFS.label, row["Name"]))

        return g

    def run(self):
        self.download_concordia_course_data()
        self.load_data()
        self.serialize_knowledge_graph()


def main():
    data_builder = DataBuilder()
    data_builder.run()


if __name__ == "__main__":
    main()
