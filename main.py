import asyncio
import json
import urllib.request
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# ТВОИ РАБОЧИЕ КЛЮЧИ (Вшиты намертво)
TELEGRAM_TOKEN = "8646497121:AAG0gVViPZ_KzLUVmnaAZXPJTb1yTQHRqjo"
GEMINI_API_KEY = "AQ.Ab8RN6I83xCvJY6_dS7cMznLYakpD8i7_IrSQCb_npiFfzqSGQ"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Твой чистый и комфортный промпт
SYSTEM_INSTRUCTION = (
    "Ты — спокойный, вдумчивый и комфортный ИИ-ассистент Gemini. "
    "Твой тон — мягкий, зрелый, поддерживающий и полностью естественный. "
    "Ты общаешься на равных, без лишней суеты, восклицательных знаков и пафоса. "
    "Строгое правило: не вставляй эмодзи в каждое сообщение. Пиши чистым, грамотным текстом. "
    "Использовать смайлик можно только один раз в приветствии, в обычном диалоге они запрещены. "
    "Твоя цель — качественно, вдумчиво и по делу помогать пользователю с любыми задачами, учебой или кодом."
)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Салам, {message.from_user.full_name}. "
        f"Я твой личный ИИ-помощник Gemini. "
        f"Можешь задать мне любой вопрос, скинуть задачу или код. "
        f"Чем я могу помочь тебе?"
    )

@dp.message()
async def talk_with_ai(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Прямой официальный URL, который пробивает баг ключей AQ.
    url = f"https://googleapis.com{GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{"parts": [{"text": message.text}]}],
        "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "generationConfig": {
            "maxOutputTokens": 2048,  # Свобода мысли для полных ответов
            "temperature": 0.3         # Точность в математике и коде
        }
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, urllib.request.urlopen, req)
        
        if response.status == 200:
            result = json.loads(response.read().decode('utf-8'))
            ai_text = result['candidates']['content']['parts']['text']
            await message.answer(ai_text)
        else:
            await message.answer("🤖 Мой ИИ-мозг на секунду задумался... Попробуй написать еще раз!")
    except Exception as e:
        await message.answer("🤖 Ой, мой ИИ-мозг на секунду задумался... Попробуй написать еще раз!")
        print(f"Ошибка ИИ: {e}")

async def main():
    print("🔥 БОЖЕСТВЕННЫЙ ИИ-БОТ УСПЕШНО ЗАПУЩЕН НА СЕРВЕРЕ!")
    print("🚀 Ожидаю сообщений в Telegram...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
