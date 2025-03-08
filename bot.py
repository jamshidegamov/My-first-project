from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
import os
import random
import datetime

# ✅ Securely fetch token from environment variable
TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Error: TELEGRAM_BOT_TOKEN is not set in environment variables.")

BOT_USERNAME: Final = '@jamshid_egamov_bot'

# ✅ User Information (Knowledge Base)
USER_INFO = {
    "name": "Jamshid Egamov",
    "major": "Financial Technologies",
    "university": "TSUE",
    "hobbies": ["coding", "reading", "playing chess"],
    "bot_purpose": "to assist and answer questions about Jamshid Egamov."
}

# ✅ Motivational Quotes
MOTIVATIONAL_QUOTES = [
    "Believe in yourself and all that you are.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Stay positive, work hard, make it happen."
]

# ✅ Possible responses for dynamic interaction
def generate_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed or 'hi' in processed:
        return random.choice(["Hey there!", "Hello! How's your day?", "Hi! What’s up?"])
    elif 'how are you' in processed:
        return random.choice(["I'm great, thanks for asking!", "Doing awesome! How about you?", "Feeling fantastic today!"])
    elif 'who are you' in processed:
        return f"I'm {USER_INFO['name']}! A bot created to answer questions about me."
    elif 'what is your major' in processed:
        return f"I'm currently studying {USER_INFO['major']} at {USER_INFO['university']}!"
    elif 'what are your hobbies' in processed:
        return f"I enjoy {', '.join(USER_INFO['hobbies'])}. What about you?"
    elif 'tell me about yourself' in processed:
        return f"I'm {USER_INFO['name']}, studying {USER_INFO['major']} at {USER_INFO['university']}. My hobbies include {', '.join(USER_INFO['hobbies'])}."
    else:
        return random.choice([
            "Hmm, I don't fully understand that, but I'm happy to chat!",
            "That's interesting! Can you tell me more?",
            "I'm still learning, can you rephrase that?"
        ])

# ✅ Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm Jamshid Egamov's bot. Ask me anything about him!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can ask me things like 'Who are you?', 'What is your major?', or 'What are your hobbies?'")

async def send_daily_quote(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    quote = random.choice(MOTIVATIONAL_QUOTES)
    await context.bot.send_message(chat_id=chat_id, text=f"🌟 Daily Motivation: {quote}")

async def start_daily_quotes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    context.job_queue.run_daily(send_daily_quote, time=datetime.time(hour=9, minute=0, second=0), chat_id=chat_id)
    await update.message.reply_text("✅ You will receive daily motivational quotes at 9 AM!")

# ✅ Handling messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text
    response: str = generate_response(text)
    await update.message.reply_text(response)

# ✅ Error Handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[ERROR] Update {update} caused error {context.error}")

# ✅ Main function to run the bot
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("dailyquote", start_daily_quotes))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)
    
    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

# ✅ Run bot
if __name__ == "__main__":
    main()
