import inspect

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from fundabot.auth import get_telegram_token
from fundabot.data import select_funds


def a(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Coletando os dados dos fundos! Por favor, aguarde...",
    )
    df = select_funds()

    for _, row in df.iterrows():
        message = inspect.cleandoc(
            f"""
            *{row["nome"]}*
            *  - Preço:* R$ {row["preco"]:.2f}
            *  - Dividend yield:* {row["dividend_yield"]:.2f}
            """
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message, parse_mode="Markdown"
        )


def main():
    updater = Updater(token=get_telegram_token(), use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler("a", a)
    dispatcher.add_handler(start_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
