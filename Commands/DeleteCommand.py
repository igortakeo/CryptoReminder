from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from DataBase.DatabaseQuerys import DeleteReminder, GetAllRemainders
from Messages import *

class DeleteCommand:
    
    def __init__(self, bot, user_id):

        self.bot = bot
        self.user_id = user_id

        self.RegisterCallbacks()
        self.DeleteReminder()

    def DeleteReminder(self):

        keyboardInline = InlineKeyboardMarkup(self.GetListOfReminders())
        self.bot.send_message(self.user_id, const_delete_message, reply_markup=keyboardInline)

    def GetListOfReminders(self):

        list_all_reminders = GetAllRemainders(self.user_id) 

        list_reminders = []

        for reminder in list_all_reminders:
            list_aux = []
            button_message = '{} - R$ {:.2f}'
            list_aux.append(InlineKeyboardButton(button_message.format(reminder[2], reminder[3]), callback_data=reminder[0]))
            list_reminders.append(list_aux)

        return list_reminders

    def RegisterCallbacks(self):

        self.bot.register_callback_query_handler(
            self.DeleteReminderCallback, 
            func=lambda callback_query : callback_query.message.text == const_delete_message
        )

    def DeleteReminderCallback(self, message):

        self.bot.delete_message(message.message.chat.id, message.message.id)

        DeleteReminder(message.data)

        self.bot.send_message(self.user_id, const_reminder_removed_message)