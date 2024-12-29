#Jio Cinema Downloader Bot Created By Aryan Chaudhary
#Ott Downloader Bot Created By Aryan Chaudhary @aryanchy451
import json
import re
import requests
import utils
import yt_dlp
import jiocine
import subprocess
from pyrogram import Client, filters, idle
from urllib import parse
import logging
from base64 import b64decode, b64encode
from yt_dlp.postprocessor import PostProcessor
from utils import scriptsDir, joinPath, realPath
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep
#from button import ButtonMaker
LOG_FILE = "log.txt"
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
def atos(func, *args, wait=True, **kwargs):
    future = run_coroutine_threadsafe(func(*args, **kwargs), bot_loop)
    return future.result() if wait else future
import os
#from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
configPath = joinPath(scriptsDir, 'config.json')
if not utils.isExist(configPath):
    utils.copyFile(joinPath(scriptsDir, 'config.def'), configPath)

# Some important variables
default_res = ""
default_strm = ''
config = utils.JSO(configPath, 4)
sudo_users = [7126874550, -1002273935741, 6209057258, 1596559467]

class ButtonMaker:
    def __init__(self):
        self.__button = []
        self.__header_button = []
        self.__first_body_button = []
        self.__last_body_button = []
        self.__footer_button = []

    def ubutton(self, key, link, position=None):
        if not position:
            self.__button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'header':
            self.__header_button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'f_body':
            self.__first_body_button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'l_body':
            self.__last_body_button.append(InlineKeyboardButton(text=key, url=link))
        elif position == 'footer':
            self.__footer_button.append(InlineKeyboardButton(text=key, url=link))

    def ibutton(self, key, data, position=None):
        if not position:
            self.__button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'header':
            self.__header_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'f_body':
            self.__first_body_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'l_body':
            self.__last_body_button.append(InlineKeyboardButton(text=key, callback_data=data))
        elif position == 'footer':
            self.__footer_button.append(InlineKeyboardButton(text=key, callback_data=data))

    def build_menu(self, b_cols=1, h_cols=8, fb_cols=2, lb_cols=2, f_cols=8):
        menu = [self.__button[i:i+b_cols]
                for i in range(0, len(self.__button), b_cols)]
        if self.__header_button:
            if len(self.__header_button) > h_cols:
                header_buttons = [self.__header_button[i:i+h_cols]
                                  for i in range(0, len(self.__header_button), h_cols)]
                menu = header_buttons + menu
            else:
                menu.insert(0, self.__header_button)
        if self.__first_body_button:
            if len(self.__first_body_button) > fb_cols:
                [menu.append(self.__first_body_button[i:i+fb_cols])
                 for i in range(0, len(self.__first_body_button), fb_cols)]
            else:
                menu.append(self.__first_body_button)
        if self.__last_body_button:
            if len(self.__last_body_button) > lb_cols:
                [menu.append(self.__last_body_button[i:i+lb_cols])
                 for i in range(0, len(self.__last_body_button), lb_cols)]
            else:
                menu.append(self.__last_body_button)
        if self.__footer_button:
            if len(self.__footer_button) > f_cols:
                [menu.append(self.__footer_button[i:i+f_cols])
                 for i in range(0, len(self.__footer_button), f_cols)]
            else:
                menu.append(self.__footer_button)
        return InlineKeyboardMarkup(menu)


def extractyt(url=None,ci=None,is_dngplay=False,is_sliv=False,is_hs=False):
    try:
        os.remove(f"info{ci}.json")
    except Exception:
        pass
    token = requests.get("https://ccroute.vercel.app/sliv").json()["token"]
    import json
    if is_dngplay:
        subprocess.run(f"yt-dlp --allow-unplayable-formats -u token -p 47c906778850df6957712a3bfd24c276 --no-check-certificate --dump-json {url} > info{ci}.json",shell=True)
    elif is_sliv:
        
        subprocess.run(f"yt-dlp --allow-unplayable-formats -u token -p {token} --no-check-certificate --proxy http://bobprakash4646:ivR8gSbjLN@103.172.85.130:49155 --dump-json {url} > info{ci}.json",shell=True)

    elif is_hs:
        url = f'"{url}"'
        subprocess.run(f"yt-dlp --allow-unplayable-formats --no-check-certificate --dump-json {url} > info{ci}.json",shell=True)
    else:
        subprocess.run(f"yt-dlp --allow-unplayable-formats --no-check-certificate --proxy http://bobprakash4646:ivR8gSbjLN@103.172.85.130:49155 --dump-json {url} > info{ci}.json",shell=True)
    import json
    with open(f'info{ci}.json', 'r') as f:
        data = json.load(f)
    return data
    
# Generate main config file from definition config before starting

app = Client(
    "jiocinemaripbot",
    bot_token="7843346619:AAHIt27qwcTMmY5-vaF_O_e8q_gOAAyeTOQ",
    api_id="5360874",
    api_hash="4631f40a1b26c2759bf1be4aff1df710",
    sleep_threshold=30
)

