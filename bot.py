import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # token env var se aayega

WELCOME_TEXT = (
    "👋 @PagaLEscrowBot 👋\n"
    "Your Trustworthy Telegram Escrow Service\n\n"
    "Welcome to @PagaLEscrowBot.\n"
    "This bot provides a reliable escrow service for your transactions on Telegram.\n"
    "Avoid scams, your funds are safeguarded throughout your deals.\n"
    "If you run into any issues, type /dispute and an arbitrator will join the group chat within 24 hours.\n\n"
    "🎟 ESCROW FEE:\n"
    "1.0% for P2P and 1.0% for OTC Flat\n\n"
    "⚠ IMPORTANT - Make sure coin is same of Buyer and Seller else you may lose your coin.\n\n"
    "💡 Type /menu to summon a menu with all bot features"
)

def home_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("COMMANDS LIST 🤖", callback_data="commands"),
         InlineKeyboardButton("☎️ CONTACT", callback_data="contact")],
        [InlineKeyboardButton("Updates 🌐", url="https://t.me/yourupdateschannel"),
         InlineKeyboardButton("Vouches ✅", url="https://t.me/yourvoucheschannel")],
        [InlineKeyboardButton("WHAT IS ESCROW ❓", callback_data="escrow_info"),
         InlineKeyboardButton("Instructions 🧑‍🏫", callback_data="instructions")],
        [InlineKeyboardButton("Terms 📝", callback_data="terms"),
         InlineKeyboardButton("Invites 👤", callback_data="invites")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=home_keyboard())

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("P2P", callback_data="p2p"),
                                InlineKeyboardButton("Product Deal", callback_data="product")]])
    await update.message.reply_text("Please select your escrow type from below.", reply_markup=kb)

async def escrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("To start a new escrow, choose /menu → P2P or Product Deal.")

async def dispute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dispute raised. An arbitrator will contact you. (placeholder)")

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    text = {
        "commands": "📋 Available Commands:\n/start, /menu, /escrow, /dispute",
        "contact": "📞 Support: @YourSupportUsername",
        "escrow_info": "ℹ️ Escrow holds funds safely until both parties complete the deal.",
        "instructions": "📘 Use /menu → pick P2P/Product → follow prompts.",
        "terms": "📑 Terms: Use same coin network; fees non-refundable after release.",
        "invites": "👤 Invite friends to use this bot!",
        "p2p": "🤝 You selected P2P Escrow. (flow coming next)",
        "product": "📦 You selected Product Deal Escrow. (flow coming next)",
    }.get(data, "Unknown action.")
    await q.edit_message_text(text)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("escrow", escrow))
    app.add_handler(CommandHandler("dispute", dispute))
    app.add_handler(CallbackQueryHandler(on_button))
    print("Bot is running...")
    app.run_polling()

if _name_ == "_main_":
    main()
