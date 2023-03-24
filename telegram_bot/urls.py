from django.urls import path, include
from telegram_bot.views import telegram_webhook

urlpatterns = [
    path('', telegram_webhook),
]
