
import subprocess
import json
import logging
import os
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.handler.playback import *
from plugins.handler.mhandler import* 


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

def mergeall(files, outpath):
    if not all(os.path.exists(file) for file in files):
        logging.error("One or more input files do not exist.")
        return "failed"

    cmd = 'ffmpeg -y '
    for audio in files:
        cmd += f'-i "{audio}" '
    
    cmd += '-map 0:v '
    for i in range(len(files) - 1):
        cmd += f'-map {i + 1}:a:0 '
    
    cmd += f'-c:v copy -c:a copy "{outpath}" '
    
    try:
        process = subprocess.run(cmd, shell=True, check=True, capture_output=True)
        logging.info(f"Merging successful: {process.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during merging: {e.stderr.decode()}")
        return "failed"
    
    return "done"
