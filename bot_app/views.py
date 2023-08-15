from decimal import Decimal

import telebot
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bot_app.models import TelegramUser, Saving
from savings_bot.settings import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)


def send_welcome_message(message, created):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    response = (
        f"Welcome, {first_name} {last_name}!"
        if created
        else f"Welcome back, {first_name} {last_name}!"
    )

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["View Profile", "View Savings", "Add Saving", "Delete Saving"]
    for button in buttons:
        keyboard.add(telebot.types.KeyboardButton(button))

    bot.send_message(message.chat.id, response, reply_markup=keyboard)


def handle_messages(message, action):
    user_id = message.from_user.id
    try:
        telegram_user = TelegramUser.objects.get(user_id=user_id)  # Get user from the database
        action(message, telegram_user)
    except ObjectDoesNotExist:  # Handle case when user is not found
        bot.send_message(message.chat.id, "User not found. Please register first.")
    except Exception as e:  # General error handling
        bot.send_message(message.chat.id, "An unexpected error occurred. Please try again.")
        print(f"Error in handle_messages: {str(e)}")


def handle_profile(message, telegram_user):
    savings = Saving.objects.filter(user=telegram_user)
    total = sum(saving.amount for saving in savings)

    result = "PROFILE\n"
    result += "====================\n"
    result += f"First name: {telegram_user.first_name}\n"
    result += f"Last name: {telegram_user.last_name}\n"
    result += f"Username: {telegram_user.username}\n"
    result += f"Money: {total}"

    bot.send_message(message.chat.id, result)


def handle_show(message, telegram_user):
    savings = Saving.objects.filter(user=telegram_user)

    result = ""
    total = 0

    for i, saving in enumerate(savings):
        result += f"{i + 1}. {saving.name}:   {saving.amount}\n"
        total += saving.amount

    result += f"======================\nTOTAL AMOUNT: {total}"

    bot.send_message(message.chat.id, result)


def handle_add(message, telegram_user):
    bot.send_message(message.chat.id, "Enter the name:")
    bot.register_next_step_handler(message, process_name_step, telegram_user)


def process_name_step(message, telegram_user):
    name = message.text.capitalize()

    bot.send_message(message.chat.id, "Enter the amount:")
    bot.register_next_step_handler(message, process_amount_step, telegram_user, name)


def process_amount_step(message, telegram_user, name):
    try:
        print(f"Processing amount step for user: {telegram_user}, name: {name}")
        amount = Decimal(message.text)

        existing_saving = Saving.objects.filter(name=name, user=telegram_user).first()
        print("Existing saving:", existing_saving)

        if existing_saving:
            print(
                f"Updating existing saving: {name}: {existing_saving.amount} + {amount}"
            )
            existing_saving.amount += amount
            existing_saving.save()
            bot.send_message(
                message.chat.id,
                f"Updated existing record. {name}: {existing_saving.amount}",
            )
        else:
            print(f"Creating new saving: {name}: {amount}")
            saving = Saving.objects.create(name=name, amount=amount, user=telegram_user)
            bot.send_message(
                message.chat.id, f"Saved new record. {saving.name}: {saving.amount}"
            )
    except ValueError:
        bot.send_message(
            message.chat.id, "Invalid amount. Please enter a valid number."
        )


def handle_delete(message, telegram_user):
    bot.send_message(message.chat.id, "Enter the name you want to delete:")
    bot.register_next_step_handler(message, process_delete_step, telegram_user)


def process_delete_step(message, telegram_user):
    name = message.text.capitalize()

    try:
        saving = Saving.objects.get(name=name, user=telegram_user)  # Get saving with the given name

        saving.delete()
        bot.send_message(message.chat.id, f"Delete existing record: {name}")
    except ObjectDoesNotExist:  # Handle case when saving is not found
        bot.send_message(message.chat.id, f"There is not this saving name: {name}")
    except ValueError:  # Handle value error
        bot.send_message(message.chat.id, "Invalid value. Please enter a valid name.")
    except Exception as e:  # General error handling
        bot.send_message(message.chat.id, "An unexpected error occurred. Please try again.")
        print(f"Error in process_delete_step: {str(e)}")


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        json_str = request.body.decode("UTF-8")
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
    return JsonResponse({"status": "ok"})


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    telegram_user, created = TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
        },
    )
    send_welcome_message(message, created)


@bot.message_handler(
    func=lambda message: message.text
    in ["View Profile", "View Savings", "Add Saving", "Delete Saving"]
)
def handle_menu_actions(message):
    actions = {
        "View Profile": handle_profile,
        "View Savings": handle_show,
        "Add Saving": handle_add,
        "Delete Saving": handle_delete,
    }
    action = actions.get(message.text)
    if action:
        handle_messages(message, action)


@bot.message_handler(func=lambda message: True)  # This will catch all messages
def unknown_command(message):
    known_commands = ["View Profile", "View Savings", "Add Saving", "Delete Saving"]
    if message.text not in known_commands:
        usage_guide = (
            "Unknown command. Here's how to use the bot:\n"
            "/start - Register or welcome back user\n"
            "Or use next buttons:\n"
            "View Profile - View your profile information\n"
            "View Savings - View your savings\n"
            "Add Saving - Add a saving record\n"
            "Delete Saving - Delete a saving record\n"
        )
        bot.send_message(message.chat.id, usage_guide)
