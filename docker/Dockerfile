# Use an official Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY docker/requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Set the environment variable for the bot token
ENV TELEGRAM_BOT_TOKEN="your_bot_token_here"

# Set the environment variable for the Leetcode API key and base URL
ENV LEETCODE_API_KEY="your_api_key_here"
ENV LEETCODE_API_URL="https://leetcode.com/api/"

# Expose the port on which the Telegram bot will listen for incoming messages
EXPOSE 8443

# Run the Telegram bot when the container launches
CMD ["python", "bot/telegram_bot.py"]
