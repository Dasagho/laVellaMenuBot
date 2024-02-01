from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import pdfplumber
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import logging

# Función para extraer texto del PDF


def extraer_texto_del_pdf(url):
    file_name = 'menu.pdf'
    need_download = False

    # Comprobar si ya es pasado las 11:45 del día actual
    now = datetime.now()
    time_limit = now.replace(hour=11, minute=45, second=0, microsecond=0)

    # Si no es aún las 11:45 y el archivo existe, no descargarlo
    if now < time_limit or os.path.exists(file_name):
        need_download = True

    # Descargar el PDF si es necesario
    if need_download:
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            return "Error: No se pudo acceder al PDF."

        with open(file_name, 'wb') as f:
            f.write(response.content)

    # Extraer el texto del PDF
    texto = ''
    with pdfplumber.open(file_name) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ''
    return texto

# Define la función que responderá al comando /menu


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'http://www.lavella.es/doc/Menu_normal.pdf'
    texto_extraido = extraer_texto_del_pdf(url)
    await update.message.reply_text(texto_extraido)

# Función principal


def main():
    # Cargar las variables de entorno del archivo .env
    load_dotenv()

    # Habilita el registro
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Suponiendo que tienes una variable de entorno llamada 'TELEGRAM_TOKEN' en tu archivo .env
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("menu", menu))

    app.run_polling()


if __name__ == '__main__':
    main()
