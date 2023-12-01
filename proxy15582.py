import csv
import json
import random
import subprocess
import PyChromeDevTools
import urllib3
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

from database2 import select_all, insert_doc_id, update_input2

# def run_scraper(count_, docname_, usstate_):
command = "google-chrome --user-data-dir=$HOME/proxy15582 --proxy-server=138.197.224.38:16626 --remote-debugging-port=16626 --remote-allow-origins=http://localhost:16626"
chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, close_fds=True)
time.sleep(5)

chrome = PyChromeDevTools.ChromeInterface(port=16626)

chrome.Network.enable()
chrome.Page.enable()
chrome.DOM.enable()
chrome.Runtime.enable()

data = []
while True:
    all_input_data = select_all()

    state_map = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
    }

    for row in all_input_data:
        docname = ""
        usstate = ""
        row_id = row['id']
        npi = row['npi']
        full_name = row['full_name']
        first_name = row['first_name']
        middle_name = row['middle_name']
        last_name = row['last_name']
        age = row['age']
        state = row['state']
        specialty = row['specialty']
        if middle_name == '' or middle_name is None:
            docname = f"{first_name}+{last_name}"
        else:
            docname = f"{first_name}+{middle_name}+{last_name}"
        if state is None:
            continue
        next_page = False
        for index in range(1):
            if index == 0:
                print(f"name: {docname} index: {row_id}")
                chrome.Page.navigate(url=f"https://www.docinfo.org/search/?practype=Physician&docname={docname}&usstate={state}&token=")
                time.sleep(random.randint(3, 5))
            else:
                chrome.Page.navigate(url=f"https://www.docinfo.org/search/?page={index + 1}&docname={docname}&usstate={state}&practype=Physician&token=")
                time.sleep(random.randint(5, 10))
            event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
            value = chrome.wait_event("Network.responseReceived", timeout=60)
            time.sleep(2)

            get_page_source_js = """
                            function getDocumentSource() {
                                return document.documentElement.outerHTML;
                            }
                            getDocumentSource();
                        """
            # javascript_code = 'console.log("Hello from JavaScript!");'
            # javascript_code = "document.querySelector('.js-encode-search').click();"
            result = chrome.Runtime.evaluate(expression=get_page_source_js)
            if result[0] is None:
                time.sleep(60)
                continue
            try:
                html_source_listing = result[0]['result']['result']['value']
                soup = BeautifulSoup(html_source_listing, 'html.parser')
                title = soup.find('title')
                if title is not None:
                    title = title.text
                    print(f"title: {title}")
                    if title == 'Burp Suite Professional':
                        time.sleep(random.randint(3, 5))
                        continue
                iframe = soup.find('iframe')
                div_elements = None
                if iframe:
                    iframe_src = iframe.get('src')
                    if '_Incapsula_Resource' in iframe_src:
                        print('captcha appeared, so solve it manually')
                        time.sleep(120)
                    else:
                        print("No iframe found in the HTML source.")

                        div_elems = soup.find_all('article', class_='row article article--list article--searchResult')
                        for elem in div_elems:
                            search_name = elem.find('span', class_='search-link').text
                            gender = elem.find('div', class_='article__subHeadline').text
                            span_element = elem.find('span', onclick=True)
                            onclick_value = span_element['onclick']
                            src = onclick_value.split("verifyOpen('ViewProfile', '")[1].replace("')", "")
                            docid = src.split("=")[1].split("&")[0]
                            li_elements = elem.find_all('li')
                            location_list = []
                            for li_elem in li_elements:
                                location_list.append(li_elem.text)
                            location_json = json.dumps(location_list)
                            insert_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, docid, search_name, gender, location_json, row_id)
                        update_input2(row_id)
                else:
                    print("No iframe found in the HTML source.")
                    # div_elems = soup.find_all('h3', class_='article__headline')
                    div_elems = soup.find_all('article', class_='row.article.article--list.article--searchResult')
                    for elem in div_elems:
                        search_name = elem.find('span', class_='search-link').text
                        gender = elem.find('div', class_='article__subHeadline').text
                        span_element = elem.find('span', onclick=True)
                        onclick_value = span_element['onclick']
                        src = onclick_value.split("verifyOpen('ViewProfile', '")[1].replace("')", "")
                        docid = src.split("=")[1].split("&")[0]
                        li_elements = elem.find_all('li')
                        location_list = []
                        for li_elem in li_elements:
                            location_list.append(li_elem.text)
                        location_json = json.dumps(location_list)
                        insert_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty, search_name, gender, docid, location_json, row_id)
                    update_input2(row_id)
            except:
                pass


chrome.Browser.close()
