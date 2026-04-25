"""
بوت تليجرام - البحث عن الإيميل بالرقم القومي
مزاولة المهنة - دور مايو 2026
"""

import logging
from openpyxl import load_workbook
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# =============================================
BOT_TOKEN = "8760936418:AAHZ5qzI7uOPRybhwHnsMPVu1psLag45C3E"
EXCEL_FILE = "data1.xlsx"
# =============================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def load_data(filepath: str) -> dict:
    data = {}
    wb = load_workbook(filepath, read_only=True)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for row in ws.iter_rows(min_row=2, values_only=True):
            national_id = row[2]
            email = row[6]
            name = row[1]
            if national_id and email:
                key = str(national_id).strip()
                data[key] = {
                    "email": str(email).strip(),
                    "name": str(name).strip() if name else ""
                }
    wb.close()
    logger.info(f"تم تحميل {len(data)} سجل من الملف")
    return data


print("جاري تحميل بيانات الإكسيل...")
DATA = load_data(EXCEL_FILE)
print(f"تم تحميل {len(DATA)} سجل بنجاح")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "اهلاً بك!\n\n"
        "ارسل رقمك القومي (14 رقم)\n"
        "وهرد عليك بالايميل المسجل في امتحان مزاولة المهنة دور مايو 2026"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("من فضلك ارسل الرقم القومي فقط (ارقام فقط، 14 رقم)")
        return

    if len(text) != 14:
        await update.message.reply_text(
            f"الرقم القومي لازم يكون 14 رقم\n"
            f"اللي بعتته {len(text)} رقم"
        )
        return

    if text in DATA:
        record = DATA[text]
        email = record["email"]
        name = record["name"]
        await update.message.reply_text(
            f"✅ تم العثور على بياناتك!\n\n"
            f"👤 الاسم: {name}\n"
            f"📧 الايميل المسجل:\n{email}"
        )
    else:
        await update.message.reply_text(
            "❌ الرقم القومي ده مش موجود في قاعدة البيانات\n\n"
            "تاكد من صحة الرقم القومي"
        )


def main():
    print("جاري تشغيل البوت...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت شغال!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
