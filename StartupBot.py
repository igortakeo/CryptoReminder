import time
import schedule
import telebot
import _thread as thread
import os
from dotenv import load_dotenv
from telebot.types import BotCommand
from CheckReminders import CheckReminders
from Commands.DeleteCommand import DeleteCommand
from Commands.PriceCommand import PriceCommand
from Commands.SetCommand import SetCommand
from Commands.ShowCommand import ShowCommnand
from Commands.StartCommand import StartCommand
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
    ('price', 'Get price of one cryptocurrency'),
    ('delete', 'Delete one reminder'),
    ('about', 'Informations about the bot'),
  ]

  listOfBotsCommands = []

  for command in listOfCommands:
    listOfBotsCommands.append(BotCommand(command[0], command[1]))

  bot.set_my_commands(listOfBotsCommands)

@bot.message_handler(commands=['start'])
def Start(message):
  StartCommand(bot, message.chat.id, message)

@bot.message_handler(commands=["about"])
def About(message):
  bot.send_message(message.chat.id, const_about_message)

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

def ScheduleReminders():
  CheckReminders(bot)

def ProcessSchedule():

  while True:
    try:
      schedule.run_pending()
    except:
      print('Error in process schedule')
    
    time.sleep(600)

def InitBot():
  CreateMenuOfOptions()
  bot.infinity_polling()

schedule.every(1).hours.do(ScheduleReminders)

thread.start_new_thread(ProcessSchedule, ())

thread.start_new_thread(InitBot(), ())