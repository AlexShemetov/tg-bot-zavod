import logging
from logging import Logger
from bot_reader.read_mode import ReadMode
from bot_reader.message_bot import MessageBot
from bot_reader.file_bot import FileBot
from telegram.ext import Application

class Bot:
    def __init__(self, *, token: str, read_mode: ReadMode) -> None:
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        self.logger: Logger = logging.getLogger(__name__)
        self.__read_mode: ReadMode = read_mode
        self.app: Application = Application.builder().token(token).build()

    def run(self) -> None:
        if self.__read_mode == ReadMode.FILE:
            FileBot(self.app).run()
        elif self.__read_mode == ReadMode.MESSAGE:
            MessageBot(self.app).run()
        else:
            raise ValueError(f"read mode: {self.__read_mode} unsupported")
