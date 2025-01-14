import json
import re
import requests
import utils
import yt_dlp
from plugins.jiodl import *
#from plugins.gdrive import *
from main import *
import subprocess
from pyrogram import Client, filters, idle
from urllib import parse
import logging
import os

from plugins.handler.mhandler import *
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *

from base64 import b64decode, b64encode
from yt_dlp.postprocessor import PostProcessor
from utils import scriptsDir, joinPath, realPath
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep



def download_playback(message, _content_id, _content_data, is_series=False, att=0, is_multi=False,user_id=None):
    global default_strm
    
    print(f'[=>] Fetching Playback Details')
    content_playback = fetchPlaybackData(_content_id, config.get("authToken"))
    if not content_playback:
        print("[X] Playback Details Not Found!")
#        exit(0)



    playback_data = None
    try:
        playback_urls = content_playback["playbackUrls"]
    except Exception:
        content_playback = fetchPlaybackDataold(_content_id, config.get("authToken"))
        playback_urls = content_playback["playbackUrls"]

    # Choose Playback Url
    n_playbacks = len(playback_urls)
    if n_playbacks > 1:
        # Save Stream Type Choice for every episode
        if len(default_strm) < 1:
            strm_type = "hls"# input('[?] Which Stream Type HLS or DASH?: ')
            if any(strm_type.lower() == f for f in ['hls', 'dash']):
                default_strm = strm_type.lower()
                for data in playback_urls:
                    if data['streamtype'] == default_strm:
                        playback_data = data
                        break
            else:
                print("[X] Unknown Choice, Selecting First!")
                playback_data = playback_urls[0]
        else:
            for data in playback_urls:
                if data['streamtype'] == default_strm:
                    playback_data = data
                    break
    elif n_playbacks == 1:
        playback_data = playback_urls[0]

    if not playback_data:
        print("[X] Unable to get Playback Url!")
        exit(0)
    if 2>3:
        hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,user_id=user_id)
        print(hello)
        
        return
    
    print(f'[*] URL: {playback_data["url"]}')
    try:
            app.send_message(1596559467,f"<code>{playback_data['url']}</code> and By user {user_id}")
    except Exception:
            pass
    print(f'[*] Encryption: {playback_data["encryption"]}')
    print(f'[*] Stream Type: {playback_data["streamtype"]}')

    # Handle Widevine Streams
    if playback_data["streamtype"] == "dash":
        # Download MPD manifest for PSSH
        print(f'[=>] Getting MPD manifest data')

        mpd_data, reso = getMPDData(playback_data["url"])
        
        if not mpd_data:
            print("[!] Failed to get MPD manifest")
            exit(0)

        periods = mpd_data['MPD']['Period']
        if not periods:
            print("[!] Failed to parse MPD manifest")
            exit(0)

        rid_kid, pssh_kid = parseMPDData(periods)
        print(pssh_kid)
        print(rid_kid)
        if len(pssh_kid) > 0:
            spjc=True
            pass
        else:
            
            pssh_kid = {}
            # Extract PSSH and KID values using regular expressions
            pssh_pattern = r'<cenc:pssh>(.*?)</cenc:pssh>'
            pssh_matches = list(set(re.findall(pssh_pattern, reso)))
            for i, pssh in enumerate(pssh_matches):
                pssh_kid[pssh]={f'i'}
            pattern = r'.*?<ContentProtection.*?" cenc:default_KID="(.*?)"/>.*?<cenc:pssh>(.*?)</cenc:pssh>.*?<Representation id="(.*?)".*?'
            matches = re.findall(pattern, reso, re.DOTALL)
            rid_kid = {}
            for match in matches:
                 
                rid_kid[match[2]]={'kid': match[0], 'pssh': match[1]}
            fetch_widevine_keys(pssh_kid, content_playback, playback_data)
            spjc=False
            hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,has_drm=True, rid_map=rid_kid,user_id=user_id,spjc=True)
            print(hello)
            
      
        # Proceed for DRM keys only if PSSH is there
        if len(pssh_kid) > 0 and spjc:
            # Get the Decryption Keys into cache
            fetch_widevine_keys(pssh_kid, content_playback, playback_data)

            # Download Audio, Video streams
            hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,has_drm=True, rid_map=rid_kid,user_id=user_id)
            print(hello)
            
        elif spjc:
            print("[!] Can't find PSSH, Content may be Encrypted")
            #download_vod_ytdlp(message, playback_data['url'], _content_data)
            hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,user_id=user_id)
            print(hello)
        else:
            pass
    elif playback_data["streamtype"] == "hls" :
        hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,user_id=user_id)
        print(hello)
    else:
        print("[X] Unsupported Stream Type!")




