import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# โหลด Environment Variable
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# สร้าง Client
app = Client(
    "my_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    parse_mode="html"
)

# --- ข้อมูลโปร ---
PRO_DATA = {
    "rov_ios": "🛒 <b>โปร ROV IOS</b>\nราคา: 30-700💸\nฟังก์ชัน: ESP, โชว์เลือด, กันแบน ...\n<a href='https://t.me/yourchannel'>คลิกที่นี่เพื่อไป Telegram</a>",
    "rov_ad": "🛒 <b>โปร ROV AD</b>\nราคา: 20-299💸\nฟังก์ชัน: Hack Map, Auto Punish ...\n<a href='https://t.me/yourchannel'>คลิกที่นี่เพื่อไป Telegram</a>",
    "ff_ios": "🛒 <b>โปร ฟีฟาย IOS</b>\nราคา: 100-750฿\nฟังก์ชัน: Aimbot, ESP ...\n<a href='https://t.me/yourchannel'>คลิกที่นี่เพื่อไป Telegram</a>",
    "ff_ad": "🛒 <b>โปร ฟีฟาย AD</b>\nราคา: 20-500💸\nฟังก์ชัน: AimKill, Ghost Hack ...\n<a href='https://t.me/yourchannel'>คลิกที่นี่เพื่อไป Telegram</a>",
}

# --- /start ---
@app.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ROV IOS", callback_data="rov_ios"),
         InlineKeyboardButton("ROV AD", callback_data="rov_ad")],
        [InlineKeyboardButton("ฟีฟาย IOS", callback_data="ff_ios"),
         InlineKeyboardButton("ฟีฟาย AD", callback_data="ff_ad")]
    ])
    await message.reply("เลือกโปรเกมที่คุณต้องการ:", reply_markup=keyboard)

# --- ตอบข้อความทั่วไป ---
@app.on_message(filters.text)
async def reply_text(client, message):
    text = message.text.lower()
    if "rov" in text:
        await message.reply("เลือก AD หรือ IOS\nAD: /rov_ad\nIOS: /rov_ios")
    elif "ฟีฟาย" in text:
        await message.reply("เลือก AD หรือ IOS\nAD: /ff_ad\nIOS: /ff_ios")
    else:
        await message.reply("ไม่พบข้อมูลโปรเกมนี้")

# --- จัดการปุ่ม Inline Keyboard ---
@app.on_callback_query()
async def button(client, callback_query):
    data = callback_query.data
    if data in PRO_DATA:
        await callback_query.message.edit_text(PRO_DATA[data])
    else:
        await callback_query.answer("ไม่พบข้อมูลโปรนี้", show_alert=True)

# --- รันบอท ---
if __name__ == "__main__":
    # start() + idle() เพื่อซิงค์เวลา
    app.start()
    print("Bot is running...")
    app.idle()
