import time
import requests
import PyChromeDevTools
import requests
import tls_client
from bs4 import BeautifulSoup
from database2 import *
import json
import subprocess


proxy_to_test = '65.21.25.28:1039:9BeAXC3urY:ZFyLXaE14k'


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
            response = session.get('https://www.jsonip.com', timeout=timeout)
            if response.status_code == 200:
                print(f"The proxy {proxy} is live: {response.json()['ip']}")
                return response.json()['ip']
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

    url = "https://www.docinfo.org:443/search/docprofile?docid=7C468AA8-A15F-4951-A14F-07119858FD7D&token="
    chrome_.Page.navigate(url=url)
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
                            return token_value
                    # break
            else:
                cookies = chrome_.Network.getAllCookies()
                for cookie in cookies[0]['result']['cookies']:
                    if cookie['name'] == 'reese84':
                        token_value = cookie['value']
                        return token_value
                # break
        except Exception as e:
            print(e)

# command = "google-chrome --user-data-dir=$HOME/docinfo --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222"
command = "google-chrome --user-data-dir=$HOME/16623 --proxy-server=65.21.25.28:1039 --remote-debugging-port=16623 --remote-allow-origins=http://localhost:16623"
chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
time.sleep(1)


# def get_cookie(chrome_, change_ip):
#     while change_ip:
#         burp0_url = "https://gridpanel.net:443/api/reboot?token=NjY2OSw4MjA5ZTk1My1kYWJkLTQ4ZTYtOTA0ZC1iZjc1YzJiNDYzZWQ%3D"
#         burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0",
#                          "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1",
#                          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
#                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#                          "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
#                          "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
#                          "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
#         res = requests.get(burp0_url, headers=burp0_headers)
#         if res.status_code == 200:
#             print(f"ip changed successfully: {res.text}")
#             time.sleep(30)
#             break
#         else:
#             time.sleep(10)
#             continue
#     url = "https://www.docinfo.org:443/search/docprofile?docid=7C468AA8-A15F-4951-A14F-07119858FD7D&token="
#     chrome_.Page.navigate(url=url)
#     event, messages = chrome_.wait_event("Page.frameStoppedLoading", timeout=60)
#     value = chrome_.wait_event("Network.responseReceived", timeout=60)
#
#     get_page_source_js = """
#                     function getDocumentSource() {
#                         return document.documentElement.outerHTML;
#                     }
#                     getDocumentSource();
#                 """
#     while True:
#         try:
#             result = chrome_.Runtime.evaluate(expression=get_page_source_js)
#             html_source_listing = result[0]['result']['result']['value']
#             soup_ = BeautifulSoup(html_source_listing, 'html.parser')
#             iframe_ = soup_.find('iframe')
#             if iframe_:
#                 iframe_src_ = iframe_.get('src')
#                 if iframe_src_ is None:
#                     break
#                 if '_Incapsula_Resource' in iframe_src_:
#                     print('captcha appeared, so solve it manually')
#                     time.sleep(3)
#                     continue
#                 else:
#                     break
#             else:
#                 break
#         except Exception as e:
#             print(e)
#     cookies = chrome_.Network.getAllCookies()
#     for cookie in cookies[0]['result']['cookies']:
#         if cookie['name'] == 'reese84':
#             token_value = cookie['value']
#             return token_value
#
#     # chrome.Browser.close()


