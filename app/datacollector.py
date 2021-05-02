import requests
import os


class Datacollector:
    def collector(self):
        try:
            # public endpoint of cowin to find centres using pin code
            endpoint = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin"

            querystring = {
                # "pincode": os.getenv("pincode"),
                "pincode": 301703,
                "date": "31-03-2021"
            }

            payload = ""
            headers = {
                "content-type": "application/json",
                "Accept-language": "hi_IN"
            }

            response = requests.request("GET", endpoint, data=payload, headers=headers, params=querystring)
            print(response.status_code)
            print(response.json())
        except KeyError:
            print("Key not available")


d = Datacollector()
d.collector()



