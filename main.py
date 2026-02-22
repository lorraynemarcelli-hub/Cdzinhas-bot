import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

TOKEN = "8517114797:AAEB11IrIVPwvQSPSDvqhqzBFuCXq3IBLFU"
GROUP_ID = -1003856619689
TOPIC_ID = 5

NOME, IDADE, CIDADE, FOTO = range(4)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💄 Bem-vinda às Cdzinhas Amigas!\n\n"
        "Qual seu nome feminino?"
    )
    return NOME

async def nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nome"] = update.message.text
    await update.message.reply_text("🎂 Qual sua idade?")
    return IDADE

async def idade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["idade"] = update.message.text
    await update.message.reply_text("📍 Qual seu município?")
    return CIDADE

async def cidade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["cidade"] = update.message.text
    await update.message.reply_text("📸 Envie uma foto sua montada (obrigatório)")
    return FOTO

async def foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("❌ Você precisa enviar uma FOTO.")
        return FOTO

    nome = context.user_data["nome"]
    idade = context.user_data["idade"]
    cidade = context.user_data["cidade"]

    texto = f"""💋 Nova integrante aprovada!

👑 Nome: {nome}
🎂 Idade: {idade}
📍 Cidade: {cidade}

Seja bem-vinda às Cdzinhas Amigas 💄✨"""

    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=texto,
        message_thread_id=TOPIC_ID
    )

    await update.message.reply_text("✅ Você foi aprovada! Bem-vinda 💖")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelado.")
    return ConversationHandler.END

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, nome)],
        IDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, idade)],
        CIDADE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cidade)],
        FOTO: [MessageHandler(filters.PHOTO, foto)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)

app.run_polling()