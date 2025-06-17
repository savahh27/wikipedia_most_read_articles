from objects.bot_object import Bot

print("Enter dates in the following format: dd.mm.yyyy")
date1 = input("Initial date: ")
date2 = input("Final date: ")

try:
    bot = Bot()
    bot.run()
    bot.set_language()
    bot.set_to_daily()
    if date1 == "" or date2 == "":
        bot.set_dates()
    else:
        bot.set_dates(date1, date2)
    bot.grab_data()
    bot.closing()
except Exception as e:
    print("Error: " + e)