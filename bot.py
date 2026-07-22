import os
import io
from PIL import Image
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# 🔑 আপনার টেলিগ্রাম বট টোকেন এবং গুগল এপিআই কি
TELEGRAM_BOT_TOKEN = "8984060917:AAGIHC3chsxZLVIJKFFpCb7QbPlySWNucC0"
GEMINI_API_KEY = "AQ.Ab8RN6JyjO-oDUcehq9WoGTLNQBHNRt40avDRPCHmt0R4B0sVA"

# Gemini Client চালু করা
client = genai.Client(api_key=GEMINI_API_KEY)

# /start কমান্ড দিলে যে উত্তর যাবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "স্বাগতম RN SIGNAL বটে! 📊\n"
        "আমাকে যেকোনো ক্যান্ডেলস্টিক চার্টের স্ক্রিনশট পাঠান। "
        "আমি এআই দিয়ে চার্ট বিশ্লেষণ করে ক্যান্ডেল আপে (Call) নাকি ডাউনে (Put) যাবে তা জানিয়ে দেব।"
    )

# চার্টের ছবি বিশ্লেষণ করার ফাংশন
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ছবিটি পাওয়া গেছে। এআই দিয়ে বিশ্লেষণ করা হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন...")
    try:
        # টেলিগ্রাম থেকে ছবি ডাউনলোড
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        image = Image.open(io.BytesIO(photo_bytes))
        
        # AI-এর জন্য প্রম্পট
        prompt = (
            "You are an expert candlestick chart analyst. Analyze this candlestick chart image carefully. "
            "Based on technical analysis, price action, support/resistance, and candlestick patterns, tell me:\n"
            "1. Is the next candle more likely to go UP (Call) or DOWN (Put)?\n"
            "2. What candlestick patterns or market signals do you observe in the image?\n"
            "3. Give a brief reasoning for your prediction.\n\n"
            "Please provide the response in clear and professional Bengali language."
        )
        
        # Gemini AI দিয়ে বিশ্লেষণ
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image, prompt]
        )
        
        # ফলাফল পাঠানো
        await update.message.reply_text(response.text)
        
    except Exception as e:
        await update.message.reply_text(f"দুঃখিত, কোনো সমস্যা হয়েছে: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("RN SIGNAL বট সফলভাবে চালু হয়েছে...")
    app.run_polling()

if __name__ == '__main__':
    main()
