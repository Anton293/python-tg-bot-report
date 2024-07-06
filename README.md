# python-tg-bot-report

The bot is designed to forward messages sent to the bot to a specified chat. There are bans in place to protect against spam.

## Setup

1. Download and unzip the project.
2. Edit the file /configs/config.py:
   CHANNEL_ADMINS_ID = <your group or supergroup chat_id>  # ID of channel admins
3. Start the bot:
   TOKEN_TG_BOT_REPORT=<token> python3 main.py

You can also find the group ID as shown in the picture:
![image](https://github.com/Anton293/python-tg-bot-report/assets/75950532/bbc889ab-b407-492e-855f-83396a5b1600)
In this case, the group ID is: -1234567890

### Additional commands for the administrator

1. /my_id - get your ID
2. /chat_id - get the group ID for use in CHANNEL_ADMINS_ID

