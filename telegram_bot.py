#===========================================================
# https://t.me/Channel_ServiceBot (@Channel_ServiceBot)
# A Telegram bot for Channel Service shippings control.
#===========================================================
from datetime import datetime as dt
import gspread
from telegram import Bot  # pip install python-telegram-bot
from telegram.ext import Updater, CommandHandler
# Just hiding Telegram bot token from script kiddies.
# To make this script work you should create such credits.py
# with only 1 line of code:
# bot_token = 'bla-bla-bla(your token actually)'
from credits import bot_token
  
#===========================================================
# Get only overdue shipping data from sheet
def get_overdue_shipping_data():
    global overdue_shippings
    # Google Sheet API initialization
    #-----------------------------------------------------
    # path for Google service account JSON secret key
    gc = gspread.service_account(filename='token.json')
    # open sheet by name
    sh = gc.open('test')
    # setting worksheet as sheet1
    worksheet = sh.sheet1
    #-----------------------------------------------------
    # getting orders ID and shipping dates lists
    orders_ids = worksheet.col_values(2)
    shipping_dates = worksheet.col_values(4)
    overdue_shippings = []
    # taking only overdue shipping dates and their order IDs 
    for i in range(1, len(shipping_dates)):
        if dt.now() >= dt.strptime(shipping_dates[i], '%d.%m.%Y'):
            overdue_shippings.append((orders_ids[i], shipping_dates[i]))
#===========================================================
# Create box-drawing character table for messages
def message_constructon():
    message = '''║ Order ID  │Shipping Date║
=======================
'''
    for i in range(len(overdue_shippings)):
        message += '║ ' + overdue_shippings[i][0] + ' │  ' + overdue_shippings[i][1] + '    ║\n'
    message += '╚═══════╧═════════╝'
    return message

# Telegram bot API initialization
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

# /commands
def commands(update, context):
    context.bot.send_message(update.effective_chat.id,
                             '''Avaliable comands:
/commands to get commands list
/shippings to get current overdue shipping list
/listening to start get notifications
/stop to stop notifications''')

# /shippings
def get_and_send_shippings(update, context):
    get_overdue_shipping_data()
    if overdue_shippings != []:
        context.bot.send_message(update.effective_chat.id,
                                 message_constructon())
    else:
        context.bot.send_message(update.effective_chat.id,
                                 'All shippings are currently in time')

# A job for /listening
def updated_shippings(context):
    global current_overdue_shippings
    get_overdue_shipping_data()
    if overdue_shippings != current_overdue_shippings:
        current_overdue_shippings = overdue_shippings
        context.bot.send_message(context.job.context,
                                 message_constructon())

# /listening
def updates_notification(update, context):
    global current_overdue_shippings 
    context.bot.send_message(update.effective_chat.id, 'Begin!')
    current_overdue_shippings = 0 # this helps to send 1st notification
    # checking for updates once per 10 seconds
    updater.job_queue.run_repeating(updated_shippings,
                                    10, context=update.message.chat_id)

# /stop
def stop_notifications(update, context):
    context.bot.send_message(update.effective_chat.id, 'Stopped!')
    updater.job_queue.stop()

# Command handlers
commands_handler = CommandHandler('commands', commands)
shippings_handler = CommandHandler('shippings', get_and_send_shippings)
listening_handler = CommandHandler('listening', updates_notification)
stop_handler = CommandHandler('stop', stop_notifications)

# Dispatchers
dispatcher.add_handler(commands_handler)
dispatcher.add_handler(shippings_handler)
dispatcher.add_handler(listening_handler)
dispatcher.add_handler(stop_handler)

updater.start_polling()
updater.idle()