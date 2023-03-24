import telegram
from django.apps import AppConfig
from django.conf import settings


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        webhook_url = settings.TELEGRAM_WEBHOOK_URL
        bot_token = settings.TELEGRAM_BOT_TOKEN
        bot = telegram.Bot(token=bot_token)
        bot.setWebhook(webhook_url)


