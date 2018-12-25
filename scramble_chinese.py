from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import random


def scramble():
    """
    Shuffle words in new_list
    Print reordered words by newline
    """
    os.system('clear')
    random.shuffle(new_list)
    print( )
    print("\n\n".join(new_list[:10]))
    print( )


def retrieve_words():
    """
    Use Google Sheets API to retrieve list of words
    Move words into new_list
    """

    print("Initializing: calling to Google Sheets")

    # Setting scope, and specifying Google workbook and sheet name
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # This SHEET_ID is the name in your url
    SHEET_ID = '<>'
    SHEET_RANGE = 'Sheet1!A:B'

    # accessing google account to read the workbook
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                    range=SHEET_RANGE).execute()
    my_list = result.get('values', [])

    # Sending output into list format
    for row in my_list:
        new_list.append('%s, %s' % (row[0], row[1]))

    scramble()


if __name__ == '__main__':
    my_list = []
    new_list = []
    retrieve_words()
