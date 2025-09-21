import os
import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    CallbackQueryHandler,
    Filters,
)

# --- CONFIG ---
TELEGRAM_LINK = "https://t.me/Hackingshop01"

# ตั้งค่า logging เพื่อดูการทำงานของบอท
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- PRODUCT DATA ---
PRO_DATA = {
    "rov_ios": """🛒 โปร ROV IOS FLASH SHOP‼️🎮
❗️สําหรับ IOS กันรีพอร์ต+แบน
[+] กันโดนแบน 1ปี และ 1เดือน !
[+] ใช้งานง่าย มีฟังก์ชันเยอะ !
[+] กันรีพอร์ทใช้ได้จริง100%🛡️
[+] ลงผ่าน  Esign / GBOX !
[+] ไม่ต้องลบตัวเกมออก
[+] ปลอดภัยมาก ‼️
🛒 ราคาจําหน่ายโปร 💸
• 1วัน = 30💸
• 3วัน = 70💸
• 7วัน = 100💸
• 15วัน = 135💸
• 31วัน = 249💸
• 60วัน = 450💸
• ถาวรตลอดชีพ 700💸

🎯 ฟังก์ชันหลัก ⚙️
[+] แฮ็กแมพ
[+] โชว์เลือดฮีโร่
[+] โชว์คูลดาวน์
[+] มุมมองสูง(ปรับได้)
[+] กันแบน 

 🎯 เมนูมอง ⚙️
[+] แสดงเส้น
[+] แสดงเลือด
[+] แสดงระยะ
[+] แสดงกรอบแบบ 2D
[+] แสดงลูกศร
[+] แสดงคูลดาวน์
[+] ไอคอนมุมหน้าจอ
[+] แสดงชื่อ
[+] แสดงไอคอน
[+] แสดงกรอบแบบ 3D
[+] ละเว้นสิ่งที่มองไม่เห็น
[+] ไอคอนฮีโร่ / เลือดและสกิล
[+] กำหนดชื่อเอง
[+] ชื่อฮีโร่
[+] แสดงมินิแมพ

 🎯 ฟังก์ชันพิเศษ ⚙️
[+] แสดงประวัติ
[+] แบนทั้งหมด
[+] แสดงชื่อตอนเลือก / แบนฮีโร่
[+] บัคระยะสกิลไกลขึ้น
[+] แสดงรูปโปรไฟล์
[+] แสดง FPS
[+] แสดงแรงค์
[+] ซ่อนไอคอนเมนู
[+] แสดงสกิลเสริม
[+] ชนะบอทออโต้
[+] สแปมแชท(ปรับได้)

  🎯เมนูสกิน ⚙️
[+] ปลดล็อกสกิน
[+] ยกเลิกสกินเสมือน
[+] กันถ่ายจอ / อัดวิดีโอไม่เห็นโปร
[+] ปุ่มสกินเลือกได้
[+] เอฟเฟกต์สังหารเลือกได้

 🎯 ล็อกเป้า ⚙️
[+] ล็อกเป้า
[+] ล็อกสกิล 1,2,3 ปรับได้
[+] ปรับระยะการล็อกเป้า
[+] ปรับความไวในการล็อกเป้า

 🎯 ออโต้ ⚙️
[+] ออโต้รำฟลอเรน คอมโบ 1 คอมโบ 2
[+] ออโต้กด Punish(ปรับได้)
[+] ออโต้กด Execute(ปรับได้)
[+] ออโต้กดแช่แข็ง(ปรับได้)
[+] ออโต้กดเพิ่มเลือดเล็ก(ปรับได้)
[+] ออโต้กดเพิ่มเลือดใหญ่ (ปรับได้)
[+] ออโต้ซื้อขายไอเทม
[+] ออโต้ซื้อไอเทม
[+] ออโต้ขายไอเทม""",
    "rov_ad": """โปรROV AD FLASH SHOP ✅
❗️สำหรับ AD 
[+] เมนูหลัก
•  HACK MAP
• มุมมองความสูง 
• แสดง คูลดาวน์
• แสดง อันติ+เลือด
• ปลดล็อก FPS
• กันแบน
• กันรายงาน
[+] เมนู ESP
• Line
• Box
• lnfor
• Alert
• lmage 
[+] เมนูล็อกเป้า
• ล็อกเป้า Skill 1 
• ล็อกเป้า Skill 2
• ล็อกเป้า Skill 3
• ปรับระยะการล็อก
• ปรับระดับคาดการณ์
[+] เมนูมอสสกิน
• ปลดล็อก สกินทั้งหมด
• ปลดล็อก ปุ่มกด+ป้ายสังหาร
• และอื่นๆอีกมากมาย
[+] เมนูออโต้
• Auto Punish
• Auto Execute
• สแปมแชทรัวๆ
• ตั้งชื่อยาว
• และอื่นๆอีกมากมาย

ราคา💸
1วัน 20
3วัน 50
7วัน 90
30วัน 180
60วัน 220
ถาวร 299
ตอนลดราคาโหดมากๆ
""",
    "ฟีฟาย_ios": """
! โปรฟีฟายค่าย 𝗙𝗹𝘂𝗼𝗿𝗶𝘁𝗲 𝗜𝗢𝗦
ราคาขาย
• 1วัน 100฿
• 7วัน 450฿
• 31วัน 750฿

ฟังชั่นโปร
- ESP มองทะลุ
- รีเซ็ตบัญชี GUEST
- ป้องกันสตรีม(อัดคลิป / ไม่เห็นโปร)
- กันแบน ViP ไม่ติดดำ เล่นได้ยาวๆ
- Aimbot ที่ปรับแต่งได้ (FOV, ความเร็ว, ระยะ, ล็อค, กำหนดเอง, ไม่ล็อคตัวที่ล้ม) 
คำเตือน !
- ตัวโปรเป็นไฟล์  iPA สิ่งสำคัญคือต้องเปิดโหมดนักพัฒนา ถึงจะใช้ได้
- ถ้าไม่มีคอม ต้องซื้อแอพ Gbox  250บาท เพื่อติดตั้ง  ใช้งานได้1วัน ถึง1ปีแล้วแต่ดวง ถ้าเพิกถอนต้องซื้อใหม่
- ติดตั้งผ่านคอมฟรีไม่เสียเงินเพิ่ม (ต้องมีคอมและสายชาร์จที่ต่อเข้าคอมได้)""",
    "ฟีฟาย_ad": """
 👑 INJECTION โปรยัด DATA ( Android ! ) 👑
▪︎ ระบบปฏิบัติการ Android - เห็นผล 100% มีการลง Path ไฟล์ต่างๆ 🛡❗️
[+] รองรับ Android 13 - 16 ☑️
[+] รองรับ Android 11 - 12 ( ที่จับคู่ Shizuku ได้ ✅️ )
[+] ANTIBAN + ANTIBLACKLIST 100% (( กัน 100% ))
[+] UI ออกแบบมาสวยใช้งานง่าย !
[+] มีการอัพเดต / ปรับปรุงไม่ปล่อยร้าง !

|| ราคาจำหน่าย ? 🎱🛒 : Cerex Modz 📮
▪︎ 1 วัน = 20.- บาท
▪︎ 3 วัน = 40.- บาท
▪︎ 7 วัน = 80.- บาท
▪︎ 15 วัน = 100.- บาท
▪︎ 31 วัน = 120.- บาท
▪︎ ใช้ได้ถึงอัพเดตใหญ่ 200.- บาท 📍
▪︎ ถาวรตลอดชีพ = 299.- บาท 🔥

☆ เป็นแบบ APK ติดตั้งแล้วใช้ได้โดยไม่ต้องทำอะไร + เสียอะไรเพิ่ม !
☆ ไม่ ROOT / แอพจำลอง !
☆ ใช้ตัวเกมใน Play Store ได้เลย !

: Menu function ☠️  [[ ฟังชั่นเมนู ]]
▪︎ สามารถใช้ได้ทั้ง FF NORMAL + FF MAX ☑️
(( 💣 ตัดเน็ตวาร์ป VPN 💣 ))
• เป้ากลางจอ เลือก UI - ปรับขนาด
• มองทะลุ V1 - V5 ( เลือกสี - เลือกตามความชอบได้ )
▪︎ มองทะลุแบบโหลดทรัพยากร / มองแบบไม่โหลดทรัพยากร
▪︎ ดูดหัว VIP มีการลงไฟล์ ไม่กลวง !
▪︎ และลูกเล่นอื่นๆอีกมากมาย !
• ไฟล์เสริมต่างๆ : ไม่ว่าจะเป็น ดูดหัว / แก้แล็ค / ช่วยลาก (( มีการลงไฟล์ทุกฟังชั่น 👑 ))
• ในอนาคตมีพัฒนาเรื่อยๆ !
------------------------------
 *HG CHEATS APK MOD*
▪️ ราคาขาย ❗️
• 1 วัน 50💸
• 10 วัน 200💸
• 20 วัน 350💸

*🛠️ อัปเดต MOD APK ใหม่แล้ว! 🛠️*

*✅ ไม่ต้องใช้ VPN อีกต่อไป*
*🎯 เพิ่ม AimKill*
*👁️ เพิ่ม Visible Aim*
*⚡️ แฮ็กความเร็ว*
*🛡️ เพิ่ม Anti-screening (แบบทั่วไป)*
*🖥️ รวม Emulator bypass*
*🧩 แก้ไขปัญหา Crash เรียบร้อยแล้ว*
------------------------------
𝗗𝗿𝗶𝗽 𝗠𝗼𝗯𝗶𝗹𝗲 𝗔𝗗
▪️ราคาขาย❗️
•  1 วัน 50💸
•  7 วัน 200💸
• 15 วัน 300💸
• 30 วัน 500💸

❗️ฟังก์ชัน ⚙️

[+] AimKill - สับปืนตาย
[+] AimKill Covre - สับปืนตายทะลุกำแพง
[+] Speed Time - วิ่งเร็ว
[+] Teleport 8M - ดึงคนเข้าหาระยะ 8 เมตร
[+] UP Player - ยกศัตรูขึ้นกลางอากาศ
[+] Ghost Hack - ถอดจิต
[+] ESP - มองทะลุต่าง ๆ
✅ รองรับ Android 64 bit ทุกรุ่น
✅ ไม่ต้องซื้ออะไรเพิ่ม / ไม่ต้องรูทเครื่อง
✅ สับปืน วิ่งเร็ว ดึงคน ถอดจิต มองทะลุ
------------------------------
โปรค่าย 𝗕𝗿-𝗠𝗼𝗱𝘀-𝗔𝗗-𝗥o̶ot(รูท)
สามารถใช้แอพจำลองได้ได้แค่แอพที่สามารถรูทได้เท่านั้น
🛒ราคาจำหน่าย💸
1 วัน 60💸
7 วัน 200💸
30 วัน 600💸
ต้องเช่า Vphone os สำคัญมาก
ราคาเช่า❗️
1เดือน ราคา110-150 💸
🎯 ฟังก์ชัน  ⚙️
▪️มองทะลุเส้น
▪️ดึงคน
▪️ล็อคหัว
▪️ กระสุนตามตัว
▪️ วิ่งไว
▪️ใช้ได้ยาวๆหนาๆ""",
    "pubg_ios": "ยังไม่มีโปรสำหรับ PUBG iOS",
    "pubg_ad": "ยังไม่มีโปรสำหรับ PUBG Android",
}

