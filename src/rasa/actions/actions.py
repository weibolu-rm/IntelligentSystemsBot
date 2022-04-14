# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import rdflib
import re


import os
import sys

# little hack cause I can't be bothered
THIS_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_PATH[: -len("rasa/actions")])
from intelligent_system_bot.sparql import Sparql

print("INITIALIZING SPARQL ENDPOINT QUERY SERVICE")
sparql = Sparql()
sparql.init()
print("done")


class ActionPersonInfo(Action):
    def name(self) -> Text:
        return "action_person_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) "
        )

        return []


class ActionCourseDescription(Action):
    def name(self) -> Text:
        return "action_course_description"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        test = tracker.slots["course"].split()
        print(test)
        if len(test) != 2:
            print("umhh hello?")

        qres = sparql.query(
            f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX vivo: <http://vivoweb.org/ontology/core#>
        PREFIX exp: <http://example.org/property/>

        SELECT DISTINCT ?subject ?num ?description 
        WHERE {{
            ?course vivo:description ?description.
            ?course rdf:type vivo:Course.
            ?course exp:courseNumber ?num.
            ?course exp:subject ?subject
            
            FILTER(?subject = "{test[0].upper()}"  && ?num = "{test[1]}" )
        }}


        """
        )
        msg = f" {tracker.slots['course']} has description: \n\n"

        # TODO: should only be one
        if len(qres) > 0:
            for row in qres:
                msg += row.description
        else:
            msg = f"No description found for {tracker.slots['course']}"

            # json_data = json.loads(response.text)
        dispatcher.utter_message(text=msg)
        return []


class ActionCourseTopics(Action):
    def name(self) -> Text:
        return "action_course_topics"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['course']} has topics: insert description here "
        )

        return []


class ActionCoursesFromTopic(Action):
    def name(self) -> Text:
        return "action_courses_from_topic"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['topic']} action_courses_from_topic"
        )

        return []


class ActionUniversityOfferingCoursesBasedOnTopic(Action):
    def name(self) -> Text:
        return "action_university_offering_courses_based_on_topic"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['topic']} action_university_offering_courses_based_on_topic"
        )

        return []


class ActionUniversityAfterCertainYear(Action):
    def name(self) -> Text:
        return "action_university_after_certain_year"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['year']} action_university_after_certain_year"
        )

        return []


class ActionCoursesHaveSubject(Action):
    def name(self) -> Text:
        return "action_courses_have_subject"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['topic']} action_courses_have_subject"
        )

        return []


class ActionStudentHasStudentId(Action):
    def name(self) -> Text:
        return "action_student_has_student_id"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        id = int(tracker.slots['course'])
        qres = sparql.query(
            f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX vivo: <http://vivoweb.org/ontology/core#>
        PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
        PREFIX exp: <http://example.org/property/>

        SELECT ?student ?given_name ?last_name ?student_id
        WHERE {{
            ?student rdf:type vivo:Student.
            ?student vcard:givenName ?given_name.
            ?student vcard:familyName ?last_name.
            ?student exp:studentId ?student_id.
            FILTER (?student_id = {id})
        }}
        """
        )
        msg = f" Student ID: {tracker.slots['course']} belongs to: \n\n"
        # TODO: should only be one
        if len(qres) > 0:
            for row in qres:
                msg += row.given_name + " " + row.last_name
        else:
            msg = f"No student with ID: {tracker.slots['course']} found"

            # json_data = json.loads(response.text)
        dispatcher.utter_message(text=msg)
        return []


class ActionStudentHasReceivedGrade(Action):
    def name(self) -> Text:
        return "action_student_has_received_grade"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['course']} action_student_has_received_grade"
        )

        return []


class ActionLectureCoversTopic(Action):
    def name(self) -> Text:
        return "action_lecture_covers_topic"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['topic']} action_student_has_student_id"
        )

        return []


