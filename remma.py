import os
import discord
import google.generativeai as genai
import random
import re

# بدلاً من وضع الرموز مباشرة، نطلبها من نظام التشغيل (الخادم)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# إعداد عقل Remma (معزول عن بياناتك الشخصية)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
    system_instruction="""
    اسمك Remma. أنتِ فتاة أنمي ذكية جداً، هادئة، وشخصيتك ساخرة (Sarcastic). 
    تتحدثين بالعامية العربية بأسلوب طبيعي ومباشر.
    
    مهمتك مراقبة السيرفر وتطبيق الشروط الـ 16 بصرامة:
    1. أي شتيمة، رابط، عنصرية، أو كلام غير لائق، يتم حذفه فوراً.
    2. عند الحذف، ردي برد ساخر وقصير مثل: (عيب 😡 يا ولد، ترا السب حرام 😔، خلك محترم).
    3. أنتِ مرجع معلوماتي ممتاز؛ أجيبي بدقة على الأسئلة التقنية والعلمية إذا سألك أحد.
    4. تجنبي المبالغة في المناداة بـ "أخوي".
    """
)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'تم تشغيل Remma بنجاح! هي الآن تراقب السيرفر. ✨')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 1. فحص الروابط (قانون رقم 1)
    if re.search(r'http[s]?://', message.content):
        try:
            await message.delete()
            await message.channel.send(f"{message.author.mention} عيب 😡.. الروابط ممنوعة!")
        except: pass
        return

    # 2. فحص الشتائم والمخالفات (عبر محرك Gemini)
    check_prompt = f"هل النص التالي مخالف (سب، عنصرية، سياسة، تعارف، قلة أدب)؟ أجب بـ 'مخالف' أو 'سليم' فقط: {message.content}"
    try:
        check = model.generate_content(check_prompt)
        if "مخالف" in check.text:
            await message.delete()
            replies = ["عيب 😡 يا ولد", "ترا السب حرام 😔", "خلك محترم..", "استغفر ربك يا ولد 🙄"]
            await message.channel.send(f"{message.author.mention} {random.choice(replies)}")
            return
    except: pass

    # 3. الرد المعلوماتي (عند ذكر اسم Remma)
    if 'Remma' in message.content or 'ريما' in message.content:
        async with message.channel.typing():
            res = model.generate_content(message.content)
            await message.reply(res.text)

client.run(DISCORD_TOKEN)
