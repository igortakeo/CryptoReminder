from DataBase.DatabaseQueries import GetRemindersById
from Messages import *

class ShowCommnand:

    def __init__(self, bot, user_id):

        self.bot = bot
        self.user_id = user_id

        self.ShowReminders()


    def ShowReminders(self):
        
        list_reminders = GetRemindersById(self.user_id)
        return_message = ''

        if len(list_reminders) == 0:
            self.bot.send_message(self.user_id, const_dont_have_reminders)
            return

        for reminder in list_reminders:
            aux_message = '{} - {} than R$ {:.2f}\n'
            return_message += aux_message.format(
                reminder[2],
                'Higher' if reminder[4] == 'higher' else 'Lower', 
                reminder[3]
            )

        self.bot.send_message(self.user_id, return_message)