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
from plugins.handler.playback import *
from main import *

from plugins.handler.mhandler import *
from plugins.dl import *
from plugins.exec import *
from plugins.jio import *
from plugins.dash import *

from base64 import b64decode, b64encode
from yt_dlp.postprocessor import PostProcessor
from utils import scriptsDir, joinPath, realPath
from asyncio import create_subprocess_exec, create_subprocess_shell, run_coroutine_threadsafe, sleep


def check_drm_hs(data):
    if data["success"]["page"]["spaces"]["player"]["widget_wrappers"][0]["widget"]["data"]["player_config"]["media_asset"]["licence_urls"][0] == "":
        return False
    else:
        return True
#from button import ButtonMaker


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


    
    




          
  

    
    
    









