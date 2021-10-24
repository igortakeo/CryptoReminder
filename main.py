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
        InlineKeyboardButton('Button 1', callback_data='bitcoin'),
        InlineKeyboardButton('Button 2', callback_data='2'),
    ]
]
''''
listButtons1 = []
button = InlineKeyboardButton('Bitcoint', '/bitcoin')
listButtons1.append(button)
list.append(listButtons1)
button = InlineKeyboardButton('Ethereum', '/ethereum')
listButtons2 = []
listButtons2.append(button)  
list.append(listButtons2)
button = InlineKeyboardButton('Litecoin', '/litecoin')
listButtons3 = []
listButtons3.append(button)
list.append(listButtons3)
'''

keyboardInline = []

@bot.callback_query_handler(lambda callback_query : callback_query.data == 'bitcoin')
def callbackBitcoin(message):
  bot.delete_message(message.message.chat.id, message.message.id)
  bitcoin(message.message)

def CreateMenuOfOptions(): 
  listOfCommands = [
    ('start', 'Start bot'),
    ('commands', 'Commands available to bot'),
    ('show', 'Show my cryptocurrencies'),
    ('bitcoin', 'Get bitcoin price'),
    ('delete', 'Delete one cryptocurrency'),
  ]

  listOfBotsCommands = []

  for command in listOfCommands:
    print(command)
    listOfBotsCommands.append(BotCommand(command[0], command[1]))

  bot.set_my_commands(listOfBotsCommands)

@bot.message_handler(commands=['start'])
def start(message):

  InsertUser(
    message.from_user.id, 
    message.from_user.first_name,
    message.from_user.last_name,
    message.from_user.username)

  user = GetUserById(message.from_user.id)[1]

  keyboardInline = InlineKeyboardMarkup(list)

  start_message = """
  Hi {} !!\nThis is a bot that analyze the cryptocurrency prices, he will notify you when the price that you choose it was achieved.\n
  /commands: to see commands available
  /help: everthing about the bot"""
  bot.send_message(message.chat.id, start_message.format(user), reply_markup=keyboardInline)

@bot.message_handler(commands=['commands'])
def commands(message):
  commands_message = """ 
  Commands available:\n
  /choose: to choose a cryptocurrency
  /show: to show the cryptocurrencies choosed
  /bitcoin: get bitcoin price
  /delete: to delete a cryptocurrency choosed"""

  bot.send_message(message.chat.id, commands_message)

@bot.message_handler(commands=['bitcoin'])
def bitcoin(message):
  price = GetCoinPrice('Bitcoin')
  bot.send_message(message.chat.id, price)

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.reply_to(message, 'Hello Igor Takeo')
  print(message.chat.id)

bot.register_callback_query_handler(callbackBitcoin, func=lambda callback_query : callback_query.data == 'bitcoin')
bot.polling()