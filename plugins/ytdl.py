#Jio Cinema Downloader Bot Created By Aryan Chaudhary
#Ott Downloader Bot Created By Aryan Chaudhary @aryanchy451
import json
import re
import requests
import utils
import yt_dlp
from plugins.jiodl import *
from plugins.gdrive import *
import subprocess
from pyrogram import filters, idle
from urllib import parse
import logging
import os
from plugins.handler.playback import *
#from plugins.buttons import *
from pyrogram import Client as app
from plugins.handler.mhandler import *
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *

from base64 import b64decode, b64encode
from yt_dlp.postprocessor import PostProcessor
from utils import scriptsDir, joinPath, realPath
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep


def extractyt(url=None,ci=None,is_dngplay=False,is_sliv=False,is_hs=False,is_zee5=False,is_dplus=False):
    try:
        os.remove(f"info{ci}.json")
    except Exception:
        pass
    
    import json
    if is_dngplay:
        subprocess.run(f"yt-dlp --allow-unplayable-formats -u token -p 47c906778850df6957712a3bfd24c276 --no-check-certificate --dump-json {url} > info{ci}.json",shell=True)
    elif is_sliv:
        url = f'"{url}"'
      #  token = requests.get("https://ccroute.vercel.app/sliv").json()["token"]
        tok = "47c6938a7c5c4bd48d503e330c9e6512-1735474637849"
        subprocess.run(f"yt-dlp --allow-unplayable-formats --add-headers x-playback-session-id:{tok} --no-check-certificate --proxy http://toonrips:xipTsP9H9s@103.171.51.246:50100 --dump-json {url} > info{ci}.json",shell=True)

    elif is_hs:
        url = f'"{url}"'
        subprocess.run(f"yt-dlp --allow-unplayable-formats --no-check-certificate --proxy http://toonrips:xipTsP9H9s@103.171.51.246:50100 --dump-json {url} > info{ci}.json",shell=True)
    else:
        url = f'"{url}"'
        subprocess.run(f"yt-dlp --allow-unplayable-formats --no-check-certificate --proxy http://toonrips:xipTsP9H9s@103.171.51.246:50100 --dump-json {url} > info{ci}.json",shell=True)
    import json
    with open(f'info{ci}.json', 'r') as f:
        data = json.load(f)
    return data

def check_drm_hs(data):
    if data["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0] == "":
        return False
    else:
        return True
#from button import ButtonMaker




                

        


                    



    
    




          
  

    
    
    









