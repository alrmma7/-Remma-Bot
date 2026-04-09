import os
import discord
import google.generativeai as genai
import re
from flask import Flask
from threading import Thread

# --- 1. إعداد السيرفر الوهمي للبقاء أونلاين ---
app = Flask('')
@app.route('/')
def home():
    return "Remma is Alive and Ready!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. إعدادات Gemini والذكاء الاصطناعي ---
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# استخدام الإصدار الأحدث والأكثر استقراراً لتجنب مشاكل المناطق
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# إعدادات الأمان (للسماح لريما بالرد بحرية أكبر)
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# --- 3. إعدادات بوت ديسكورد ---
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم
