import requests
import os
import urllib3
import pandas
from googleapiclient import discovery
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
CREDENTIALS_FILE = 'arcane-icon-318919-c0d3bef62ab4.json'
urllib3.disable_warnings()
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
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в google sheets api
# req = requests.get(url=URL, headers=headers, verify=False) #делаем запрос к tequila
# response_json = req.json()['locations']
# print(response_json)
# for i in response_json:
#     IATA.append(i["code"])
#     city.append(i["name"])
#
#     cities = {
#         "code": IATA,
#         "city": city,
#     }

service = discovery.build('sheets', 'v4', http=httpAuth)
request = service.spreadsheets().values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
response = request.execute()['values']
print(response)
df_sheets = pandas.DataFrame(response, columns=['City', 'IATA Code', 'Lowest Price'])

df_sheets_list = df_sheets.to_dict('records')
print("df_sheets_list", df_sheets_list) #df without index
for c in df_sheets_list:
    URL_city = f"https://tequila-api.kiwi.com/locations/query?term={c['City'].lower()}&locale=en-US&location_types=city&active_only=true"
    req_1 = requests.get(url=URL_city, headers=headers, verify=False)  # делаем запрос к tequila
    code_IATA = req_1.json()['locations'][0]['code']
    IATA.append(code_IATA)
    city.append(c["City"])

    cities = {
        "code": IATA,
        "city": city,
    }

df = pandas.DataFrame(cities)

IATA_modified = [cities["code"][i:i+1] for i in range(0, len(cities["code"]), 1)]
print(IATA_modified)
Body = {
    "values": IATA_modified,
}
result = service.spreadsheets().values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=Body, valueInputOption='RAW', range='prices!B2:B10').execute()
print(Body)
print(df)
