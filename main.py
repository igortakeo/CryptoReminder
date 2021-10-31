from datetime import MAXYEAR
import telebot
import os
from dotenv import load_dotenv
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from DataBase.database import GetAllCoins, GetUserById, InsertUser
from Services.CoinService import GetCoinPrice, GetDolarValue

load_dotenv()

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.callback_query_handler(lambda callback_query : True)
def GetPrice(message):
  bot.delete_message(message.message.chat.id, message.message.id)
  GetPrice(message)

def CreateMenuOfOptions(): 
  listOfCommands = [
    ('start', 'Start bot'),
    ('commands', 'Commands available to bot'),
    ('show', 'Show my cryptocurrencies'),
    ('price', 'Get price of cryptocurrencies'),
    ('delete', 'Delete one cryptocurrency'),
  ]

  listOfBotsCommands = []

  for command in listOfCommands:
    listOfBotsCommands.append(BotCommand(command[0], command[1]))

  bot.set_my_commands(listOfBotsCommands)

@bot.message_handler(commands=['start'])
def Start(message):

  InsertUser(
    message.from_user.id, 
    message.from_user.first_name,
    message.from_user.last_name,
    message.from_user.username)

  user = GetUserById(message.from_user.id)[1]

  start_message = """
  Hi {} !!\nThis is a bot that analyze the cryptocurrency prices, he will notify you when the price that you choose it was achieved.\n
  /commands: to see commands available
  /help: everthing about the bot"""

  bot.send_message(message.chat.id, start_message.format(user))

@bot.message_handler(commands=['commands'])
def Commands(message):
  commands_message = """ 
  Commands available:\n
  /choose: to choose a cryptocurrency
  /show: to show the cryptocurrencies choosed
  /price: get price of cryptocurrencies
  /delete: to delete a cryptocurrency choosed"""

  bot.send_message(message.chat.id, commands_message)

def GetPrice(message):

  price = GetCoinPrice(message.data)

  dolar_value = GetDolarValue()

  value_in_real = price*dolar_value

  price_format = '{}: R$ {:.2f}'
  bot.send_message(message.from_user.id, price_format.format(message.data, value_in_real))

@bot.message_handler(commands=['price'])
def Price(message):

  list_all_coins = GetAllCoins() 

  list_coins = []

  for coin in list_all_coins:
    list_aux = []
    list_aux.append(InlineKeyboardButton(coin[0], callback_data=coin[0]))
    list_coins.append(list_aux)

  keyboardInline = InlineKeyboardMarkup(list_coins)

  price_message = """
  Coins available:
  """
  bot.send_message(message.chat.id, price_message, reply_markup=keyboardInline)

@bot.message_handler(commands=['hello'])
def Hello(message):
  bot.reply_to(message, 'Hello Igor Takeo')
  print(message.chat.id)


bot.register_callback_query_handler(GetPrice, func=lambda callback_query : True)
bot.polling()