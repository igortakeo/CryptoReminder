from DataBase.DatabaseQueries import GetUserById, InsertUser
from Messages import *

class StartCommand:

    def __init__(self, bot, user_id, message):

        self.bot = bot
        self.user_id = user_id
        self.message = message

        self.RegisterUser()
        self.InitMessage()

    def RegisterUser(self):

        InsertUser(
            self.message.from_user.id, 
            self.message.from_user.first_name,
            self.message.from_user.last_name,
            self.message.from_user.username)

    def InitMessage(self):
        
        user = GetUserById(self.user_id)[1]

        self.bot.send_message(self.user_id, const_start_message.format(user))