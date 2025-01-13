
import subprocess
import json
import logging
import os
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *



#import logging
import requests
from cryptography.fernet import Fernet


import subprocess
import logging

def downloaddash(name: str, key: str = None, frmts: str = None, url: str) -> str:
    # Construct the command for yt-dlp
    cmd = ['yt-dlp', url, '-o', name]
    
    # Add format if provided
    if frmts:
        cmd.extend(['-f', frmts])
    
    # Add authentication key if provided
    if key:
        cmd.extend(['--key', key])  # Example placeholder; depends on yt-dlp usage

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logging.info(f"Download successful: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during download: {e.stderr}")
        return "failed"

    return f"done: {name}"

def downloadduash(name, key, frmts, url):
    # Download the file
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        encrypted_data = response.content
        logging.info("Download successful.")
    except requests.RequestException as e:
        logging.error(f"Error during download: {e}")
        return "failed"

    # Decrypt the file
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        # Save the decrypted data to a file
        with open(name, 'wb') as file:
            file.write(decrypted_data)
        logging.info("Decryption and file writing successful.")
    except Exception as e:
        logging.error(f"Error during decryption: {e}")
        return "failed"

    return "done"
    
def downltoaddash(name, key, frmts, url):
    cmd = f'/usr/src/app/spjc "{url}" {key} -o "{name}"'
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
        logging.info(f"Download and decryption successful: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error during download: {e.stderr.decode()}")
        return "failed"
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
