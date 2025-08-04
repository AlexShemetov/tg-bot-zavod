import json
import io
from typing import Dict, Any
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from bot_reader.abstract_bot import AbstractReadBot

class FileBot(AbstractReadBot):
    def __init__(self, app: Application):
        super().__init__(app)
        app.add_handler(MessageHandler(
            filters.Document.FileExtension("json"),
            self.handle_document
        ))

    def run(self) -> None:
        self.app.run_polling()

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            document = update.message.document
            file = await document.get_file()
            
            buf = io.BytesIO()
            await file.download_to_memory(buf)
            buf.seek(0)
            
            file_content = buf.read().decode('utf-8')
            data = json.loads(file_content)
                
            if not self._validate_data(data):
                await update.message.reply_text("Неверный формат данных в файле")
                return
            
            self.save_data(update.effective_chat.id, data)
            await update.message.reply_text("Данные успешно обработаны")

        except json.JSONDecodeError:
            await update.message.reply_text("Файл должен быть в формате JSON")
        except UnicodeDecodeError:
            await update.message.reply_text("Неверная кодировка файла (должен быть UTF-8)")
        except Exception as e:
            await update.message.reply_text(f"Ошибка обработки файла: {str(e)}")

    def _validate_data(self, data: Dict[str, Any]) -> bool:
        return all(key in data for key in self.PARAMETERS)