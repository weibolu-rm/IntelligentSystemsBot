# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json
import pandas as pd


class ActionPersonInfo(Action):

    def name(self) -> Text:
        return "action_person_info"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f"If you are asking about {tracker.slots['person']}, Best Human Ever!!! ;-) ")

        return []


class ActionCourseDescription(Action):

    def name(self) -> Text:
        return "action_course_description"

    def run(self,
         dispatcher: CollectingDispatcher,
         tracker: Tracker,
         domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        course_string = tracker.slots['course']

        course_strings = course_string.split()
        course_strings[0] = course_strings[0].upper()
        print()
        print()
        print(course_strings)
        print()
        print()
        filter = text=f"FILTER(?subject = \"{course_strings[0]}\"  && ?num = \"{course_strings[1]}\" )"
        query = """SELECT DISTINCT ?subject ?num ?description WHERE {
                            ?course vivo:description ?description.
                            ?course rdf:type vivo:Course.
                            ?course exp:courseNumber ?num.
                            ?course exp:subject ?subject
                            
                            """ + filter + "}"
        print()
        print()
        print(query)
        print()
        print()
        
        response = requests.post('http://localhost:3030/idk/query',
        data={'query': query})

        json_data = json.loads(response.text)
        print("_________________________________")
        print(json_data)
        dispatcher.utter_message(text=f" {tracker.slots['course']} has description: insert description here {json_data['results']['bindings']} ")
        return []


class ActionCourseTopics(Action):

    def name(self) -> Text:
        return "action_course_topics"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['course']} has topics: insert description here ")

        return []


class ActionCoursesFromTopic(Action):

    def name(self) -> Text:
        return "action_courses_from_topic"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['topic']} action_courses_from_topic")

        return []


class ActionUniversityOfferingCoursesBasedOnTopic(Action):

    def name(self) -> Text:
        return "action_university_offering_courses_based_on_topic"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['topic']} action_university_offering_courses_based_on_topic")

        return []


class ActionUniversityAfterCertainYear(Action):

    def name(self) -> Text:
        return "action_university_after_certain_year"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['year']} action_university_after_certain_year")

        return []


class ActionCoursesHaveSubject(Action):

    def name(self) -> Text:
        return "action_courses_have_subject"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['topic']} action_courses_have_subject")

        return []


class ActionStudentHasStudentId(Action):

    def name(self) -> Text:
        return "action_student_has_student_id"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['studentId']} action_student_has_student_id")

        return []


class ActionStudentHasReceivedGrade(Action):

    def name(self) -> Text:
        return "action_student_has_received_grade"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['course']} action_student_has_received_grade")

        return []


class ActionLectureCoversTopic(Action):

    def name(self) -> Text:
        return "action_lecture_covers_topic"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['topic']} action_student_has_student_id")

        return []


class ActionCourseHasCourseNumber(Action):

    def name(self) -> Text:
        return "action_course_has_course_number"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['course_number']} actions_course_has_course_number")

        return []


class ActionTopicProvenance(Action):

    def name(self) -> Text:
        return "action_topic_provenance"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['topic']} action_topic_provenance")

        return []


class ActionLectureNumberOfLectureWithTitle(Action):

    def name(self) -> Text:
        return "action_lecture_number_of_lecture_with_title"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['topic']} action_lecture_number_of_lecture_with_title")

        return []


class ActionTitleOfCourseWithCourseNumber(Action):

    def name(self) -> Text:
        return "action_title_of_course_with_course_number"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=f" {tracker.slots['course_number']} action_title_of_course_with_course_number")

        return []