# Check Multi lang support
def multi_lang(_content_data, message):
    if "assetsByLanguage" in _content_data and len(_content_data["assetsByLanguage"]) > 0:
        other_langs = []

        for _lang in _content_data["assetsByLanguage"]:
            if _lang['id'] in jiocine.LANG_MAP:
                other_langs.append({
                    'id': _lang['id'],
                    'name': jiocine.LANG_MAP[_lang['id']],
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
        'id': jiocine.REV_LANG_MAP[def_lang],
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
def decrypt_vod_mp4d(kid, key, input_path, output_path):
    # Create mp4decrypt command
    mp4decPath = realPath(joinPath(scriptsDir, config.get('mp4decPath')))
    command = ["mp4decrypt", '--key', f"{kid}:{key}", input_path, output_path]
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    


# Use ffmpeg to merge video and audio
def merge_vod_ffmpeg(in_video, in_audio, output_path):
    # Create ffmpeg command
    ffmpegPath = realPath(joinPath(scriptsDir, config.get('ffmpegPath')))
    command = ["ffmpeg", '-hide_banner', '-i', in_video, '-i', in_audio, '-c:v', 'copy', '-c:a', 'copy', output_path]
    process = subprocess.run(command, stderr=subprocess.PIPE, universal_newlines=True)
    


# Use yt-dlp to download vod(video on demand) as m3u8 or dash streams into a video file
def download_vod_ytdlp(url, message, content_id, user_id, is_multi=False, has_drm=False, rid_map=None,is_jc=True):
    global default_res
    status = app.send_message(message.chat.id, f"[+] Downloading")
    ci = content_id
    with open(f"{user_id}.json",'r') as f:
        datajc = json.load(f)
    rid_map = datajc['rid_map']
    has_drm = datajc['has_drm']
    is_hs = datajc['is_hs']
    license_url = datajc['license_url']
    is_multi = datajc['is_multi']
    is_series = datajc['is_series']
    content_id = datajc['content_id']
    url = datajc['url']
    formats = datajc['formats']
    language = datajc['language']
    
    print(is_multi)
    if is_jc:
        content = jiocine.getContentDetails(content_id)
    else:
        content = {"isPremium": False}
    base_url = url

    # Output dir path
    
    temp_dir = realPath(joinPath(scriptsDir, config.get('tempPath')))
    ffmpegPath = realPath(joinPath(scriptsDir, config.get('ffmpegPath')))
    if is_jc:
    # Separate out baseUrl and Query
        parsed_url = parse.urlparse(url)
        base_url = url.replace(parsed_url.query, '')[:-1]
        
        query_head = parsed_url.query.replace("=", ":", 1).split(":")
    
    def speedmeter(d):
        if d['status'] == 'downloading':
            percentage_str = d['_percent_str']
            status.edit(f"Download Progress: {percentage_str}")
    # Add more Headers
    if is_jc:
      ydl_headers = {
          query_head[0]: query_head[1]
      }
      ydl_headers.update(jiocine.headers)

    ydl_opts = {
        'no_warnings': True,
        'nocheckcertificate': True,
        'paths': {
            'temp': temp_dir,
        },
        
    }
    if is_jc:
        ydl_opts['http_headers'] = ydl_headers
    if os.path.exists(f"{ci}.json"):
        with open(f"{ci}.json",'r') as f:
            drm = json.load(f)
        has_drm = drm['has_drm']
        rid_map = drm['rid_map']
    if is_multi:
        ydl_opts["allow_multiple_audio_streams"] = True
        ydl_opts["allow_multiple_video_streams"] = True
        print("done")
    else:
        ydl_opts["allow_multiple_audio_streams"] = True
        ydl_opts["allow_multiple_video_streams"] = True
    # yt-dlp can't download or merge if DRM is present
    if is_jc:
        is_series_episode = content["mediaType"] == "EPISODE"
    else:
        is_series_episode = False
    if has_drm:
        ydl_opts['allow_unplayable_formats'] = True
    elif is_jc and content['isPremium'] or (any(pattern in base_url for pattern in ["widevine"])):
        print("premium pass")
        pass
    else:
        if is_series_episode:
            base_url = f"https://www.jiocinema.com/tv-shows/h/1/h/{ci}"

        else:
            base_url = f"https://www.jiocinema.com/movies/h/{ci}"
    ydl_opts["proxy"] = "http://bobprakash4646:ivR8gSbjLN@103.172.85.130:49155"
    ydl_opts["no_check_certificate"] = True
    
    
    # Save Resolution Choice for every episode
 #   for audio, video in format.items():
    with open (f"hs{user_id}.json","r") as file:
        datar = json.load(file)
    formats = formats[1:]
    formats = '+'.join(datar[i] for i in formats.split('+'))
    ydl_opts['format'] = f"{formats}"
        
    if is_multi:
#    	for audio, video in format.items():
        	ydl_opts['format'] = f"bv*+mergeall[vcodec=none]"
    # Update output name
    
    
    
    if is_series_episode & is_jc:
        output_name = f'E{content["episode"]}-{content["fullTitle"]}'
        
    else:
        output_name = "OTT-DL-(BETA)"
        if is_hs:
            output_name = "Hotstar.WebDl"
            ydl_opts['proxy'] = ""
            print("proxy Removed")
        if(any(pattern in url for pattern in ["www.sonyliv.com", "sonyliv.com", "sonyliv", "https://www.sonyliv.com"])):
            is_sliv=True 
            token = requests.get("https://ccroute.vercel.app/sliv").json()["token"]
            ydl_opts['username']='token'
            ydl_opts['password']= token
            output_name = url.split("/")[-2]
        else:
            is_sliv=False
            
        if(any(pattern in url for pattern in ["dangalplay.com", "www.dangalplay.com", "dangalplay", "https://www.dangalplay.com"])):
            
            ydl_opts['username']='token'
            print("Dangal Play")
            ydl_opts['password']='47c906778850df6957712a3bfd24c276'
            ydl_opts['proxy'] = ""
            print("proxy Removed")
            output_name = url.split("/")[-1]
        if is_jc:
            output_name = f'{content["fullTitle"]}-({content["releaseYear"]})'
            print("is_jc")
        print(f"[=>] Downloading ")
    
    
    try:
        content_info = yt_dlp.YoutubeDL(ydl_opts).extract_info(base_url, download=False)
    except yt_dlp.utils.DownloadError as e:
        print(f"[!] Error Fetching Content Info: {e}")
        return
    try:
        output_name += f'.{content_info["height"]}p'
    except Exception:
        pass
    output_name += f'.{language}'
    output_name += '.WEB-DL-JC'
    output_name += ".@aryanchy451"
    

    # Audio Codec
    
    output_name += '.x264'
    
    output = f"{output_name}"
    output_name += '.%(ext)s'
    import asyncio
    chatid = message.chat.id
    message.delete()
  #  ms = message.reply_text(f"[+] Downloading {output_name}.mp4")
    ms = status.edit(f"[+] Downloading {output_name}.mp4")
    ydl_opts["external_downloader"] = "aria2c"
        
    print(output)
    print(output_name)
    
    ydl_opts['outtmpl'] = output_name
    frmts = formats.split("+")
    link = url
    
     # aria = subprocess.run(f"yt-dlp -f {dejc} -o downloads/temp/{dest} --external-downloader aria2c --proxy http://bobprakash4646:ivR8gSbjLN@103.171.50.159:49155 {link} --allow-unplayable-formats")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Custom Decryter for DRM Vids
            if has_drm:
                class DRMDecryptPP(PostProcessor):
                    def run(self, info):
                        # If hls stream
                        if 'requested_formats' not in info:
                            return [], info

                        # If decrypted file already there
                        if 'filepath' not in info['requested_formats'][0]:
                            return [], info

                        del_paths = []
                        dec_paths = []
                        self.to_screen('Doing Post Processing')
                        pssh_cache = config.get("psshCacheStore")

                        # Try finding key for
                        for fmts in info['requested_formats']:
                            fmt_id = fmts['format_id']
                            filepath = fmts['filepath']

                            fmt_code = f"f{fmt_id}"
                            outPath = fmts['filepath'].replace(fmt_code, fmt_code + "dec")

                            if fmt_id in rid_map:
                                _data = rid_map[fmt_id]
                                pssh = _data['pssh']
                                kid = _data['kid'].lower()

                                if pssh in pssh_cache:
                                    _data = pssh_cache[pssh]
                                    self.to_screen(f'{kid}:{_data[kid]}')
                                    self.to_screen('Decrypting Content')
                                    status.edit(f"[+]<code> Decrypting </code> With Keys Please Wait {filepath}")
                                    decrypt_vod_mp4d(kid, _data[kid], filepath, outPath)
                                    del_paths.append(filepath)
                                    dec_paths.append(outPath)

                        # Merge both decrypted parts
                        self.to_screen('Merging Audio and Video')
                        status.edit(f"[+]<code> Muxing </code> Please Wait")
                        merge_vod_ffmpeg(dec_paths[0], dec_paths[1], info['filepath'])

                        # Delete temp files
                        del_paths.extend(dec_paths)

                        # Move final Video to Out Dir
                        info['__files_to_move'] = {
                            info['filepath']: None
                        }

                        self.to_screen('Completed Post Processing')
                        return del_paths, info

                ydl.add_post_processor(DRMDecryptPP(), when='post_process')
               
            print(base_url)
            ydl.download([base_url])
            
            file_path = ydl.prepare_filename(content_info)
            config.set("authToken","")
            try:
                from tg import tgUploader
                uploader = tgUploader(app, ms, ms.chat.id)
                up = uploader.upload_file(file_path)
            except Exception as e:
                print(f"UPLOADING failed Contact Developer @aryanchy451{e}")
            try:
                #file_path = ydl.prepare_filename(content_info)
                file_path = file_path[:-1][:-1][:-1][:-1]+".mkv"
                from tg import tgUploader
                uploader = tgUploader(app, ms, ms.chat.id)
                up = uploader.upload_file(file_path)
            except Exception as e:
                print(f"UPLOADING failed Contact Developer @aryanchy451{e}")
    except yt_dlp.utils.DownloadError as e:
        print(f"[!] Error Downloading Content: {e}")


def download_playback(message, _content_id, _content_data, is_series=False, att=0, is_multi=False,user_id=None):
    global default_strm
    
    print(f'[=>] Fetching Playback Details')
    content_playback = jiocine.fetchPlaybackData(_content_id, config.get("authToken"))
    if not content_playback:
        print("[X] Playback Details Not Found!")
#        exit(0)

    # Display Content Info
    # print(f'[*] Id: {content_playback["contentId"]}')
    # print(f'[*] Name: {content_playback["fullTitle"]}')
    # print(f'[*] Type: {content_playback["contentType"]}')
    # print(f'[*] Language: {content_playback["defaultLanguage"]}')
    # print(f'[*] Total Duration: {content_playback["totalDuration"]}')

    playback_data = None
    try:
        playback_urls = content_playback["playbackUrls"]
    except Exception:
        content_playback = jiocine.fetchPlaybackDataold(_content_id, config.get("authToken"))
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
    print(f'[*] Encryption: {playback_data["encryption"]}')
    print(f'[*] Stream Type: {playback_data["streamtype"]}')

    # Handle Widevine Streams
    if playback_data["streamtype"] == "dash":
        # Download MPD manifest for PSSH
        print(f'[=>] Getting MPD manifest data')

        mpd_data = jiocine.getMPDData(playback_data["url"])
        if not mpd_data:
            print("[!] Failed to get MPD manifest")
            exit(0)

        periods = mpd_data['MPD']['Period']
        if not periods:
            print("[!] Failed to parse MPD manifest")
            exit(0)

        rid_kid, pssh_kid = jiocine.parseMPDData(periods)

        # Proceed for DRM keys only if PSSH is there
        if len(pssh_kid) > 0:
            # Get the Decryption Keys into cache
            fetch_widevine_keys(pssh_kid, content_playback, playback_data)

            # Download Audio, Video streams
            hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,has_drm=True, rid_map=rid_kid,user_id=user_id)
            print(hello)
        else:
            print("[!] Can't find PSSH, Content may be Encrypted")
            #download_vod_ytdlp(message, playback_data['url'], _content_data)
            hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,user_id=user_id)
            print(hello)
    elif playback_data["streamtype"] == "hls" :
        hello = youtube_link(playback_data["url"], message, _content_id, is_series=is_series, att=att,is_multi=is_multi,user_id=user_id)
        print(hello)
    else:
        print("[X] Unsupported Stream Type!")

