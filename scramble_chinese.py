from __future__ import print_function
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import sys
import random
import argparse


def get_args(argv = None):
    """
    Defining options to be passed from command line
    """
    # Load Chinese characters if option is passed through
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--chinese',
        action = 'store_true',
        help = 'Read Chinese column from sheet'
        )

    # Change number of output lines (defaults to 15 lines)
    parser.add_argument(
        '-n', '--noutput',
        type = int,
        default = 15,
        help = 'Number of lines in output (defaults to 15)'
        )

    return parser.parse_args()


def scramble_words(noutput):
    """
    Shuffle words in new_list
    Print reordered words by newline
    Note: Clear is used for ipython in terminal
    """
    os.system('clear')
    random.shuffle(new_list)
    print( )
    print("\n\n".join(new_list[:noutput]))
    print( )


def retrieve_words(first_column, second_column):
    """
    Use Google Sheets API to retrieve values
    Passing in arguments on which column to retrieve
    """
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID,
                                    range=SHEET_RANGE).execute()
    my_list = result.get('values', [])

    # Sending output into list format
    for row in my_list:
        new_list.append('%s, %s' % (row[first_column], row[second_column]))

    scramble_words(args.noutput)


if __name__ == '__main__':

    print("Initializing: calling to Google Sheets")

    # Setting scope, and specifying Google workbook and sheet name
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

    # This SHEET_ID is the name in your url
    SHEET_ID = '<hidden for privacy purposes>'
    SHEET_RANGE = 'words!B:D'

    # Accessing google account to read the workbook
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('sheets', 'v4', credentials=creds)

    # Defining a few empty variables for later use
    first_column = ()
    second_column = ()

    my_list = []
    new_list = []

    # Start the program checking switches (if any) used
    args = get_args(sys.argv)

    if args.chinese:
        retrieve_words(2, 1)
    else:
        retrieve_words(1, 0)
