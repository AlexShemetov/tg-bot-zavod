import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler,
    MessageHandler, 
    filters, 
    CallbackQueryHandler, 
    ContextTypes,
)

class Bot:
    __PARAMETERS = {
        "length": "Длина",
        "width": "Ширина",
        "thickness": "Толщина",
        "time": "Время",
    }

    def __init__(self, __token: str):
        self.__token = __token
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)

    def run(self):
        app = Application.builder().token(self.__token).build()
        app.add_handler(CommandHandler("start", Bot.start))
        app.add_handler(CallbackQueryHandler(Bot.button_click))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, Bot.handle_value_input))
        app.run_polling()

    def save_data(user_id: int, user_data: dict):
        with open("data/data.csv", "a") as file:
            result = [f"{user_id}"]
            for param, _ in Bot.__PARAMETERS.items():
                result.append(f"{user_data[param]}")
            file.write(f"{','.join(result)}\n")

    def create_keyboard(user_data: dict) -> InlineKeyboardMarkup:
        keyboard = []
        for param, name in Bot.__PARAMETERS.items():
            value = user_data.get(param, "?")
            button_text = f"{name}: {value}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=param)])
        if set(Bot.__PARAMETERS.keys()).issubset(user_data.keys()):
            keyboard.append([InlineKeyboardButton("Сохранить результаты", callback_data="save")])
        return InlineKeyboardMarkup(keyboard)

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        reply_markup = Bot.create_keyboard(context.user_data)
        await update.message.reply_text(
            "Выберите параметр для ввода или изменения",
            reply_markup=reply_markup,
        )

    async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        if query.data == "save":
            Bot.save_data(
                update.effective_chat.id,
                context.user_data
            )
            context.user_data.clear()
            await query.edit_message_text("Хотите заполнить форму заново? /start")
            return
        context.user_data["param"] = query.data
        await query.edit_message_text(f"Введите значение для {Bot.__PARAMETERS[query.data]}:")

    async def handle_value_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try: 
            param = context.user_data["param"]
            value = int(update.message.text)
            context.user_data[param] = value
            reply_markup = Bot.create_keyboard(context.user_data)
            await update.message.reply_text(
                f"Значение сохранено!",
                reply_markup=reply_markup,
            )
        except ValueError:
            await update.message.reply_text("Введите число!") 
