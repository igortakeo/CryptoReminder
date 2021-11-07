from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from DataBase.DatabaseQueries import DeleteReminder, GetRemindersById
from Messages import *

class DeleteCommand:
    
    def __init__(self, bot, user_id):

        self.bot = bot
        self.user_id = user_id

        self.RegisterCallbacks()
        try:
            self.DeleteReminder()
        except:
            self.bot.send_message(self.user_id, const_dont_have_reminders)

    def DeleteReminder(self):

        keyboardInline = InlineKeyboardMarkup(self.GetListOfReminders())
        self.bot.send_message(self.user_id, const_delete_message, reply_markup=keyboardInline)

    def GetListOfReminders(self):

        list_all_reminders = GetRemindersById(self.user_id) 

        if len(list_all_reminders) == 0:
            raise Exception('Not exist reminders')

        list_reminders = []

        for reminder in list_all_reminders:
            list_aux = []
            button_message = '{} - {} than R$ {:.2f}'
            list_aux.append(InlineKeyboardButton(
                button_message.format(
                    reminder[2],
                    'Higher' if reminder[4] == 'higher' else 'Lower',
                    reminder[3]
                ), 
                callback_data=reminder[0])
            )

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