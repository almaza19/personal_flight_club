import requests
import os
import urllib3
import pandas
from googleapiclient import discovery
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
SHEET_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SAMPLE_SPREADSHEET_ID}/values/{SAMPLE_RANGE_NAME}"

req = requests.get(url=URL, headers=headers, verify=False)
response_json = req.json()['locations']
for i in response_json:
    IATA.append(i["code"])
    city.append(i["name"])

    cities = {
        "code": IATA,
        "city": city,
    }
credentials = None

service = discovery.build('sheets', 'v4', credentials=credentials)
request = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
response = request.execute()
print(response)
#values = result.get('values', [])
df = pandas.DataFrame(cities)

print(df)
