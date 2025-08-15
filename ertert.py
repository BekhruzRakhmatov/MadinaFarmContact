from telegram import Bot

BOT_TOKEN = "8452330949:AAE-FY9aBwNWXwvSlOwLc_HN3ibuCcS8wIk"
bot = Bot(token=BOT_TOKEN)

updates = bot.get_updates()
for u in updates:
    print(u.message.chat.id)
