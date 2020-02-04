import os.path
import pickle
import pprint
from jinja2 import Environment
from collections import defaultdict

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def toid(s):
    valid_chars = ''.join(c for c in s if c.isalnum() or c.isspace())
    return '-'.join(valid_chars.split())

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
    cabin = int(t[2])
    deck = int(cabin / 1000)
    if cabin % 2 == 0:
        return (deck, cabin)
    else:
        return (deck, -cabin)


def main():
    creds = login()
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(
            spreadsheetId='1mkmNYD7_YRz2qtpRio-c15HLdrNW61uTWT2Ayq1bnXg',
            range='2020 SMM Team Allocation!A7:E581').execute()
    values = result.get('values', [])
    
    name_to_teams = defaultdict(list)
    team_to_names = defaultdict(list)
    for team, name, preferred, cabin, considerations in (a for a in values if len(a) == 5):
        name_to_teams[name].append(team)
        team_to_names[team].append((name, preferred, cabin, considerations))

    # Stupid temporary(?) workaround
    for team, name, preferred, cabin in (a for a in values if len(a) == 4):
        name_to_teams[name].append(team)
        team_to_names[team].append((name, preferred, cabin, "N/A"))

    teammates = {}
    for name in name_to_teams.keys():
        teammates[name] = sorted((person for team in name_to_teams[name] for person in team_to_names[team] if person[0] != name), key=key)

    env = Environment()
    env.filters['toid'] = toid
    with open('output.jinja') as f:
        tmpl = env.from_string(f.read())
    print(tmpl.render(teammates=teammates))


if __name__ == '__main__':
    main()

