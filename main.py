import logging
import os
import pytz

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
except ImportError as e:
    raise ImportError(
        f"This script requires python-telegram-bot v20+. "
        f"Please install with: pip install python-telegram-bot[all]. Error: {e}"
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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

ESP มองทะลุ

รีเซ็ตบัญชี GUEST

ป้องกันสตรีม(อัดคลิป / ไม่เห็นโปร)

กันแบน ViP ไม่ติดดำ เล่นได้ยาวๆ

Aimbot ที่ปรับแต่งได้ (FOV, ความเร็ว, ระยะ, ล็อค, กำหนดเอง, ไม่ล็อคตัวที่ล้ม)
คำเตือน !

ตัวโปรเป็นไฟล์  iPA สิ่งสำคัญคือต้องเปิดโหมดนักพัฒนา ถึงจะใช้ได้

ถ้าไม่มีคอม ต้องซื้อแอพ Gbox  250บาท เพื่อติดตั้ง  ใช้งานได้1วัน ถึง1ปีแล้วแต่ดวง ถ้าเพิกถอนต้องซื้อใหม่

ติดตั้งผ่านคอมฟรีไม่เสียเงินเพิ่ม (ต้องมีคอมและสายชาร์จที่ต่อเข้าคอมได้)""",
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

HG CHEATS APK MOD
▪️ ราคาขาย ❗️
• 1 วัน 50💸
• 10 วัน 200💸
• 20 วัน 350💸

🛠️ อัปเดต MOD APK ใหม่แล้ว! 🛠️

✅ ไม่ต้องใช้ VPN อีกต่อไป
🎯 เพิ่ม AimKill
👁️ เพิ่ม Visible Aim
⚡️ แฮ็กความเร็ว
🛡️ เพิ่ม Anti-screening (แบบทั่วไป)
🖥️ รวม Emulator bypass
🧩 แก้ไขปัญหา Crash เรียบร้อยแล้ว

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

GAMES_LIST = ["rov", "ฟีฟาย", "pubg"]

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN_HERE")
TELEGRAM_LINK = os.getenv("TELEGRAM_LINK", "https://t.me/YOUR_TELEGRAM_USERNAME_HERE")

async def start(update: Update, context: CallbackContext) -> None:
    message = getattr(update, "message", None)
    if message:
        await message.reply_text(
            f"สวัสดีครับ!\n"
            f"ผมคือบอทอัตโนมัติสำหรับดูข้อมูลโปรเกม\n"
            f"เกมที่มีตอนนี้คือ: {', '.join(GAMES_LIST)}\n"
            f"สนใจข้อมูลเกมไหน พิมพ์ชื่อเกมมาได้เลยครับ"
        )

async def handle_message(update: Update, context: CallbackContext) -> None:
    message = getattr(update, "message", None)
    if message and getattr(message, "text", None):
        text = message.text.lower()
        user_data = getattr(context, "user_data", {})
        current_game = user_data.get("current_game")

        if current_game:
            if text in ("ad", "ios"):
                product_key = f"{current_game}_{text}"
                if product_key in PRO_DATA:
                    await message.reply_text(PRO_DATA[product_key])
                    await message.reply_text(f"สนใจสั่งซื้อหรือสอบถามเพิ่มเติม ติดต่อได้ที่นี่ครับ: {TELEGRAM_LINK}")
                else:
                    await message.reply_text(f"ขออภัยครับ ยังไม่มีข้อมูลสำหรับ {current_game.upper()} {text.upper()}")
                if "current_game" in user_data:
                    del user_data["current_game"]
            else:
                await message.reply_text("กรุณาพิมพ์ 'ad' หรือ 'ios' เพื่อดูข้อมูลครับ")
        elif text in GAMES_LIST:
            await message.reply_text(
                f"คุณสนใจโปรเกม {text.upper()} ใช่ไหมครับ?\n"
                f"ตอนนี้มีสำหรับ AD หรือ IOS ครับ? (พิมพ์ ad หรือ ios)"
            )
            user_data["current_game"] = text
        else:
            await message.reply_text(
                "ขออภัยครับ ไม่เข้าใจคำสั่ง กรุณาลองพิมพ์ชื่อเกมที่มี "
                "(เช่น rov, ฟีฟาย) หรือพิมพ์ /start เพื่อเริ่มใหม่ครับ"
            )

def main() -> None:
    # Set timezone to UTC for APScheduler compatibility
    os.environ["TZ"] = "UTC"
    
    # Try to create application with proper timezone handling
    try:
        # Create JobQueue with pytz UTC timezone
        from telegram.ext import JobQueue
        job_queue = JobQueue()
        job_queue.scheduler.configure(timezone=pytz.UTC)
        
        application = Application.builder().token(TOKEN).job_queue(job_queue).build()
    except Exception as e:
        print(f"Error with job queue: {e}")
        # Fallback: try without job queue
        try:
            application = Application.builder().token(TOKEN).build()
        except Exception as e2:
            print(f"Error creating application: {e2}")
            return
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=None)

if __name__ == "__main__":
    main()
    
