import telebot
import os
from dotenv import load_dotenv
from DataBase.database import GetUserById, InsertUser
from Services.CoinService import GetCoinPrice

load_dotenv()

API_KEY = os.environ.get('API_KEY')
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):

  InsertUser(
    message.from_user.id, 
    message.from_user.first_name,
    message.from_user.last_name,
    message.from_user.username)

  user = GetUserById(message.from_user.id)[1]

  start_message = """
  Hi {} !!\n
  This is a bot that analyze the cryptocurrency prices, 
  he will notify you when the price that you choose it was achieved.\n
  /commands: to see commands available
  /help: everthing about the bot"""

  bot.send_message(message.chat.id, start_message.format(user))

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
  

bot.polling()