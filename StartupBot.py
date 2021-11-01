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
from Commands.PriceCommand import PriceCommand
from Commands.SetCommand import SetCommand
from Commands.ShowCommand import ShowCommnand
from Commands.StartCommand import StartCommand
from DataBase.DatabaseQueries import GetAllCoins, GetAllRemainders, GetUserById, InsertReminder, InsertUser
from Services.CoinService import GetCoinPrice, GetDolarValue
from Messages import *

load_dotenv()

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

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

@bot.message_handler(commands=['start'])
def Start(message):
  StartCommand(bot, message.chat.id, message)

@bot.message_handler(commands=['delete'])
def Delete(message):
  DeleteCommand(bot, message.chat.id)

@bot.message_handler(commands=['commands'])
def Commands(message):
  bot.send_message(message.chat.id, const_commands_message)

@bot.message_handler(commands=['price'])
def Price(message):
  PriceCommand(bot, message.chat.id)

@bot.message_handler(commands=['show'])
def Show(message):
  ShowCommnand(bot, message.chat.id)
  
@bot.message_handler(commands=['set'])
def Set(message):
  SetCommand(bot, message.chat.id)

# def check():
#   bot.send_message(user_id, 'EIIII')

# def MySchedule():
#   while True:
#     print('HEII')
#     schedule.run_pending()
#     time.sleep(5)


CreateMenuOfOptions()
# schedule.every(10).seconds.do(check)

#thread.start_new_thread(MySchedule, ())

bot.infinity_polling()