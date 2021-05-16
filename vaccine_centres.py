import http.client
import json
import os
import sys
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Main function to run the functions
def run_api():
    # Store the dictionary object within the list accumulated_data
    accumulated_data = []

    # Get the pin codes from json
    pincodes = get_json_info("details", "pincode")

    # Get the current date
    cur_date = date.today().strftime("%d-%m-%Y")

    # Get data based on pincodes in the json file
    for item in pincodes:
        data = fetch_data_api(item, cur_date)
        accumulated_data.append(data_handler(data))

    # Get the sender from json data
    sender = get_json_info("notification", "from")
    # Get the list of recipients
    recipients = get_json_info("notification", "recipients")
    # Get the subject of the email
    subject = get_json_info("notification", "subject")
    
    # notify the user with response
    notification_mailer(sender, recipients, subject, accumulated_data)

# API code to fetch data from api setu
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

# Data handler code to manipulate and cherry pick data from json
def data_handler(data):
    data_handler = json.loads(data)
    data_item = data_handler.get("sessions")

    # Store data as key value pair from the api data
    covid_center_info = {}

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
        
        # return data in dictionary
        return covid_center_info
    else:
        # return data in dictionary if list is empty
        covid_center_info.update({"message": "No data present currently"})
        
        return covid_center_info

# Create json file reader object
def get_json_info(parent_obj, child_obj):
    jsondata = ""
    
    with open("data.json", "r") as jsonobj:
        jsondata = json.load(jsonobj)
    
    try:
        return jsondata.get(parent_obj).get(child_obj)
    except KeyError:
        sys.exit(0)


# Mailer code to send notifications
def notification_mailer(sender, recipients, subject, data):
    from_address = sender
    to_address = recipients
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    
    # Create the message (HTML).
    html = ' '.join([str(elem) for elem in data])
    # Record the MIME type - text/html.
    part1 = MIMEText(html, 'html')
    
    # Attach parts into message container
    msg.attach(part1)
    
    # Credentials
    username = os.getenv("user_email")
    password = os.getenv("user_password") 
    
    # Sending the email
    server = smtplib.SMTP('smtp.gmail.com', 587) 
    server.ehlo()
    server.starttls()
    server.login(username,password)  
    server.sendmail(from_address, to_address, msg.as_string())  
    server.quit()

run_api()