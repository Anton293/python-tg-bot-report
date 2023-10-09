"""Main"""
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
import logging
from threading import Thread
import os


from modules.report import Report
from modules.special_functions import *

from configs.config import *

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
logger_bot = logging.getLogger(__name__)


class BotThread(Thread):
    def __init__(self, bot):
        Thread.__init__(self)
        self.bot = bot

    def run(self):
        self.bot.run()


class TelegramBot(Report):
    """Head class for telegram bot"""
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.bot = Bot(token=token)
        self.dispatcher = self.updater.dispatcher
        self.banned_list_users = BANNED_LIST_USERS  # list of banned users
        self.banned_list_users_info = BANNED_LIST_USERS_INFO  # list of couple banned users

    def start(self, update, context):
        if update.message.chat.type == "private":
            print("[INFO] send message in bot!")
            print(update)  # debug
            user_name = update.effective_chat.first_name
            result_text = (f"Привіт {user_name}! Я бот для звітів. "
                           f"Відправ мені повідомлення і я його передам адміністраторам.")
            context.bot.send_message(chat_id=update.effective_chat.id, text=result_text)

    def error(self, update, context):
        logger_bot.warning('Update "%s" caused error "%s"', update, context.error)
        print(context.error)

    def chat_id(self, update, context):  # debug & settings
        """Get chat id"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Chat id: {update.effective_chat.id}")

    def my_id(self, update, context):  # debug & settings
        """Get my id"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your id: {update.message.from_user.id}")

    def add_command(self, command, func):
        self.dispatcher.add_handler(CommandHandler(command, func))

    def buttons(self, update, context):
        """Buttons"""
        query = update.callback_query
        query.answer()
        if "ban" in query.data:
            self.ban(update, context)
        elif "unban" in query.data:
            self.unban(update, context)

    def run(self):
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        #self.dispatcher.add_error_handler(self.error)
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))
        self.dispatcher.add_handler(CallbackQueryHandler(self.buttons))
        self.updater.start_polling()


if __name__ == '__main__':
    bot = TelegramBot(token=os.getenv("TOKEN_TG_BOT_REPORT"))
    bot.add_command('chat_id', bot.chat_id)  # debug & settings
    bot.add_command('my_id', bot.my_id)  # debug & settings
    bot.add_command('ban', bot.ban_user)  # ban user
    bot.add_command('unban', bot.unban_user)  # unban user
    bot.add_command('bl', bot.get_banned_users)  # banned list

    BotThread(bot).start()
    print("Bot started")
