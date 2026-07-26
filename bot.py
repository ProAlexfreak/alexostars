from telegram import Update, LabeledPrice
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    PreCheckoutQueryHandler,
)
import config

ASK_AMOUNT = 1


# 🌟 START COMMAND (Handles deep links + UI)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    # 🎯 Handle payment deep link
    if args:
        data = args[0]

        if data.startswith("pay_"):
            try:
                amount = int(data.split("_")[1])

                prices = [LabeledPrice("🌟 Premium Access", amount)]

                await update.message.reply_invoice(
                    title="🌟 Premium Membership",
                    description=(
                        "✨ Unlock Exclusive Features\n"
                        "🚀 Instant Activation\n"
                        "🔒 100% Secure Payment\n\n"
                        f"💳 Amount: {amount} Stars"
                    ),
                    payload=f"pay_{amount}",
                    provider_token=config.PROVIDER_TOKEN,
                    currency="XTR",
                    prices=prices,
                )
                return
            except:
                pass

    # 💎 Normal start UI
    await update.message.reply_text(
        "👋 *Welcome to Premium Access Bot*\n\n"
        "✨ Get access to exclusive premium features\n"
        "⚡ Fast • Secure • Instant Activation\n\n"
        "💳 Use a payment link to unlock premium\n\n"
        "🔐 Admin: /makelink",
        parse_mode="Markdown"
    )


# 🔐 ADMIN COMMAND
async def makelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != config.ADMIN_ID:
        await update.message.reply_text("🚫 *Access Denied*", parse_mode="Markdown")
        return ConversationHandler.END

    await update.message.reply_text(
        "💰 *Create Payment Link*\n\n"
        "Enter amount in Stars (example: 50)",
        parse_mode="Markdown"
    )
    return ASK_AMOUNT


# 🔗 GENERATE LINK
async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = int(update.message.text)

        bot_username = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start=pay_{amount}"

        await update.message.reply_text(
            "✅ *Payment Link Generated*\n\n"
            f"💳 Amount: *{amount} Stars*\n"
            f"🔗 Link:\n{link}\n\n"
            "📤 Share this link with users",
            parse_mode="Markdown"
        )

        return ConversationHandler.END

    except:
        await update.message.reply_text("❌ Please enter a valid number")
        return ASK_AMOUNT


# 💳 PRECHECKOUT
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


# 🎉 SUCCESS PAYMENT
async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 *Payment Successful!*\n\n"
        "✅ Your Premium Access is now *Activated*\n\n"
        "📩 Next Step:\n"
        "Send payment screenshot to:\n"
        "👉 @alex_clb\n\n"
        "⚡ Activation will be confirmed shortly",
        parse_mode="Markdown"
    )


# 🚀 MAIN
def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("makelink", makelink)],
        states={
            ASK_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)
            ]
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    print("🚀 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
