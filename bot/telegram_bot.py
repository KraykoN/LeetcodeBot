import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from leetcode.leetcode_api import get_user_progress, get_username_from_database, get_daily_problems, get_latest_news

# Create a Telegram bot instance
bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])


# Define a command handler for the /start command
def start(update, context):
    update.message.reply_text(
        "Welcome to the Leetcode bot! Type /help to see available commands."
    )


# Define a command handler for the /help command
def help(update, context):
    update.message.reply_text(
        """/daily - Get daily Leetcode problems\n
        /progress - Get your Leetcode progress\n
        /news - Get the latest news from Leetcode"""
    )


# Define a command handler for the /daily command
def daily(update, context):
    # Get the user's Leetcode username from the database
    username = get_username_from_database(update.message.chat_id)

    # Get the daily problems from the Leetcode API
    problems = get_daily_problems(username)

    # Send the problems to the user
    for problem in problems:
        update.message.reply_text(problem["title"] + "\n" + problem["url"])


# Define a command handler for the /progress command
def progress(update, context):
    # Get the user's Leetcode username from the database
    username = get_username_from_database(update.message.chat_id)

    # Get the user's progress from the Leetcode API
    progress = get_user_progress(username)

    # Send the progress to the user
    update.message.reply_text(
        "Your Leetcode progress:\nSolved: {}\nTotal: {}\nAccuracy: {}%".format(
            progress["solved"], progress["total"], progress["accuracy"]
        )
    )


# Define a command handler for the /news command
def news(update, context):
    # Get the latest news from the Leetcode API
    news_items = get_latest_news()

    # Send the news items to the user
    for item in news_items:
        update.message.reply_text(item["title"] + "\n" + item["url"])


# Define a message handler for unknown commands
def unknown(update, context):
    update.message.reply_text(
        """Sorry, I don't understand that command.\n
        Type /help to see available commands."""
    )


# Create an updater for the bot
updater = Updater(token=os.environ["TELEGRAM_BOT_TOKEN"], use_context=True)

# Create handlers for the commands and messages
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
daily_handler = CommandHandler("daily", daily)
progress_handler = CommandHandler("progress", progress)
news_handler = CommandHandler("news", news)
unknown_handler = MessageHandler(Filters.command, unknown)

# Add the handlers to the updater
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(daily_handler)
updater.dispatcher.add_handler(progress_handler)
updater.dispatcher.add_handler(news_handler)
updater.dispatcher.add_handler(unknown_handler)

# Start the bot
updater.start_polling()
updater.idle()
