import uuid
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, MessageAutoDeleteTimerChanged
from DataBase.DatabaseQueries import GetAllCoins, InsertReminder
from Messages import *

class SetCommand:

    coin = ''
    price = 0.0

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

        self.bot.register_callback_query_handler(
            self.SetHigherOrLower, 
            func=lambda callback_query : callback_query.message.text == const_choose_higher_or_lower
        )

    def SetReminderCallback(self, message):

        self.bot.delete_message(message.message.chat.id, message.message.id)
        
        self.SetRemainder(message)

    def CancelSetRemainder(self, message):
        self.coin = ""
        self.price = 0.0

        self.bot.delete_message(message.message.chat.id, message.message.id)
        
        self.bot.clear_step_handler_by_chat_id(self.user_id)

        self.bot.send_message(message.message.chat.id, const_canceled_message)

    def SetHigherOrLower(self, message):

        if(message.data == 'cancel'):
            self.CancelSetRemainder(message)
        else:
            self.bot.delete_message(message.message.chat.id, message.message.id)
            
            InsertReminder(str(uuid.uuid1()), message.from_user.id, self.coin, self.price, message.data)

            self.bot.send_message(message.message.chat.id, const_reminder_saved_message)

    def SetRemainder(self, message):

        self.cancel_remainder = InlineKeyboardMarkup(self.CreateCancelButton())
        self.coin = message.data
        reminder_message_reply = self.bot.send_message(message.from_user.id, const_set_reminder_message, reply_markup=self.cancel_remainder)
        print(reminder_message_reply)
        self.bot.register_next_step_handler(reminder_message_reply, self.ProcessReminder, reminder_message_reply.chat.id, reminder_message_reply.id)

    def ProcessReminder(self, message, chat_to_delete, message_to_delete):

        try:
            price = message.text

            if self.is_valid(price):
                self.price = price

                buttons_higher_and_lower = InlineKeyboardMarkup(self.CreateHigherAndLowerButton())

                self.bot.delete_message(chat_to_delete, message_to_delete)

                self.bot.send_message(message.from_user.id, const_choose_higher_or_lower, reply_markup=buttons_higher_and_lower)

                return
            else:
                self.bot.delete_message(chat_to_delete, message_to_delete)

                error_message = self.bot.send_message(message.from_user.id, const_error_message, reply_markup=self.cancel_remainder)
                self.bot.register_next_step_handler(message, self.ProcessReminder, error_message.chat.id, error_message.id)

        except Exception as e:
            self.bot.reply_to(message, 'Error in the application')


    def CreateCancelButton(self):

        cancel_button = []
        cancel_button_row = []

        cancel_button_row.append(InlineKeyboardButton(const_cancel_set_remainder_message, callback_data='cancel'))

        cancel_button.append(cancel_button_row)

        return cancel_button

    def CreateHigherAndLowerButton(self):

        hl_button = []
        hl_button_row = []
        cancel_button_row = []
        
        higher_message = 'Higher than R$ {:.2f}'
        lower_message = 'Lower than R$ {:.2f}'

        hl_button_row.append(InlineKeyboardButton(higher_message.format(float(self.price)), callback_data='higher'))
        hl_button_row.append(InlineKeyboardButton(lower_message.format(float(self.price)), callback_data='lower'))
        cancel_button_row.append(InlineKeyboardButton(const_cancel_set_remainder_message, callback_data='cancel'))


        hl_button.append(hl_button_row)
        hl_button.append(cancel_button_row)

        return hl_button


    def is_valid(self, n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return True