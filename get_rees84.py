import asyncio
import subprocess
import PyChromeDevTools
import time


def get_cookie(chrome_):
    url = "https://www.docinfo.org:443/search/docprofile?docid=7C468AA8-A15F-4951-A14F-07119858FD7D&token="
    # chrome = PyChromeDevTools.ChromeInterface()
    # chrome.Network.enable()
    # chrome.Page.enable()
    # chrome.DOM.enable()
    chrome_.Page.navigate(url=url)
    event, messages = chrome_.wait_event("Page.frameStoppedLoading", timeout=60)
    value = chrome_.wait_event("Network.responseReceived", timeout=60)

    cookies = chrome_.Network.getAllCookies()
    for cookie in cookies[0]['result']['cookies']:
        if cookie['name'] == 'reese84':
            token_value = cookie['value']
            return token_value

    # chrome.Browser.close()
