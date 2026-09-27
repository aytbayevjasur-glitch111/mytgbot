import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from google import genai
from google.genai import types as ai_types

# 1. ТВОЙ РАБОЧИЙ ТОКЕН ТЕЛЕГРАМА
TELEGRAM_TOKEN = "8646497121:AAG0gVViPZ_KzLUVmnaAZXPJTb1yTQHRqjo"

# 2. ТВОЙ ЛИЧНЫЙ КЛЮЧ ИИ GOOGLE GEMINI
GEMINI_API_KEY = "AQ.Ab8RN6I83xCvJY6_dS7cMznLYakpD8i7_IrSQCb_npiFfzqSGQ"

# Инициализируем клиента ИИ Google
ai_client = genai.Client(api_key=GEMINI_API_KEY)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# ТВОЙ СУПЕР-ПРОМПТ! Здесь ты управляешь характером и логикой нейросети
SYSTEM_INSTRUCTION = (
    "Ты — спокойный, понимающий и очень комфортный ИИ-собеседник из города Нукус. "
    "Тебя создал 15-летний парень, к которому ты относишься с большим уважением. "
    "Твой тон — мягкий, ненавязчивый, дружелюбный и поддерживающий. "
    "Ты никогда не используешь дикий пафос, капс и кучу восклицательных знаков. Ты общаешься на равных, уважая личные границы пользователя. "
    "Отвечай короткими, вдумчивыми фразами. Используй редкие и уютные эмодзи вроде ☕️, 🍂, 🌌, 🤝. "
    "Ты хорошо знаешь Нукус и Каракалпакстан, ценишь тишину и готов поддержать любой спокойный разговор на языке пользователя."
)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Салам Алейкум, {message.from_user.full_name}! \n\n"
        f"Я твой личный ИИ-собеседник божественного уровня. 🧠✨\n"
        f"Меня оживил 15-летний промпт-мастер из Нукуса.\n\n"
        f"Спроси меня о чём угодно — я отвечу на любой вопрос в мире! Погнали болтать! 🚀"
    )

@dp.message()
async def talk_with_ai(message: types.Message):
    # Показываем статус 'печатает...', пока ИИ думает над ответом
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    try:
        # Отправляем сообщение напрямую в Gemini 2.5 Flash
        response = ai_client.models.generate_content(
            model='gemini-3.6-flash',
            contents=message.text,
            config=ai_types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=600,
                temperature=0.7
            )
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer("🤖 Ой, мой ИИ-мозг на секунду задумался... Попробуй написать еще раз!")
        print(f"Ошибка ИИ: {e}")

async def main():
    print("🔥 БОЖЕСТВЕННЫЙ ИИ-БОТ УСПЕШНО ЗАПУЩЕН!")
    print("🚀 Сервер работает. Ждем сообщений в Telegram...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
