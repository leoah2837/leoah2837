from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import os

ADMIN_ID = 24357904
USER_FILE = "users.txt"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    # Store user ID
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            f.write(user_id + "\n")
    else:
        with open(USER_FILE, "r") as f:
            users = f.read().splitlines()
        if user_id not in users:
            with open(USER_FILE, "a") as f:
                f.write(user_id + "\n")

    photo_url = 'https://i.postimg.cc/m2TG919g/6210773536562332212.jpg'
    keyboard = [
        [
            InlineKeyboardButton("အောကာတွန်းရုပ်ပြ", url='https://t.me/blackpandamm'),
            InlineKeyboardButton("အစုံဖောင်းဒိုင်းကားများ", url='https://t.me/pandamm17')
        ],
        [
            InlineKeyboardButton("မြန်မာအောကားသီးသန့်", url='https://t.me/backmyanmar'),
            InlineKeyboardButton("အပြာစာအုပ်များ", url='https://t.me/aphyar_book')
        ],
        [
            InlineKeyboardButton("အင်္ဂလိပ်အောကားသီးသန့်", url='https://t.me/milfpandamm')
        ],
        [
            InlineKeyboardButton("ဂျပန်အောကားသီးသန့်", url='https://t.me/blackaphyar')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo=photo_url,
        caption="Vd ကြည့်မယ်ဆို Channel လေးအရင် join ပေးပါဗျ",
        reply_markup=reply_markup
    )

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("သင်သည် Admin မဟုတ်ပါ!")
        return

    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            users = f.read().splitlines()
        count = len(set(users))
    else:
        count = 0

    await update.message.reply_text(f"ʀᴇᴀʟ ᴛɪᴍᴇ ᴜꜱᴇʀꜱ: {count}")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("သင်သည် Admin မဟုတ်ပါ!")
        return

    if not context.args:
        await update.message.reply_text("စာသားမထည့်ရသေးပါ။ /broadcast <message>")
        return

    message = " ".join(context.args)

    if not os.path.exists(USER_FILE):
        await update.message.reply_text("User မရှိသေးပါ")
        return

    with open(USER_FILE, 'r') as f:
        user_ids = list(set(f.read().splitlines()))

    total = len(user_ids)
    success = 0
    failed = 0

    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=int(uid), text=message)
            success += 1
        except Exception:
            failed += 1

    result = (
        "ʙʀᴏᴀᴅᴄᴀꜱᴛ ʀᴇᴘᴏʀᴛ\n\n"
        f"Total Users: {total}\n"
        f"Successful: {success}\n"
        f"Failed: {failed}"
    )

    await update.message.reply_text(result)

def main():
    application = ApplicationBuilder().token("8102407777:AAFmnLdvaLGAo0Eh7Fh4r-S4vDpkv30WRcE").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("user", show_users))
    application.add_handler(CommandHandler("broadcast", broadcast))
    application.run_polling()

if __name__ == "__main__":
    main()