from pyrogram import Client, filters as Filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import yt_dlp
queue = {}
import subprocess
import threading
import time
LANG_MAP = {     "en": "English",     "hi": "Hindi",     "gu": "Gujarati",     "ta": "Tamil",     "te": "Telugu",     "kn": "Kannada",     "mr": "Marathi",     "ml": "Malayalam",     "bn": "Bengali",     "bho": "Bhojpuri",     "pa": "Punjabi",     "or": "Oriya" }
jiodl = 'bot/jiod'


proxy = "0"
def download_video(url, format, message):
    if proxy != "0":
        for audio, video in format.items():
           jio_cmd = [f"{jiodl}", "-f", f"{audio}+{video}", "--proxy", f"{proxy}",  "-P", "downloads", "--cache-dir", "temp", f"{url}"]

    for audio, video in format.items():
        print(f"{audio}+{video}")
        jio_cmd = [f"jiod", "-f", f"bestaudio[language={audio}]+{video}", f"{url}"]
    try:
        process = subprocess.run(jio_cmd)
        while process.poll() is None:
            output = process.stdout.readline().decode('utf-8')
            if 'Downloading' in output:
                speed = output.split('at')[1].strip()
                message.edit(f'Downloading video at {speed}...')
                time.sleep(1)
    except Exception as e:
        print(e)
    directory = "downloads"
 #    file_name = os.listdir("downloads")[0]

    #file_path = yt_dlp.utils.get_downloaded_file(url)
    from yt_dlp import YoutubeDL

    ydl_opts = {}
    ydl = YoutubeDL(ydl_opts)
    info = ydl.extract_info(url, download=False)
    filename = ydl.prepare_filename(info)
    file_path = f"{filename}"
