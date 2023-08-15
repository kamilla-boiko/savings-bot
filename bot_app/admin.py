from django.contrib import admin

from bot_app.models import TelegramUser, Saving

admin.site.register(TelegramUser)
admin.site.register(Saving)
