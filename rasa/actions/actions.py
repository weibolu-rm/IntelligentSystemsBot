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
        
        response = requests.post('http://localhost:3030/idk/query',
        data={'query': r"""PREFIX vcard: <http://www.w3.org/2006/vcard/ns#>
                        PREFIX vivo: <http://vivoweb.org/ontology/core#>
                        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                        SELECT ?name WHERE {
                        ?x vcard:givenName ?name.
                        ?x rdf:type vivo:Student .
                        } LIMIT 10"""})

        json_data = json.loads(response.text)
        dispatcher.utter_message(text=f" {tracker.slots['course']} has description: insert description here {json_data['results']['bindings']} ")
        return []


class ActionCourseTopic(Action):

    def name(self) -> Text:
     return "action_course_topic"

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
     dispatcher.utter_message(text=f" {tracker.slots['topic']} is covered in courses: ")

     return []