import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# from pygooglenews import GoogleNews
# from bs4 import BeautifulSoup

import requests


def newsapi(country):
    """api call for getting top news hedline based on country """
    urlcoun = 'https://newsapi.org/v2/top-headlines?country=' + country + '&apiKey=0594f5154edd4117b416e3db461b2f0d'
    response = requests.get(urlcoun)
    data = response.json()
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


class NewsheadlineIndia(Action):
    """example of custom action"""

    def name(self):
        """name of the custom action"""
        return "action_news_headline_india"

    def run(self, dispatcher, tracker, domain):
        """displaying news headlines of india"""
        data = newsapi("in")
        leng = len(data['articles'])
        elems = []
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


class NewsBBC(Action):
    """example of custom action"""   
    def name(self):
        """name of the custom action"""
        return "action_news_bbc"

    def run(self,dispatcher,tracker,domain):
        """disply news headlines from bbc news"""  
        data=sourcenews("bbc-news")
        leng=len(data)
        print(leng)
        elems = []
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
        leng=len(data)
        elems = []
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
        leng=len(data)
        elems = []
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