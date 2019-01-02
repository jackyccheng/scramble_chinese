from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
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
        '-c',
        '--chinese',
        action = 'store_true',
        help = 'Read Chinese column from sheet'
        )

    # Change number of output lines (defaults to 15 lines)
    parser.add_argument(
        '-n',
        '--noutput',
        type = int,
        default = 15,
        help = 'Number of lines in output'
        )

    return parser.parse_args()


def scramble_words(noutput):
    """
    Shuffle words in new_list
    Print reordered words by newline
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
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

    # This SHEET_ID is the name in your url
    SHEET_ID = '1NRIfGro5mnUXnOsW4jzygqtyfv4vGefkbG_kzq1td7E'
    SHEET_RANGE = 'words!A:C'

    # Accessing google account to read the workbook
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

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
        retrieve_words(0, 1)
