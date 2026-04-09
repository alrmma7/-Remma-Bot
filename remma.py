import os
import discord
import google.generativeai as genai
import re
from flask import Flask
from threading import Thread

# --- إعداد السيرفر الوهمي (عشان Render ما يطفي) ---
app = Flask('')
@app.route('/')
def home():
    return "Remma is Online!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- إعدادات Gemini ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تشغيل {client.user} بنجاح!')
    await client.change_presence(activity=discord.Game(name="مراقبة السيرفر 🛡️"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # منع الروابط
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} الروابط ممنوعة! 🛡️")
        except: pass
        return

    # الرد الذكي
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            try:
                response = model.generate_content(message.content)
                if response.text:
                    await message.reply(response.text)
                else:
                    await message.reply("سمعتك، بس جوجل حظر الرد.. جرب سؤال ثاني! 🌚")
            except Exception as e:
                print(f"Error: {e}")
                await message.reply("عندي مشكلة فنية حالياً، شيك على الـ API Key! ⚠️")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
