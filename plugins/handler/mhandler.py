import json
import re
import requests
from main import *

#from plugins.ytdl import *
import utils
import yt_dlp
from plugins.jiodl import *
import subprocess
from pyrogram import Client, filters, idle
from urllib import parse
import logging
import os
#from plugins.handler.playback import *
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *
from yt_dlp.postprocessor import PostProcessor
from utils import scriptsDir, joinPath, realPath


from base64 import b64decode, b64encode
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep


def multi_lang(_content_data, message):
    if "assetsByLanguage" in _content_data and len(_content_data["assetsByLanguage"]) > 0:
        other_langs = []

        for _lang in _content_data["assetsByLanguage"]:
            if _lang['id'] in LANG_MAP:
                other_langs.append({
                    'id': _lang['id'],
                    'name': LANG_MAP[_lang['id']],
                    'assetsId': _lang['assetId']
                })
        langr = "-"
        print('[=>] Multiple Languages Found:')
        for _idx, _lang in enumerate(other_langs):
            message.reply_text(f'[{_idx + 1}] {_lang["name"]}')
            langr+=_lang["name"]

        asset_idx = message.reply_text(f'[?] Which language you want to choose(Default: {_content_data["defaultLanguage"]})?: ')
     #   if len(asset_idx) < 1:
        asset_idx = 1
        asset_idx = int(asset_idx) - 1
        if asset_idx < 0 or asset_idx >= len(other_langs):
            print("[!] Unknown Language Choice")
            
        print("This Working")
        return other_langs[asset_idx]

    # Default language
    def_lang = _content_data["defaultLanguage"]
    return {
        'id': REV_LANG_MAP[def_lang],
        'name': def_lang,
        'assetsId': _content_data['id'],
    }


# Fetch Widevine keys using PSSH
def fetch_widevine_keys(pssh_kid_map, content_playback, playback_data):
    got_cert = False
    cert_data = None
    pssh_cache = config.get("psshCacheStore")

    # Get Keys for all KIDs of PSSH
    for pssh in pssh_kid_map.keys():
        

        # Need to fetch even if one key missing
        fetch_keys = False
        if pssh in pssh_cache:
            fetch_keys = False
                    
        else:
            fetch_keys = True
        
        if fetch_keys:
            pssh_cache[pssh] = requests.get(url='https://hls-proxifier-sage.vercel.app/jc',headers={"pyid":content_playback["playbackId"],"url":playback_data["licenseurl"],"pssh":pssh}).json()["keys"]
            config.set("psshCacheStore", pssh_cache)
# Use mp4decrypt to decrypt vod(video on demand) using kid:key

    


    
    

# Use yt-dlp to download vod(video on demand) as m3u8 or dash streams into a video file
