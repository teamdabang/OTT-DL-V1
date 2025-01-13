import subprocess
import yt_dlp
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *

def downloadformat(ydl_opts, url, info):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        file_path = ydl.prepare_filename(info)
        return file_path

def decrypt_vod_mp4(kid, key, input_path, output_path):
    mp4decPath = realPath(joinPath(scriptsDir, config.get('mp4decPath')))
    command = ["mp4decrypt", '--key', f"{kid}:{key}", input_path, output_path]
    
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    
    if process.returncode != 0:
        raise RuntimeError(f"mp4decrypt failed: {process.stderr}")
    
    return "Decryption completed successfully."

def merge_vod_ffmpeg(in_video, in_audio, output_path):
    ffmpegPath = realPath(joinPath(scriptsDir, config.get('ffmpegPath')))
    command = ["ffmpeg", '-hide_banner', '-i', in_video, '-i', in_audio, '-c:v', 'copy', '-c:a', 'copy', output_path]
    
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    
    if process.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {process.stderr}")
    
    return "Merging completed successfully."
