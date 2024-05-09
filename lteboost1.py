import csv
import json
import random
import subprocess
import PyChromeDevTools
import tls_client
import urllib3
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

from database2 import select_all, insert_doc_id, update_input2, get_name_n_location

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

proxy_to_test = '65.21.25.28:1040:09rPFmJhUh:r951Ue1Uk3'
# proxy_to_test = '65.21.25.28:1039:cPyQtBjODE:pU8LsUM1l4'

proxy_parts = proxy_to_test.split(':')
ip_address = proxy_parts[0]
port = proxy_parts[1]
username = proxy_parts[2]
password = proxy_parts[3]


def test_proxy(proxy, timeout=5):
    proxy_live_status: bool = False
    while not proxy_live_status:
        try:
            proxy_parts = proxy.split(':')
            ip_address = proxy_parts[0]
            port = proxy_parts[1]
            username = proxy_parts[2]
            password = proxy_parts[3]
            session = requests.Session()
            session.proxies = {'http': f'http://{username}:{password}@{ip_address}:{port}',
                               'https': f'http://{username}:{password}@{ip_address}:{port}'}
            response = session.get('https://icanhazip.com:443/', timeout=timeout)
            if response.status_code == 200:
                print(f"The proxy {proxy} is live: {response.text}")
                return response.text.strip()
            else:
                time.sleep(1)
                print(f"The proxy {proxy} returned a non-200 status code: {response.status_code}")
                proxy_live_status = False
        except requests.RequestException as e:
            time.sleep(1)
            print(f"Error testing proxy {proxy}: {e}")
            proxy_live_status = False


def get_cookie(chrome_, ip_):
    _ip = test_proxy(proxy_to_test, 5)
    while ip_ == _ip:
        _ip = test_proxy(proxy_to_test, 5)
        time.sleep(2)
        print(f"ip_: {ip_} and _ip: {_ip}")

    url = "https://www.docinfo.org/"
    chrome_.Page.navigate(url=url)
    time.sleep(5)
    event, messages = chrome_.wait_event("Page.frameStoppedLoading", timeout=60)
    value = chrome_.wait_event("Network.responseReceived", timeout=60)

    get_page_source_js = """
                    function getDocumentSource() {
                        return document.documentElement.outerHTML;
                    }
                    getDocumentSource();
                """
    while_count = 0
    while True:
        while_count += 1
        if while_count > 20:
            break
        try:
            result = chrome_.Runtime.evaluate(expression=get_page_source_js)
            if result[0] is None:
                cookies = chrome_.Network.getAllCookies()
                for cookie in cookies[0]['result']['cookies']:
                    if cookie['name'] == 'reese84':
                        token_value = cookie['value']
                        chrome.Network.clearBrowserCookies()
                        cookies = chrome.Network.getCookies()
                        print(f"Cookies after clearing: {cookies}")
                        chrome.Page.navigate(url="https://www.google.com/")
                        return token_value
            html_source_listing = result[0]['result']['result']['value']
            soup_ = BeautifulSoup(html_source_listing, 'html.parser')
            iframe_ = soup_.find('iframe')
            if iframe_:
                iframe_src_ = iframe_.get('src')
                if iframe_src_ is None:
                    break
                if '_Incapsula_Resource' in iframe_src_:
                    print(f'{while_count}: captcha appeared, so solve it manually')
                    time.sleep(3)
                    continue
                else:
                    cookies = chrome_.Network.getAllCookies()
                    for cookie in cookies[0]['result']['cookies']:
                        if cookie['name'] == 'reese84':
                            token_value = cookie['value']
                            chrome.Network.clearBrowserCookies()
                            cookies = chrome.Network.getCookies()
                            print(f"Cookies after clearing: {cookies}")
                            chrome.Page.navigate(url="https://www.google.com/")
                            return token_value
                    # break
            else:
                cookies = chrome_.Network.getAllCookies()
                for cookie in cookies[0]['result']['cookies']:
                    if cookie['name'] == 'reese84':
                        token_value = cookie['value']
                        chrome.Network.clearBrowserCookies()
                        cookies = chrome.Network.getCookies()
                        print(f"Cookies after clearing: {cookies}")
                        chrome.Page.navigate(url="https://www.google.com/")
                        return token_value
                # break
        except Exception as e:
            print(e)
    chrome.Network.clearBrowserCookies()
    cookies = chrome.Network.getCookies()
    print(f"Cookies after clearing: {cookies}")
    chrome.Page.navigate(url="https://www.google.com/")


