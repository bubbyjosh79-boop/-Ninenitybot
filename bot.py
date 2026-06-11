import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Load local environment variables for testing
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
ai_client = OpenAI(api_key=OPENAI_API_KEY)

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "✨ **Welcome to Ninenitybot!** ✨\n\n"
        "I am your AI-powered writing assistant. Send me any rough text, "
        "and I will fix the grammar, improve the flow, and enhance its overall impact!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# AI writing logic handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Send a placeholder "typing" reaction or message
    processing_msg = await update.message.reply_text("🔄 Processing and polishing your text...")

    try:
        # Prompt telling the AI exactly how to behave as a writing assistant
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",  # Highly efficient and cost-effective model
            messages=[
                {"role": "system", "content": "You are Ninenitybot, an expert AI writing assistant. Your job is to improve, rewrite, and enhance the text provided by the user. Correct spelling and grammar errors, improve sentence structure, and make it sound elegant and natural while retaining the original meaning."},
                {"role": "user", "content": f"Please polish this text:\n\n{user_text}"}
            ]
        )
        
        enhanced_text = response.choices[0].message.content
        
        # Edit the processing message with the finalized text
        await processing_msg.edit_text(f"📝 **Enhanced Version:**\n\n{enhanced_text}", parse_mode="Markdown")

except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        await processing_msg.edit_text("❌ Oops! Something went wrong while trying to enhance your text. Please try again later.")

if __name__ == "__main__":
    # Build the Telegram application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    # Run the bot using polling mode
    print("Ninenitybot is running...")
    app.run_polling()
