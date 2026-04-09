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
model = genai.GenerativeModel('gemini-pro')


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 1. فحص الروابط
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} الروابط ممنوعة! 🛡️")
        except: pass
        return

    # 2. الرد المعلوماتي (تم تعديل الموديل وطريقة الإرسال)
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            try:
                # محاولة توليد الرد
                response = model.generate_content(message.content)
                
                # إرسال النص (استخدمنا أسلوباً أبسط لضمان الوصول)
                if response and response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("جوجل حظرت الرد بسبب قوانين الأمان، حاول تسألني شي ثاني! 🙄")
                    
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                # رد بسيط يوضح لك أن المشكلة في المفتاح أو الموديل
                await message.reply("عندي مشكلة فنية بسيطة مع Gemini.. تأكد من صلاحية الـ API Key!")

# --- تشغيل البوت ---
if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
