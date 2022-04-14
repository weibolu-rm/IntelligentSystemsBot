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
        dispatcher.utter_message(
            text=f" {tracker.slots['studentId']} action_student_has_student_id"
        )

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


class ActionTopicProvenance(Action):
    def name(self) -> Text:
        return "action_topic_provenance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=f" {tracker.slots['topic']} action_topic_provenance"
        )

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
        dispatcher.utter_message(
            text=f" {tracker.slots['topic']} action_lecture_number_of_lecture_with_title"
        )

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
        dispatcher.utter_message(
            text=f" {tracker.slots['course_number']} action_title_of_course_with_course_number"
        )

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
        dispatcher.utter_message(
            text=f" {tracker.slots['student']} action_student_is_competent_in"
        )

        return []
