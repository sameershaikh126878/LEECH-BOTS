import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from core import download_pdf, download_video
from logs import setup_logger

logger = setup_logger()

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHANNEL_ID = -1002359983884

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 नमस्ते! PW Leech Bot चालू है। कोई वीडियो या PDF लिंक भेजो।")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("🔄 लिंक प्रोसेस हो रहा है, कृपया इंतज़ार करें...")
    try:
        if ".pdf" in url.lower():
            file_path = download_pdf(url)
        else:
            file_path = download_video(url)

        file_name = os.path.basename(file_path)
        caption = f"📥 {file_name}"

        if file_path.endswith(".pdf"):
            await context.bot.send_document(chat_id=CHANNEL_ID, document=open(file_path, 'rb'), caption=caption)
        else:
            await context.bot.send_video(chat_id=CHANNEL_ID, video=open(file_path, 'rb'), caption=caption)

        await update.message.reply_text("✅ Upload सफल रहा! चैनल में भेज दिया गया है।")
        logger.info(f"✅ Uploaded: {file_path}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")
        logger.error(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))
    print("🤖 Bot is running...")
    app.run_polling()
