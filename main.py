import os
from bot import Bot
from dotenv import load_dotenv
from bot_reader.read_mode import ReadMode

def main():
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        raise ValueError("Bot token not found")
    READ_MODE = ReadMode[os.getenv('TELEGRAM_BOT_READ_MODE')]
    bot = Bot(token=TOKEN, read_mode=READ_MODE)
    bot.run()

if __name__ == "__main__":
    main()