import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Konfigurasi Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Abaikan pesan yang bukan teks
    if not update.message or not update.message.text:
        return
        
    user_text = update.message.text
    
    # Kirim indikator "typing..." di grup
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Panggil Gemini untuk menjawab
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Duh, ada error nih: {e}")

if __name__ == '__main__':
    # Ambil token dari environment variable
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(telegram_token).build()
    
    # Respons semua pesan teks
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot berjalan...")
    app.run_polling()
