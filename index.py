from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import os

# --- Sozlamalar ---
BOT_TOKEN = "8452330949:AAE-FY9aBwNWXwvSlOwLc_HN3ibuCcS8wIk"
CHANNEL_ID = -1002677233135
STICKER_ID = "CAACAgIAAxkBAAE5KzlolgmREymPXI-BviRA_HlPPfaqdAACmxsAAhjAOEkY9cLcaS6HBTYE"

# Word fayl yo‘li (serverga yuklaganda to‘g‘ri joyga o‘zgartirasiz)
WORD_FILE_PATH = r"C:\Users\user\Desktop\MadinaFarmContact\ДОГОВОР МАДИНА ФАРМ СИНТЕЗ.docx"

# --- Menyular ---
main_menu = [
    [KeyboardButton("📝 E'tiroz va takliflar.")],
    [KeyboardButton("📞 Xodimlar bilan bog'lanish.")],
    [KeyboardButton("📍Biz haqimizda.")],
    [KeyboardButton("✒️ Hamkorlik.")],
    [KeyboardButton("📑 Dori vositalari uchun sertifikat olish.")]
]

feedback_menu = [
    [KeyboardButton("Sifat va Nazorat")],
    [KeyboardButton("Yetkazib berish")],
    [KeyboardButton("Buyurtmalarni qabul qilish (Bron)")],
    [KeyboardButton("Taminot bo‘limi xodimlari")],
    [KeyboardButton("⬅️ Orqaga")]
]

contact_menu = [
    [KeyboardButton("Rahbariyat")],
    [KeyboardButton("Sifat va Nazorat")],
    [KeyboardButton("Buyurtmalarni qabul qilish (Bron)")],
    [KeyboardButton("Yetkazib berish")],
    [KeyboardButton("Omborxona mudiri")],
    [KeyboardButton("⬅️ Orqaga")]
]

def _norm(s: str) -> str:
    return " ".join(s.strip().lower().split())

menu_responses = {
    "feedback": {
        _norm("Sifat va Nazorat"): "Sizda {text} bo‘yicha e‘tiroz va takliflaringiz bo‘lsa matn, video yoki ovozli xabar yuboring.",
        _norm("Yetkazib berish"): "Sizda {text} bo‘yicha e‘tiroz va takliflaringiz bo‘lsa matn, video yoki ovozli xabar yuboring.",
        _norm("Buyurtmalarni qabul qilish (Bron)"): "Sizda {text} bo‘yicha e‘tiroz va takliflaringiz bo‘lsa matn, video yoki ovozli xabar yuboring.",
        _norm("Taminot bo‘limi xodimlari"): "Sizda {text} bo‘yicha e‘tiroz va takliflaringiz bo‘lsa matn, video yoki ovozli xabar yuboring."
    },
    "contact": {
        _norm("Rahbariyat"): "Rahbariyat bilan bog‘lanish uchun: +998000000000",
        _norm("Sifat va Nazorat"): "Sifat va nazorat bo‘limi bilan bog‘lanish uchun: +998914149200",
        _norm("Buyurtmalarni qabul qilish (Bron)"): "Buyurtma bo‘limi bilan bog‘lanish uchun: +998655056505",
        _norm("Yetkazib berish"): """👨‍💼 Yetkazib berish bo`limiga mas`ul xodim.
📞 +998934767476 Abduraxmon

📍 Buxoro shahar va Gazli hududi.
📞 +998954403300 Mavlonov Murod

📍 Kogon tumani, Zarafshon va Zafarobod hududlari.
📞 +998952203300 Ahmedov Alimuhammad

📍Olot va Qorako`l tumanlari.
📞 +998954469900 Nabiyev Ohunjon

📍Jondor va Qorako`l tumanlari.
📞 +998952204400 Safarov Nurali

📍Gijduvon tumani 1-2
📞 +998952208800 Qurbonov Mahmud

📍Galaosio, Rometan va Peshku tumanlari.
📞 +998952209900 Sulaymonov Javohir

📍Vobkent va Shofirkon tumanlari.
📞 +998952205500 Sharipov O`tkir

📍 Navoiy shahar.
📞 +998954406600 Sulaymonov Azamat

📍 Navoiy tuman.
📞 +998952206600 Hasanov Azizbek

📍Samarqand viloyati.
📞 +998954401100 Vasiyev Shuhrad
""",
        _norm("Omborxona mudiri"): "Omborxona mudiri bilan bog‘lanish uchun:\n+998933590378\n+998914416995"
    },
    "main": {}
}

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_sticker(STICKER_ID)
    except Exception:
        pass

    desc_text = "Doim biz bilan bo`ling!"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 IOS", url="https://apps.apple.com/us/app/madina-farm/id6739846964")],
        [InlineKeyboardButton("📱 Android", url="https://play.google.com/store/apps/details?id=com.mpsintez.madinapharmsintez_app")],
        [InlineKeyboardButton("🌐 Instagram sahifamiz", url="https://www.instagram.com/mps_bukhara?igsh=ZG9hejlweWlydHRv")],
        [InlineKeyboardButton("📢 Telegram Kanal", url="https://t.me/MadinaFarm")]
    ])

    await update.message.reply_text(desc_text, reply_markup=keyboard, parse_mode="HTML")
    await update.message.reply_text("🏪 Iltimos dorixonangiz nomini yozing.")
    context.user_data["waiting_reply_after_salom"] = True

