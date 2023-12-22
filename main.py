from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import pdfplumber
from datetime import datetime
from dotenv import load_dotenv
import os


# Cargar las variables de entorno del archivo .env
load_dotenv()

# Suponiendo que tienes una variable de entorno llamada 'TELEGRAM_TOKEN' en tu archivo .env
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Función para extraer texto del PDF
def extraer_texto_del_pdf(url):
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        return "Error: No se pudo acceder al PDF."

    # Obtener la fecha actual para nombrar el archivo
    fecha_actual = datetime.now().strftime('%d-%m-%Y')
    nombre_archivo = f'{fecha_actual}.pdf'

    # Guardar el PDF con el nombre de la fecha actual
    with open(nombre_archivo, 'wb') as f:
        f.write(response.content)

    with pdfplumber.open(nombre_archivo) as pdf:
        texto = ''
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ''
    return texto

# Comando /menu
def menu(update: Update, context: CallbackContext) -> None:
    url = 'http://www.lavella.es/doc/Menu_normal.pdf'
    texto_extraido = extraer_texto_del_pdf(url)
    update.message.reply_text(texto_extraido)

# Función principal para iniciar el bot
def main():
    updater = Updater(TELEGRAM_TOKEN)

    # Registrar el comando /menu
    updater.dispatcher.add_handler(CommandHandler('menu', menu))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
