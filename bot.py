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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\nUse /makelink (admin only) to create payment."
    )


async def makelink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != config.ADMIN_ID:
        await update.message.reply_text("❌ Not allowed")
        return ConversationHandler.END

    await update.message.reply_text("Enter amount in Stars:")
    return ASK_AMOUNT


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = int(update.message.text)

        prices = [LabeledPrice("Premium Access", amount)]

        await update.message.reply_invoice(
            title="Premium Access",
            description="Pay to activate premium",
            payload="premium",
            provider_token=config.PROVIDER_TOKEN,
            currency="XTR",
            prices=prices,
        )

        return ConversationHandler.END

    except:
        await update.message.reply_text("❌ Send valid number")
        return ASK_AMOUNT


async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ Your Premium Activated!\n\nContact @alex_clb and send screenshot."
    )


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
