import os.path
import pickle
import pprint
from collections import defaultdict

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def login():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', 
                ['https://www.googleapis.com/auth/spreadsheets.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def key(t):
    try:
        cabin = int(t[3])
    except:
        return (0, 0)
    deck = int(cabin / 1000)
    if cabin % 2 == 0:
        return (deck, cabin)
    else:
        return (deck, -cabin)


def get_teammates():
    creds = login()
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(
            spreadsheetId='15GO3ULXRCch83uhF9LPGB-2irMHhj9wIXL4hBUaqVNQ',
            range='2024 Kraken Post TEAM ALLOCATION!A8:F357').execute()
    values = result.get('values', [])
    
    name_to_teams = defaultdict(list)
    team_to_names = defaultdict(list)
    for team_and_no, name, preferred, cabin, boat_section, considerations in (a for a in values if len(a) == 6):
        _, _, team = team_and_no.partition('. ')
        name_to_teams[name].append(team)
        team_to_names[team].append((team, name, preferred, cabin, boat_section, considerations))

    for team_and_no, name, preferred, cabin, boat_section in (a for a in values if len(a) == 5):
        _, _, team = team_and_no.partition('. ')
        name_to_teams[name].append(team)
        team_to_names[team].append((team, name, preferred, cabin, boat_section, 'N/A'))

    teammates = {}
    for name in name_to_teams.keys():
        teammates[name] = sorted((person for team in name_to_teams[name] for person in team_to_names[team] if person[1] != name), key=key)

    return teammates


if __name__ == '__main__':
    with open('teammates.pickle', 'wb') as f:
        pickle.dump(get_teammates(), f)