# --- Xabarlarni boshqarish ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_raw = update.message.text or ""
    text_norm = _norm(text_raw)

    # Har qanday xabarni kanalda forward qilish
    try:
        await update.message.forward(chat_id=CHANNEL_ID)
    except Exception as e:
        print("Forward xatosi:", e)

    if context.user_data.get("waiting_reply_after_salom"):
        context.user_data["waiting_reply_after_salom"] = False
        context.user_data["menu"] = "main"
        keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text("Kerakli bo‘limni tanlang 👇", reply_markup=keyboard)
        return

    # 📝 E'tiroz va takliflar
    if text_norm == _norm("📝 e'tiroz va takliflar."):
        context.user_data["menu"] = "feedback"
        keyboard = ReplyKeyboardMarkup(feedback_menu, resize_keyboard=True)
        await update.message.reply_text("Kerakli bo‘limga murojaat qiling 👇", reply_markup=keyboard)
        return

    # 📞 Xodimlar bilan bog'lanish
    if text_norm == _norm("📞 xodimlar bilan bog'lanish."):
        context.user_data["menu"] = "contact"
        keyboard = ReplyKeyboardMarkup(contact_menu, resize_keyboard=True)
        await update.message.reply_text("Kerakli bo‘limga murojaat qiling 👇", reply_markup=keyboard)
        return

    # 📍 Biz haqimizda
    if text_norm == _norm("📍biz haqimizda."):
        await update.message.reply_text("Madina Farm Sintez — 2013-yildan beri sog‘lig‘ingiz posboni! 10 kishilik jamoa sifatida yo‘lga chiqqan biz, bugun 150 dan ortiq malakali xodim bilan Buxoro, Navoiy, Samarqand, Toshkent, Qashqadaryo va Surxandaryo viloyatlaridagi dorixonalarga sifatli dori vositalarini yetkazib beramiz. Sizning salomatligingiz — bizning ustuvor vazifamiz!")
        await update.message.reply_location(latitude=39.74431634817175, longitude=64.48376947514521)
        return

    # 📑 Sertifikat olish
    if text_norm == _norm("📑 dori vositalari uchun sertifikat olish."):
        await update.message.reply_text("Sertifikat olish uchun murojaat qiling:\n+998912439200\n+998913119200")
        return

    # ✒️ Hamkorlik — Word fayl yuborish
    if text_norm == _norm("✒️ hamkorlik."):
        if os.path.exists(WORD_FILE_PATH):
            await update.message.reply_document(document=open(WORD_FILE_PATH, "rb"))
        else:
            await update.message.reply_text("❌ Fayl topilmadi. Administrator bilan bog‘laning.")
        return

    # ⬅️ Orqaga
    if text_norm == _norm("⬅️ orqaga"):
        context.user_data["menu"] = "main"
        keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        await update.message.reply_text("Asosiy menyu 👇", reply_markup=keyboard)
        return

    # Feedback menyusi
    if context.user_data.get("menu") == "feedback":
        resp = menu_responses["feedback"].get(text_norm)
        if resp:
            await update.message.reply_text(resp.format(text=text_raw))
        else:
            await update.message.reply_text("✅ Murojaatingiz qabul qilindi. Tez orada ko‘rib chiqamiz.")
        return

    # Contact menyusi
    if context.user_data.get("menu") == "contact":
        resp = menu_responses["contact"].get(text_norm)
        if resp:
            await update.message.reply_text(resp)
            return

    await update.message.reply_text("Menyudan tugmani tanlang 🔘")

# --- Botni ishga tushirish ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
