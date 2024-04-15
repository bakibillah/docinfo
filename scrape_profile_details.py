import json
import random
import subprocess
import threading
import PyChromeDevTools
import time
from bs4 import BeautifulSoup
min_interval = 1
max_interval = 3
from database2 import *


get_page_source_js_ = """
                function getDocumentSource() {
                    return document.documentElement.outerHTML;
                }
                getDocumentSource();
            """


def check_captcha_status(chrome_):
    while True:
        result = chrome_.Runtime.evaluate(expression=get_page_source_js_)
        html_source_detailed = result[0]['result']['result']['value']
        soup_ = BeautifulSoup(html_source_detailed, 'html.parser')
        iframe = soup_.find('iframe')
        if iframe:
            iframe_src = iframe.get('src')
            if 'geo.captcha-delivery.com/captcha' in iframe_src:
                time.sleep(5)
            else:
                break
    return True


def run_scraper(count_):
    command = "google-chrome --user-data-dir=$HOME/profile_15582 --proxy-server=138.197.224.38:15582 --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222"
    chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, close_fds=True)
    time.sleep(5)

    chrome = PyChromeDevTools.ChromeInterface()
    chrome.Network.enable()
    chrome.Page.enable()
    chrome.DOM.enable()
    chrome.Runtime.enable()
    all_doc_id = get_doc_id()
    for doc_id in all_doc_id:
        doc_id_ = doc_id['href']
        row_id = doc_id['id']
        chrome.Page.navigate(url="https://www.docinfo.org/search/docprofile?docid={}&token=".format(doc_id_))
        print('-------------------------------------------------')
        try:
            event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
            value = chrome.wait_event("Network.responseReceived", timeout=60)
            time.sleep(random.randint(3, 5))

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
                if '_Incapsula_Resource' in iframe_src:
                    print('captcha appeared, so solve it manually')
                    time.sleep(120)
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
                    update_doc_id(row_id, locations_in_profile_json, education_json, certification_json, active_license_json, all_action_json)
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
        finally:
            print('finally')
    chrome.Browser.close()


run_scraper(1)
