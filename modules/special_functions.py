"""Special functions for bot"""
import configs.config as config


def check_group(func):
    """Decorator for check user permission"""

    def wrapper(self, update, context):
        if update.message.chat.type != "private" and update.message.chat.id == config.CHANNEL_ADMINS_ID:
            func(self, update, context)

    return wrapper
