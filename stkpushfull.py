import requests
import base64
import json
from datetime import datetime
import os

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
shortcode = os.getenv('shortcode')
passkey = os.getenv('passkey') 
phone_number = "Phonenumber"    #In 254 format ie 254722000000
amount = 1    #(The amount you will pay)


api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
r = requests.get(api_url, auth=(consumer_key, consumer_secret))
try:
    r.raise_for_status()
    access_token = json.loads(r.text)['access_token']
except requests.HTTPError as e:
    print(f"Request failed with status code {r.status_code}: {r.text}")
    raise e

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
data_to_encode = shortcode + passkey + timestamp
encoded_data = base64.b64encode(data_to_encode.encode())
password = encoded_data.decode('utf-8')

payload = {
    "BusinessShortCode": shortcode,
    "Password": password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": phone_number,
    "PartyB": shortcode,
    "PhoneNumber": phone_number,
    "CallBackURL": "Callback url", 
    "AccountReference": "Robertstkdemo",
    "TransactionDesc": "Demo"
}

api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
headers = {
    "Authorization": "Bearer %s" % access_token,
    "Content-Type": "application/json"
}

response = requests.post(api_url, json=payload, headers=headers)

try:
    response.raise_for_status()
    print(response.text)
except requests.HTTPError as e:
    print(f"Request failed with status code {response.status_code}: {response.text}")
    raise e
