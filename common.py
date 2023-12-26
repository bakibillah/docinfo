import time
import requests
from bs4 import BeautifulSoup


def clear_cookies_except_domain(chrome_, domain_to_keep="google.com"):
    cookies = chrome_.Network.getAllCookies()[0]['result']['cookies']
    cookies_to_clear = [cookie["name"] for cookie in cookies if domain_to_keep not in cookie["domain"]]

    # for cookie_name in cookies_to_clear:
    chrome_.Network.deleteCookies(name='reese84')

    cookies = chrome_.Network.getCookies()
    print(f"Cookies after clearing: {cookies}")


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


def get_cookie(chrome_, ip_, proxy_to_test):
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
        print(while_count)
        if while_count > 20:
            print('now break')
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
                            chrome_.Network.clearBrowserCookies()
                            # chrome_.Network.deleteCookies({'name': 'reese84'})
                            # clear_cookies_except_domain(chrome_)
                            # cookies = chrome_.Network.getCookies()
                            # print(f"Cookies after clearing: {cookies}")
                            chrome_.Page.navigate(url="https://www.jsonip.com/")
                            return token_value
                    # break
            else:
                cookies = chrome_.Network.getAllCookies()
                for cookie in cookies[0]['result']['cookies']:
                    if cookie['name'] == 'reese84':
                        token_value = cookie['value']
                        chrome_.Network.clearBrowserCookies()
                        # clear_cookies_except_domain(chrome_)
                        # cookies = chrome_.Network.getCookies()
                        # print(f"Cookies after clearing: {cookies}")
                        chrome_.Page.navigate(url="https://www.jsonip.com/")
                        return token_value
                # break
        except Exception as e:
            print(e)
    chrome_.Network.clearBrowserCookies()
    # clear_cookies_except_domain(chrome_)
    # cookies = chrome_.Network.getCookies()
    # print(f"Cookies after clearing: {cookies}")
    chrome_.Page.navigate(url="https://www.jsonip.com/")
