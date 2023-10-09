"""Module for report"""
from configs.config import CHANNEL_ADMINS_ID
from modules.special_functions import check_group


import json
import re
import datetime
import random


def find_user_id(text):
    """Find user id in text"""
    return re.search(f"\((.*)\)", text).group(1).strip()


#print(find_user_id("Відправник: [New user](tg://user?id=123456789)"))

class Report:
    """Class for report"""
    def save_banned_list(self):
        with open("configs/banned.json", "w") as file:
            json.dump({"banned": self.banned_list_users, "banned_info": self.banned_list_users_info}, file, indent=4, ensure_ascii=False)

    @check_group
    def ban_user(self, update, context):
        """Ban user"""
        array_input_user = update.message.text.split(" ")
        if not len(array_input_user) > 1:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Command: /ban <user_id> <reason>")
            return
        user_id = int(array_input_user[1])
        username = self.bot.get_chat(chat_id=user_id).username or ''
        first_name = self.bot.get_chat(chat_id=user_id).first_name or ''
        reason = " ".join(array_input_user[2:])
        if user_id not in self.banned_list_users:
            self.banned_list_users.append(user_id)
            self.banned_list_users_info[f"user_id__{user_id}"] = {"username": username,
                                        "first_name": first_name,
                                        "date": f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}",
                                        "reason": reason}
            self.save_banned_list()
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Користувач @{username} успішно заблокований!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Цей користувач @{username} вже заблокований!")

    @check_group
    def unban_user(self, update, context):
        """Unban user"""
        array_input_user = update.message.text.split(" ")
        if len(array_input_user) != 2:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Command: /unban <user_id>")
            return
        user_id = int(array_input_user[1])
        username = self.bot.get_chat(chat_id=user_id).username or ''
        if user_id in self.banned_list_users:
            self.banned_list_users.remove(user_id)
            del self.banned_list_users_info[f"user_id__{user_id}"]
            self.save_banned_list()
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Користувач @{username} успішно розблокований!")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Цей користувач @{username} не був заблокований!")

    @check_group
    def get_banned_users(self, update, context):
        """Count banned users"""
        result_text = "Заблоковані користувачі (max last 10):\n"
        array_keys = list(self.banned_list_users_info.keys()).copy()
        array_keys.reverse()
        if len(array_keys) == 0:
            result_text = "Заблокованих користувачів немає!"

        for i, id_user in enumerate(array_keys):
            if i > 10:  # Max view 10 last users
                break
            user = self.banned_list_users_info[id_user]
            result_text += f"👤 @{user['username']} ({id_user.split('__')[1]})\n"
            result_text += f"📅 {user['date']}\n"
            result_text += f"📝 {user['reason']}\n\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=result_text)

    def echo(self, update, context):
        """Echo all messages"""
        if update.message.chat.type == "private" and update.message.from_user.id not in self.banned_list_users:
            data = update.message.from_user
            first_name = data.first_name
            last_name = data.last_name
            username = data.username

            # Створюємо текст повідомлення в діловому стилі
            result_text = f"📬 Від: {first_name or ''} {last_name or ''}\n"
            result_text += f"👤 @{username or ''} ({data.id})\n"
            result_text += f"\n\n{update.message.text}"

            context.bot.send_message(chat_id=CHANNEL_ADMINS_ID, text=result_text)
            array_thanks_reply = [
                "Дякую, повідомлення відправлено!",
                "Дякую, я повідомлю адміністраторам про це!",
                "Спасибі, ваше повідомлення успішно надіслано.",
                "Спасибі, ми повідомимо адміністраторів про це.",
                "Ваше повідомлення прийнято, дякую за сповіщення!"
            ]
            context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(array_thanks_reply), parse_mode="Markdown")

