
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
def mergeall(files,outpath):
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





    


