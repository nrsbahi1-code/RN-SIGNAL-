import io
import os
import google.genai as genai
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# আপনার টেলিগ্রাম বট টোকেন
TELEGRAM_BOT_TOKEN = "8984060917:AAGIHC3chsxZLVIJKFFpCb7QbPlySWNucC0"

# Gemini ক্লায়েন্ট সেটআপ
client = genai.Client()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! ক্যান্ডেলস্টিক চার্টের একটি ছবি পাঠান, আমি অ্যানালাইসিস করে সিগন্যাল দিচ্ছি।")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ছবিটি পাওয়া গেছে। এআই দিয়ে বিশ্লেষণ করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    try:
        # টেলিগ্রাম থেকে ছবি ডাউনলোড
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(photo_bytes))

        # AI-এর জন্য প্রম্পট
        prompt = (
            "You are an expert candlestick chart analyst. "
            "Based on technical analysis, price action, support/resistance, tell me: "
            "1. Is the next candle more likely to go UP (CALL) or DOWN (PUT)? "
            "2. What candlestick patterns or market signals support this prediction? "
            "3. Give a brief reasoning for your prediction. "
            "Please provide the response in clear and professional Bangla language."
        )

        # Gemini AI দিয়ে বিশ্লেষণ (সঠিক মডেল নেম সহ)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[image, prompt]
        )

        # ফলাফল পাঠানো
        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"দুঃখিত, কোনো সমস্যা হয়েছে: {e}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("RN SIGNAL বট সফলভাবে চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
