import os
import smtplib
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import asyncio

load_dotenv()

# Configuración desde variables de entorno
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")
CHANNEL = os.getenv("CHANNEL")  # Formato: '@nombre_del_canal'

SENDER = os.getenv("SENDER")
PASS = os.getenv("PASS")
RECIPIENT = os.getenv("MAIL")

app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

def enviar_email(subject: str, body: str, file_path: str = None):
    msg = MIMEMultipart()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if file_path:
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
            msg.attach(part)

    with smtplib.SMTP("disroot.org", 587) as server:
        server.starttls()
        server.login(SENDER, PASS)
        server.send_message(msg)

@app.on_message(filters.channel & filters.chat(CHANNEL))
async def recibir_mensaje(client: Client, message: Message):
    if message.text:
        enviar_email("📩 Nuevo mensaje en Telegram", message.text)

    elif message.photo:
        file_path = await message.download()
        caption = message.caption or "(sin descripción)"
        enviar_email("📸 Nueva foto en Telegram", caption, file_path)

    elif message.video:
        file_path = await message.download()
        caption = message.caption or "(sin descripción)"
        enviar_email("🎥 Nuevo video en Telegram", caption, file_path)

async def main():
    await app.start()
    print("Bot iniciado y operativo.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Detención forzada realizada")
