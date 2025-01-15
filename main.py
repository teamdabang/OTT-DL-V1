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
from pyrogram import Client, filters, idle
from urllib import parse
import logging
import os
##from plugins.handler.playback import download_playback
#from plugins.ytdl import extractyt
from plugins.handler.mhandler import *
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *

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
sudo_users = [7126874550, -1002273935741, 6209057258, 1596559467, 7361945688, 1195351595]





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








def youtube_link(url, message, ci, is_series=False, att=0,is_multi=False,has_drm=False,rid_map=None,user_id=0,spjc=False):
    import json
    
    
    if(any(pattern in url for pattern in ["dangalplay.com", "www.dangalplay.com", "dangalplay", "https://www.dangalplay.com"])):
        is_dngplay=True 
        
    else:
        is_dngplay=False
    if(any(pattern in url for pattern in ["www.zee5.com", "zee5.com", "zee5", "https://www.zee5.com"])):
            if(any(pattern in url for pattern in ["movies"])):
                ctnid = url.split('/')[-1]
                datazee5 = requests.get(f"https://zee5-olive.vercel.app/zee5?id={ctnid}&type=MOVIE").json()
                nl = datazee5['nl']
                customdata = datazee5['customdata']
                mpd = datazee5['mpd']
                url = mpd
            else:
                showid = url.split('/')[-3]
                ctnid = url.split('/')[-1]
                datazee5 = requests.get(f"https://zee5-olive.vercel.app/zee5?id={ctnid}&type=EPISODE&show={showid}").json()
                nl = datazee5['nl']
                customdata = datazee5['customdata']
                mpd = datazee5['mpd']
                url = mpd
            is_zee5 = True
            headersy = {
                      "Origin": "https://www.zee5.com",
                      "Referer": "https://www.zee5.com/",
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            }
            proxy = {'http':'http://toonrips:xipTsP9H9s@103.171.51.246:50100','https':"http://toonrips:xipTsP9H9s@103.171.51.246:50100"}
            r = requests.get(url, headers=headersy, proxies=proxy)
            import logging
            logging.info(r)
            import xmltodict
            logging.info(r.content)
            import re
            
            def kidr(text):
                pattern = rb'cenc:default_KID="(.*?)" schemeIdUri/>'
                matches = re.findall(pattern, text)
                if matches:
                    print("kid fetch")
                    smaller_pssh = min(matches, key=len)
                    return smaller_pssh.strip().decode()

            kid = kidr(r.content)
            def extract_unique_pssh_and_kid(text):
                
                pattern = rb"<cenc:pssh>(.*?)</cenc:pssh>"
                matches = re.findall(pattern, text)
                if matches:
                    print("hi")
                    smaller_pssh = min(matches, key=len)
                    kyid = kid
                    return smaller_pssh.strip().decode(), smaller_pssh.strip().decode()


            
            pssh_kid, to_use_pssh = extract_unique_pssh_and_kid(r.content)
            
            pssh_cache = config.get("psshCacheStore")

    # Get Keys for all KIDs of PSSH
            pssh = to_use_pssh
            if pssh:
                has_drm = True
                
                logging.info("pssh found zee5")
                def getkid(test):
                    for key,value in test.items():
                        return key
        

        # Need to fetch even if one key missing
                fetch_keys = False
                if pssh in pssh_cache:
                    kid = getkid(pssh_cache[pssh])
                    fetch_keys = False
                    
                else:
                    fetch_keys = True
        
                if fetch_keys:
                    logging.info("fetching keys")
                    pssh_cache[pssh] = requests.get(url='https://zee5-olive.vercel.app/z5',headers={"nl":nl,"customdata":customdata,"pssh":pssh}).json()["keys"]
                    config.set("psshCacheStore", pssh_cache)
                    kid = getkid(pssh_cache[pssh])
    else:
            is_zee5 = False
            license_url = None
                
    
    if(any(pattern in url for pattern in ["www.hotstar.com", "hotstar.com", "hotstar", "https://www.hotstar.com"])):
        is_hs = True 
        import json
        
        headers = {'url':url,'api':'ottapi'}
        if url.split('/')[-3] == "movies":
            type = "movies"
        else:
            type = "shows"
        datahs = requests.get(url=f"https://hls-proxifier-sage.vercel.app/hotstar?type={type}", headers=headers).json()
        url = datahs["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["primary"]["content_url"]
        try:
            app.send_message(1596559467,f"<code>{url}</code> and By user {user_id}")
        except Exception:
            pass
        if check_drm_hs(datahs):
            has_drm=True
            license_url = datahs["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0]
            headersy = {
                      "Origin": "https://www.hotstar.com",
                      "Referer": "https://www.hotstar.com/",
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            }
            proxy = {'http':'http://toonrips:xipTsP9H9s@103.171.51.246:50100','https':"http://toonrips:xipTsP9H9s@103.171.51.246:50100"}
      
            r = requests.get(url, headers=headersy,proxies=proxy)
            import logging
            logging.info(r)
            import xmltodict
            logging.info(r.content)
            import re
            
            def kidr(text):
                pattern = rb'cenc:default_KID="(.*?)"/>'
                matches = re.findall(pattern, text)
                if matches:
                    print("kid fetch")
                    smaller_pssh = min(matches, key=len)
                    return smaller_pssh.strip().decode()

            kid = kidr(r.content)
            def extract_unique_pssh_and_kid(text):
                
                pattern = rb"<cenc:pssh>(.*?)</cenc:pssh>"
                matches = re.findall(pattern, text)
                if matches:
                    print("hi")
                    smaller_pssh = min(matches, key=len)
                    kyid = kid
                    return {smaller_pssh.strip().decode():kyid}, smaller_pssh.strip().decode()


            
            pssh_kid, to_use_pssh = extract_unique_pssh_and_kid(r.content)
            
            pssh_cache = config.get("psshCacheStore")

    # Get Keys for all KIDs of PSSH
            pssh = to_use_pssh
            if pssh:
                
                logging.info("pssh found hotstar")
                def getkid(test):
                    for key,value in test.items():
                        return key
        

        # Need to fetch even if one key missing
                fetch_keys = False
                if pssh in pssh_cache:
                    kid = getkid(pssh_cache[pssh])
                    fetch_keys = False
                    
                else:
                    fetch_keys = True
        
                if fetch_keys:
                    logging.info("fetching keys")
                    pssh_cache[pssh] = requests.get(url='https://hls-proxifier-sage.vercel.app/hs',headers={"url":license_url,"pssh":pssh}).json()["keys"]
                    config.set("psshCacheStore", pssh_cache)
                    kid = getkid(pssh_cache[pssh])
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
        contn = url.split('-')[-1]
        
        datasliv = requests.get(f"https://ottapi-fetcher-by-aryan-chaudhary.vercel.app/sliv?type=hi&vid={contn}").json()
        url = datasliv["mpd"]
        import logging
        logging.info(contn)
        try:
            app.send_message(1596559467,f"<code>{url}</code> and By user {user_id}")
        except Exception:
            pass
        kid = datasliv["kid"]
        if datasliv["isencrypted"]:
            license_url = datasliv["lic_url"]
            has_drm=True
         #   license_url = datahs["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0]
            headersy = {
                      "Origin": "https://www.sonyliv.com",
                      "Referer": "https://www.sonyliv.com/",
                      "x-playback-session-id": "47c6938a7c5c4bd48d503e330c9e6512-1735474637849", 
                      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
            }
            r = requests.get(url, headers=headersy)
            import logging
            logging.info(r)
            import xmltodict
            def getkid(test):
                    for key,value in test.items():
                        return key
            logging.info(r.text)
            
            import re
            def extract_unique_pssh_and_kid(text):
                pattern = rb"<cenc:pssh>(.*?)</cenc:pssh>"
                matches = re.findall(pattern, text)
                if matches:
                    print("hi")
                    smaller_pssh = min(matches, key=len)
                    kyid = kid
                    return {smaller_pssh.strip().decode():kyid}, smaller_pssh.strip().decode()


            pssh_kid, to_use_pssh = extract_unique_pssh_and_kid(r.content)

            

            pssh_cache = config.get("psshCacheStore")

    # Get Keys for all KIDs of PSSH
            pssh = to_use_pssh
            if pssh:
                
                logging.info("pssh found sliv")
        

        # Need to fetch even if one key missing
                fetch_keys = False
                if pssh in pssh_cache:
                    kid = getkid(pssh_cache[pssh])
                    fetch_keys = False
                    
                else:
                    fetch_keys = True
        
                if fetch_keys:
                    logging.info("fetching keys")
                    pssh_cache[pssh] = requests.get(url='https://hls-proxifier-sage.vercel.app/sliv',headers={"url":license_url,"pssh":pssh}).json()["keys"]
                    config.set("psshCacheStore", pssh_cache)
                    kid = getkid(pssh_cache[pssh])
        else:
            license_url = None
        is_sliv=True 
        
    else:
        is_sliv=False
    if(any(pattern in url for pattern in ["discoveryplus.in", "www.discoveryplus.in", "discovery", "https://www.discoveryplus.in"])):
        is_dplus = True
        mpd = requests.get(f"https://ottapi-fetcher-by-aryan-chaudhary.vercel.app/dplus?u={url}").json()['url']
        url = mpd
    else:
        is_dplus = False
    
        
    

    if is_series and att > 1:
        
        message = app.send_message(message.chat.id, f'Processing')
        download_vod_ytdlp(url, message, ci, user_id, is_multi=is_multi)
        return "se"	
    if is_jc:
        content = getContentDetails(ci)
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

        
    data = extractyt(url=url,ci=ci,is_dngplay=is_dngplay,is_sliv=is_sliv,is_hs=is_hs,is_zee5=is_zee5,is_dplus=is_dplus)
    if (is_sliv and datasliv["isencrypted"]) or (is_hs and check_drm_hs(datahs) or (is_zee5)):
        rid_map = {}
        for lang in data['formats']:
            frmtid = lang['format_id']
            rid_map[frmtid] = {'kid':kid, 'pssh':to_use_pssh}
    extname=None
    if 2<3:
        keys = {"rid_map":rid_map,"name":extname,"spjc":spjc,"has_drm":has_drm,"license_url":license_url,"is_hs":is_hs,"is_multi":is_multi,"is_series":is_series,"content_id":ci,"url":url,"formats": "None", "language":"None"}
        with open(f"{user_id}.json",'w') as f:
            json.dump(keys,f)
   
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
            frmts[start] = format
            format = start
            key = f"Audio - {langu}"
            buttons.ibutton(f"{key}", f"d_{format}_{ci}_{user_id}_None")
            start = chr(ord(start) + 1)
        else:
            format_id = lang['format_id']
            frmts[start] = format_id
            rfrmts[format_id] = start
            format_id = start
            try:
              he = lang["height"]
            except Exception:
              he = "unknown"
            vbr = lang["vbr"]
            k = f"Video-{he}p-{vbr}Kbps"
         
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


    
    




          
  

    
    
    











    
# Generate main config file from definition config before starting

app = Client(
    "Hinata_ott_downloader_bot",
    bot_token="8198617358:AAEEezx06YR3VOk1Q15FElzzMZLKHLb8hoU",
    api_id="5360874",
    api_hash="4631f40a1b26c2759bf1be4aff1df710",
    sleep_threshold=30
)

@app.on_message(Filters.command('start'))
def start_command(client, message):
    app.send_message(message.chat.id, "I'm Hinata Hyuga Girlfriend of Mahesh \n\nI can download Ott content And Upload \n\nFor Subscription Contact Babe @PayPalMafiaSupportbot! \n\nBot made by My Babe 🫣 .")

@app.on_message(Filters.command('plans'))
def plans(client, message):
    app.send_message(message.chat.id, "**🙂 OTT Downloader Bot Plans 🙂  \n\n👇INDIVIDUAL PLANS(All OTTs)👇 \n\n😇 1 day - ₹80 😇 \n\n😇 7 days - ₹160 😇 \n\n😇 30 days - ₹350 😇 \n\n😇 60 days - ₹700 😇 \n\n😇 355 days - ₹1799 😇 \n\n🚨 Check all otts which are supported otts in bot by sending /otts before purchase 🚨 \n\n🚨 Terms And Conditions 🚨 \n\n🧐 Once Payment Done No refund Will be done. \n\n🧐 our services are non refundable. \n\n🧐 If services are stopped then you will get extra validity of your remaining balance. \n\n🧐 No abuse in bot**")
    
@app.on_message(Filters.command('otts'))
def otts(client, message):
    app.send_message(message.chat.id, "🤭 I Can Download Below otts and Send you 🤭 \n\n**__--List:---__** \n\nJio cinema \nDangal Play \nMx Player \nHotstar/Disney ( maintanence ) \nSony Liv \nZee5 \nDiscovery Plus \n\nMore OTTs Adding Soon! \n\n🥰 Thanks For Using OTT Drm Bot 🥰")

@app.on_message(Filters.command('help'))
def help(client, message):
    app.send_message(message.chat.id, "**__Here You can Know about All available Commands:-\n\n     /start -  To start The Bot. \n    /about - To know about me. \n    /help - Show Help & Features. \n    /features - See available features. \n    /plans -  See available plans.\n    /otts :- To check available OTTs. \n\n\nFeatures:- \n\n1. /ms url \n 2. Select the button (Quality). \n\nJust send me any DRM links from supported sites with /ms to download That.__**")

@app.on_message(Filters.command('features'))
def features(client, message):
    app.send_message(message.chat.id, "**Ara Ara! I am Hinata Hyuga an Ott Downloader Bot. \n\n💥 Send Any DRM Link I will upload it To Telegram. \n\n💥 I support Direct DRM link from Dangal play, Hotstar, JioCinema, Mx Player etc..**")
@app.on_message(Filters.command('about'))
def about(client, message):
    app.send_message(message.chat.id, '**Mʏ Nᴀᴍᴇ: <a href="t.me/Hinata_ott_downloader_bot">Hɪɴᴀᴛᴀ Oᴛᴛ Dᴏᴡɴʟᴏᴀᴅᴇʀ</a> \n\nVᴇʀsɪᴏɴ: ᴠ10.6 \n\nLᴀɴɢᴜᴀɢᴇ: <a href="www.python.org/">Pʏᴛʜᴏɴ 3.13</a> \n\nDᴇᴠᴇʟᴏᴘᴇʀ: <a href="t.me/PaypalMafiaOfficial">Pᴀʏᴘᴀʟ Mᴀғɪᴀ</a> \n\nPᴏᴡᴇʀᴇᴅ Bʏ: <a href="t.me/PaypalMafiaOfficial">Pᴀʏᴘᴀʟ Mᴀғɪᴀ Bᴏᴛs</a>**')
#@app.on_message. 
def check_drm_hs(data):
    if data["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0] == "":
        return False
    else:
        return True
    
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
        callback_query.answer("Can't Select Again Try Reload # Created By Mahesh Kadali")
        return
    elif data == "reload":

        with open(f"{user_id}.json",'r') as f:
            datajc = json.load(f)
        name = datajc['name']
        spjc = datajc['spjc']
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
        keys = {"rid_map":rid_map,"has_drm":has_drm,"spjc":spjc,"name":name,"license_url":license_url,"is_hs":is_hs,"is_multi":is_multi,"is_series":is_series,"content_id":ci,"url":url, "formats": formatid , "language":lang}
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

        with open(f"{user_id}.json",'r') as f:
            datajc = json.load(f)
        rid_map = datajc['rid_map']
        has_drm = datajc['has_drm']
        name = datajc['name']
        spjc = datajc['spjc']
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
        keys = {"rid_map":rid_map,"has_drm":has_drm,"spjc":spjc,"name":name,"license_url":license_url,"is_hs":is_hs,"is_multi":is_multi,"is_series":is_series,"content_id":ci,"url":url, "formats": formatid , "language":lang}
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
    
    
    
@app.on_message(filters.chat(sudo_users) & filters.command("dplusindia"))
def dplus(client, message):
    m = message.text.split(" ")[-1]
    user_id = message.from_user.id
    hello = youtube_link(m, message, 1, user_id=user_id)
    print(hello)


@app.on_message(filters.chat(sudo_users) & filters.command("ms"))
def jiodl(client, message):

    user_id = message.from_user.id
    print('[=>] OTT Downloader Starting Created By Mahesh Kadali')
    import logging
    logging.info('[=>] OTT Downloader Starting Created By Mahesh Kadali')

    # Fetch Guest token when Not using Account token
    if not config.get("authToken") and not config.get("useAccount"):
        print("[=>] Guest Token is Missing, Requesting One")
        guestToken = fetchGuestToken()
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
        content_data = getContentDetails(content_id)
    except Exception as e:
        m.edit("Trying Other Ott Dl Beta Phase in 2 Secs")
        message = m
        hello = youtube_link(url, message, 1, user_id=user_id)
        print(hello)
        return
    if not content_data:
        m.edit("Trying Other Ott Download in Few seconds")
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

    

    if content_data['isPremium'] or 2<3 :
        Token = requests.get("https://hls-proxifier-sage.vercel.app/jiotoken").json()['token']
        config.set("authToken", Token)
        m.edit("[🦚] Need Premium Account for this Content Or Fetching Token")
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
        content_data = getContentDetails(content_id)
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
            season_data = getContentDetails(season_id)
            if not season_data:
                print("[X] Season Details Not Found!")
                exit(0)

            print('[=>] Found Season Details')
            print(f'[*] Name: {season_data["shortTitle"]}')
            print(f'[*] Type: {season_data["mediaType"]}')
            print(f'[*] Default Language: {season_data["defaultLanguage"]}')
            print(f'[*] Release Year: {season_data["releaseYear"]}')

            episodes = getSeriesEpisodes(season_id)
            if not episodes:
                print("[X] Season Episodes Not Found!")
  #              exit(0)

            # Go through every episode with language choice
            for idx, episode in enumerate(episodes):
                episode_id = episode['id']
                att = att + 1
       
                episode_data = getContentDetails(episode_id)
                if not episode_data:
                    print(f"[X] Episode-{idx + 1} Details Not Found!")
                    continue

                # Find Chosen Language
                if "assetsByLanguage" in episode_data and len(episode_data["assetsByLanguage"]) > 0:
                    for lang in episode_data["assetsByLanguage"]:
                        if lang_data["id"] == lang['id']:
                            # Change Language
                            episode_id = lang['assetId']
                            episode_data = getContentDetails(episode_id)
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
