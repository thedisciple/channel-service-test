import time
from datetime import date
import requests
import xml.etree.ElementTree as ET                  # usd rate
import gspread                                      # google sheets API
import psycopg2                                     # SQL


#===========================================================
# initialization before getting data from google sheet
def google_sheets_initialization():
    global worksheet
    # path for google service account JSON secret key
    gc = gspread.service_account(filename='token.json')
    # open sheet by name
    sh = gc.open("test")
    # setting worksheet as sheet1
    worksheet = sh.sheet1
#===========================================================
# get ALL sheet data function
def get_sheet():
    global list_of_lists
    # getting all the data from sheet1 as list of lists
    list_of_lists = worksheet.get_all_values()
#===========================================================
# get usd rate from https://www.cbr.ru function
startdate = date.today()
def get_usd_rate():
    global startdate, usd_rate
    startdate = date.today()
    usd_rate = float(
        ET.fromstring(requests.get('https://www.cbr.ru/scripts/XML_daily.asp').text)
        .find("./Valute[CharCode='USD']/Value")
        .text.replace(',', '.'))
#===========================================================
# connection to your localhost DB (change credentials)
conn = psycopg2.connect(dbname='testdb', user='postgres', 
                        password='Dusya', host='localhost',
                        port="5432")
cur = conn.cursor()
#===========================================================
# data insert function
def data_insert():
    global conn, cur, list_of_lists
    for row in list_of_lists:
        if row == list_of_lists[0]:
            continue
        cur.execute('''INSERT INTO test_table
            (table_id, order_number, value_usd, value_rub, shipping_date)
            VALUES (%s, %s, %s, %s, %s);
            ''',
            (row[0],
            row[1],
            row[2],
            round(float(row[2])*usd_rate, 2),
            row[3]))
        conn.commit()

#===========================================================
# checking if the table "test_table" exists
cur.execute("SELECT EXISTS(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME=%s)",
            ('test_table',))
if not cur.fetchone()[0]:
    cur.execute('''CREATE TABLE test_table  
                (table_id INT,
                order_number INT,
                value_usd NUMERIC,
                value_rub NUMERIC,
                shipping_date DATE);''')
    print("Table created successfully")
conn.commit()
print("Table allready exists")

# first data insert
get_usd_rate()
google_sheets_initialization()
get_sheet()
data_insert()
print("Data inserted")

# data update loop
starttime = time.time()
current_list_of_lists = 0
while True:
    if date.today() != startdate:
        startdate = date.today()
        get_usd_rate()
    # get sheet data once per minute
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    get_sheet()
    # data insert only if sheet was updated
    if list_of_lists != current_list_of_lists:
        current_list_of_lists = list_of_lists
        cur.execute('DELETE FROM test_table;')
        data_insert()
        print("Data updated")
