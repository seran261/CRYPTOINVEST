from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID

bot = Bot(token=TELEGRAM_TOKEN)

async def send_signal(data):
    msg = f"""
🚀 *CRYPTO PATTERN SIGNAL*

📊 Pair: {data['symbol']}
⏱ TF: {data['timeframe']}
📐 Pattern: {data['pattern']}

🎯 Entry: {data['entry']}
✅ TP: {data['tp']}
🛑 SL: {data['sl']}

🔥 Confidence: {data['confidence']} / 100
"""
    await bot.send_message(
        chat_id=CHAT_ID,
        text=msg,
        parse_mode="Markdown"
    )
