import PyChromeDevTools
import time, random
from bs4 import BeautifulSoup
import json
from database import *
import subprocess


if __name__ == '__main__':
    while True:
        command = "google-chrome --user-data-dir=$HOME/truepeople --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222 --blink-settings=imagesEnabled=true"
        chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
        time.sleep(5)

        all_doc_id = get_name()

        chrome = PyChromeDevTools.ChromeInterface()
        chrome.Network.enable()
        chrome.Page.enable()
        chrome.DOM.enable()
        chrome.Runtime.enable()
        num = 0
        count_ = 0
        chrome.Network.clearBrowserCookies()
        for doc_id in all_doc_id:
            done = False
            profile_link_set = dict()
            count_ += 1
            first_name = ''
            middle_name = ''
            last_name = ''
            full_name = doc_id['search_name']
            # print(full_name)
            if ',' in full_name:
                name = full_name.split(',')[0]
                first_middle_lat = name.split(' ')
                if len(first_middle_lat) == 3:
                    first_name = first_middle_lat[0]
                    middle_name = first_middle_lat[1]
                    last_name = first_middle_lat[2]
                elif len(first_middle_lat) == 2:
                    first_name = first_middle_lat[0]
                    middle_name = None
                    last_name = first_middle_lat[1]
                    continue
                elif len(first_middle_lat) == 4:
                    first_name = first_middle_lat[0]
                    middle_name = None
                    last_name = first_middle_lat[3]
                    continue
                else:
                    continue
            else:
                name = full_name
                first_middle_lat = name.split(' ')
                if len(first_middle_lat) == 3:
                    first_name = first_middle_lat[0]
                    middle_name = first_middle_lat[1]
                    last_name = first_middle_lat[2]
                elif len(first_middle_lat) == 2:
                    first_name = first_middle_lat[0]
                    middle_name = None
                    last_name = first_middle_lat[1]
                    continue
                elif len(first_middle_lat) == 4:
                    first_name = first_middle_lat[0]
                    middle_name = None
                    last_name = first_middle_lat[3]
                    continue
                else:
                    continue

            locations_in_profile = doc_id['locations_in_profile']
            location = json.loads(locations_in_profile)
            location.reverse()
            count = 0
            for item in location:
                if item == '-':
                    continue
                count += 1
                if count > 4:
                    break
                # if len(location) > 1:
                #     if count == 1:
                #         continue

                city = item.split(',')[0]
                state = item.split(',')[1].strip()
                state_code = None
                try:
                    state_code = state_map_2[state]
                except KeyError:
                    continue
                url = f"https://www.usphonebook.com/225-305-6276"

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
                    title = soup.find('title')
                    # print(f"title: {title}")
                    if title == 'Just a moment...':
                        while True:
                            time.sleep(5)
                            result = chrome.Runtime.evaluate(expression=get_page_source_js)
                            html_source_listing = result[0]['result']['result']['value']
                            soup = BeautifulSoup(html_source_listing, 'html.parser')
                            title = soup.find('title')
                            if title == 'Just a moment...':
                                continue
                            else:
                                break
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
                    url2 = soup.find('a', class_='btn btn-dark m-0 btn-continue').get('href')
                    num += 1
                    print(f"{num}: {url2}")
                    chrome.Page.navigate(url=url2)
                    time.sleep(2)
                    # js_click_details = "document.querySelector('.btn.btn-dark.m-0.btn-continue').click()"
                    # chrome.Runtime.evaluate(expression=js_click_details)
                    # time.sleep(1)
                except:
                    pass

        print('now close the browser')
        chrome.browser.close()
        time.sleep(3)
