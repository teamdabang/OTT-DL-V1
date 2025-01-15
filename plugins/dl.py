import subprocess
import yt_dlp
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *
##from plugins.handler.playback import *
#from plugins.handler.mhandler import* 
#from plugins.ytdl import *

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

    

def downloadformat(ydl_opts,url,info):
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        file_path = ydl.prepare_filename(info)
        return file_path
        
def decrypt_vod_mp4(kid, key, input_path, output_path):
    # Create mp4decrypt command
   # mp4decPath = realPath(joinPath(scriptsDir, config.get('mp4decPath')))
    command = ["mp4decrypt", '--key', f"{kid}:{key}", input_path, output_path]
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    try:
        process.wait()
    except Exception:
        pass
    return "Done"
        
def decrypt_vod_mp4d(kid, key, input_path, output_path):
    # Create mp4decrypt command
   # mp4decPath = realPath(joinPath(scriptsDir, config.get('mp4decPath')))
    command = ["mp4decrypt", '--key', f"{kid}:{key}", input_path, output_path]
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    return "Done"
    


# Use ffmpeg to merge video and audio
def merge_vod_ffmpeg(in_video, in_audio, output_path):
    # Create ffmpeg command
   # ffmpegPath = realPath(joinPath(scriptsDir, config.get('ffmpegPath')))
    command = ["ffmpeg", '-hide_banner', '-i', in_video, '-i', in_audio, '-c:v', 'copy', '-c:a', 'copy', output_path]
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    
