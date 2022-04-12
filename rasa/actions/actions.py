# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from intelligent_system_bot.sparl import Sparql

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
     dispatcher.utter_message(text=f" {tracker.slots['course']} has description: insert description here ")

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