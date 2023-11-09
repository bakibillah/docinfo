import random
import subprocess
import threading
import PyChromeDevTools
import time
from bs4 import BeautifulSoup
min_interval = 1
max_interval = 3

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
    command = "google-chrome --user-data-dir=$HOME/docinfo1 --proxy-server=127.0.0.1:8080 --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222"
    chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                      stderr=subprocess.DEVNULL, close_fds=True)
    time.sleep(5)

    chrome = PyChromeDevTools.ChromeInterface()
    try:
        chrome.Network.enable()
        chrome.Page.enable()
        chrome.DOM.enable()
        chrome.Runtime.enable()
        # t = threading.Thread(target=event_listener)
        # t.start()
        chrome.Page.navigate(url="https://www.docinfo.org/search/docprofile?docid=8CDA8490-0C18-421F-B0AC-097E83D11E14&docname=ALENA T VELASCO&usstate=Hawaii&practype=all")
        event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
        value = chrome.wait_event("Network.responseReceived", timeout=60)
        time.sleep(1)

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
                captcha_solved = input('has captcha solved? enter yes or no?\n')
                if captcha_solved == 'yes':
                    print('restarting the script')
                    result = chrome.Runtime.evaluate(expression=get_page_source_js)
                    html_source_listing = result[0]['result']['result']['value']
                    soup = BeautifulSoup(html_source_listing, 'html.parser')
                    div_elements = soup.find_all('div', class_='listing-item')
                else:
                    return
            else:
                print("No iframe found in the HTML source.")
                div_elements = soup.find_all('div', class_='listing-item')
        else:
            print("No iframe found in the HTML source.")
            print(html_source_listing)
    finally:
        print('finally')
        chrome.Browser.close()


run_scraper(1)
