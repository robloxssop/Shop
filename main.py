import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# โหลด Environment Variable
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

app = Client("my_bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

# --- ข้อมูลโปร ---
PRO_DATA = {
    "rov_ios": "🛒 โปร ROV IOS\nราคา: 30-700💸\nฟังก์ชัน: ESP, โชว์เลือด, กันแบน ...\nลิงก์ Telegram: https://t.me/yourchannel",
    "rov_ad": "🛒 โปร ROV AD\nราคา: 20-299💸\nฟังก์ชัน: Hack Map, Auto Punish ...\nลิงก์ Telegram: https://t.me/yourchannel",
    "ff_ios": "🛒 โปร ฟีฟาย IOS\nราคา: 100-750฿\nฟังก์ชัน: Aimbot, ESP ...\nลิงก์ Telegram: https://t.me/yourchannel",
    "ff_ad": "🛒 โปร ฟีฟาย AD\nราคา: 20-500💸\nฟังก์ชัน: AimKill, Ghost Hack ...\nลิงก์ Telegram: https://t.me/yourchannel",
}

# --- คำสั่งเริ่ม / เรียกเมนู ---
@app.on_message(filters.command("start"))
async def start(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("ROV IOS", callback_data="rov_ios"),
         InlineKeyboardButton("ROV AD", callback_data="rov_ad")],
        [InlineKeyboardButton("ฟีฟาย IOS", callback_data="ff_ios"),
         InlineKeyboardButton("ฟีฟาย AD", callback_data="ff_ad")]
    ])
    await message.reply("เลือกโปรเกมที่คุณต้องการ:", reply_markup=keyboard)

# --- ตอบข้อความทั่วไป (ไม่ใช่คำสั่ง /command) ---
@app.on_message(filters.text & ~filters.command())
async def reply_text(client, message):
    text = message.text.lower()
    if "rov" in text:
        await message.reply("เลือก AD หรือ IOS\nAD: /rov_ad\nIOS: /rov_ios")
    elif "ฟีฟาย" in text:
        await message.reply("เลือก AD หรือ IOS\nAD: /ff_ad\nIOS: /ff_ios")
    else:
        await message.reply("ไม่พบข้อมูลโปรเกมนี้")

# --- จัดการปุ่มกด Inline Keyboard ---
@app.on_callback_query()
async def button(client, callback_query):
    data = callback_query.data
    if data in PRO_DATA:
        await callback_query.message.edit_text(PRO_DATA[data])
    else:
        await callback_query.answer("ไม่พบข้อมูลโปรนี้", show_alert=True)

# รันบอท
app.run()
