#!/usr/bin/python
import requests
import os
import random
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


class Datacollector:
    def collector(self):
        req_proxy = RequestProxy()  # you may get different number of proxy when  you run this at each time
        proxies = req_proxy.get_proxy_list()  # th
        ind_proxies = []  # int is list of Indian proxy
        for proxy in proxies:
            if proxy.country == 'India':
                ind_proxies.append(proxy.get_address())

        try:
            # public endpoint of cowin to find centres using pin code
            endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"

            querystring = {
                "pincode": os.getenv("pincode"),
                "date": "31-03-2021"
            }

            proxy = {
                "http": "http://"+str(random.choice(ind_proxies)),
                "https": "http://"+str(random.choice(ind_proxies))
            }

            headers = {
                "content-type": "application/json",
                "Accept-language": "hi_IN"
            }

            response = requests.request("GET", endpoint, headers=headers, params=querystring, proxies=proxy)
            print(response.status_code)
            print(response.json())
        except Exception as e:
            print(e)


d = Datacollector()
d.collector()