# --- HANDLERS ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "สวัสดีครับ! 👋\n"
        "พิมพ์ชื่อเกมที่ต้องการดูโปร เช่น 'rov', 'ฟีฟาย', 'pubg'"
    )

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    game_found = None
    if "rov" in text:
        game_found = "rov"
    elif "ฟีฟาย" in text or "ff" in text:
        game_found = "ฟีฟาย"
    elif "pubg" in text:
        game_found = "pubg"
    
    if game_found:
        ask_device(update, game_found)
    else:
        update.message.reply_text("ขอโทษครับ ไม่พบข้อมูลโปรของเกมนี้")

def ask_device(update: Update, game_name: str):
    keyboard = [
        [
            InlineKeyboardButton("AD (Android)", callback_data=f"{game_name}_ad"),
            InlineKeyboardButton("IOS", callback_data=f"{game_name}_ios")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        f"คุณต้องการโปรสำหรับ AD หรือ IOS?",
        reply_markup=reply_markup
    )

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    key = query.data

    if key in PRO_DATA:
        query.message.reply_text(PRO_DATA[key])
    else:
        query.message.reply_text("ไม่พบข้อมูล")

    # เพิ่มปุ่มติดต่อหลังจากแสดงข้อมูล
    contact_keyboard = [[InlineKeyboardButton("ติดต่อ Telegram เพื่อสั่งซื้อ", url=TELEGRAM_LINK)]]
    query.message.reply_text(
        "สนใจสั่งซื้อโปรแกรม ติดต่อได้ที่:",
        reply_markup=InlineKeyboardMarkup(contact_keyboard)
    )

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        logging.error("กรุณาตั้ง Environment Variable ชื่อ TELEGRAM_BOT_TOKEN ก่อนรันบอท")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    logging.info("บอทเริ่มทำงานแล้ว...")
    updater.idle()

if __name__ == "__main__":
    main()
