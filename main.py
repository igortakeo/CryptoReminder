import os
import telebot


API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['start'])
def start(message):

  start_message = """
  This is a bot that analyze the cryptocurrency prices, he will notify you when the price that you choose it was achieved.\n
  /commands: to see commands available
  /help: everthing about the bot"""

  bot.send_message(message.chat.id, start_message)


@bot.message_handler(commands=['commands'])
def commands(message):
  commands_message = \
  'Commands available:\n\n'\
  '/choose: to choose a cryptocurrency\n'\
  '/show: to show the cryptocurrencies choosed\n'\
  '/delete: to delete a cryptocurrency choosed\n'

  bot.send_message(message.chat.id, commands_message)

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.reply_to(message, 'Hello Igor Takeo')
  print(message.chat.id)
  

bot.polling()