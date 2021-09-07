import json
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
    # urlcoun = 'https://newsapi.org/v2/top-headlines?country=' + country + '&apiKey=0594f5154edd4117b416e3db461b2f0d'
    # response = requests.get(urlcoun)
    # data = response.json()
    data = {"status":"ok","totalResults":38,"articles":[{"source":{"id":"news","name":"NDTV News"},"author":"Nithya P Nair","title":"Realme Dizo Watch 2, Dizo Watch Pro India Launch Set for September 15 - Gadgets 360","description":"Realme sub-brand Dizo will expand its smartwatch portfolio later this month with two new wearables — Realme Dizo Watch 2 and Realme Dizo Watch Pro. Realme Dizo Watch 2 will have a 1.69-inch display, while the Dizo Watch Pro will offer heart rate and blood oxy…","url":"https://gadgets.ndtv.com/wearables/news/realme-dizo-watch-2-pro-launch-price-in-india-specifications-features-september-15-2532957","urlToImage":"https://i.gadgets360cdn.com/large/Realme_Dizo_Watch_2_1631020210060.jpeg","publishedAt":"2021-09-07T13:49:24Z","content":"Realme Dizo Watch 2 and Realme Dizo Watch Pro are set to launch in India on September 15 at 12pm IST at a virtual event. The Realme sub-brand launched the vanilla Dizo Watch in the country in August,… [+1995 chars]"},{"source":{"id":"news","name":"WION"},"author":"WION Web Team","title":"Australian musk duck recorded saying `you bloody fool` - WION","description":"Several birds are famous for being able to imitate human speech. Parrots come to mind first. But there are other birds who can give parrots a stiff competition. Australian musk ducks are one of them. Now a recording of such a duck has resurfaced. In this reco…","url":"https://www.wionews.com/world/australian-musk-duck-recorded-saying-you-bloody-fool-411340","urlToImage":"https://cdn.wionews.com/sites/default/files/styles/story_page/public/2020/06/15/144984-untitled-design-2.jpg, kept at 90 degrees fahrenheit, at Hudson Valley Duck Farm December 15, 2017 in Ferndale, New York\" typeof=\"foaf:Image\" />","publishedAt":"2021-09-07T10:17:31Z","content":"Several birds are famous for being able to imitate human speech. Parrots come to mind first. But there are other birds who can give parrots a stiff competition. Australian musk ducks are one of them.… [+1417 chars]"}]}
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
        data = newsapi("in")
        leng = len(data["articles"])
        # print(leng)
        for i in range(leng):
            gt = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": data['articles'][i]['title']
                        },
                    },
                    {
                        "type": "image",
                        "title": {
                            "type": "plain_text",
                            "text": "image1"
                        },
                        "image_url": data['articles'][i]['urlToImage'],
                        "alt_text": "image1"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": data['articles'][i]['description']
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": " "
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Read more"
                            },
                            "value": "click_me_123",
                            "url": data['articles'][i]['url'],
                            "action_id": "button-action"
                        }
                    }
                ]
            }
            dispatcher.utter_message(json_message=gt)
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
