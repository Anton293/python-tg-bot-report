"""Config file for telegram bot"""
import json

# Load config from file
try:
    with open("configs/banned.json", "r") as file:
        data = json.load(file)
        BANNED_LIST_USERS = data["banned"]
        BANNED_LIST_USERS_INFO = data["banned_info"]
except (FileNotFoundError, json.decoder.JSONDecodeError):
    BANNED_LIST_USERS = []
    BANNED_LIST_USERS_INFO = {}
    with open("configs/banned.json", "w") as file:
        json.dump({"banned": [], "banned_info": {}}, file)


CHANNEL_ADMINS_ID = -4074318227  # ID of channel admins


print("[INFO] Config success loaded!")
print("[INFO] List Banned users:", BANNED_LIST_USERS)