break_while = True
while break_while:
    time.sleep(2)
    chrome = PyChromeDevTools.ChromeInterface(port=16623)
    chrome.Network.enable()
    chrome.Page.enable()
    chrome.DOM.enable()
    reese84 = get_cookie(chrome, "127.0.0.1")
    print(reese84)
    all_doc_id = get_doc_id()
    n = 0
    for doc_id in all_doc_id:
        n += 1
        print(n)
        session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
        doc_id_ = doc_id['href']
        row_id = doc_id['id']

        burp0_url = f"https://www.docinfo.org:443/search/docprofile?docid={doc_id_}&token="

        burp0_cookies = {"visid_incap_2587692": "", "ai_user": "", "incap_ses_872_2587692": "", "nlbi_2587692": "",
                         "reese84": reese84, "ASP.NET_SessionId": "", "ARRAffinity": "", "ARRAffinitySameSite": "",
                         "_gid": "", "_gat_UA-40572798-14": "", "_ga": "", "ai_session": "",
                         "nlbi_2587692_2147483392": "",
                         "_ga_NTPKCKQSFL": ""}

        burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0",
                         "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                         "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
                         "Accept-Language": "en-US,en;q=0.9"}

        session.headers = {}
        session.headers = burp0_headers
        try:
            ip = test_proxy(proxy_to_test, 5, )
            res = session.get(burp0_url, proxy="http://9BeAXC3urY:ZFyLXaE14k@65.21.25.28:1039", cookies=burp0_cookies, timeout_seconds=35)
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
                    time.sleep(3)
                    continue
                else:
                    print("No iframe found in the HTML source.")
                    reported_locations = soup.find(class_='profile__aside').find_all('li')
                    locations = []
                    for location in reported_locations:
                        locations.append(location.text)
                    locations_in_profile_json = json.dumps(locations)
                    print("locations: ", locations_in_profile_json)
                    profile_sections = soup.find_all('div', class_='profile__section')
                    education_json = None
                    certification_json = None
                    active_license_json = None
                    all_action_json = None

                    for elem in profile_sections:
                        headline = elem.find('h2').text.strip()
                        educations = []
                        certifications = []
                        active_license = []
                        all_actions = []
                        if headline == 'Education':
                            all_education = elem.find_all('p')
                            for education in all_education:
                                educations.append(education.text.strip())
                            education_json = json.dumps(educations)
                            print("educations: ", education_json)
                        elif headline == 'Certifications':
                            all_certification = elem.find_all('li')
                            for each_certification in all_certification:
                                certifications.append(each_certification.text.strip())
                            certification_json = json.dumps(certifications)
                            print("certifications: ", certification_json)
                        elif headline == 'Active Licenses':
                            all_active_licenses = elem.find_all('li')
                            for all_active_license in all_active_licenses:
                                active_license.append(all_active_license.text.strip())
                            active_license_json = json.dumps(active_license)
                            print("active license: ", active_license_json)
                        elif headline == 'Actions':
                            all_actions_elems = elem.find_all('li')
                            for all_action in all_actions_elems:
                                all_actions.append(all_action.text.strip())
                            all_action_json = json.dumps(all_actions)
                            print("all actions: ", all_action_json)
                    update_doc_id(row_id, locations_in_profile_json, education_json, certification_json,
                                  active_license_json,
                                  all_action_json)
            else:
                print("No iframe found in the HTML source.")
                reported_locations = soup.find(class_='profile__aside').find_all('li')
                locations = []
                for location in reported_locations:
                    locations.append(location.text)
                locations_in_profile_json = json.dumps(locations)
                print(locations_in_profile_json)
                profile_sections = soup.find_all('div', class_='profile__section')
                education_json = None
                certification_json = None
                active_license_json = None
                all_action_json = None
                for elem in profile_sections:
                    headline = elem.find('h2').text.strip()
                    educations = []
                    certifications = []
                    active_license = []
                    all_actions = []
                    if headline == 'Education':
                        all_education = elem.find_all('p')
                        for education in all_education:
                            educations.append(education.text.strip())
                        education_json = json.dumps(educations)
                        print("educations: ", education_json)
                    elif headline == 'Certifications':
                        all_certification = elem.find_all('li')
                        for each_certification in all_certification:
                            certifications.append(each_certification.text.strip())
                        certification_json = json.dumps(certifications)
                        print("certifications: ", certification_json)
                    elif headline == 'Active Licenses':
                        all_active_licenses = elem.find_all('li')
                        for all_active_license in all_active_licenses:
                            active_license.append(all_active_license.text.strip())
                        active_license_json = json.dumps(active_license)
                        print("active license: ", active_license_json)
                    elif headline == 'Actions':
                        all_actions_elems = elem.find_all('li')
                        for all_action in all_actions_elems:
                            all_actions.append(all_action.text.strip())
                        all_action_json = json.dumps(all_actions)
                        print("all actions: ", all_action_json)
                update_doc_id(row_id, locations_in_profile_json, education_json, certification_json,
                              active_license_json, all_action_json)

        except Exception as e:
            print(e)
            continue