command = f"google-chrome --user-data-dir=$HOME/1063 --proxy-server={ip_address}:{port} --remote-debugging-port={port} --remote-allow-origins=http://localhost:{port} --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'"
chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL, close_fds=True)
time.sleep(5)

chrome = PyChromeDevTools.ChromeInterface(port=port)

chrome.Network.enable()
chrome.Page.enable()
chrome.DOM.enable()
chrome.Runtime.enable()

data = []
while True:
    all_input_data = select_all()
    reese84 = get_cookie(chrome, "127.0.0.1")
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
        state_original = row['state']
        specialty = row['specialty']
        if middle_name == '' or middle_name is None:
            docname = f"{first_name}+{last_name}"
        else:
            docname = f"{first_name}+{middle_name}+{last_name}"

        state_split = state_original.split("|")[0]
        if state_split is None:
            continue
        state = ''
        try:
            # this is applicable for new set of input data
            state = state_map[state_split]
        except KeyError:
            pass
        next_page = False
        for index in range(1):
            session = tls_client.Session(
                client_identifier="chrome112",
                random_tls_extension_order=True
            )
            if reese84 is None:
                reese84 = get_cookie(chrome, '127.0.0.1')
                continue
            burp0_url = f"https://www.docinfo.org:443/search/?practype=Physician&docname={docname}&usstate={state}&token="
            burp0_cookies = {"ai_user": "",
                             "visid_incap_2587692": "",
                             "_ga": "",
                             "_ga_NTPKCKQSFL": "",
                             "incap_ses_1579_2587692": "",
                             "reese84": reese84,
                             "nlbi_2587692": "",
                             "ASP.NET_SessionId": "",
                             "ARRAffinity": "",
                             "ARRAffinitySameSite": "",
                             "nlbi_2587692_2147483392": "",
                             "incap_ses_872_2587692": ""
                             }
            burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"118\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0",
                             "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                             "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                             "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                             "Sec-Fetch-Dest": "document", "Referer": "https://www.docinfo.org/",
                             "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

            session.headers = {}
            session.headers = burp0_headers
            try:
                ip = test_proxy(proxy_to_test, 5, )
                res = session.get(burp0_url, proxy=f"http://{username}:{password}@{ip_address}:{port}",
                                  cookies=burp0_cookies, timeout_seconds=10)

                print(burp0_url)
                # proxy = "http://KlbNcNG3nZ:DoYXg5YHlx@65.21.25.28:1037",
                html_source = res.text
                # print(html_source)
                soup = BeautifulSoup(html_source, 'html.parser')
                iframe = soup.find('iframe')
                if iframe:
                    iframe_src = iframe.get('src')
                    if '_Incapsula_Resource' in iframe_src:
                        print('captcha appeared, so solve it manually. now switching to browser')
                        reese84 = get_cookie(chrome, ip)
                        print(reese84)
                        time.sleep(1)
                        continue
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
                            for index in range(4):
                                try:
                                    text = li_elements[index].text
                                    location_list.append(text)
                                except IndexError:
                                    location_list.append("-")
                            location_json = json.dumps(location_list)
                            # first_middle_last_ = search_name[0].split(' ')
                            # print(npi, full_name, first_name, middle_name, last_name, age, state, specialty, docid, search_name, gender, location_json, row_id)
                            insert_doc_id(npi, full_name, first_name, middle_name, last_name, age, state, specialty,
                                          docid, search_name, gender, location_json, row_id)

                        update_input2(row_id)

            except Exception as e:
                print(e)

# chrome.Browser.close()
