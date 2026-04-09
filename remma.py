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

    # 1. فحص الروابط (شغال تمام)
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} الروابط ممنوعة يا بطل! 🛡️")
        except: pass
        return

    # 2. الرد المعلوماتي (تم تعديله لإلغاء فلاتر الأمان)
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            try:
                # إعدادات لإلغاء حظر المحتوى (عشان ريما ترد ببراحة)
                safety = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
                
                # نطلب الرد من الموديل مع إعدادات الأمان الجديدة
                response = model.generate_content(message.content, safety_settings=safety)
                
                # التأكد من أن الرد يحتوي على نص قبل الإرسال
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("سمعتك، بس ما أدري وش أقول! 😅")
                    
            except Exception as e:
                print(f"Error details: {e}")
                # إذا فشل بسبب الأمان، نحاول إرسال رد بسيط
                await message.reply("واضح إن كلامك حساس وجوجل زعلت منه! حاول تغير الأسلوب شوي. 🌚")
