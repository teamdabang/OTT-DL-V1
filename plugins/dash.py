
import subprocess
import json
import logging
import os
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
##from plugins.handler.playback import *
#from plugins.handler.mhandler import* 
#from plugins.ytdl import *


#import logging
import requests


import subprocess
import logging
import os


def downloaddash(name, key, frmts, url):
    cmd = f'/usr/src/app/spjc "{url}" {key} -o "{name}"'
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
        logging.info(f"Download and decryption successful: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during download: {e.stderr.decode()}")
        return "failed"
    return "done"

def loaddash(name, key, frmts, url):

    # Define the download directory
    download_dir = 'downloads'

    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    # Define the full path for the output file
    output_file_path = os.path.join(download_dir, name)

    cmd = [url, key, '-o', output_file_path]  # Use the full path for the output file
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info(f"Download and decryption successful: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during download: {e.stderr}")
        raise RuntimeError("Download failed") from e  # Raise a more informative error
    return "done"






def detector(ci, fr):
    try:
        with open(f"info{ci}.json", "r") as file:
            data = json.load(file)
            for frm in data['formats']:
                if frm['format_id'] == fr:
                    return 1 if frm['resolution'] == "audio only" else 2
    except FileNotFoundError:
        logging.error(f"File info{ci}.json not found.")
    except json.JSONDecodeError:
        logging.error("Error decoding JSON.")
    return None





def mergeall(files,outpath):
    cmd = f'ffmpeg -y '
    for i, audio in enumerate(files):
            
            cmd += f'-i "{audio}" '
    cmd += '-map 0:v '
#ffmpeg -i input.mp4 -map 0:v -map 0:a:0 -map 0:a:1 -map 0:a:2 -c:v copy -c:a copy output.mp4
#for i in range(len(self.audio_data)):
#            ffmpeg_opts.extend(["-map", f"{i+1}:a:0"])
#    cmd += '-map 0:a:0? '
    for i in range(len(files)-1):
       cmd += f'-map {i+1}:a:0 '
    cmd += f'-c:v copy -c:a copy "{outpath}" '
    import logging
    logging.info("merged")
    process = subprocess.run(cmd, shell=True)
    return 1


