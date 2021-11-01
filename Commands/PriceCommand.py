from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from DataBase.DatabaseQueries import GetAllCoins
from Messages import *
from Services.CoinService import GetCoinPrice, GetDolarValue

class PriceCommand:

    def __init__(self, bot, user_id):

        self.bot = bot
        self.user_id = user_id

        self.RegisterCallbacks()
        self.ShowCoins()
    
    def ShowCoins(self):

        keyboardInline = InlineKeyboardMarkup(self.GetListOfCoins())

        self.bot.send_message(self.user_id, const_price_message, reply_markup=keyboardInline)


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
            self.GetPriceCallback, 
            func=lambda callback_query : callback_query.message.text == const_price_message
        )

    def GetPriceCallback(self, message):
        
        self.bot.delete_message(message.message.chat.id, message.message.id)

        price = GetCoinPrice(message.data)

        dolar_value = GetDolarValue()

        value_in_real = price*dolar_value

        price_format = '{}: R$ {:.2f}'

        self.bot.send_message(message.from_user.id, price_format.format(message.data, value_in_real))