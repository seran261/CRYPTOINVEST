from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from config import TELEGRAM_TOKEN, CHAT_ID
from tracker import stats

# ---------- SEND SIGNAL (USED BY SCANNER) ----------
async def send_signal(data):
    msg = f"""
🚀 *CRYPTO PATTERN SIGNAL*

📊 Pair: {data['symbol']}
⏱ Timeframe: {data['timeframe']}
📐 Pattern: {data['pattern']}

🎯 Entry: {data['entry']}
✅ TP: {data['tp']}
🛑 SL: {data['sl']}

🔥 Confidence: {data['confidence']} / 100
"""
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text=msg,
        parse_mode="Markdown"
    )

# ---------- /stats COMMAND ----------
async def stats_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    s = stats()

    msg = f"""
📊 *BOT PERFORMANCE STATS*

📈 Total Trades: {s['total']}
✅ Wins: {s['wins']}
❌ Losses: {s['losses']}

🏆 Win-rate: *{s['winrate']}%*
"""
    await update.message.reply_text(
        msg,
        parse_mode="Markdown"
    )

# ---------- APP INIT ----------
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("stats", stats_command))
