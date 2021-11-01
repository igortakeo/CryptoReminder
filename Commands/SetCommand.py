import uuid
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from DataBase.DatabaseQueries import GetAllCoins, InsertReminder
from Messages import *

class SetCommand:

    def __init__(self, bot, user_id):

        self.bot = bot
        self.user_id = user_id

        self.RegisterCallbacks()
        self.ShowCoins()

    def ShowCoins(self):

        keyboardInline = InlineKeyboardMarkup(self.GetListOfCoins())

        self.bot.send_message(self.user_id, const_set_message, reply_markup=keyboardInline)

    def GetListOfCoins(self):

        list_all_coins = GetAllCoins()

        list_coins = []

        for coin in list_all_coins:
            list_aux = []
            list_aux.append(InlineKeyboardButton(coin[0], callback_data=coin[0]))
            list_coins.append(list_aux)

        return list_coins

    def RegisterCallbacks(self):

        self.bot.register_callback_query_handler(
            self.SetReminderCallback, 
            func=lambda callback_query : callback_query.message.text == const_set_message
        )

        self.bot.register_callback_query_handler(
            self.CancelSetRemainder, 
            func=lambda callback_query : callback_query.message.text == const_set_reminder_message or callback_query.message.text == const_error_message
        )

    def SetReminderCallback(self, message):

        self.bot.delete_message(message.message.chat.id, message.message.id)
        
        self.SetRemainder(message)

    def CancelSetRemainder(self, message):

        self.bot.delete_message(message.message.chat.id, message.message.id)
        
        self.bot.clear_step_handler_by_chat_id(self.user_id)
        
        self.bot.send_message(self.user_id, const_canceled_message)
    
    def SetRemainder(self, message):

        self.cancel_remainder = InlineKeyboardMarkup(self.CreateCancelButton())

        reminder_message_reply = self.bot.send_message(message.from_user.id, const_set_reminder_message, reply_markup=self.cancel_remainder)
        self.bot.register_next_step_handler(reminder_message_reply, self.ProcessReminder, message.data)

    def ProcessReminder(self, message, coin):

        try:
            price = message.text

            if self.is_valid(price):

                InsertReminder(str(uuid.uuid1()), message.from_user.id, coin, price)
                self.bot.reply_to(message, const_reminder_saved_message)

                return
            else:
                self.bot.send_message(self.user_id, const_error_message, reply_markup=self.cancel_remainder)
                self.bot.register_next_step_handler(message, self.ProcessReminder, coin)

        except Exception as e:
            self.bot.reply_to(message, 'Error')
    

    def CreateCancelButton(self):

        cancel_button = []
        cancel_button_row = []

        cancel_button_row.append(InlineKeyboardButton('Cancel set remainder', callback_data='cancel'))

        cancel_button.append(cancel_button_row)

        return cancel_button


    def is_valid(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return True