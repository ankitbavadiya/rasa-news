from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
def newsapi(country):
    """api call for getting top news hedline based on country """
    urlcoun = 'https://newsapi.org/v2/top-headlines?country=' + country + '&apiKey=0594f5154edd4117b416e3db461b2f0d'
    print(urlcoun)
    response = requests.get(urlcoun)
    data = response.json()
    return data


class newsHeadlineus(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action"""
        return "action_news_headline_us"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of us"""
        data = newsapi("us")
        leng = len(data)
        for i in range(leng):
            gt = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": data['articles'][i]['title'],
                                "image_url": data['articles'][i]['urlToImage'],
                                "subtitle": data['articles'][i]['description'],
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": data['articles'][i]['url'],
                                        "title": "Read More"
                                    },
                                ]
                            },
                        ]
                    }
                }
            }
            dispatcher.utter_custom_json(gt)
        return []


class NewsheadlineIndia(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action"""
        return "action_news_headline_india"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of india"""
        data = newsapi("india")
        leng = len(data)
        for i in range(leng):
            gt = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": data['articles'][i]['title'],
                                "image_url": data['articles'][i]['urlToImage'],
                                "subtitle": data['articles'][i]['description'],
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": data['articles'][i]['url'],
                                        "title": "Read More"
                                    },
                                ]
                            },
                        ]
                    }
                }
            }
            print(gt)
            dispatcher.utter_message(response=gt)
        return []


class NewsHeadlineAustralia(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action australia"""
        return "action_news_headline_au"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of """
        data = newsapi("au")
        leng = len(data)
        for i in range(leng):
            gt = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": data['articles'][i]['title'],
                                "image_url": data['articles'][i]['urlToImage'],
                                "subtitle": data['articles'][i]['description'],
                                "buttons": [
                                    {
                                        "type": "web_url",
                                        "url": data['articles'][i]['url'],
                                        "title": "Read More"
                                    },
                                ]
                            },
                        ]
                    }
                }
            }
            dispatcher.utter_custom_json(gt)
        return []
