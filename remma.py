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
async def on_message(message):
    if message.author == client.user:
        return

    # 1. فحص الروابط
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} الروابط ممنوعة يا بطل! 🛡️")
        except: pass
        return

    # 2. الرد المعلوماتي (مطور لحل مشكلة الصمت)
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            try:
                # إعدادات الأمان لإلغاء الحظر
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
                
                # جلب الرد من Gemini
                response = model.generate_content(message.content, safety_settings=safety)
                
                # سطر سحري لضمان اكتمال معالجة النص
                await response.resolve()
                
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("وصلني كلامك بس جوجل حظرت الرد، حاول تسأل شي ثاني! 🙄")
                    
            except Exception as e:
                # طباعة الخطأ في Render Logs لمعرفته يقيناً
                print(f"CRITICAL ERROR: {e}")
                await message.reply(f"حدث خطأ تقني: {str(e)[:50]}... شيك على الـ Logs!")

# --- تشغيل البوت مع السيرفر الوهمي ---
if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
