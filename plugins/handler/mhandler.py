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
def download_vod_ytdlp(url, message, content_id, user_id, is_multi=False, has_drm=False, rid_map=None,is_jc=True,spjc=False):
    global default_res
    import os
    
    status = app.send_message(message.chat.id, text=f"[😋] Downloading")
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
    


# Check Multi lang support


    
    def speedmeter(d):
        if d['status'] == 'downloading':
            percentage_str = d['_percent_str']
            status.edit(f"Download Progress: {percentage_str}")
    # Add more Headers
    if is_jc:
      ydl_headers = {}
      ydl_headers.update(headers)
      
    ydl_opts = {
        'no_warnings': True,
        'nocheckcertificate': True,
        'paths': {
            'temp': temp_dir,
        },
        
    }
    if is_jc:
        
        ydl_opts['http_headers'] = ydl_headers
        base_url = url
    if is_hs:
        headersy = {
                      "Origin": "https://www.hotstar.com",
                      "Referer": "https://www.hotstar.com/",
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        }
        ydl_opts['http_headers'] = headersy
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
    elif is_jc:
        if is_series_episode:
            base_url = f"https://www.jiocinema.com/tv-shows/h/1/h/{ci}"

        else:
            base_url = f"https://www.jiocinema.com/movies/h/{ci}"
    ydl_opts["proxy"] = "http://toonrips:xipTsP9H9s@103.171.51.246:50100"
    ydl_opts["no_check_certificate"] = True
    
    
    # Save Resolution Choice for every episode
 #   for audio, video in format.items():
    with open (f"hs{user_id}.json","r") as file:
        datar = json.load(file)

        import logging
        logging.info(json.dumps(datar))
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
        output_name = "OTT-DL"
        if is_hs:
            output_name = "Hotstar"
       #     ydl_opts['proxy'] = ""
         #   print("proxy Removed")
            
        if(any(pattern in url for pattern in ["www.sonyliv.com", "sonyliv.com", "sonyliv", "https://www.sonyliv.com"])):
            is_sliv=True 

            output_name = "SonyLiv"
            head = {
                      "x-playback-session-id": "47c6938a7c5c4bd48d503e330c9e6512-1735474637849"
                }
            ydl_opts['http_headers'] = head
        else:
            is_sliv=False

        if(any(pattern in url for pattern in ["ZEE5"])):
            output_name = "Zee5DL"
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
        if(any(pattern in url for pattern in ["dplus"])):
            is_dplus = True
            ydl_opts['proxy'] = ""
        else:
            is_dplus = False
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
    output_name += ".@PayPalMafiaOfficial"
    

    # Audio Codec
    
    output_name += '.x264'
    
    output = f"{output_name}"
    ffout = output + '.mkv'
    ffout = f'{ffout}'
    file_downloaded = []
    dc = {}
    output_name += '.%(ext)s'
    import asyncio
    chatid = message.chat.id
    message.delete()
  #  ms = message.reply_text(f"[😋] Downloading {output_name}.mp4")
    ms = status.edit(f"[😋] Downloading {output_name}.mp4")
    ydl_opts["external_downloader"] = "aria2c"
        
    print(output)
    print(output_name)
    
    ydl_opts['outtmpl'] = output_name
    frmts = formats.split("+")
    frt = frmts[0]
    dcr = {}
    import logging
    if is_hs:
      for fr in frmts:

        r = detector(content_id,fr)
        if r == 1:
            ns = content_id + f'.{fr}' + '.%(ext)s'
            use = content_id + f'.{fr}' + '.m4a'
        else:
            ns = content_id + f'.{fr}' + '.%(ext)s'
            use = content_id + f'.{fr}' + '.mp4'
        ydl_opts['outtmpl'] = ns
        fmt_code = f"{fr}"
        
        logging.info(fmt_code)
        logging.info("Done fr")
        ydl_opts['format'] = fr
        try:
            res = downloadformat(ydl_opts,base_url,content_info)
        except Exception as e:
            logging.info(f"error in fr {e}")
        
        outPath = use.replace(fmt_code, fmt_code + "dec")
        pssh_cache = config.get("psshCacheStore")
        if has_drm:

            file_downloaded.append(f'{outPath}')
            dc[fr] = outPath
            dcr[fr] = use
        else:
            file_downloaded.append(f'{use}')
            logging.info(outPath)

            logging.info(f"res={res}")
      
        if has_drm and fr in rid_map:
                                _data = rid_map[fr]
                                pssh = _data['pssh']
                                
                                kid = _data['kid'].lower()

                                if pssh in pssh_cache:
                                    _data = pssh_cache[pssh]
                                    logging.info(f'{kid}:{_data[kid]}')
                                    dc[fr] = f'{dc[fr]}'
                                    dcr[fr] = f'{dcr[fr]}'
                                    logging.info('Decrypting Content')
                                    status.edit(f"[+]<code> Decrypting </code> With Keys Please Wait {dcr[fr]}")
                                    try:
                                        logging.info(f"use {dcr[fr]} to {dc[fr]}")
                                        import os
                                        if os.path.exists(dcr[fr]):
                                            pass
                                        else:
                                            return
                                        try:
                                           # command = f'mp4decrypt --key "{kid}:{_data[kid]}" "{dcr[fr]}" "{dc[fr]}"'
                                            di = decrypt_vod_mp4(kid, _data[kid], dcr[fr], dc[fr])
                                            logging.info(di)
                                        except subprocess.CalledProcessError as e:
                                            logging.info(e)
                                        
                                        print("Done Decrypt")
                                    except Exception as e:
                                        logging.info(e)
                                    try:
                                      pass
                                    #  os.remove(res)
                                    except Exception:
                                      logging.info("not found")
      try:
          logging.info("Merging")
          rd = mergeall(file_downloaded,ffout)
          print(rd)
      except Exception as e:
            logging.info(f"error in ffmpeg {e}")
      file_path = ffout
      try:
                from tg import tgUploader
                uploader = tgUploader(app, ms, ms.chat.id)
                up = uploader.upload_file(file_path)
      except Exception as e:
                print(f"UPLOADING failed Contact Developer @aryanchy451{e}")
    elif spjc:
        keyt = ""
        if has_drm and frt in rid_map:
                                _data = rid_map[frt]
                                pssh = _data['pssh']
                                pssh_cache = config.get("psshCacheStore")
                                if pssh in pssh_cache:
                                    _data = pssh_cache[pssh]
        for f,g in _data.items():
            keyt = keyt + f'--key "{f}:{g}" '
        ch = downloaddash(ffout,keyt,frmts,url)
        print(ch)
        file_path = ffout
        try:
                from tg import tgUploader
                uploader = tgUploader(app, ms, ms.chat.id)
                up = uploader.upload_file(file_path)
        except Exception as e:
                print(f"UPLOADING failed Contact Developer @aryanchy451{e}")
        
    else:
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
                        files = []
                        dec_paths = []
                        self.to_screen('Doing Post Processing')
                        pssh_cache = config.get("psshCacheStore")

                        # Try finding key for
                        for fmts in info['requested_formats']:
                            fmt_id = fmts['format_id']
                            filepath = fmts['filepath']

                            fmt_code = f"f{fmt_id}"
                            outPath = fmts['filepath'].replace(fmt_code, fmt_code + "dec")
                            files.append(outPath)

                            if fmt_id in rid_map:
                                _data = rid_map[fmt_id]
                                pssh = _data['pssh']
                                kid = _data['kid'].lower()

                                if pssh in pssh_cache:
                                    _data = pssh_cache[pssh]
                                    self.to_screen(f'{kid}:{_data[kid]}')
                                    self.to_screen('Decrypting Content')
                                    status.edit(f"[🥰]<code> Decrypting </code> With Keys Please Wait {filepath}")
                                    self.to_screen(filepath)
                                    self.to_screen(outPath)
                                    decrypt_vod_mp4(kid, _data[kid], filepath, outPath)
                                    del_paths.append(filepath)
                                    dec_paths.append(outPath)

                        # Merge both decrypted parts
                        self.to_screen('Merging Audio and Video')
                        status.edit(f"[👊]<code> Muxing </code> Please Wait")
                        mergeall(files, info['filepath'])  #dec_paths[0], dec_paths[1]

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
                out_file_name = file_path
    
                ms.edit("Uploading To Google Drive it takes just below 1 minute")
                import time
                #from gdrive import GoogleDriveUploader
                srt = time.time()
                upload_path = "BOT Uploads/{}/{}".format("OTTDOWNLOAD", "Driver")
                uploader = GoogleDriveUploader(app, ms, srt)
                uploader.upload_file(out_file_name, upload_path)
                print("File Uploaded")
            except Exception as e:
                print(f"UPLOADING failed Contact Developer @maheshsirop{e}")
            try:
                #file_path = ydl.prepare_filename(content_info)
                file_path = file_path[:-1][:-1][:-1][:-1]+".mkv"
                #from gdrive import GoogleDriveUploader
                import time
                upload_path = "BOT Uploads/{}/{}".format("OTTDOWNLOAD", "Driver")
                srt = time.time()
                uploader = GoogleDriveUploader(app, ms, srt)
                uploader.upload_file(file_path, upload_path)
                print("File Uploaded")
            except Exception as e:
                print(f"UPLOADING failed Contact Developer @maheshsirop{e}")
      except yt_dlp.utils.DownloadError as e:
        print(f"[!] Error Downloading Content: {e}")



            
      

            





