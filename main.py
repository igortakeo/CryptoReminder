from datetime import MAXYEAR
from typing import Pattern
import telebot
import os
from dotenv import load_dotenv
from telebot.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from DataBase.database import GetUserById, InsertUser
from Services.CoinService import GetCoinPrice

load_dotenv()

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)
updater = Updater(API_KEY)

list =  [
    [
      InlineKeyboardButton('Bitcoin', callback_data='Bitcoin'),
    ],
    [
      InlineKeyboardButton('Ethereum', callback_data='Ethereum'),
    ],
    [
      InlineKeyboardButton('Cardano', callback_data='Cardano'),
    ],
    [
      InlineKeyboardButton('Litecoin', callback_data='Litecoin'),
    ],
    [
      InlineKeyboardButton('Yearn Finance', callback_data='yearn.finance'),
    ],
    [
      InlineKeyboardButton('XRP', callback_data='XRP'),
    ],
]

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
  price_format = '{}: US$ {:.2f}'
  bot.send_message(message.from_user.id, price_format.format(message.data, float(price)))

@bot.message_handler(commands=['price'])
def Price(message):
  keyboardInline = InlineKeyboardMarkup(list)
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