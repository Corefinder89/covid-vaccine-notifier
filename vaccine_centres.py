import http.client
# import sys
import json
from datetime import date

def run_api():
    jsondata = ""

    with open("data.json", "r") as jsonobj:
        jsondata = json.load(jsonobj)

    # Get the pin codes from the entered
    pincodes = jsondata.get("details").get("pincode")

    # Get the current date
    cur_date = date.today().strftime("%d-%m-%Y")

    for item in pincodes:
        data = fetch_data_api(item, cur_date)
        data_handler(data)


def fetch_data_api(zip_code, date):
    conn = http.client.HTTPSConnection("cdn-api.co-vin.in")

    payload = ""

    headers = {
        'content-type': "application/json",
        'Accept-language': "hi_IN",
    }

    conn.request("GET", f"/api/v2/appointment/sessions/public/findByPin?pincode={zip_code}&date={date}", payload, headers)

    res = conn.getresponse()

    if res.status == 200:
        data = res.read()
        return data.decode("utf-8")
    else:
        return res.reason

def data_handler(data):
    data_handler = json.loads(data)
    data_item = data_handler.get("sessions")

    # Store data as key value pair from the api data
    covid_center_info = {}
    # Store the dictionary object within the list accumulated_data
    accumulated_data = []

    if data_item:
        for data in data_item:
            covid_center_info.update({"name": data.get("name")})
            covid_center_info.update({"state": data.get("state_name")})
            covid_center_info.update({"district": data.get("district_name")})
            covid_center_info.update({"block": data.get("block_name")})
            covid_center_info.update({"pincode": data.get("pincode")})
            covid_center_info.update({"fee_type": data.get("fee_type")})
            covid_center_info.update({"capacity": data.get("available_capacity")})
            covid_center_info.update({"fee": data.get("fee")})
            covid_center_info.update({"age_limit": data.get("min_age_limit")})
            covid_center_info.update({"vaccine_type": data.get("vaccine")})
            covid_center_info.update({"slots": data.get("slots")})
        
        accumulated_data.append(covid_center_info)
        # return data in list if list is not empty
        return accumulated_data
    else:
        accumulated_data.append("No data present currently")
        # return data in list if list is empty
        return accumulated_data

run_api()