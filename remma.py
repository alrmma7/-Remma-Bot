import os
import discord
import google.generativeai as genai
import re
from flask import Flask
from threading import Thread

# --- إعداد السيرفر الوهمي (لضمان استقرار التشغيل على Render) ---
app = Flask('')
@app.route('/')
def home():
    return "Remma is Alive and Ready!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات الذكاء الاصطناعي (Gemini) ---
# سحب المفاتيح من إعدادات Render (Environment Variables)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# إعداد نموذج جوجل (استخدمنا gemini-pro لضمان العمل)
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# إعدادات ديسكورد
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تشغيل {client.user} بنجاح!')
    await client.change_presence(activity=discord.Game(name="مراقبة السيرفر 🛡️"))

@client.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه
    if message.author == client.user:
        return

    # 1. نظام حماية الروابط
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} عيب.. الروابط ممنوعة! 😡")
        except: pass
        return

    # 2. نظام الرد الذكي (عند مناداتها بـ ريما أو Remma)
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            try:
                # طلب الرد من Gemini
                response = model.generate_content(message.content)
                
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("سمعتك، بس جوجل حظر الرد.. جرب سؤال ثاني! 🌚")
            except Exception as e:
                print(f"خطأ تقني: {e}")
                await message.reply("عندي مشكلة في استيعاب الكلام حالياً.. تأكد من الـ API Key! ⚠️")

# تشغيل السيرفر ثم البوت
if __name__ == "__main__":
    keep_alive()
    if DISCORD_TOKEN:
        client.run(DISCORD_TOKEN)
    else:
        print("خطأ: لم يتم العثور على DISCORD_TOKEN في إعدادات Render!")
