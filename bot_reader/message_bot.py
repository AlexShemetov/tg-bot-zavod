from bot_reader.abstract_bot import AbstractReadBot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)

class MessageBot(AbstractReadBot):
    
    def run(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.button_click))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_value_input))
        self.app.run_polling()
    
    @classmethod
    def create_keyboard(cls, user_data: dict) -> InlineKeyboardMarkup:
        keyboard = []
        for param, name in cls.PARAMETERS.items():
            value = user_data.get(param, "?")
            button_text = f"{name}: {value}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=param)])
        if set(cls.PARAMETERS.keys()).issubset(user_data.keys()):
            keyboard.append([InlineKeyboardButton("Сохранить результаты", callback_data="save")])
        return InlineKeyboardMarkup(keyboard)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        reply_markup = self.create_keyboard(context.user_data)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Выберите параметр для ввода или изменения",
            reply_markup=reply_markup
        )

    async def button_click(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        if query.data == "restart":
            await self.start(update, context)
            return
        if query.data == "save":
            self.save_data(
                update.effective_chat.id,
                context.user_data
            )
            context.user_data.clear()
            keyboard = [[InlineKeyboardButton("Заполнить заново", callback_data="restart")]]
            await query.edit_message_text(
                "Хотите заполнить форму заново?",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
        context.user_data["param"] = query.data
        await query.edit_message_text(f"Введите значение для {self.PARAMETERS[query.data]}:")

    async def handle_value_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            param = context.user_data["param"]
            value = int(update.message.text)
            context.user_data[param] = value
            reply_markup = self.create_keyboard(context.user_data)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Значение сохранено!",
                reply_markup=reply_markup
            )
        except ValueError:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Введите число!"
            )