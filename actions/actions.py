import json
import asyncio
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

# from pygooglenews import GoogleNews
# from bs4 import BeautifulSoup

import requests
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps
from requests.models import Response

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")

# database
db = conn.rasa


def newsapi(country):
    """api call for getting top news hedline based on country """
    urlcoun = 'https://newsapi.org/v2/top-headlines?country=' + country + '&apiKey=0594f5154edd4117b416e3db461b2f0d'
    response = requests.get(urlcoun)
    data = response
    # gn = GoogleNews(lang = 'en', country = country)
    # print(gn)
    # business = gn.topic_headlines('business')
    # data = business

    return data

def sourcenews(source):
    """api call for getting hedlines from specific source"""
    urlsour = 'https://newsapi.org/v2/top-headlines?sources=' + source + '&apiKey=0594f5154edd4117b416e3db461b2f0d'
    response=requests.get(urlsour)
    data=response.json()
    return data

def topicnews(topic):
    """api call for getting news based on specific topic"""
    urlcoun = 'https://newsapi.org/v2/everything?q=' + topic + '&apiKey=01407b6466d24267914333bb846a2a6a'
    response=requests.get(urlcoun)
    data=response.json()
    return data

def dbEntry(data, type):
    modifyData = json.loads(dumps(data))
    if type == 'country':
        db.country.insert_many(modifyData)
    elif type == 'source':
        db.source.insert_many(modifyData)
    elif type == 'topic':
        db.topic.insert_many(modifyData)

class newsHeadlineus(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action"""
        return "action_news_headline_us"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of us"""
        data = newsapi("us")
        leng = len(data["articles"])
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
                    "title": data['articles'][i]['title'],
                    "image_url": data['articles'][i]['urlToImage'],
                    "subtitle": data['articles'][i]['description'],
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": data['articles'][i]['url'],
                            "title": "Read More"
                        },
                    ],
                    "meta": "US"
                })

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
            dbEntry(elems, 'country')
        return []


class NewsheadlineIndia(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action"""
        return "action_news_headline_india"

    async def run(self, dispatcher, tracker, domain):
        """displaying news headlines of india"""
        data = newsapi("in")
        leng = len(data['articles'])
        elems = []

        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
                    "title": data['articles'][i]['title'],
                    "image_url": data['articles'][i]['urlToImage'],
                    "subtitle": data['articles'][i]['description'],
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": data['articles'][i]['url'],
                            "title": "Read More"
                        },
                    ],
                    "meta": "india"
                })
            
            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
            dbEntry(elems, 'country')

        return []


class NewsheadlineGujarat(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action"""
        return "action_news_headline_gu"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of india"""
        newsurl = "https://www.gujaratsamachar.com/api/stories/5993f2985b03ab694185ad38?type=top-read-news"
        response = requests.get(newsurl)
        data = response.json()
        leng = len(data['data'])
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(text=data['data'][i]['heading'],image='https://static.gujaratsamachar.com/articles/articles_thumbs/thumbnails/'+data['data'][i]['articleImage'])
                output = '*Title* \n[%s](%s)  \n\n' % (data['data'][i]['heading'], data['data'][i]['articleUrl'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        else:
            for i in range(leng):
                elems.append({
                    "title": data['data'][i]['heading'],
                    "image_url": 'https://static.gujaratsamachar.com/articles/articles_thumbs/thumbnails/'+data['data'][i]['articleImage'],
                    "subtitle": "",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": data['data'][i]['articleUrl'],
                            "title": "Read More"
                        },
                    ],
                    "meta": "gujarati"
                })

            dbEntry(elems, 'country')

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
        return []


class NewsHeadlineAustralia(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action australia"""
        return "action_news_headline_au"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of """
        data = newsapi("au")
        leng = len(data["articles"])
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
                    "title": data['articles'][i]['title'],
                    "image_url": data['articles'][i]['urlToImage'],
                    "subtitle": data['articles'][i]['description'],
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": data['articles'][i]['url'],
                            "title": "Read More"
                        },
                    ],
                    "meta": "australia"
                })

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
            dbEntry(elems, 'country')
        return []


class NewsBBC(Action):
    """example of custom action"""   
    def name(self):
        """name of the custom action"""
        return "action_news_bbc"

    def run(self,dispatcher,tracker,domain):
        """disply news headlines from bbc news"""  
        data=sourcenews("bbc-news")
        leng=len(data["articles"])
        print(leng)
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
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
                })

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
        return []


class NewsABC(Action):
    """example of custom action"""   
    def name(self):
        """name of the custom action"""
        return "action_news_abc"

    def run(self,dispatcher,tracker,domain):
        """display news headlines from abc news"""  
        data=sourcenews("abc-news")
        leng=len(data["articles"])
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
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
                })

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
        return []


class NewsCNN(Action):
    """example of custom action"""   
    def name(self):
        """name of the custom action"""
        return "action_news_cnn"

    def run(self,dispatcher,tracker,domain):
        """display news headlines from cnn news"""  
        data=sourcenews("cnn")
        leng=len(data["articles"])
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
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
                })

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)
        return []


class SearchForm(FormAction):
    """Example of a custom form action"""   
    def name(self):
        """Unique identifier of the form"""  
        return "search_form"

    def required_slots(self,tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""  
        return ["topic"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "topic": [
                self.from_text(),
            ],
        }
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled""
            dispatcher.utter_message("here is related news")"""    
        return []


class NewsTopic(Action):
    def name(self):
        """name of the custom action"""
        return "action_news_search"

    def run(self,dispatcher,tracker,domain):
        """displaying news headlines based on specfic topic"""  
        topics=tracker.get_slot("topic")  
        data=topicnews(topics)
        leng=len(data["articles"])
        elems = []
        channel = tracker.get_latest_input_channel()
        if(channel == 'telegram'):
            for i in range(leng):
                # dispatcher.utter_message(link=data['articles'][i]['url'])
                # output = data['articles'][i]['title'] + "\n" + data['articles'][i]['description'] + "\n\n" + data['articles'][i]['url'] + "\n"
                # dispatcher.utter_message(output)
                output = '*Title* \n[%s](%s)  \n\n*Description* \n%s...\n' % (data['articles'][i]['title'], data['articles'][i]['url'], data['articles'][i]['description'])
                dispatcher.utter_custom_json({'text': output, 'parse_mode': 'markdown'})
        elif(channel == 'slack'):
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
        else:
            for i in range(leng):
                elems.append({
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
                })

            gt = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elems
                }
            }
            dispatcher.utter_message(attachment=gt)   
        return []