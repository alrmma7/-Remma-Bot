import os
import discord
import google.generativeai as genai
import random
import re
from flask import Flask
from threading import Thread

# --- إعداد السيرفر الوهمي (ضروري لـ Render) ---
app = Flask('')
@app.route('/')
def home():
    return "Remma is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الذكاء الاصطناعي (تم تحديث الموديل ليعمل 100%) ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
# استخدمنا 'gemini-1.5-flash' وهو الأحدث والأسرع
model = genai.GenerativeModel('gemini-1.5-flash')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تشغيل {client.user} بنجاح!')
    # لتغيير الحالة إلى "Online" بشكل صريح
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="مراقبة السيرفر 🛡️"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 1. فحص الروابط
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} عيب 😡.. الروابط ممنوعة!")
        except: pass
        return

    # 2. الرد المعلوماتي
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            try:
                response = model.generate_content(message.content)
                await message.reply(response.text)
            except Exception as e:
                print(f"خطأ في Gemini: {e}")
                await message.channel.send("عندي مشكلة في استيعاب الكلام حالياً.. جرب مرة ثانية.")

# تشغيل السيرفر ثم البوت
if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
