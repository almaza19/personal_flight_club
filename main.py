import requests
import os
import service
import urllib3
import pandas
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

API_KEY = os.environ["api_key"]
urllib3.disable_warnings()
IATA = []
city = []
SAMPLE_SPREADSHEET_ID = "1Ko1L1Bz7iR-dv7UIyQIq8ls7d9fdIi5q8jktus8ZDL8"
SAMPLE_RANGE_NAME = "A2:C10"


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
