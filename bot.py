import discord
import os
import re
import asyncio

# إعداد الصلاحيات (Intents)
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

# ==================================
# الكلمات الممنوعة
# ==================================
bad_words = [
    "قحبه",
    "ازغبك",
    "امك",
    "اركب عليه",
    "كس",
    "انيك",
    "انيكك",
    "امكك",
    "اني..ك",
    "طيزك",
    "زب",
    "زبك",
    "مكوتك",
    "جمل ابو راسين",
    "مص",
    "تنيك",
    "كس امك",
    "مزغوب",
    "قح.به",
    "يامفتوح"
]

# ==================================
# تنظيف النص من التشكيل والتحايل
# ==================================
def normalize(text):
    if not text:
        return ""
    # تحويل إلى أحرف صغيرة
    text = text.lower()
    # إزالة التشكيل والمد
    text = re.sub(r'[\u064B-\u065F\u0670\u0640]', '', text)
    # توحيد الألفات
    text = re.sub(r'[أإآٱ]', 'ا', text)
    # توحيد الياء
    text = text.replace('ى', 'ي')
    # إزالة أي رموز أو مسافات غير الحروف والأرقام
    text = re.sub(r'[^\w\s]', '', text)
    return text

forbidden = [normalize(word) for word in bad_words if word]

# ==================================
# تشغيل البوت
# ==================================
@client.event
async def on_ready():
    print(f'Bot is online: {client.user}')

# ==================================
# مراقبة الرسائل
# ==================================
@client.event
async def on_message(message):
    if not message.guild or message.author.bot:
        return

    content = normalize(message.content)

    found = any(word in content for word in forbidden)

    if not found:
        return

    try:
        # حذف رسالة العضو فوراً
        await message.delete()

        # Timeout لمدة 10 ثوانٍ (يحتاج صلاحيات Moderation للبوت)
        duration = discord.utils.utcnow() + discord.timedelta(seconds=10)
        await message.author.timeout(duration, reason="استخدام كلمة ممنوعة")

        print(f"تم حذف رسالة ومعاقبة {message.author}")

        # الانتظار حتى انتهاء العقوبة (10 ثواني)
        await asyncio.sleep(10)

        # إرسال التحذير بعد انتهاء العقوبة
        warning = await message.channel.send(
            content=f"⚠️ {message.author.mention} ممنوع تقول كلام بذيئ او قذف"
        )

        # حذف التحذير بعد 20 ثانية
        await asyncio.sleep(20)
        try:
            await warning.delete()
        except Exception as error:
            print("تعذر حذف التحذير:", error)

    except Exception as error:
        print("Error:", error)

# ==================================
جهل وتسجيل الدخول
# ==================================
token = os.getenv('TOKEN')
if not token:
    raise ValueError("TOKEN غير موجود في متغيرات البيئة!")

client.run(token)
