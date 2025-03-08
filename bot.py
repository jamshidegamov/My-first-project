from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# ✅ Securely fetch token from environment variable
TOKEN: Final = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    raise ValueError("Error: TELEGRAM_BOT_TOKEN is not set in environment variables.")

BOT_USERNAME: Final = '@jamshid_egamov_bot'


# ✅ Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I'm Jamshid Egamov!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm Jamshid Egamov! Please type something so I can respond!")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')


# ✅ Response Handling
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    if 'how are you' in processed:
        return 'I am good!'
    if 'who are you' in processed:
        return 'My name is Jamshid Egamov'
    if 'what is your major' in processed:
        return 'I am currently studying at TSUE for financial technologies'

    return 'I do not understand what you wrote...'


# ✅ Handling messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    print(f'User ({update.message.chat.id}): "{text}"')

    response: str = handle_response(text)
    print('Bot:', response)

    await update.message.reply_text(response)


# ✅ Error Handling
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# ✅ Main function to run the bot
def main():
    app = Application.builder().token(TOKEN).build()

    # ✅ Adding command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # ✅ Handling messages (non-commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # ✅ Log errors
    app.add_error_handler(error)

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


# ✅ Run bot
if __name__ == "__main__":
    main()