#import httplib2
#import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread

import sqlite3


def get_the_table(gsheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('PythonProject-f09d6a83a144.json', scope)
    gs = gspread.authorize(credentials)
    wks = gs.open(gsheet_name).sheet1
    wks_values = wks.get_all_values()
    wks_key = wks_values[0]
    wks_rows = wks_values[1:]
    #print(wks_rows)
    #print(wks_key)
    return [wks_key, wks_rows]

def save_into_db(table_data, table_name):
    conn = sqlite3.connect('db1.sqlite')
    cursor = conn.cursor()

    colomn_names = ''
    inserting_str = '('
    for i in table_data[0]:
        colomn_names += i + ' text, '
        inserting_str += '?,'
    colomn_names = colomn_names[:-2]
    inserting_str = inserting_str[:-1] + ')'

    cursor.execute(f"CREATE TABLE if not exists {table_name} ({colomn_names})")
    cursor.execute(f"DELETE FROM {table_name}")
    cursor.executemany(f"INSERT INTO {table_name} VALUES {inserting_str}", table_data[1])
    conn.commit()

def push_table_to_gsheets(table_name, doc_name):

    conn = sqlite3.connect('db1.sqlite')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}", )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print(results)

if __name__ == '__main__':
   table_data = get_the_table('Test')
   save_into_db(table_data, 'employees')
   push_table_to_gsheets('employees', 'Test')
