import time
import requests
import PyChromeDevTools
import requests
import tls_client
from bs4 import BeautifulSoup
from common import get_cookie, test_proxy
from database2 import *
import json
import subprocess


proxy_to_test = '65.21.25.28:1034:3kdBLFfdND:hfarnlS4Qo'
# proxy_to_test = '65.21.25.28:1060:DEx4GMcTW25u:2MUQdyqjDa'
proxy_parts = proxy_to_test.split(':')
ip_address = proxy_parts[0]
port = proxy_parts[1]
username = proxy_parts[2]
password = proxy_parts[3]


command = f"google-chrome --user-data-dir=$HOME/{port} --proxy-server={ip_address}:{port} --remote-debugging-port={port} --remote-allow-origins=http://localhost:{port} --user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'"
chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
time.sleep(1)

break_while = True
while break_while:
    time.sleep(2)
    chrome = PyChromeDevTools.ChromeInterface(port=port)
    chrome.Network.enable()
    chrome.Page.enable()
    chrome.DOM.enable()
    reese84 = get_cookie(chrome, "127.0.0.1", proxy_to_test)
    print(reese84)
    all_doc_id = get_doc_id()
    if len(all_doc_id) == 0:
        print('no doc id left to scrape data')
        break_while = False
        continue
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
        if reese84 is None:
            reese84 = get_cookie(chrome, '127.0.0.1', proxy_to_test)
            continue
        burp0_cookies = {"visid_incap_2587692": "", "ai_user": "", "incap_ses_872_2587692": "", "nlbi_2587692": "",
                         "reese84": reese84, "ASP.NET_SessionId": "", "ARRAffinity": "", "ARRAffinitySameSite": "",
                         "_gid": "", "_gat_UA-40572798-14": "", "_ga": "", "ai_session": "",
                         "nlbi_2587692_2147483392": "",
                         "_ga_NTPKCKQSFL": ""}

        burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0",
                         "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
                         "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                         "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                         "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
                         "Accept-Language": "en-US,en;q=0.9"}

        session.headers = {}
        session.headers = burp0_headers
        try:
            ip = test_proxy(proxy_to_test, 5)
            res = session.get(burp0_url, proxy=f"http://{username}:{password}@{ip_address}:{port}", cookies=burp0_cookies,  timeout_seconds=10)
            print(burp0_url)
            html_source = res.text
            soup = BeautifulSoup(html_source, 'html.parser')
            iframe = soup.find('iframe')
            if iframe:
                iframe_src = iframe.get('src')
                if '_Incapsula_Resource' in iframe_src:
                    print('captcha appeared, so solve it manually. now switching to browser')
                    reese84 = get_cookie(chrome, ip, proxy_to_test)
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
