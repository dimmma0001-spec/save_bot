import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8318330106:AAG1KkHc0C-gfoRapGgWQzPm5VEN4YEKwyk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 Salom! Menga YouTube, Instagram, Facebook yoki TikTok link yuboring — men videoni yuklab beraman!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("📥 Video yuklanyapti, iltimos kuting...")

    try:
        # YT-DLP sozlamalari
        ydl_opts = {
            "outtmpl": "video.%(ext)s",
            "format": "bestvideo+bestaudio/best",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            new_name = "video.mp4"
            if os.path.exists(file_name):
                os.rename(file_name, new_name)
            elif os.path.exists(file_name.replace(".webm", ".mp4")):
                os.rename(file_name.replace(".webm", ".mp4"), new_name)

        await update.message.reply_video(video=open("video.mp4", "rb"), caption="✅ Video yuklandi!")
        os.remove("video.mp4")

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)[:200]}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("🚀 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
