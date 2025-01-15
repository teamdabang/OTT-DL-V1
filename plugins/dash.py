
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




def downloaddash(name,key,frmts,url):
    
    cmd = f'/usr/src/app/spjc "{url}" {key} -o "{name}"'
    hi = subprocess.run(cmd,shell=True)
    return "done"
def detector(ci,fr):
    with open(f"info{ci}.json","r") as file:
        
        data = json.load(file)
        for frm in data['formats']:
            frmid = frm['format_id']
            if frmid == fr:
                if frm['resolution'] == "audio only":
                    return 1
                else:
                    return 2
def merrrrgeall(files,outpath):
    cmd = f'ffmpeg -y '
    
    for i, audio in enumerate(files):
            
            cmd += f'-i "{audio}" '
    cmd += '-map 0:v:0 '
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
    for i, audio in enumerate(files):
            os.remove(audio)
    return 1





import subprocess
import os
import logging

def mergeall(files, outpath):
    if not files:
        logging.error("No files provided for merging.")
        return 0
    cmd = 'ffmpeg -y '

    for audio in files:
        cmd += f'-i "{audio}" '

    
    cmd += '-map 0:v:0? '
    for i in range(len(files)):
        cmd += f'-map {i + 1}:a:0 '  # Map the first audio stream of each input

    # Specify the output codec and output file
    cmd += '-c:v copy -c:a aac -b:a 192k "{outpath}"'

    # Log the command for debugging
    logging.info(f"Running command: {cmd}")

    # Execute the command
    process = subprocess.run(cmd, shell=True)

    # Check if the process was successful
    if process.returncode != 0:
        logging.error("ffmpeg command failed.")
        return 0

    # Remove the input files after merging
    for audio in files:
        try:
            os.remove(audio)
        except OSError as e:
            logging.error(f"Error removing file {audio}: {e}")

    logging.info("Merging completed successfully.")
    return 1    


