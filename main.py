import os
from bot import Bot
from dotenv import load_dotenv

def main():
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        raise ValueError("Bot token not found")
    bot = Bot(TOKEN)
    bot.run()

if __name__ == "__main__":
    main()