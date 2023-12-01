import csv
import subprocess

import PyChromeDevTools
import urllib3
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time

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

# reese84 = "3:HOVevO2BHM6F/QCWfp57wQ==:y1r9M9Z8Y+oNPWWVgqTMv2MQG/GKyWi7m+/VEOSGgmEtGjA2Hu7F7BZc9aW9wXJGg0otOU9NfxRYjdiuduNbRMi3RcwCdV9QvGB/QUFlQXM4ADy8CYnkTB93mN7MuZQoBz01A27RTKdb7IS8lonkCQcQbdv29z0aJMaf/Z6WNLg10RR2XYHMpWxsIjlQLgiqVTCUNKfXmxhJPjkEyCA6CYXHwRfDI+rtsa6QjocciwL6g4fcAB5BNen0PxAGLVint4RdGq7QHL5e1kt4TmY+pahr7t7tcKUdKGDHbKdADaOsoDWafKIf7jXZFly03vr5nBi6UcFsajsWgh3JhkuBJUnpDYi3TpxUnBRFX/joXsjxnl85RlvFp08F0D3RX4HYWFEBduYPbtdIQXPM3cawrR+/SYMH+D1kGXEtW9Y5zojlt34xX+Rtpi81ix18AiTMD05F5/GwjVNjLv9XOuDTtffpkPbYiTvaDekNYOF9ulQyXxAFMOOK3MlC70pr5Dfj:lD7IMVkM7jer23M1dyT2EOBj/J5tOKIaQRIYPslJd/s="

# Replace 'your_file.csv' with the actual path to your CSV file.
csv_file = '500k_docinfo.csv'

# Initialize an empty list to store the data
data = []

# Open the CSV file and read its contents
with open(csv_file, 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

    # def run_scraper(count_, docname_, usstate_):
    command = "google-chrome --user-data-dir=$HOME/docinfo1 --proxy-server=127.0.0.1:8080 --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222"
    chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, close_fds=True)
    time.sleep(5)

    chrome = PyChromeDevTools.ChromeInterface()

    chrome.Network.enable()
    chrome.Page.enable()
    chrome.DOM.enable()
    chrome.Runtime.enable()
        # Display the data
    for row in data:
        docname = ""
        usstate = ""
        # full_name = row['Full Name']
        f_name = row['First Name']
        m_name = row['Middle Name']
        l_name = row['Last Name']
        docname = f"{f_name}+{m_name}+{l_name}"
        usstate_code = row['State']
        usstate = state_map[usstate_code]

        chrome.Page.navigate(url=f"https://www.docinfo.org/search/?practype=all&docname={docname}&usstate={usstate}&token=")
        event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        value = chrome.wait_event("Network.responseReceived", timeout=60)
        time.sleep(10)

        get_page_source_js = """
                        function getDocumentSource() {
                            return document.documentElement.outerHTML;
                        }
                        getDocumentSource();
                    """
        # javascript_code = 'console.log("Hello from JavaScript!");'
        # javascript_code = "document.querySelector('.js-encode-search').click();"
        result = chrome.Runtime.evaluate(expression=get_page_source_js)
        html_source_listing = result[0]['result']['result']['value']
        soup = BeautifulSoup(html_source_listing, 'html.parser')
        iframe = soup.find('iframe')
        div_elements = None
        if iframe:
            iframe_src = iframe.get('src')
            if 'geo.captcha-delivery.com/captcha' in iframe_src:
                print('captcha appeared, so solve it manually')

            else:
                print("No iframe found in the HTML source.")

                div_elems = soup.find_all('h3', class_='article__headline')
                for elem in div_elems:
                    span_element = elem.find('span', onclick=True)
                    onclick_value = span_element['onclick']
                    src = onclick_value.split("verifyOpen('ViewProfile', '")[1].replace("')", "")
                    href = f"https://www.docinfo.org{src}"
                    print(href)
                    chrome.Page.navigate(url=href)
                    event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
                    value = chrome.wait_event("Network.responseReceived", timeout=60)

        else:
            print("No iframe found in the HTML source.")
            div_elems = soup.find_all('h3', class_='article__headline')
            for elem in div_elems:
                span_element = elem.find('span', onclick=True)
                onclick_value = span_element['onclick']
                src = onclick_value.split("verifyOpen('ViewProfile', '")[1].replace("')", "")
                href = f"https://www.docinfo.org{src}"
                print(href)
                chrome.Page.navigate(url=href)
                event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
                value = chrome.wait_event("Network.responseReceived", timeout=60)

    chrome.Browser.close()
