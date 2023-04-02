from telegram.ext import CommandHandler, MessageHandler, Filters


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Welcome to the LeetCode bot! Use the /help command to see what I can do.",
    )


def help(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Here are the commands I understand:\n/daily - Get today's LeetCode problems\n/news - Get the latest LeetCode news",
    )


def daily(update, context):
    # Get the daily problems from the LeetCode API and send them to the user
    daily_problems = get_daily_problems()
    message = "Here are today's LeetCode problems:\n"
    for problem in daily_problems:
        message += f"{problem['title']} - {problem['url']}\n"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


def news(update, context):
    # Get the latest news from the LeetCode discussion page and send it to the user
    latest_news = get_latest_news()
    message = "Here are the latest LeetCode news items:\n"
    for news_item in latest_news:
        message += f"{news_item['title']} - {news_item['url']}\n"
    context.bot.send_message(chat_id=update.message.chat_id, text=message)


start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
daily_handler = CommandHandler("daily", daily)
news_handler = CommandHandler("news", news)
unknown_handler = MessageHandler(Filters.command, unknown)
