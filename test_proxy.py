import requests


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
                print(f"The proxy {proxy} is live.")
                proxy_live_status = True
            else:
                print(f"The proxy {proxy} returned a non-200 status code: {response.status_code}")
                proxy_live_status = False
        except requests.RequestException as e:
            print(f"Error testing proxy {proxy}: {e}")
            proxy_live_status = False


proxy_to_test = '65.21.25.28:1033:UgBrYOQBMQ:Vjkf0Luidz'
test_proxy(proxy_to_test, 5)

# while not proxy_live_status:
#     proxy_live_status = test_proxy(proxy_to_test, timeout=timeout_value)
