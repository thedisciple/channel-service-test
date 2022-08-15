# **channel-service-test**
## **Before sttart:**
To check how the main script is working, you will need edit access to this [google sheet](https://docs.google.com/spreadsheets/d/1ms5ogrXWULnPVnajCidj8DAScstxTqw5OtTyjZsSlNU/edit?usp=sharing) to change some data. For now such access have amkolotov@gmail.com, me, and service account from google API. If you need additional access you may contact me by Telegram: [@TheDisciple](https://t.me/thedisciple)

To solve Google Sheets API configuration problems you may use this Russian-language [guide](https://dvsemenov.ru/google-tablicy-i-python-podrobnoe-rukovodstvo-s-primerami/)
Basically you just need to do:
```
pip install gspread
```
[How to use gspred in russian](https://dvsemenov.ru/google-tablicy-i-python-podrobnoe-rukovodstvo-s-primerami/).

Also you may find ***//token.json*** file which is used for access. (Please don't use it to hack sheets from this account 🙂)

---
Next thing you need is [PostgreSQL](https://www.postgresql.org) with [pgAdmin](https://www.pgadmin.org) or some other DB administration platform installed on your local machine. Also you need to make small changes (such as password) in test.py here:
```
conn = psycopg2.connect(dbname='testdb', user='postgres', 
                        password='Dusya', host='localhost',
                        port="5432")
```
And don't forget to install SQL module:
```
pip install psycopg2
```
[Guide for psycopg2 in English](https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries)

---
Also be sure you have installed ***requests*** module for python:
```
pip install requests
```
It will help you to get currencies data from https://www.cbr.ru.

---
## **Running the script:**
To test the work of the script run ***//test.py*** making all the small changings described above.

---
## **Running the Telegram bot:**
You may find the [telegram_bot.py](//telegram_bot.py) in repository. To check how it works you need to find the bot in Telegram:

https://t.me/Channel_ServiceBot

The project was deployed on https://www.pythonanywhe free account, so I'll try to maintain the bot running daily, but if console was reset, just let me know to restart it: [@TheDisciple](https://t.me/thedisciple).
The bot has few commands which you may find in it's menu:
- /commands to get commands list
- /shippings to get current overdue shipping list
- /listening to start get notifications if you have new overdue shippings
- /stop to stop notifications

It shares all the necessary information about overdue shipppings with user.