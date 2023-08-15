#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import requests


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "savings_bot.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def set_webhook():
    bot_token = '6134564626:AAEbztmjrLySxHnz3wiRKq4_5DuSzTYotBU'
    webhook_url = 'https://d0b9-93-73-222-85.ngrok-free.app/webhook/'

    response = requests.get(
        f'https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}'
    )

    print(response.text)


if __name__ == "__main__":
    main()
    set_webhook()
