import requests
import os
import urllib3
import pandas
from googleapiclient import discovery
import httplib2
import pylint
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

CREDENTIALS_FILE = "arcane-icon-318919-c0d3bef62ab4.json"
API_KEY = os.environ["api_key"]
urllib3.disable_warnings()
IATA = []
city = []
today = datetime.date.today()
tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%d/%m/%Y")
months_6 = (datetime.date.today() + datetime.timedelta(days=180)).strftime("%d/%m/%Y")
print(months_6)
SAMPLE_SPREADSHEET_ID = "1Ko1L1Bz7iR-dv7UIyQIq8ls7d9fdIi5q8jktus8ZDL8"
SAMPLE_RANGE_NAME = "A2:C10"


headers = {"apikey": API_KEY}
URL = "https://tequila-api.kiwi.com/locations/query?term=paris&locale=en-US&location_types=city&active_only=true"
SEARCH_URL = f"https://tequila-api.kiwi.com/v2/search?fly_from=LON&fly_to=PAR&dateFrom={tomorrow}&dateTo={months_6}&curr=GBP&max_stopovers=0"
SHEET_URL = f"https://sheets.googleapis.com/v4/spreadsheets/{SAMPLE_SPREADSHEET_ID}/values/{SAMPLE_RANGE_NAME}"
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в google sheets api
# req = requests.get(url=URL, headers=headers, verify=False) #делаем запрос к tequila
# response_json = req.json()['locations']
# print(response_json)

service = discovery.build("sheets", "v4", http=httpAuth)
request = (
    service.spreadsheets()
    .values()
    .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
)
response = request.execute()["values"]
print(response)
df_sheets = pandas.DataFrame(response, columns=["City", "IATA Code", "Lowest Price"])
print("df sheets", df_sheets)
df_sheets_list = df_sheets.to_dict("records")  # df without index
print(df_sheets_list)
for c in df_sheets_list:
    URL_city = f"https://tequila-api.kiwi.com/locations/query?term={c['City'].lower()}&locale=en-US&location_types=city&active_only=true"
    req_1 = requests.get(
        url=URL_city, headers=headers, verify=False
    )  # делаем запрос к tequila
    code_IATA = req_1.json()["locations"][0]["code"]
    IATA.append(code_IATA)
    city.append(c["City"])

    cities = {
        "code": IATA,
        "city": city,
    }

df = pandas.DataFrame(cities)
for i in cities["code"]:
    req_search = requests.get(
        url=f"https://tequila-api.kiwi.com/v2/search?fly_from=IST&fly_to={i}&dateFrom={tomorrow}&dateTo={months_6}&curr=GBP&max_stopovers=0",
        headers=headers,
        verify=False,
    ).json()["data"]
print(req_search)
IATA_modified = [cities["code"][i : i + 1] for i in range(0, len(cities["code"]), 1)]
Body = {
    "values": IATA_modified,
}
result = (
    service.spreadsheets()
    .values()
    .update(
        spreadsheetId=SAMPLE_SPREADSHEET_ID,
        body=Body,
        valueInputOption="RAW",
        range="prices!B2:B",
    )
    .execute()
)
print(df)
