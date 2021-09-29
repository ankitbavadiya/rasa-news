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
    # response = requests.get(urlcoun)
    response = {'status': 'ok', 'totalResults': 38, 'articles': [{'source': {'id': None, 'name': 'Business Standard'}, 'author': 'BS Web Team', 'title': 'Coronavirus live updates: India logs 18,870 new cases and 378 deaths - Business Standard', 'description': 'Covid-19 live updates: Pfizer submits research on the effectiveness of its vaccine in children; Japan to lift a state of emergency at the end of September.', 'url': 'https://www.business-standard.com/article/current-affairs/covid-19-live-updates-who-holds-covaxin-clearance-sri-lanka-to-end-curfew-121092900081_1.html', 'urlToImage': 'https://bsmedia.business-standard.com/_media/bs/img/article/2021-09/29/full/1632876440-8143.jpg', 'publishedAt': '2021-09-29T04:25:09Z', 'content': 'BS Web Team\xa0| New Delhi\r\n\xa0\r\nLast Updated at September 29, 2021 09:55 IST'}, {'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'ANI', 'title': 'Russia to launch 5 spacecraft to International Space Station in 2022 - Times of India', 'description': 'Rest of World News: Russia plans to launch two Soyuz manned spacecraft and three Progress cargo spacecraft to the International Space Station (ISS) next year, according t', 'url': 'https://timesofindia.indiatimes.com/world/rest-of-world/russia-to-launch-5-spacecraft-to-international-space-station-in-2022/articleshow/86604076.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-86604162,width-1070,height-580,imgsize-85946,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 'publishedAt': '2021-09-29T04:25:00Z', 'content': 'Russia to launch 5 spacecraft to International Space Station in 2022'}, {'source': {'id': None, 'name': 'Hindustan Times'}, 'author': 'hindustantimes.com', 'title': '60 students of Bengaluru boarding test positive for Covid-19, school shut - Hindustan Times', 'description': 'Among them, one student who had high fever is undergoing treatment at Lady Curzon and Bowring Hospital, while another one is in home quarantine. The rest are asymptomatic. | Bengaluru News', 'url': 'https://www.hindustantimes.com/cities/bengaluru-news/60-students-of-bengaluru-residential-school-test-positive-for-covid-101632888163066.html', 'urlToImage': 'https://images.hindustantimes.com/img/2021/09/29/1600x900/students-exams-schools-closed-PTI_1630454902279_1632888355841.jpg', 'publishedAt': '2021-09-29T04:07:17Z', 'content': 'At least 60 students from a residential school at Electronic City in Bengaluru have tested positive for the coronavirus disease. Among them, one student who had high fever is undergoing treatment at … [+2510 chars]'}, {'source': {'id': None, 'name': 'NDTV News'}, 'author': None, 'title': '"His (Navjot Sidhu) Real Character": Captain\'s \'1996 England Tour\' Dig - NDTV', 'description': 'Amarinder Singh, after delivering a "told-you-so" barb at the Gandhis on rival Navjot Singh Sidhu\'s shock resignation as Punjab Congress Chief, stacked up more digs at the cricketer-turned-politician.', 'url': 'https://www.ndtv.com/india-news/punjab-congress-crisis-amarinder-singh-on-navjot-singh-sidhu-known-this-boy-since-his-childhood-a-loner-2557361', 'urlToImage': 'https://i.ndtvimg.com/i/2017-01/amarinder-singh-navjot-sidhu-afp_650x400_51485507811.jpg', 'publishedAt': '2021-09-29T03:59:10Z', 'content': 'Amarinder Singh stacked up more digs at Navjot Singh Sidhu.\r\nChandigarh: Amarinder Singh, after delivering a "told-you-so" barb at the Gandhis on rival Navjot Singh Sidhu\'s shock resignation as Punja… [+2370 chars]'}, {'source': {'id': None, 'name': 'NDTV News'}, 'author': None, 'title': 'US Denies Flight With Over 100 Americans From Kabul From Landing: Report - NDTV', 'description': 'The Department of Homeland Security on Tuesday denied U.S. landing rights for a charter plane carrying more than 100 Americans and U.S. green card holders evacuated from Afghanistan, organizers of the flight said.', 'url': 'https://www.ndtv.com/world-news/afghanistan-taliban-takeover-us-bars-flight-from-landing-with-over-100-americans-from-kabul-report-2557359', 'urlToImage': 'https://c.ndtvimg.com/2021-08/67133km8_afghanistan-evacuation-reuters_625x300_28_August_21.jpg', 'publishedAt': '2021-09-29T03:57:20Z', 'content': 'US denied landing for charter plane carrying more than 100 Americans, report said. (File)\r\nWashington: The Department of Homeland Security on Tuesday denied U.S. landing rights for a charter plane ca… [+2508 chars]'}, {'source': {'id': None, 'name': 'Hindustan Times'}, 'author': 'HT Entertainment Desk', 'title': "Shah Rukh Khan reacts to sons Aryan Khan-AbRam bonding over games: 'Brothers who play together...' - Hindustan Times", 'description': "Shah Rukh Khan has reacted to a picture of his sons, Aryan Khan and AbRam Khan, playing games together. Check out his comment on wife Gauri Khan's post here. | Bollywood", 'url': 'https://www.hindustantimes.com/entertainment/bollywood/shah-rukh-khan-reacts-to-sons-aryan-khan-abram-bonding-over-games-brothers-who-play-together-101632885184602.html', 'urlToImage': 'https://images.hindustantimes.com/img/2021/09/29/1600x900/shah_rukh_khan_1632885798473_1632885804756.jpg', 'publishedAt': '2021-09-29T03:36:55Z', 'content': "Actor Shah Rukh Khan has reacted to a picture of his sons Aryan Khan and AbRam Khan bonding over games. Taking to Instagram recently, Shah Rukh's wife and film producer-interior designer Gauri Khan g… [+2099 chars]"}, {'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'K Shriniwas Rao', 'title': "Cricket's bidding wars to begin: BCCI sounds bugle ahead of ICC, announces IPL media-rights tender - Times of India", 'description': "Cricket News: The BCCI has just sounded the bugle for what is going to be cricket industry's biggest war-cry over the next six months - sale of Indian Premier Leagu", 'url': 'https://timesofindia.indiatimes.com/sports/cricket/ipl/top-stories/crickets-bidding-wars-to-begin-bcci-sounds-bugle-ahead-of-icc-announces-ipl-media-rights-tender/articleshow/86602930.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-86602865,width-1070,height-580,imgsize-66194,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 'publishedAt': '2021-09-29T03:29:00Z', 'content': "Cricket's bidding wars to begin: BCCI sounds bugle ahead of ICC, announces IPL media-rights tender"}, {'source': {'id': None, 'name': 'Livemint'}, 'author': 'Livemint', 'title': 'NEET PG 2021 result declared; NBEMS to activate direct link shortly - Mint', 'description': 'The National Eligibility cum Entrance Test (NEET) - PG was held at 679 centres in 270 cities on September 11.Candidates can check the result by visiting the following websites: nbe.edu.in or natboard.edu.in', 'url': 'https://www.livemint.com/news/india/neet-pg-2021-result-declared-nbems-to-activate-direct-link-shortly-11632884211303.html', 'urlToImage': 'https://images.livemint.com/img/2021/09/29/600x338/20210912-DLI-SKH-MN-NEET-Exam-9-0_1632885172122_1632885195264.jpg', 'publishedAt': '2021-09-29T03:15:27Z', 'content': 'NEET PG 2021 examination result has been declared on Wednesday. National Board of Examinations in Medical Sciences, NBEMS said candidates can check the result by visiting the following websites: nbe.… [+1304 chars]'}, {'source': {'id': None, 'name': 'Gadgets Now'}, 'author': 'Gadgets Now Bureau', 'title': 'Amazon announces new speaker, fitness band, home robot and more: Key specs and what may come to India and what - Gadgets Now', 'description': "Amazon held its 2021 edition of its annual hardware event. And like previous years, the company announced a slew of devices. The list includes new editions to the Echo Show family, flying security cameras, home robots and more. Here's a list of all that Amazo…", 'url': 'https://www.gadgetsnow.com/slideshows/amazon-announces-new-speaker-fitness-band-home-robot-and-more-key-specs-and-what-may-come-to-india-and-what-not/photolist/86602041.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-86602077,width-800,resizemode-4,imgsize-34330/share.jpg', 'publishedAt': '2021-09-29T03:07:00Z', 'content': 'Amazon has announced its first home robot, Astro. The robot serves three primary functions: guard home security, monitor loved ones and offer portable Alexa experience. Like Echo devices, Astro has a… [+289 chars]'}, {'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'TIMESOFINDIA.COM', 'title': 'Akshay Kumar asks the audience to help the entertainment industry revive by coming back to theatres, hope - Times of India', 'description': 'Akshay Kumar, who has about five films lined up for theatrical release, asks the audience to come out and watch the', 'url': 'https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news/akshay-kumar-asks-the-audience-to-help-the-entertainment-industry-revive-by-coming-back-to-theatres-hopes-the-worst-is-over/articleshow/86601660.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-86601660,width-1070,height-580,overlay-toi_sw,pt-32,y_pad-40,resizemode-75,imgsize-32826/86601660.jpg', 'publishedAt': '2021-09-29T03:06:00Z', 'content': None}, {'source': {'id': None, 'name': 'NDTV News'}, 'author': None, 'title': 'UP Businessman Dies In Police Raid At Gorakhpur Hotel, 6 Cops Suspended - NDTV', 'description': "Six policemen in Uttar Pradesh's Gorakhpur, Chief Minister Yogi Adityanath's homestead, have been suspended after a businessman died during a late-night police raid at a city hotel on Tuesday.", 'url': 'https://www.ndtv.com/india-news/up-businessman-dies-in-police-raid-at-gorakhpur-hotel-6-cops-suspended-2557314', 'urlToImage': 'https://c.ndtvimg.com/2021-09/9oa83h4k_up-businessman-650_625x300_29_September_21.jpg', 'publishedAt': '2021-09-29T03:00:00Z', 'content': "Kanpur businessman Manish Kumar Gupta died in police raid at a Gorakhpur hotel\r\nLucknow: Six policemen in Uttar Pradesh's Gorakhpur, Chief Minister Yogi Adityanath's homestead, have been suspended af… [+2335 chars]"}, {'source': {'id': 'the-times-of-india', 'name': 'The Times of India'}, 'author': 'Gaurav Gupta', 'title': 'IPL 2021, MI vs PBKS: Mumbai Indians keep playoff hopes alive with a six-wicket win over Punjab Kings - Times of India', 'description': 'Cricket News: \u200b\u200b\u200bUnder fire for not playing, and then not bowling in the second leg of IPL-2021, ahead of the T20 World Cup, Pandya smashed an unbeaten 40 (30b, 4x4', 'url': 'https://timesofindia.indiatimes.com/sports/cricket/ipl/top-stories/ipl-2021-mi-vs-pbks-mumbai-indians-keep-playoff-hopes-alive-with-a-six-wicket-win-over-punjab-kings/articleshow/86601335.cms', 'urlToImage': 'https://static.toiimg.com/thumb/msid-86601279,width-1070,height-580,imgsize-84470,resizemode-75,overlay-toi_sw,pt-32,y_pad-40/photo.jpg', 'publishedAt': '2021-09-29T02:49:00Z', 'content': 'IPL 2021: Mumbai Indians beat Punjab Kings by 6 wickets'}, {'source': {'id': None, 'name': 'Hindustan Times'}, 'author': 'hindustantimes.com', 'title': 'Eoin Morgan reacts on heated exchange with R Ashwin, says, ‘things can boil over on hot days’ - Hindustan Times', 'description': "After KKR's 3-wicket win, Morgan was asked about what went down in the middle with Ashwin by former cricketer and broadcaster Ian Bishop. The KKR captain did not read too much into it.\xa0 | Cricket", 'url': 'https://www.hindustantimes.com/cricket/things-can-boil-over-on-hot-days-eoin-morgan-reacts-on-heated-exchange-with-r-ashwin-101632882336545.html', 'urlToImage': 'https://images.hindustantimes.com/img/2021/09/29/1600x900/Eoin_Morgan_1632883082441_1632883082586.jpg', 'publishedAt': '2021-09-29T02:41:56Z', 'content': "The Indian Premier League (IPL) 2021 match between Kolkata Knight Riders and Delhi Capitals in Sharjah saw an argument break out in the middle between KKR captain Eoin Morgan and DC's Ravichandran As… [+1564 chars]"}, {'source': {'id': None, 'name': 'News18'}, 'author': 'Kamalika Sengupta', 'title': 'Booster Shot for TMC as Ex-Goa CM, Sahitya Akademi Awardee Among 12 Leaders Likely to Join Party Today - News18', 'description': "Konkani writer N Shivdas, known for his Sahitya Akademi award-winning collection of short stories 'Bhangarsall', is among a dozen people from Goa who are expected to join Mamata Banerjee's Trinamool Congress on Wednesday along with former chief minister Luizi…", 'url': 'https://www.news18.com/news/politics/booster-shot-for-tmc-as-ex-goa-cm-sahitya-akademi-awardee-among-12-leaders-to-join-party-today-4259480.html', 'urlToImage': 'https://images.news18.com/ibnlive/uploads/2021/09/luizinho-faleiro-goa2.jpg', 'publishedAt': '2021-09-29T02:35:00Z', 'content': 'Konkani writer N Shivdas, known for his Sahitya Akademi award-winning collection of short stories ‘Bhangarsall’, is among a dozen people from Goa who are expected to join Mamata Banerjee‘s Trinamool … [+1870 chars]'}, {'source': {'id': None, 'name': 'Hindustan Times'}, 'author': 'hindustantimes.com', 'title': "Surgical strike day: Here's how the 2016 operation was carried out - Hindustan Times", 'description': 'PM Modi said that while talking to the Army, he realised that they wanted justice for soldiers killed in Uri attack and the government gave them the “free hand” to plan and execute the surgical strikes. | Latest News India', 'url': 'https://www.hindustantimes.com/india-news/surgical-strike-day-here-s-how-the-2016-operation-was-carried-out-101632882272993.html', 'urlToImage': 'https://images.hindustantimes.com/img/2021/09/29/1600x900/_ff70cd0c-0087-11eb-ac80-07fcacbe9f14_1632882459230.png', 'publishedAt': '2021-09-29T02:30:10Z', 'content': 'In September 2016, the Indian Army launched surgical strikes against terrorist camps in Pakistan Occupied Kashmir. The strike on September 28, 2016, was in response to an attack by Pakistan-based ter… [+1716 chars]'}, {'source': {'id': None, 'name': 'News18'}, 'author': 'Rajat Mishra', 'title': 'Stocks To Watch: Infosys, HCL, Bharti Airtel, HDFC AMC, Lupin, KSE, Atul Auto and More - News18', 'description': 'Indian markets on Wednesday tracking negative global cues may open flat, However PMI Manufacturing, Infrastructure output data that are scheduled to be released this week will decide the course of the market.', 'url': 'https://www.news18.com/news/business/stocks-to-watch-infosys-hcl-bharti-airtel-hdfc-amc-lupin-kse-atul-auto-and-more-4259489.html', 'urlToImage': 'https://images.news18.com/ibnlive/uploads/2021/08/shutterstock_1049641082-1-163008106116x9.jpg', 'publishedAt': '2021-09-29T02:14:31Z', 'content': 'Indian markets on Wednesday tracking negative global cues may open flat, However PMI Manufacturing, Infrastructure output data that are scheduled to be released this week will decide the course of th… [+4201 chars]'}, {'source': {'id': None, 'name': 'Moneycontrol'}, 'author': None, 'title': 'Top 10 things to know before the market opens - Moneycontrol.com', 'description': 'Trends on SGX Nifty indicate a negative opening for the index in India with a 107-points loss.', 'url': 'https://www.moneycontrol.com/news/business/markets/top-10-things-to-know-before-the-market-opens-121-7519501.html', 'urlToImage': 'https://images.moneycontrol.com/static-mcnews/2018/11/BSE_Sensex-e1542611342127-770x433.jpg', 'publishedAt': '2021-09-29T02:11:57Z', 'content': 'The Indian stock market is expected to open in the red as trends on SGX Nifty indicate a\xa0negative\xa0opening for the index in India with a\xa0107-points loss.\r\nThe BSE Sensex dropped 410.28 points to 59,66… [+4763 chars]'}, {'source': {'id': None, 'name': 'Hindustan Times'}, 'author': 'Hindustantimes', 'title': 'Top US military officials advised keeping troops in Afghanistan, warned Biden against withdrawal - Hindustan Times', 'description': "General Mark Milley, the chairman of the US Joint Chiefs of Staff, claimed that the United States' withdrawal of troops from Afghanistan amid the Taliban offensive had ‘damaged’ American credibility. | World News", 'url': 'https://www.hindustantimes.com/world-news/top-us-military-officials-advised-keeping-troops-in-afghanistan-warned-biden-against-withdrawal-101632875435774.html', 'urlToImage': 'https://images.hindustantimes.com/img/2021/09/29/1600x900/US-POLITICS-AFGHANISTAN-HEARING-12_1632877655301_1632877678442.jpg', 'publishedAt': '2021-09-29T01:13:58Z', 'content': 'Top military officials of the United States, while testifying before a high-level Senate committee on Tuesday, revealed that they had recommended US president Joe Biden to keep some 2,500 American tr… [+2636 chars]'}, {'source': {'id': None, 'name': 'NDTV News'}, 'author': None, 'title': 'North Korea Says It Tested Hypersonic Missile - NDTV', 'description': "North Korea has successfully tested a hypersonic gliding missile, state media reported Wednesday, in what would be the nuclear-armed nation's latest advance in weapons technology.", 'url': 'https://www.ndtv.com/world-news/north-korea-says-it-tested-hypersonic-missile-2557243', 'urlToImage': 'https://c.ndtvimg.com/2020-10/k2vu2vhg_north-korea-reuters-650_625x300_09_October_20.jpg', 'publishedAt': '2021-09-28T23:36:00Z', 'content': 'Hypersonic missiles move far faster and are more nimble than ordinary ones (Representational)\r\nSeoul, South Korea: North Korea has successfully tested a hypersonic gliding missile, state media report… [+2042 chars]'}, {'source': {'id': None, 'name': 'Notebookcheck.net'}, 'author': 'Enrico Frahn', 'title': "The iPhone 13 Pro Max's record-setting OLED display is the brightest smartphone display on the market according to DisplayMate's review - Notebookcheck.net", 'description': "The display-centric tech website DisplayMate has tested the display of the iPhone 13 Pro Max and concluded that Apple's biggest and most expensive flagship smartphone has a record setting OLED display that supposedly is one of the best in the entire industry.", 'url': 'https://www.notebookcheck.net/The-iPhone-13-Pro-Max-s-record-setting-OLED-display-is-the-brightest-smartphone-display-on-the-market-according-to-DisplayMate-s-review.567251.0.html', 'urlToImage': 'https://www.notebookcheck.net/fileadmin/Notebooks/News/_nc3/iphone_13_pro_max_display.jpeg', 'publishedAt': '2021-09-28T22:13:35Z', 'content': "Apple's latest and greatest smartphones are all the buzz after they have officially launched last week, and profound reviews of the flagships of the Cupertino-based company are slowly but surely appe… [+1204 chars]"}]}
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