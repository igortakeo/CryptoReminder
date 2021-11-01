from datetime import MAXYEAR
from logging import error
from time import sleep
import time
import schedule
import telebot
import _thread as thread
import os
import uuid
from dotenv import load_dotenv
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from Commands.DeleteCommand import DeleteCommand
from Commands.StartCommand import StartCommand
from DataBase.database import GetAllCoins, GetAllRemainders, GetUserById, InsertReminder, InsertUser
from Services.CoinService import GetCoinPrice, GetDolarValue

load_dotenv()

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

#Messages

commands_message = """ 
Commands available:\n
/show: to show reminders
/set: to set a reminder
/price: get price of cryptocurrencies
/delete: to delete a reminder"""

set_message = """Choose one coin:"""

price_message = """Coins available:"""

delete_message = """Choose one reminder to delete:"""

set_reminder_message = """Type the price you want to be notified !"""

error_message = """
Entrada inválida !
Digite Novamente
"""
reminder_saved_message = """Reminder saved \U00002705"""

#Utilities

def CreateMenuOfOptions(): 
  listOfCommands = [
    ('start', 'Start bot'), 
    ('commands', 'Commands available to bot'),
    ('show', 'Show my reminders'),
    ('set', 'Set a reminder'),
    ('price', 'Get price of cryptocurrencies'),
    ('delete', 'Delete one reminder'),
  ]

  listOfBotsCommands = []

  for command in listOfCommands:
    listOfBotsCommands.append(BotCommand(command[0], command[1]))

  bot.set_my_commands(listOfBotsCommands)


def GetListOfCoins():

  list_all_coins = GetAllCoins() 

  list_coins = []

  for coin in list_all_coins:
    list_aux = []
    list_aux.append(InlineKeyboardButton(coin[0], callback_data=coin[0]))
    list_coins.append(list_aux)

  return list_coins

def GetPrice(message):

  price = GetCoinPrice(message.data)

  dolar_value = GetDolarValue()

  value_in_real = price*dolar_value

  price_format = '{}: R$ {:.2f}'
  bot.send_message(message.from_user.id, price_format.format(message.data, value_in_real))

def SetReminder(message):
  
  reminder_message_reply = bot.send_message(message.from_user.id, set_reminder_message)
  bot.register_next_step_handler(reminder_message_reply, ProcessReminder, message.data)

def is_valid(n):
  try:
    float(n)
  except ValueError:
    return False
  else:
    return True

def ProcessReminder(message, coin):

  try:
    price = message.text

    if is_valid(price):
      InsertReminder(str(uuid.uuid1()), message.from_user.id, coin, price)
      bot.reply_to(message, reminder_saved_message)
      return

    else:
      bot.reply_to(message, error_message)

      bot.register_next_step_handler(message, ProcessReminder, coin)

  except Exception as e:
    bot.reply_to(message,'Erro')

#Callback functions

@bot.callback_query_handler(lambda callback_query : callback_query.message.text == price_message)
def GetPriceCallback(message):

  bot.delete_message(message.message.chat.id, message.message.id)
  GetPrice(message)

@bot.callback_query_handler(lambda callback_query : callback_query.message.text == set_message)
def SetReminderCallback(message):

  bot.delete_message(message.message.chat.id, message.message.id)
  SetReminder(message)


#Commands functions

@bot.message_handler(commands=['start'])
def Start(message):
  StartCommand(bot, message.chat.id, message)

@bot.message_handler(commands=['delete'])
def Delete(message):
  DeleteCommand(bot, message.chat.id)

@bot.message_handler(commands=['commands'])
def Commands(message):
  bot.send_message(message.chat.id, commands_message)

@bot.message_handler(commands=['price'])
def Price(message):

  keyboardInline = InlineKeyboardMarkup(GetListOfCoins())

  bot.send_message(message.chat.id, price_message, reply_markup=keyboardInline)

@bot.message_handler(commands=['show'])
def Show(message):

  list_reminders = GetAllRemainders(message.chat.id)
  return_message = ''

  for reminder in list_reminders:
    aux_message = '{} - R$ {:.2f}\n'
    return_message += aux_message.format(reminder[2], reminder[3])

  bot.send_message(message.chat.id, return_message)
  

@bot.message_handler(commands=['set'])
def Set(message):

  keyboardInline = InlineKeyboardMarkup(GetListOfCoins())

  bot.send_message(message.chat.id, set_message, reply_markup=keyboardInline)

@bot.message_handler(commands=['hello'])
def Hello(message):
  bot.reply_to(message, 'Hello Igor Takeo')
  print(message.chat.id)

# def check():
#   bot.send_message(user_id, 'EIIII')

# def MySchedule():
#   while True:
#     print('HEII')
#     schedule.run_pending()
#     time.sleep(5)


CreateMenuOfOptions()
# schedule.every(10).seconds.do(check)
bot.register_callback_query_handler(GetPriceCallback, func=lambda callback_query : callback_query.message.text == price_message)
bot.register_callback_query_handler(SetReminderCallback, func=lambda callback_query : callback_query.message.text == set_message)

#thread.start_new_thread(MySchedule, ())

bot.infinity_polling()