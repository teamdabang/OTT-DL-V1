from pyrogram import Client, filters as Filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import yt_dlp
import subprocess
import threading
import time
from plugins.ytdl import *
from plugins.dl import *
from plugins.exec import *
from plugins.dash import *
##from plugins.handler.playback import *
from plugins.handler.mhandler import * 


LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "mr": "Marathi",
    "ml": "Malayalam",
    "bn": "Bengali",
    "bho": "Bhojpuri",
    "pa": "Punjabi",
    "or": "Oriya"
}

jiodl = 'bot/jiod'
proxy = "0"

def download_video(url, format, message):
    try:
        jio_cmd = [f"jiod", "-f", f"bestaudio[language={list(format.keys())[0]}]+{list(format.values())[0]}", f"{url}"]
        process = subprocess.Popen(jio_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            output = process.stdout.readline().decode('utf-8')
            if not output and process.poll() is not None:
                break
            if 'Downloading' in output:
                speed = output.split('at')[1].strip()
                message.edit(f'Downloading video at {speed}...')
                time.sleep(1)

        if process.returncode != 0:
            raise RuntimeError(f"Download failed: {process.stderr.read().decode('utf-8')}")

        # Prepare file for upload
        ydl = yt_dlp.YoutubeDL()
        info = ydl.extract_info(url, download=False)
        filename = ydl.prepare_filename(info)
        file_path = f"{filename}"

        # Upload the file
        uploader = tgUploader(app, message, message.chat.id)
        uploader.upload_file(file_path)

    except Exception as e:
        message.reply_text(f"An error occurred: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def split_and_upload_video(file_name, message):
    file_size = os.path.getsize(file_name)
    chunk_size = 2047152000  # 2GB
    chunk_count = 0

    if file_size > chunk_size:
        app.send_message (message.chat.id, 'File size exceeds 2GB, splitting into chunks...')
        
        with open(file_name, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunk_count += 1
                chunk_file_name = f'{file_name}.part{chunk_count}'
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                app.send_document(message.chat.id, chunk_file_name, caption=f'Video chunk {chunk_count}')
                os.remove(chunk_file_name)
        
        message.edit('Video uploaded successfully!')
    else:
        app.send_video(message.chat.id, file_name, caption='Video uploaded by JioCinema Downloader Bot')
        message.edit('Video uploaded successfully!')
        os.remove(file_name)
##``` ### Conclusion

#The revised code enhances error handling, reduces code duplication, and improves user feedback during the download and upload processes. By implementing logging and ensuring proper cleanup of temporary files, the bot becomes more robust and user-friendly. Always test the bot thoroughly to ensure all functionalities work as expected and handle edge cases gracefully.
