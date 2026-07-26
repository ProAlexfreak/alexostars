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


# START (handles deep link)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args:
        data = args[0]

        if data.startswith("pay_"):
            try:
                amount = int(data.split("_")[1])

                prices = [LabeledPrice("Premium Access", amount)]

                await update.message.reply_invoice(
                    title="Premium Access",
                    description=f"Pay {amount} Stars to activate premium",
                    payload=f"pay_{amount}",
                    provider_token=config.PROVIDER_TOKEN,
                    currency="XTR",
                    prices=prices,
                )
                return
            except:
                pass

    await update.message.reply_text(
        "👋 Welcome!\nUse /makelink (admin only)"
    )


# ADMIN COMMAND
async def makelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != config.ADMIN_ID:
        await update.message.reply_text("❌ Not allowed")
        return ConversationHandler.END

    await update.message.reply_text("Enter amount in Stars:")
    return ASK_AMOUNT


# GENERATE LINK
async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = int(update.message.text)

        bot_username = (await context.bot.get_me()).username
        link = f"https://t.me/{bot_username}?start=pay_{amount}"

        await update.message.reply_text(
            f"✅ Payment Link:\n\n{link}"
        )

        return ConversationHandler.END

    except:
        await update.message.reply_text("❌ Invalid number")
        return ASK_AMOUNT


# PAYMENT HANDLING
async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Your Premium Activated!\n\nContact @alex_clb and send screenshot."
    )


# MAIN
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

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
