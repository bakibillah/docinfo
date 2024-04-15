import PyChromeDevTools
import time, random
from bs4 import BeautifulSoup
import json
from database2 import state_map_2
import pymysql


proxy_lte_boost = '65.21.25.28:1039:9BeAXC3urY:ZFyLXaE14k'


def conn():
    return pymysql.connect(host='localhost',
                           user='',
                           password='',
                           database='docinfo_org',
                           charset='utf8mb4',
                           autocommit=True,
                           cursorclass=pymysql.cursors.DictCursor)


def get_name():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM docinfo_org.doc_id2 where done is TRUE order by id limit 500;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()
chrome.DOM.enable()
chrome.Runtime.enable()
all_doc_id = get_name()
for doc_id in all_doc_id:
    first_name = ''
    middle_name = ''
    last_name = ''
    full_name = doc_id['search_name']
    if ',' in full_name:
        name = full_name.split(',')[0]
        first_middle_lat = name.split(' ')
        if len(first_middle_lat) == 3:
            first_name = first_middle_lat[0]
            middle_name = first_middle_lat[1]
            last_name = first_middle_lat[2]
        elif len(first_middle_lat):
            first_name = first_middle_lat[0]
            middle_name = None
            last_name = first_middle_lat[1]
    else:
        name = full_name
        first_middle_lat = name.split(' ')
        if len(first_middle_lat) == 3:
            first_name = first_middle_lat[0]
            middle_name = first_middle_lat[1]
            last_name = first_middle_lat[2]
        elif len(first_middle_lat):
            first_name = first_middle_lat[0]
            middle_name = None
            last_name = first_middle_lat[1]
    locations_in_profile = doc_id['locations_in_profile']
    location = json.loads(locations_in_profile)
    for item in location:
        if item == '-':
            continue
        city = item.split(',')[0]
        state = item.split(',')[1].strip()

        state_code = state_map_2[state]
        if middle_name is None:
            url = f"https://www.truepeoplesearch.com/results?name={first_name}%20{last_name}&citystatezip={city},%20{state_code}"
        else:
            url = f"https://www.truepeoplesearch.com/results?name={first_name}%20{middle_name}%20{last_name}&citystatezip={city},%20{state_code}"
        chrome.Page.navigate(url=url)

        try:
            event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
            value = chrome.wait_event("Network.responseReceived", timeout=60)
            # time.sleep(random.randint(3, 5))

            get_page_source_js = """
                                function getDocumentSource() {
                                    return document.documentElement.outerHTML;
                                }
                                getDocumentSource();
                            """
            result = chrome.Runtime.evaluate(expression=get_page_source_js)
            html_source_listing = result[0]['result']['result']['value']
            soup = BeautifulSoup(html_source_listing, 'html.parser')
            iframe = soup.find('iframe')
            if iframe:
                iframe_src = iframe.get('src')
                if iframe_src is not None:
                    if 'challenge-platform' in iframe_src:
                        print('captcha appeared, so solve it manually')
                        time.sleep(15)

            result = chrome.Runtime.evaluate(expression=get_page_source_js)
            html_source_listing = result[0]['result']['result']['value']
            soup = BeautifulSoup(html_source_listing, 'html.parser')
            record_found_text = soup.find('div', class_='record-count').text.strip().split('record')[0]
            print("Record Found:", int(record_found_text))
            break
        except:
            pass