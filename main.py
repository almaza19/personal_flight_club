from __future__ import print_function
import requests
import os

import service
import urllib3
import pandas
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials




urllib3.disable_warnings()
IATA = []
city = []


API_KEY = "adk_dkkO9ibY5SBQk-OoqcUYQ3HrG0Gu"
headers = {
    "apikey": API_KEY
}
URL = "https://tequila-api.kiwi.com/locations/query?term=paris&locale=en-US&location_types=city&active_only=true"

req = requests.get(url=URL, headers=headers, verify=False)
response_json = req.json()['locations']
for i in response_json:
    IATA.append(i["code"])
    city.append(i["name"])

    cities = {
        "code": IATA,
        "city": city,
    }
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
df = pandas.DataFrame(cities)

print(df)
