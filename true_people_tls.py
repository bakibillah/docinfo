
import tls_client

session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )

cookies = {
    'cookieconsent_status': 'dismiss',
    'cf_clearance': '1436xwseApLEsGsKRJdbMgp5dyHHrscRACf38mzb8H0-1702299172-0-1-ace9ea27.d4d1f179.fbe8b5c7-160.0.0',
    '__cf_bm': '1QWBvpzrnC.Xa63pY8WNvNhsMbgFevu5E7GJWw8e17Y-1702298208-1-AQqxM0eBEza8E3dhTBVbCphHWi6JnoUQOJL84DSIqijdDMqIZ/roJyz4kM2U1rJ6Ms+rNSan1ZgtxaOhlmRZbY0=',
    '_ga': 'GA1.1.1132983443.1702298209',
    '_ga_JB1DKYFLTX': 'GS1.1.1702298209.1.1.1702298244.0.0.0',
}

headers = {
    'authority': 'www.truepeoplesearch.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7,it;q=0.6',
    # 'cookie': 'cookieconsent_status=dismiss; cf_clearance=pYTuYx.lSWR9fpUkOe.U3BdTnCKaqxqu6XWaVY8K4eo-1702298195-0-1-284b3fa7.639819ea.7f4a6047-160.0.0; __cf_bm=1QWBvpzrnC.Xa63pY8WNvNhsMbgFevu5E7GJWw8e17Y-1702298208-1-AQqxM0eBEza8E3dhTBVbCphHWi6JnoUQOJL84DSIqijdDMqIZ/roJyz4kM2U1rJ6Ms+rNSan1ZgtxaOhlmRZbY0=; _ga=GA1.1.1132983443.1702298209; _ga_JB1DKYFLTX=GS1.1.1702298209.1.1.1702298244.0.0.0',
    'referer': 'https://www.truepeoplesearch.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'service-worker-navigation-preload': 'true',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


url = 'https://www.truepeoplesearch.com/results?name=Burney%20William%20Gibson&citystatezip=Irving,%20TX'

session.headers = {}
session.headers = headers
res = session.get(url, proxy=f"http://9BeAXC3urY:ZFyLXaE14k@65.21.25.28:1039", cookies=cookies, timeout_seconds=10)

data = res.text
