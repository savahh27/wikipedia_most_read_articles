from objects.bot_object import Bot

bot = Bot()
bot.run()
bot.set_language()
bot.set_to_daily()
bot.set_dates("31.5.2021", "1.6.2021")
bot.grab_data()