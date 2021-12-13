# Crypto Reminder
[Crypto Reminder](https://t.me/CryptoReminder_bot) is a Telegram bot developed in Python with a PostgreSQL (not available in repository). <br/>
The purpose of the bot is send you a message when the price of cryptocurrency in your reminder is achieved and get price of the cryptocurrencies in real time. <br/>

 
The bot has a routine running in parallel to verify the prices of cryptocurrencies.
 
 
 Available more than 120 coins.

## Commands
 - /start: To init the bot
 - /commands: Commands available to bot
 - /show: Show my reminders
 - /set: Set a reminder
 - /price: Get price of one cryptocurrency
 - /delete: Delete one reminder
 - /about: Informations about the bot

## APIs
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Coin Ranking API](https://developers.coinranking.com/api/documentation)
- [Awesome API](https://docs.awesomeapi.com.br/api-de-moedas#outras-conversoe)

## Libraries
- psycopg2 2.9.1
- pyTelegramBotAPI 4.1.1
- python-dotenv 0.19.1
- requests 2.22.0
- schedule 1.1.0