class ActionCourseHasCourseNumber(Action):
    def name(self) -> Text:
        return "action_course_has_course_number"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['course_number']} actions_course_has_course_number"
        )

        return []

#TODO ___________ requires title
class ActionTopicProvenance(Action):
    def name(self) -> Text:
        return "action_topic_provenance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        topic = tracker.slots['topic']
        print(tracker.slots)
        qres = sparql.query(
            f"""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX exp: <http://example.org/property/>

                SELECT ?x ?name
                WHERE{{
                    ?topic exp:provenance ?x.
                    ?x vivo:title ?name.
                FILTER (?topic = <http://example.org/topic/Support_Vector_Machines>)
                }}


            """
        )
        msg = f"The topic ({topic}) is covered by lecture number: "

        # TODO: should only be one
        if len(qres) > 0:
            for row in qres:
                msg += row.num + " of lectue: " + row.lecture + "\n"

        else:
            msg = f"The topic ({topic}) is not covered in any lectures: "

            # json_data = json.loads(response.text)
        dispatcher.utter_message(text=msg)
        return []


class ActionLectureNumberOfLectureWithTitle(Action):
    def name(self) -> Text:
        return "action_lecture_number_of_lecture_with_title"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        topic = tracker.slots['topic']
        print(tracker.slots)
        qres = sparql.query(
            f"""
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX exp: <http://example.org/property/>

                SELECT DISTINCT ?lecture ?num
                WHERE {{
                    ?lecture rdf:type <http://example.org/ontology/Lecture>.
                    ?lecture vivo:title ?name.
                    ?lecture exp:lectureNumber ?num
                    FILTER (?name = "{topic}")
                }}

            """
        )
        msg = f"The topic ({topic}) is covered by lecture number: "

        # TODO: should only be one
        if len(qres) > 0:
            for row in qres:
                msg += row.num + " of lectue: " + row.lecture + "\n"

        else:
            msg = f"The topic ({topic}) is not covered in any lectures: "

            # json_data = json.loads(response.text)
        dispatcher.utter_message(text=msg)
        return []


class ActionTitleOfCourseWithCourseNumber(Action):
    def name(self) -> Text:
        return "action_title_of_course_with_course_number"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        print(tracker.slots)
        course_number = tracker.slots['course_number']
        qres = sparql.query(
            f"""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>
                PREFIX exp: <http://example.org/property/>

                SELECT DISTINCT ?title
                WHERE {{
                    ?course rdf:type vivo:Course.
                    ?course vivo:title ?title.
                    ?course exp:courseNumber ?num.
                FILTER (?num = "{course_number}")
                }}
            """
        )
        msg = f" The following courses have the course number ({course_number}): \n\n"

        # TODO: should only be one
        if len(qres) > 0:
            for row in qres:
                msg += row.title + "\n"
        else:
            msg = f"There are no courses with course number ({course_number}): "

            # json_data = json.loads(response.text)
        dispatcher.utter_message(text=msg)
        return []


class ActionStudentIsCompetentIn(Action):
    def name(self) -> Text:
        return "action_student_is_competent_in"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        
        print(tracker.slots['student'])
 
        qres = sparql.query(
            f"""
                PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX exp: <http://example.org/property/>
                PREFIX exo: <http://example.org/ontology/>
                PREFIX vivo: <http://vivoweb.org/ontology/core#>

                SELECT DISTINCT ?topic
                WHERE{{
                    ?student exp:competentIn ?topic.
                    ?student vcard:givenName ?name.
                    
                FILTER (?name = "{tracker.slots['student']}") }}
            """
        )
        msg = f" student is competent in: \n\n"

        # TODO: should only be one
        if len(qres) > 0:
            for row in qres:
                msg += row.topic + "\n"
        else:
            msg = f"this {tracker.slots['student']} is bung at everything"

            # json_data = json.loads(response.text)
        dispatcher.utter_message(text=msg)
        return []
