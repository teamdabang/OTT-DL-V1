
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




import subprocess
import logging
import os

def mergeall(files, outpath):
    # Check if input files exist
    for audio in files:
        if not os.path.isfile(audio):
            logging.error("Input file does not exist: %s", audio)
            return 0  # Indicate failure

    # Start building the ffmpeg command
    cmd = ['ffmpeg', '-y']  # '-y' to overwrite output file without asking
    
    # Add input files to the command
    for audio in files:
        cmd += ['-i', audio]
    
    # Map the video stream from the first input file
    cmd += ['-map', '0:v']
    
    # Map audio streams from all input files
    for i in range(len(files)):
        cmd += [f'-map', f'{i}:a']
    
    # Specify the output codec and output file path
    cmd += ['-c:v', 'copy', '-c:a', 'aac', outpath]
    
    
    logging.info("Executing command: %s", ' '.join(cmd))
    
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    
    if process.returncode != 0:
        logging.error("ffmpeg command failed with return code: %d", process.returncode)
        logging.error("ffmpeg output: %s", process.stderr)
        return 0  
    logging.info("Merging completed successfully.")
    return 1

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    files = ["input1.mp4", "input2.mp4", "input3.mp4"]  # Replace with your actual file paths
    outpath = "output.mp4"  # Replace with your desired output file path
    mergeall(files, outpath)


def mergealgl(files,outpath):
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


