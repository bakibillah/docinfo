# import requests
import tls_client


url = "https://www.searchpeoplefree.com/find/Anjali-Gokhale-Martinez/MD/Baltimore"


session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )

# burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"112\", \"Not;A=Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0",
#                  "Sec-Ch-Ua-Platform": "\"Linux\"", "Upgrade-Insecure-Requests": "1",
#                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
#                  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#                  "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
#                  "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br",
#                  "Accept-Language": "en-US,en;q=0.9"}

cf_bm = ''
cf_clearance = '3CDR5xNggw4ZNiT483f6Ye_KjezyyZ3WRevMKw0qIxQ-1704371010-0-2-5957873b.aa5c71a8.8b6b78a2-0.2.1704371010'

headers = {
    "host": "www.searchpeoplefree.com",
    "connection": "keep-alive",
    "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"112\", \"Google Chrome\";v=\"112\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cookie": f"__cf_bm={cf_bm}; _uc_referrer=https://www.searchpeoplefree.com/?__cf_chl_tk=mQ1MHzoTAZ.45FRMB0R4_BdNIgQIrROFbP9j78uJNuM-1704367746-0-gaNycGzNC5A; _gcl_au=1.1.709943261.1704367768; _lr_retry_request=true; _lr_env_src_ats=false; _gid=GA1.2.1218252305.1704367770; _tfpvi=NTRlYjc4NDItMTM2Zi00ZWFmLTliY2QtNmFkY2U0NDE4MDBhIzMtNA%3D%3D; cf_clearance={cf_clearance}; panoramaId_expiry=1704972571318; _cc_id=b5b8ff481277641148d46eec375149b3; panoramaId=2ac709c1affb13d11a14f65ec58e185ca02c9aa41c67a6cd5bf8c3a2b4680f57; pbjs_li_nonid=%7B%7D; pbjs_li_nonid_cst=zix7LPQsHA%3D%3D; cto_bundle=QKZgW19ON0lRT0pDSFVwMjdaVkZ5aHpMc1FXaENiSWwlMkJCWXMlMkZra1JrZzVuZUJZR253UFVRWXFnMkZiV01FSndLVmRFcEpocEw1VFlXbGpMa3ZpTFQlMkZsZ3BTMFpKa3RReHlxdGdyT0F4cFprclNOeENpeHhscHl1ejdKcUM3d2ROVDN5Yw; cto_bidid=xY0yg19tM1NQSXM5dEd2NXh1THdRell3czhiTm5FMkZIb3h0Z0RhUmZDZkR4dnMlMkYxbWpxJTJGZkRMZENVYUsxWGVvTkd6V3ZRcyUyRiUyQkdFVGlzRDJGdkpyY2VSbDVMelptU3VSTHJwd2YzT0xrbzc0bkhjJTNE; gcid_first=9128add9-7d66-4f51-b913-9645a485a584; __qca=P0-1862523072-1704367771686; _au_1d=AU1D-0100-001704367776-87S83LL8-XURW; _au_last_seen_pixels=eyJhcG4iOjE3MDQzNjc3NzYsInR0ZCI6MTcwNDM2Nzc3NiwicHViIjoxNzA0MzY3Nzc2LCJydWIiOjE3MDQzNjc3NzYsInRhcGFkIjoxNzA0MzY3Nzc2LCJhZHgiOjE3MDQzNjc3NzYsImdvbyI6MTcwNDM2Nzc3NiwiaW1wciI6MTcwNDM2Nzc3Niwic29uIjoxNzA0MzY3Nzc2LCJ1bnJ1bHkiOjE3MDQzNjc3NzZ9; __gads=ID=231e88b667ed57a4:T=1704367771:RT=1704367771:S=ALNI_Mbf0BlisrAxiH-EeSFBW_KNqjcmkw; __gpi=UID=00000d345a49bae2:T=1704367771:RT=1704367771:S=ALNI_MYrPZGeymLuRVekdSIW0dBGqQdP7w; _ga=GA1.2.297123773.1704367770; _ga_829D3Z6VT7=GS1.1.1704367770.1.0.1704367798.0.0.0"
}

session.headers = {}
session.headers = headers

res = session.get(
    url,
    proxy="http://34.125.218.126:3128",
    timeout_seconds=35
    )

# response = requests.get(url, headers=headers)

print(res.text)

