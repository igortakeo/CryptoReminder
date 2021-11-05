from DataBase.DatabaseQueries import DeleteReminder, GetAllReminders
from Services.CoinService import GetCoinPrice, GetDolarValue
from Messages import *

class CheckReminders:

    def __init__(self, bot):
        self.bot = bot
        self.dolar_value = GetDolarValue()
        self.ProcessReminders()


    def ProcessReminders(self):
        
        print('Started Process Reminders...')

        list_reminders = GetAllReminders()
        coin = 'Coin'
        price = 0.0

        for reminder in list_reminders:

            id_reminder = reminder[0]
            user_id = reminder[1]
            coin_reminder_name = reminder[2]
            coin_reminder_price = reminder[3]
            option_coin_reminder = reminder[4]

            if coin_reminder_name != coin:
                coin = coin_reminder_name
                price = GetCoinPrice(coin)*self.dolar_value
        
            if option_coin_reminder == 'higher':

                if price > coin_reminder_price:
                    self.bot.send_message(user_id, const_price_is_higher.format(
                        coin_reminder_name,
                        coin_reminder_price,
                        price
                    ))

                    DeleteReminder(id_reminder)

            else:

                if price < coin_reminder_price:
                    self.bot.send_message(user_id, const_price_is_lower.format(
                        coin_reminder_name,
                        coin_reminder_price,
                        price
                    ))

                    DeleteReminder(id_reminder)

        print('Finished Process Reminders')