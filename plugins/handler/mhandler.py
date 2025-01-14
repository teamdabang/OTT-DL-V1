import pyrogram 
import logging 
import requests 
from main import *


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
def download_vod_ytdlp(url, message, content_id, user_id, is_multi=False, has_drm=False, rid_map=None,is_jc=True,spjc=False):
    global default_res
    import os
    
    status = app.send_message(message.chat.id, f"[😋] Downloading")
    ci = content_id
    with open(f"{user_id}.json",'r') as f:
        datajc = json.load(f)
    rid_map = datajc['rid_map']
    has_drm = datajc['has_drm']
    is_hs = datajc['is_hs']
    name = datajc['name']
    spjc = datajc['spjc']
    license_url = datajc['license_url']
    is_multi = datajc['is_multi']
    is_series = datajc['is_series']
    content_id = datajc['content_id']
    url = datajc['url']
    formats = datajc['formats']
    language = datajc['language']
    
    print(is_multi)
    if is_jc:
        content = getContentDetails(content_id)
    else:
        content = {"isPremium": False}
    base_url = url

    # Output dir path
    
    temp_dir = realPath(joinPath(scriptsDir, config.get('tempPath')))
    ffmpegPath = realPath(joinPath(scriptsDir, config.get('ffmpegPath')))
