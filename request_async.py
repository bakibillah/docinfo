import asyncio
import time
import os
import aiohttp
import aiofiles
from aiohttp import *
url_list = ["https://www.docinfo.org:443/search/docprofile?docid=7C468AA8-A15F-4951-A14F-07119858FD7D&token="]

proxy_local = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

url = "https://www.docinfo.org:443/search/docprofile?docid=7C468AA8-A15F-4951-A14F-07119858FD7D&token="


async def fetch(session, url, count, reese84, user_agent):
    proxy_url = "http://127.0.0.1:8080"

    url = "https://www.docinfo.org:443/search/docprofile?docid=7C468AA8-A15F-4951-A14F-07119858FD7D&token="
    cookies = {"visid_incap_2587692": "3n9C89pRS0+q8/LPzqhGZM4/S2UAAAAAQkIPAAAAAABpA5m7gCuOEJTyChRFVc5k",
                     "ai_user": "gyGvY|2023-11-08T08:13:43.810Z",
                     "incap_ses_872_2587692": "GpbeYCpitGrNjKgHe/gZDM2RWWUAAAAAw8XP52ZclsuF7KcGALfbMw==",
                     "nlbi_2587692": "9pWPR9eiJh+XIFULFRmBVgAAAADYP86A08Z/fjrPa0bLnKMO",
                     "ASP.NET_SessionId": "wja3fwiefmxkrkzzgoimdm5y",
                     "ARRAffinity": "251713a3670669a2347c83bc0d84771de48ec74a2bdedef060afe0819af03e24",
                     "ARRAffinitySameSite": "251713a3670669a2347c83bc0d84771de48ec74a2bdedef060afe0819af03e24",
                     "_gid": "GA1.2.996957047.1700368858",
                     "incap_ses_452_2587692": "5DRaGBI3d2Ubny39WdVFBrCTWWUAAAAA1jFVesZHSi1961g9B8HIgw==",
                     "incap_sh_2587692": "gZRZZQAAAAA2uhIXBgAQganmqgabkJYUJmmPGIIEuGArqKY2",
                     "incap_ses_198_2587692": "Jrf7W4ChRTkyigfTg3C/AoGUWWUAAAAAixFST2dRkHCQvFqYax9Kfg==",
                     "incap_ses_1579_2587692": "HhzqWahGoEXXkcewubzpFRSVWWUAAAAADjd68dMNx/++oc79NbOupQ==",
                     "reese84": "3:IA3dY0t2fQGjcrvmPTCxOg==:1aVQocuUVMhHfPY/fAV7xtnkDlrcREtdelDnkysmjb57Q7Drl4fIXOOh3rA9VS04dqa3TwtSyaakKDJD4mUKa51DW6I3ZIHZe/K2BfhpmLhZhDrogN3b321VauS2APOXlfSFczbuPhU2LYprmvMJJHOSjrNOhmIY7wMXvxt0auIOwYKV/G0FK2bqPOnBV4RoFoNLb2qZRhmxpSj1iiJgojNDIyvxEYXLB5NIXoFDQbvg11FfgurvGlmavQRcNKyHM7vpGoxpVxjhqe5MQFV6cIzLV3xRX2/d9WMB1yBcwTt5si2/6HjihxGmB8sxyREbDC93QwIvTCgqkoGCQ86JwPg2NDwxzjHFHuMG1a0GWQOHn9hqTvwrNi9h1hAXRqqdbzFMJPgJ3YPCorzA0AaaZM7DuCgkU6FxpKt3ZD462NEpFc7KZDgEbHGQIdAtdMwy1C4q6LLiyNgqeSTF9tYAzwX4K14ZVxWVbtujiclk0JsyRC46ur8j+o6NJsVYPFqE:NyIOmLYOJzbOAb89HBbHmI6+i27iu9kaY2b6JGu6rlE=",
                     "nlbi_2587692_2147483392": "2JobNflNm325wCtcFRmBVgAAAAAZ1V6Ldcut6SkspKP/cziz",
                     "ai_session": "Zyql4|1700368859739|1700370641840.7",
                     "_ga_NTPKCKQSFL": "GS1.1.1700368857.10.1.1700370642.0.0.0", "_ga": "GA1.1.2032412878.1699431226"}
    headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"",
                     "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1",
                     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                     "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                     "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
                     "Accept-Language": "en-US,en;q=0.9"}

    # async with session.get(url, headers=headers, cookies=cookies) as response:
    async with session.get(url, headers=headers, cookies=cookies, proxy=proxy_url) as response:
        data = response.status
        print(f"{count}-{data}")
        if response.status == 200:
            html_content = await response.text()
            async with aiofiles.open(f'html_files/output-{count}.html', mode='w', encoding='utf-8') as file:
                await file.write(html_content)
            print(f'{count} - HTML content saved successfully.')
        else:
            print(f'Failed to retrieve content. Status code: {response.status}')


async def main_request(token_value, user_agent):

    reese84 = token_value
    output_directory = "html_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        for count, url in enumerate(url_list, 1):
            task = fetch(session, url, count, reese84, user_agent)
            tasks.append(task)

        await asyncio.gather(*tasks)


asyncio.run(main_request("token_value", user_agent="user_agent"))


import requests

session = requests.session()

