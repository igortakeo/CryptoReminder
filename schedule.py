import os
import telebot
import schedule
import time

API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['Hello'])
def hello(message):
  bot.reply_to(message, 'Hello Igor Takeo')
  print(message.chat.id)
  
def schedule_hello():
  bot.send_message('514157041', 'Hi Fera')


schedule.every(10).seconds.do(schedule_hello)

bot.polling()

while True:
  schedule.run_pending()
  time.sleep(1)

