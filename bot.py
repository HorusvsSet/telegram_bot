from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import asyncio
import os

HORAS, MINUTOS, TAREA = range(3)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Horas?")
    return HORAS

async def horas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["horas"] = int(update.message.text)
    await update.message.reply_text("Minutos?")
    return MINUTOS

async def minutos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["minutos"] = int(update.message.text)
    await update.message.reply_text("Tarea?")
    return TAREA

async def tarea(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["tarea"] = update.message.text

    total = context.user_data["horas"] * 3600 + context.user_data["minutos"] * 60

    async def enviar():
        await asyncio.sleep(total)
        await update.message.reply_text("Recordatorio: " + context.user_data["tarea"])

    asyncio.create_task(enviar())

    await update.message.reply_text("Tarea programada.")
    return ConversationHandler.END

app = Application.builder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("new", start)],
    states={
        HORAS: [MessageHandler(filters.TEXT & ~filters.COMMAND, horas)],
        MINUTOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, minutos)],
        TAREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, tarea)],
    },
    fallbacks=[]
)

app.add_handler(conv)

app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url="https://TU-URL.onrender.com"
)
