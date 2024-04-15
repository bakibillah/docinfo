# import requests
import tls_client

import re

import PyChromeDevTools
import time, random
from bs4 import BeautifulSoup
import json
# from database import *
import subprocess
from lxml import html

from database import conn, search_people_data


def get_all_name():
    try:
        with conn().cursor() as cursor:
            select_sql = "SELECT * FROM `doc_id4` where `listofaddress1` is not null and listofaddress2 is null limit 100000;"
            cursor.execute(select_sql)
            data_ = cursor.fetchall()
            return data_
    except Exception as e:
        print(e)


if __name__ == '__main__':
    while True:
        command = "google-chrome --user-data-dir=$HOME/truepeople --remote-debugging-port=9222 --remote-allow-origins=http://localhost:9222 --blink-settings=imagesEnabled=false"
        chrome_process = subprocess.Popen(command, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                          stderr=subprocess.DEVNULL, close_fds=True)
        time.sleep(5)

        all_doc_id = get_all_name()
        print(f"starting to scrape data for {len(all_doc_id)}")
        chrome = PyChromeDevTools.ChromeInterface()
        chrome.Network.enable()
        chrome.Page.enable()
        chrome.DOM.enable()
        chrome.Runtime.enable()
        num_ = 0
        count_ = 0
        # chrome.Network.clearBrowserCookies()
        for doc_id in all_doc_id:
            try:
                num_ += 1
                # print(f"{num_}: {doc_id['search_name']} location: {doc_id['locations_in_profile']}")
                row_id = doc_id['id']
                url = doc_id['details_page_url1']
                chrome.Page.navigate(url=url)
                event, messages = chrome.wait_event("Page.frameStoppedLoading", timeout=60)
                value = chrome.wait_event("Network.responseReceived", timeout=60)

                get_page_source_js = """
                                    function getDocumentSource() {
                                        return document.documentElement.outerHTML;
                                    }
                                    getDocumentSource();
                                """
                result = chrome.Runtime.evaluate(expression=get_page_source_js)
                html_source = result[0]['result']['result']['value']

                tree = html.fromstring(html_source)
                name_titile = tree.xpath("//article[1]/article[1]//header/p/text()")
                age = tree.xpath("//article[1]/article[1]/div[1]/div[1]/text()")
                top_phone_ = tree.xpath("//article[1]/div[1]/div[1]/p/i")
                addresses = tree.xpath("//article[1]/article[2]//li")
                phone_data = tree.xpath("//article[@class='phone-bg']")[0].xpath(".//a/text()")
                phone_list = []
                for item in top_phone_:
                    if item.text == ' - Wireless':
                        wireless_ = item.xpath("..")
                        wireless = wireless_[0].xpath(".//a/text()")
                        phone_list[0] = ['wireless', wireless[0]]
                    elif item.text == ' - ]Home/LandLine Phone':
                        landline = item.xpath("..")
                        landline2 = landline[0].xpath(".//a/text()")
                        phone_list[1] = ['home', landline2[0]]
                for each_phone in phone_data:
                    try:
                        street = each_phone.xpath(".//a/text()")
                        phone_list.append(street[0].strip())
                    except IndexError:
                        street = each_phone.text
                        phone_list.append(street.strip())

                # reported_time = each_phone.xpath("./time/text()")
                # print(street[0].strip(), reported_time[0].strip())
                addresses_list = []
                for each_address in addresses:
                    reported_time = None
                    try:
                        reported_time = each_address.xpath("./time/text()")
                        street = each_address.xpath("./a/text()")
                        # print(street[0].strip())
                        addresses_list.append([street[0].strip(), reported_time])
                    except IndexError:
                        street = each_address.text
                        # print(street.strip())
                        addresses_list.append([street.strip(), reported_time])
                        # print('dgd')

                    # print(street[0].strip(), reported_time[0].strip())

                name = name_titile[0].strip()
                age_ = age[2].strip()
                print(addresses_list)
                print('--------------------------------')
                search_people_data(row_id=row_id, listofphones1=json.dumps(phone_list), listofaddress1=json.dumps(addresses_list),
                                   alsoknownas1=None, age_from_searchpeoplefree1=age_,
                                   name_found_in_search1=name)
            except Exception as e:
                print(e)