#    for file in os.listdir(directory):
 #           if file.endswith(".mkv") or file.endswith(".mp4"):
  #              file_path = os.path.join(directory, file)
    from tg import tgUploader
    try:
        uploader = tgUploader(app, message, message.chat.id)
        uploader.upload_file(file_path)
    except Exception as e:
        message.reply_text(f"UPLOADING failed Contact Developer @aryanchy451{e}")
#    split_and_upload_video(file_path, message)

def split_and_upload_video(file_name, message):
    file_size = os.path.getsize(file_name)
    chunk_size = 2047152000
    chunk_count = 0
    
    if file_size > chunk_size:
        app.send_message(message.chat.id, 'File size exceeds 2GB, splitting into chunks...')
        
        with open(file_name, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                chunk_count += 1
                chunk_file_name = f'{file_name}.part{chunk_count}'
                with open(chunk_file_name, 'wb') as chunk_file:
                    chunk_file.write(chunk)
                app.send_document(message.chat.id, chunk_file_name, caption=f'Video chunk {chunk_count}')
                os.remove(chunk_file_name)
        
        message.edit('Video uploaded successfully!')
    else:
        app.send_video(message.chat.id, file_name, caption='Video uploaded by JioCinema Downloader Bot')
        message.edit('Video uploaded successfully!')
        os.remove(file_name)
@app.on_message(Filters.command('start'))
def start_command(client, message):
    app.send_message(message.chat.id, 'Send a JioCinema link to download!')
#@app.on_message. 
def check_drm_hs(data):
    if data["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0] == "":
        return False
    else:
        return True
def youtube_link(url, message, ci, is_series=False, att=0,is_multi=False,has_drm=False,rid_map=None,user_id=0):
    import json
    
    if(any(pattern in url for pattern in ["dangalplay.com", "www.dangalplay.com", "dangalplay", "https://www.dangalplay.com"])):
        is_dngplay=True 
        
    else:
        is_dngplay=False
    if(any(pattern in url for pattern in ["www.hotstar.com", "hotstar.com", "hotstar", "https://www.hotstar.com"])):
        is_hs = True 
        import json
        headers = {'url':url,'api':'ottapi'}
        datahs = requests.get(url="https://hls-proxifier-sage.vercel.app/hotstar", headers=headers).json()
        url = datahs["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["primary"]["content_url"]
        if check_drm_hs(datahs):
            has_drm=True
            license_url = datahs["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0]
            headersy = {
                      "Origin": "https://www.hotstar.com",
                      "Referer": "https://www.hotstar.com/",
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            }
            r = requests.get(mpd_url, headers=headersy)
            mpd_data = xmltodict.parse(r.content)
            if not mpd_data:
                print("[!] Failed to get MPD manifest")
                return
                

            periods = mpd_data['MPD']['Period']
            if not periods:
                print("[!] Failed to parse MPD manifest")
                return
            

            rid_kid, pssh_kid = jiocine.parseMPDData(periods)
            rid_map = rid_kid
            pssh_cache = config.get("psshCacheStore")

    # Get Keys for all KIDs of PSSH
            for pssh in pssh_kid.keys():
        

        # Need to fetch even if one key missing
                fetch_keys = False
                if pssh in pssh_cache:
                    fetch_keys = False
                    
                else:
                    fetch_keys = True
        
                if fetch_keys:
                    pssh_cache[pssh] = requests.get(url='https://hls-proxifier-sage.vercel.app/hotstar',headers={"url":license_url,"pssh":pssh}).json()["keys"]
                    config.set("psshCacheStore", pssh_cache)
        else:
            license_url = None
    else:
        is_hs = False   
        license_url = None
    if(any(pattern in url for pattern in ["www.jiocinema.com", "jiocinema.com", "jiocinema", "https://www.jiocinema.com"])):
        is_jc=True 
    else:
        is_jc = False
    if(any(pattern in url for pattern in ["www.sonyliv.com", "sonyliv.com", "sonyliv", "https://www.sonyliv.com"])):
        is_sliv=True 
        
    else:
        is_sliv=False
        
    if 2<3:
        keys = {"rid_map":rid_map,"has_drm":has_drm,"license_url":license_url,"is_hs":is_hs,"is_multi":is_multi,"is_series":is_series,"content_id":ci,"url":url,"formats": "None", "language":"None"}
        with open(f"{user_id}.json",'w') as f:
            json.dump(keys,f)

    if is_series and att > 1:
        
        message = app.send_message(message.chat.id, f'Processing')
        download_vod_ytdlp(url, message, ci, user_id, is_multi=is_multi)
        return "se"	
    if is_jc:
        content = jiocine.getContentDetails(ci)
        print("nice")
        if is_jc:
            is_series_episode = content["mediaType"] == "EPISODE"
        else:
            is_series_episode = False
        
        if content['isPremium'] or (any(pattern in url for pattern in ["widevine"])):
            pass
        else:
            if is_series_episode:
                url = f"https://www.jiocinema.com/tv-shows/h/1/h/{ci}"
                print(url)
            else:
                url = f"https://www.jiocinema.com/movies/h/{ci}"
                print(url)

        
    data = extractyt(url=url,ci=ci,is_dngplay=is_dngplay,is_sliv=is_sliv,is_hs=is_hs)
   
    keyboard = []
    buttons = ButtonMaker()
    if is_multi:
        buttons.ibutton(f"Multi Audio", f"d_hi_{ci}_{usrid}_None")
        reply_markup = buttons.build_menu(2)
        message.reply(f'Select formats to download For', reply_markup=reply_markup)
        import time
        time.sleep(1)
        message.delete()
        return "hi"
    with open(f"hs{user_id}.json",'w') as writ, open(f"hsr{user_id}.json",'w') as rwrit:
      frmts = {}
      rfrmts = {}
      start = 'a'
      for lang in data['formats']:
        if lang['resolution'] == "audio only":
            langu = lang['language']
            format = lang['format_id']
            rfrmts[format] = start
            frmts['start'] = format
            format = start
            key = f"Audio - {langu}"
            buttons.ibutton(f"{key}", f"d_{format}_{ci}_{user_id}_None")
            start = chr(ord(start) + 1)
        else:
            format_id = lang['format_id']
            frmts['start'] = format_id
            rfrmts[format_id] = start
            format_id = start
            try:
              he = lang["height"]
            except Exception:
              he = "unknown"
            vbr = lang["vbr"]
            k = f"Video-{he}p-{vbr}Kbps"
         #   k = f"Video-{lang["height"]}p-{lang["vbr"]}Kbps"
            buttons.ibutton(k, f"d_{format_id}_{ci}_{user_id}_None")
            start = chr(ord(start) + 1)
      json.dump(frmts, writ)

      json.dump(rfrmts, rwrit)
            
            
        

    buttons.ibutton("Cancel", f"d_cancel_{ci}_{user_id}_None")
    buttons.ibutton("Reload 🔃", f"d_reload_{ci}_{user_id}_None")
  #  buttons.ibutton("Done", f"d_done_{ci}_{user_id}_None")
    reply_markup = buttons.build_menu(2)
    app.send_message(message.chat.id, text=f'Select formats to download', reply_markup=reply_markup)
    import time
    time.sleep(1)
    message.delete()
    return "hi"


    
    

@app.on_callback_query(Filters.regex(r'^d_.*$'))
def download_button(_, callback_query):
    message = callback_query.message
    
    ci = callback_query.data[1:][1:].rpartition("_")[0].rpartition("_")[0].rpartition("_")[2]
    
    
    user_id = callback_query.data[1:][1:].rpartition("_")[0].rpartition("_")[2]
    data = callback_query.data[1:][1:].rpartition("_")[0].rpartition("_")[0].rpartition("_")[0]
    lang = callback_query.data.rpartition("_")[2]
    if int(user_id.replace(" ","")) != int(callback_query.from_user.id):
            callback_query.answer("Not Yours Query Button")
            return
    buttons = ButtonMaker()
    if data == "cancel":
        try:
    	    os.remove(f"{user_id}.json")
        except Exception:
            pass
        try:
    	    os.remove(f'format{ci}{user_id}.json')
        except Exception:
            pass
        callback_query.message.delete()
        return
    elif data == "done":
        with open(f"{user_id}.json",'r') as f: 
            datajc = json.load(f)
        url = datajc['url']
        message = app.send_message(callback_query.message.chat.id, f'Processing') 
        callback_query.message.delete() 
        if int(ci) == 1:
            download_vod_ytdlp(url, message, ci,user_id=user_id,is_jc=False) 
        else:
            download_vod_ytdlp(url, message, ci,user_id=user_id) 
        return
    elif data == "selected":
        callback_query.answer("Can't Select Again Try Reload # Created By Aryan Chaudhary")
        return
    elif data == "reload":
 #       print(user_id)
#        print(callback_query.from_user.id)
   #     if int(user_id.replace(" ","")) != int(callback_query.from_user.id):
  #          callback_query.answer("Not Yours Query Button")
 #           return
        with open(f"{user_id}.json",'r') as f:
            datajc = json.load(f)
        rid_map = datajc['rid_map']
        has_drm = datajc['has_drm']
        is_hs = datajc['is_hs']
        license_url = datajc['license_url']
        is_multi = datajc['is_multi']
        is_series = datajc['is_series']
        content_id = datajc['content_id']
        url = datajc['url']
        formats = datajc['formats']
        language = datajc['language']
        formatid = "None"
        lang = "None"
       # formatid = f"{formats}+{data}".replace("None","").replace("none","").replace("None+","").replace("none+","").replace(" ","").replace("++","+")
     #   print(formatid)
      #  lang = lang.upper()
#        fromatid = formatid[:-1]
#        format_ids = formatid.split('+')
 #       unique_format_ids = set(format_ids)
#        formatid = formatid[1:]
  #      formatid = '+'.join(unique_format_ids)
       # lang = f"{language}+{lang}".replace("None","").replace(" ","").replace("NONE","").replace("NONE+","").replace("++","")
        keys = {"rid_map":rid_map,"has_drm":has_drm,"license_url":license_url,"is_hs":is_hs,"is_multi":is_multi,"is_series":is_series,"content_id":ci,"url":url, "formats": formatid , "language":lang}
        with open(f"{user_id}.json",'w') as f:
            json.dump(keys,f)
        with open(f'info{ci}.json', 'r') as f:
            data = json.load(f)
        formatsa = formatid.split("+")
        with open(f"hsr{user_id}.json",'r') as writ:
          frmts = json.load(writ)
          
          for lange in data['formats']:
            if lange['resolution'] == "audio only":
                langu = lange['language']
                format = lange['format_id']
                format = frmts[format]
                
                key = f"Audio - {langu}"
                for keys in formatsa:
                    if format == keys:
                        key = f"{key}✅"
                if key.endswith("✅"):
                    buttons.ibutton(f"{key}", f"d_selected_{ci}_{user_id}_{langu}")
                else:
                    buttons.ibutton(f"{key}", f"d_{format}_{ci}_{user_id}_{langu}")
            else:
                format_id = lange['format_id']
                format_id = frmts[format_id]
                try:
                  he = lange["height"]
                except Exception:
                  he = "unknown"
                vbr = lange["vbr"]
                key = f"Video-{he}p-{vbr}Kbps"
                for keys in formatsa:
                    if format_id == keys:
                        key = f"{key}✅"
                if key.endswith("✅"):
                    buttons.ibutton(f"{key}", f"d_selected_{ci}_{user_id}_None")
                else:
                    buttons.ibutton(f"{key}", f"d_{format_id}_{ci}_{user_id}_None")
        

        buttons.ibutton("Cancel", f"d_cancel_{ci}_{user_id}_None")
        buttons.ibutton("Reload 🔃", f"d_reload_{ci}_{user_id}_None")
        buttons.ibutton("Done", f"d_done_{ci}_{user_id}_None")
        reply_markup = buttons.build_menu(1)
        app.edit_message_reply_markup(message.chat.id, message.id, reply_markup)
        return
    
    else:
    #    if user_id != callback_query.from_user.id:
     #       callback_query.answer("Not Yours Query Button")
      #      return
        with open(f"{user_id}.json",'r') as f:
            datajc = json.load(f)
        rid_map = datajc['rid_map']
        has_drm = datajc['has_drm']
        is_multi = datajc['is_multi']
        is_series = datajc['is_series']
        content_id = datajc['content_id']
        url = datajc['url']
        is_hs = datajc['is_hs']
        license_url = datajc['license_url']
        formats = datajc['formats']
        language = datajc['language']
        formatid = f"{formats}+{data}".replace("None","").replace("none","").replace("None+","").replace("none+","").replace(" ","").replace("++","+")
        print(formatid)
        lang = lang.upper()
        lang = f"{language}+{lang}".replace("None","").replace(" ","").replace("NONE","").replace("NONE+","").replace("++","")
        keys = {"rid_map":rid_map,"has_drm":has_drm,"license_url":license_url,"is_hs":is_hs,"is_multi":is_multi,"is_series":is_series,"content_id":ci,"url":url, "formats": formatid , "language":lang}
        with open(f"{user_id}.json",'w') as f:
            json.dump(keys,f)
        with open(f'info{ci}.json', 'r') as f:
            data = json.load(f)
        formatsa = formatid.split("+")
        with open(f"hsr{user_id}.json",'r') as writ:
          frmts = json.load(writ)
          import logging 
          try:
              logging.info(json.dumps(frmts))
          except Exception:
              pass
          for lange in data['formats']:
            if lange['resolution'] == "audio only":
                langu = lange['language']
                format = lange['format_id']
                format = frmts[format]
                key = f"Audio - {langu}"
                for keys in formatsa:
                    if format == keys:
                        key = f"{key}✅"
                if key.endswith("✅"):
                    buttons.ibutton(f"{key}", f"d_selected_{ci}_{user_id}_{langu}")
                else:
                    buttons.ibutton(f"{key}", f"d_{format}_{ci}_{user_id}_{langu}")
            else:
                format_id = lange['format_id']
                format_id = frmts[format_id]
                try:
                  he = lange["height"]
                except Exception:
                  he = "unknown"
                vbr = lange["vbr"]
                key = f"Video-{he}p-{vbr}Kbps"
                
                for keys in formatsa:
                    if format_id == keys:
                        key = f"{key}✅"
                if key.endswith("✅"):
                    buttons.ibutton(f"{key}", f"d_selected_{ci}_{user_id}_None")
                else:
                    buttons.ibutton(f"{key}", f"d_{format_id}_{ci}_{user_id}_None")
        

        buttons.ibutton("Cancel", f"d_cancel_{ci}_{user_id}_None")
        buttons.ibutton("Reload 🔃", f"d_reload_{ci}_{user_id}_None")
        buttons.ibutton("Done", f"d_done_{ci}_{user_id}_None")
        reply_markup = buttons.build_menu(2)
        app.edit_message_reply_markup(message.chat.id, message.id, reply_markup)
        return
    
    
    
    


@app.on_message(filters.chat(sudo_users) & filters.command("dl"))
def jiodl(client, message):

    user_id = message.from_user.id
    print('[=>] OTT Downloader Starting Created By Aryan Chaudhary')
    import logging
    logging.info('[=>] OTT Downloader Starting Created By Aryan Chaudhary')

    # Fetch Guest token when Not using Account token
    if not config.get("authToken") and not config.get("useAccount"):
        print("[=>] Guest Token is Missing, Requesting One")
        guestToken = jiocine.fetchGuestToken()
        if not guestToken:
            print("[!] Guest Token Not Received")
#            exit(0)

        print("[=>] Got Guest Token :)")
        config.set("authToken", guestToken)

    print(f'[=>] Welcome {config.get("accountName")}, Jio Cinema Free User')

    # content_id = input(f'[?] Enter Content Id: ')
    # if len(content_id) < 1:
    #     print("[!] Enter Valid Id")
    #     exit(0)

    content_url = (message.text[1:][1:][1:][1:]).split(" -")[0]# input(f'[?] Enter Content Url: ')
    url = content_url
    if len(content_url) < 1:
        print("[!] Enter Valid Url")
 #       exit(0)

    # Ref: https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    # URL Sanitization
    urlRegex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    m = message.reply_text("Processing")
    # URL Check
    if re.match(urlRegex, content_url) is None:
        m.edit("Please Provide Valid URL!")
  #      exit(0)

    # Get and validate content id
    content_url = content_url.split('/')
    try:
        int(content_url[-1])
        content_id = content_url[-1]
    except:
        print("Please Provide Valid URL!!")
        content_id = 1
   #     exit(0)
#    m = message.reply_text("Processing")
    print('[=>] Fetching Content Details')
    # content_id = 3216132  # 3760812  # 4K Test: 3719559
    try:
        content_data = jiocine.getContentDetails(content_id)
    except Exception as e:
        m.edit("Trying Other Ott Dl Beta Phase in 2 Secs")
        message = m
        hello = youtube_link(url, message, 1, user_id=user_id)
        print(hello)
        return
    if not content_data:
        m.edit("Trying Other Ott Dl Beta Phase in 2 Secs")
        message = m
        hello = youtube_link(url, message, 1, user_id=user_id)
        print(hello)
        return
    #    exit(0)

 #   m.edit('[+] Found Video Details')
  #  m.edit(f'[+] Id: {content_data["id"]}')
    m.edit(f'[+] Name: {content_data["shortTitle"]}')
    
    print(f'[*] Type: {content_data["mediaType"]}')
#    m.edit(f'[*] Default Language: {content_data["defaultLanguage"]}')
    print(f'[*] Release Year: {content_data["releaseYear"]}')

    

    if content_data['isPremium'] :
        Token = requests.get("https://hls-proxifier-sage.vercel.app/jiotoken").json()['token']
        config.set("authToken", Token)
        m.edit("[+] Need Premium Account for this Content")
     #   exit(0)

    # Show and Series links are complicated
    if content_data["mediaType"] == "SHOW" or content_data["mediaType"] == "SERIES":
        m.edit("[+] Shows/Series Link Unsupported, Download Using Individual Episodes Links")
      #  exit(0)

    # There may be other languages
    lang_data = {}
    lang_data['assetsId'] = content_id
    
    if lang_data and content_id!= lang_data['assetsId']:
        print('[=>] Language Changed!')
        print(f'[*] Id: {lang_data["id"]}')
        m.edit(f'[+] Language: {lang_data["name"]}')
        # Update Content Details
        content_id = lang_data['assetsId']
        content_data = jiocine.getContentDetails(content_id)
        if not content_data:
            print("[X] Content Details Not Found!")
 #           exit(0)
#
    
    tef = message.text
    # Give Full Series a Chance ;)
    if(any(pattern in tef for pattern in ["-multi", "- multi", " -multi", " - multi"])):
        	is_multi=True
    else:
        	is_multi=False
    if content_data["mediaType"] == "EPISODE" and len(content_data["seasonId"]) > 0:
        need_series = "no"#input('[?] Do you want to download whole series (yes/no)?: ')
        
        tef = message.text
        if(any(pattern in tef for pattern in ["-full", "- full", " -full", " - full"])):
    
            season_id = content_data['seasonId']
            att = 0
            season_data = jiocine.getContentDetails(season_id)
            if not season_data:
                print("[X] Season Details Not Found!")
                exit(0)

            print('[=>] Found Season Details')
            print(f'[*] Name: {season_data["shortTitle"]}')
            print(f'[*] Type: {season_data["mediaType"]}')
            print(f'[*] Default Language: {season_data["defaultLanguage"]}')
            print(f'[*] Release Year: {season_data["releaseYear"]}')

            episodes = jiocine.getSeriesEpisodes(season_id)
            if not episodes:
                print("[X] Season Episodes Not Found!")
  #              exit(0)

            # Go through every episode with language choice
            for idx, episode in enumerate(episodes):
                episode_id = episode['id']
                att = att + 1
       
                episode_data = jiocine.getContentDetails(episode_id)
                if not episode_data:
                    print(f"[X] Episode-{idx + 1} Details Not Found!")
                    continue

                # Find Chosen Language
                if "assetsByLanguage" in episode_data and len(episode_data["assetsByLanguage"]) > 0:
                    for lang in episode_data["assetsByLanguage"]:
                        if lang_data["id"] == lang['id']:
                            # Change Language
                            episode_id = lang['assetId']
                            episode_data = jiocine.getContentDetails(episode_id)
                            if not episode_data:
                                print(f"[X] Episode-{idx + 1} Details Not Found!!")
                                continue
                            break
                message = m
                # Download Each Episode of Season
              #  if(any(pattern in tef for pattern in ["-full", "- full", " -full", " - full"])):
                download_playback(message, episode_id, episode_data, is_series=True, att=att, is_multi=is_multi,user_id=user_id)
        else:
            # Download Single Episode Only
            message = m
            
            download_playback(message, content_id, content_data,is_series=False,att=0,is_multi=is_multi,user_id=user_id)
    else:
        # Download Single Episode or Movie
        message = m
        download_playback(message, content_id, content_data,is_series=False,att=0,is_multi=is_multi,user_id=user_id)

    print("[=>] Jio Cinema Playback And Button Created")

from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe
from asyncio.subprocess import PIPE
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.types import InputMediaPhoto
from pyrogram.errors import ReplyMarkupInvalid, FloodWait, PeerIdInvalid, ChannelInvalid, RPCError, UserNotParticipant, MessageNotModified, MessageEmpty, PhotoInvalidDimensions, WebpageCurlFailed, MediaEmpty


#from asyncio import sleep

from random import choice as rchoice
from time import time
from re import match as re_match


async def sendFile(message, file, caption=None, buttons=None):
    try:
        return await message.reply_document(document=file, quote=True, caption=caption, disable_notification=True, reply_markup=buttons)

    except Exception as e:
       # LOGGER.error(str(e))
        return str(e)

async def sendMessage(message, text, buttons=None, photo=None, **kwargs):
    try:
        return await message.reply(text=text, quote=True, disable_web_page_preview=True, disable_notification=True,
                                    reply_markup=buttons, reply_to_message_id=rply.id if (rply := message.reply_to_message) and not rply.text and not rply.caption else None,
                                    **kwargs)

    except Exception as e:
     #   LOGGER.error(format_exc())
        return str(e)

async def cmd_exec(cmd, shell=False):
    
    if shell:
        proc = await create_subprocess_shell(cmd, stdout=PIPE, stderr=PIPE)
    else:
        proc = await create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()
    return stdout, stderr, proc.returncode

#!/usr/bin/env python3
from pyrogram.handlers import MessageHandler, EditedMessageHandler
from pyrogram.filters import command
from io import BytesIO

import os
import time
import sys
from asyncio import create_subprocess_exec, gather, run as asyrun
@app.on_message(filters.chat(sudo_users) & filters.command("restart"))
async def restart(client, message):
    # Check if the message is from the owner
    if 2<3:
        restart_message = await message.reply_text('RESTARTING')
        # Send a confirmation message to the owner
        
        proc1 = await create_subprocess_exec('pkill', '-9', '-f', 'ffmpeg|gunicorn')
        proc2 = await create_subprocess_exec('python3', 'update.py')
        await gather(proc1.wait(), proc2.wait())
      #  async with aiopen(".restartmsg", "w") as f:
          #  await f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
        # Restart the bot
        os.execl(sys.executable, sys.executable, "main.py")
        
    else:
        await message.reply("You're not authorized to restart the bot!")

@app.on_message(filters.chat(sudo_users) & filters.command("reset"))
def reset(client, message):
    config.set("authToken","")
    message.reply_text("Done")
@app.on_message(filters.chat(sudo_users) & filters.command("fetch"))
def resety(client, message):
    import requests
    Token = requests.get("https://hls-proxifier-sage.vercel.app/jiotoken").json()['token']
    config.set("authToken",Token)
    message.reply_text("Done")

async def shell(_, message):
    cmd = message.text.split(maxsplit=1)
    if len(cmd) == 1:
        await sendMessage(message, 'No command to execute was given.')
        return
    if message.from_user.id not in sudo_users:
        await sendMessage(message, 'You Cant use shell')
        return
    cmd = cmd[1]
    stdout, stderr, _ = await cmd_exec(cmd, shell=True)
    reply = ''
    if len(stdout) != 0:
        reply += f"*Stdout*\n{stdout}\n"
       # LOGGER.info(f"Shell - {cmd} - {stdout}")
    if len(stderr) != 0:
        reply += f"*Stderr*\n{stderr}"
       # LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with BytesIO(str.encode(reply)) as out_file:
            out_file.name = "shell_output.txt"
            await sendFile(message, out_file)
    elif len(reply) != 0:
        await sendMessage(message, reply)
    else:
        await sendMessage(message, 'No Reply')
def main():
    app.start()
    app.add_handler(MessageHandler(shell, filters=command('shell') ))
    app.add_handler(EditedMessageHandler(shell, filters=command('shell') ))
 
    print("bot started")
    idle()
    app.stop()
app.loop.run_until_complete(main())
