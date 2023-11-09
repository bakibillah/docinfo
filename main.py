import requests
from bs4 import BeautifulSoup

reese84 = "3:cIofc3/HCM467nGqn3Znog==:6yerje8P6XSic7uRFKxKLWBXj+dQLCcqD6BZPg1Vb8aGpRiQngvhotV2p432PYHfCA4RU6tnb7rsG+n9gyRqvNcQ/winLd5XyIuUoefg3G4K/stZZAxohbqxm4ZXhF5U/MNoTKox08cXzEN9OggJX8LS3jO71gS3ntLlcOsWNWIFDwjk6Rnmv/4vbwyWhzCqY+Gmp0Rq/hOTUzQnUh20+fw88jgfPB6Q/LsVc3Jut6R7c63ztDhl6g13dIWCa7a8rzMp6J9h+tRhQs226pmsKVYeF1YBjk67MAaJaDk6wSfXIDDqvuHCKOsskmRIJCDp3idT6O5jty7wHtvIFzeCZlAw0xMchFABXLAkciYTExlJmNBfCRyY5HIasOE1vyXhcDtnUk/a8SpDebL3bY3qpgDOT9yPRNvfxfMjeZ9iRt5kEEzmzJPpFpJ+4E7W9aUqnxTkT8q9W+xUz+Bmghhs1K1zFYpc8wqdIZwucMdimtwi5COU7I+daNSbNCwfFSg+:izS2eaY5Dyr0GsqPDMmg5BRCmpxRa8IC3qBmz/OWMOc="


def scrape_doc():
    docname = "MICHAEL%20J%20ANTONINI"
    usstate = "California"
    session = requests.session()
    session.proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080',
               }
    session.headers = {}
    session.headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Linux\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.docinfo.org/", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
    # session.headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}

    # session.proxies = {
    #     'http': 'http://tareqsani:as598249@138.197.224.38:15582',
    #     'https': 'http://tareqsani:as598249@138.197.224.38:15582',
    #            }

    url = f"https://www.docinfo.org:443/api/docinfo/typeahead?docname={docname}&usstate={usstate}&practype=all"
    cookies = {"visid_incap_2587692": "", "incap_ses_1702_2587692": "", "nlbi_2587692": "", "reese84": reese84, "ASP.NET_SessionId": "", "ARRAffinity": "", "ARRAffinitySameSite": "", "nlbi_2587692_2147483392": "", "ai_user": "", "_ga_NTPKCKQSFL": "", "_ga": "", "_gid": "", "_gat_UA-40572798-14": "1", "ai_session": ""}
    doc_ids_res = session.get(url, cookies=cookies, verify=False)
    if doc_ids_res.status_code == 403:
        return
    json_doc_id = doc_ids_res.json()
    for item in json_doc_id:
        docname = item['Name']
        doc_id = item['Id']

        # docname = "MICHAEL%20J%20ANTONINI"

        burp0_url = f"https://www.docinfo.org:443/search/docprofile?docid={doc_id}&docname={docname}&usstate={usstate}&practype=all"
        burp0_cookies = {"visid_incap_2587692": "", "incap_ses_1702_2587692": "", "nlbi_2587692": "", "ASP.NET_SessionId": "", "ARRAffinity": "", "ARRAffinitySameSite": "", "ai_user": "", "_gid": "", "incap_ses_1370_2587692": "", "_ga_NTPKCKQSFL": "", "_ga": "", "ai_session": "", "nlbi_2587692_2147483392": "", "reese84": reese84}
        session.headers = {}
        session.headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9"}
        res = session.get(burp0_url, cookies=burp0_cookies, verify=False)
        html_source = res.text

        soup = BeautifulSoup(html_source, 'html.parser')
        elems = soup.find('div', class_='profile__subheading').text
        profile_sections = soup.find_all('div', class_='profile__section')
        for elem in profile_sections:
            headline = elem.find('h2').text.strip()
            if headline == 'Education':
                print(elem.find('p').text)
            elif headline == 'Certifications':
                all_certification = elem.find_all('ul')
                for each_certification in all_certification:
                    print('certification: ', each_certification.text)
            elif headline == 'Active Licenses':
                all_active_licenses = elem.find_all('ul')
                for all_active_license in all_active_licenses:
                    print('active license: ', all_active_license.text)
            elif headline == 'Actions':
                all_actions = elem.find_all('ul')
                for all_action in all_actions:
                    print(all_action.text)


scrape_doc()
