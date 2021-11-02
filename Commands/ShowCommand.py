from DataBase.DatabaseQueries import GetAllRemainders

class ShowCommnand:

    def __init__(self, bot, user_id):

        self.bot = bot
        self.user_id = user_id

        self.ShowReminders()


    def ShowReminders(self):
        
        list_reminders = GetAllRemainders(self.user_id)
        return_message = ''

        for reminder in list_reminders:
            aux_message = '{} - {} than R$ {:.2f}\n'
            return_message += aux_message.format(
                reminder[2],
                'Higher' if reminder[4] == 'higher' else 'Lower' , 
                reminder[3]
            )

        self.bot.send_message(self.user_id, return_message)