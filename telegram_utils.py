from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)
from config import TELEGRAM_TOKEN
from tracker import stats

# ---------- COMMAND HANDLERS ----------

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = stats()
    msg = (
        "📊 *BOT PERFORMANCE*\n\n"
        f"📈 Total Trades: {s['total']}\n"
        f"✅ Wins: {s['wins']}\n"
        f"❌ Losses: {s['losses']}\n\n"
        f"🏆 Win-rate: *{s['winrate']}%*"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")


# ---------- APP FACTORY ----------

def build_app():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("stats", stats_command))
    return app
