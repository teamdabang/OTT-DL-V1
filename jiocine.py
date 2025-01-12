import requests
import xmltodict
import logging 

#Jio Cinema Downloader Bot Created By Aryan Chaudhary
# Request object with Session maintained
session = requests.Session()
#session.proxies.update({'http': "http://toonrips:xipTsP9H9s@103.171.51.246:50100"})
session.proxies.update({'http': "http://toonrips:xipTsP9H9s@103.171.51.246:50100"})
proxy = {'http':'http://toonrips:xipTsP9H9s@103.171.51.246:50100','https':"http://toonrips:xipTsP9H9s@103.171.51.246:50100"}
# Common Headers for Session
headers = {
    "Origin": "https://www.jiocinema.com",
    "Referer": "https://www.jiocinema.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}

# Content Type Dir Map
contentTypeDir = {
    "CAC": "promos",
    "MOVIE": "movies",
    "SHOW": "series",
    "SERIES": "series",
    "EPISODE": "series"
}

# Language Id Name Map
LANG_MAP = {
    "en": "English",
    "hi": "Hindi",
    "gu": "Gujarati",
    "ta": "Tamil",
    "te": "Telugu",
    "kn": "Kannada",
    "mr": "Marathi",
    "ml": "Malayalam",
    "bn": "Bengali",
    "bho": "Bhojpuri",
    "pa": "Punjabi",
    "or": "Oriya"
}

REV_LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Marathi": "mr",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Bhojpuri": "bho",
    "Punjabi": "pa",
    "Oriya": "or"
}

# Audio Codec Decode Map
AUDIO_CODECS = {
    "1": "PCM",
    "mp3": "MP3",
    "mp4a.66": "MPEG2_AAC",
    "mp4a.67": "MPEG2_AAC",
    "mp4a.68": "MPEG2_AAC",
    "mp4a.69": "MP3",
    "mp4a.6B": "MP3",
    "mp4a.40.2": "MPEG4_AAC",
    "mp4a.40.02": "MPEG4_AAC",
    "mp4a.40.5": "MPEG4_AAC",
    "mp4a.40.05": "MPEG4_AAC",
    "mp4a.40.29": "MPEG4_AAC",
    "mp4a.40.42": "MPEG4_XHE_AAC",
    "ac-3": "AC3",
    "mp4a.a5": "AC3",
    "mp4a.A5": "AC3",
    "ec-3": "EAC3",
    "mp4a.a6": "EAC3",
    "mp4a.A6": "EAC3",
    "vorbis": "VORBIS",
    "opus": "OPUS",
    "flac": "FLAC",
    "vp8": "VP8",
    "vp8.0": "VP8",
    "theora": "THEORA",
}

# Initialize session and # Define your proxy if needed

# Fetch Video URL details using Token
def fetch_playback_data(content_id: str, token: str) -> dict:
    playback_url = f"https://apis-jiovoot.voot.com/playback/v1/{content_id}"
    
    play_data = {
        "4k": True,
        "ageGroup": "18+",
        "appVersion": "3.4.0",
        "bitrateProfile": "xxhdpi",
        "capability": {
            "drmCapability": {
                "aesSupport": "yes",
                "fairPlayDrmSupport": "none",
                "playreadyDrmSupport": "yes",
                "widevineDRMSupport": "yes"
            },
            "frameRateCapability": [
                {
                    "frameRateSupport": "60fps",
                    "videoQuality": "2160p"
                }
            ]
        },
        "continueWatchingRequired": False,
        "dolby": True,
        "downloadRequest": False,
        "hevc": True,
        "kidsSafe": False,
        "manufacturer": "Android",
        "model": "Android",
        "multiAudioRequired": True,
        "osVersion": "10",
        "parentalPinValid": False,
        "x-apisignatures": "o668nxgzwff",
        "deviceRange": "",
        "networkType": "4g",
        "deviceMemory": 4096
    }
    
    play_headers = {
        "authority": "apis-jiovoot.voot.com",
        "accesstoken": token,
        "x-platform": "androidweb",
        "x-platform-token": "web",
        "appname": "RJIL_JioCinema",
        "jc-user-agent": "JioCinema/2411044 (web; mweb/10; tablet; Chrome Android)",
        "uniqueid": "0a97cbb8e9a871ba2ae6fde431e24efe",
        "x-apisignatures": "o668nxgzwff",
        "versioncode": "2411044",
        "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site"
    }
    
    play_headers.update(headers)

    try:
        response = session.post(playback_url, json=play_data, headers=play_headers, proxies=proxy)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        
        if not result.get('data'):
            logging.error("No playback data found in the response.")
            return None
        
        return result['data']
    
    except requests.RequestException as e:
        logging.error(f"Error fetching playback data: {e}")
        return None


# Fetch Series Episode List from Server
def get_series_episodes(content_id: str) -> list:
    episode_query_url = f"https://content-jiovoot.voot.com/psapi/voot/v1/voot-web//content/generic/series-wise-episode?sort=episode:asc&id={content_id}"

    try:
        response = session.get(episode_query_url, headers=headers, proxies=proxy)
        response.raise_for_status()  # Raise an error for bad responses
        result = response.json()
        
        if not result.get('result') or len(result['result']) < 1:
            logging.error("No episodes found in the response.")
            return None
        
        return result['result']
    
    except requests.RequestException as e:
        logging.error(f"Error fetching series episodes: {e}")
        return None


# Fetch MPD Data
def get_mpd_data(mpd_url: str, is_hs: bool = False) -> tuple:
    headers_hs = {
        "Origin": "https://www.hotstar.com",
        "Referer": "https://www.hotstar.com/",
        "User -Agent": "Mozilla/5.0 ( Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    headers_jcs = {
        "Origin": "https://www.jiocinema.com",
        "Referer": "https://www.jiocinema.com/",
        "User -Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    
    headers_to_use = headers_hs if is_hs else headers_jcs

    try:
        response = session.get(mpd_url, headers=headers_to_use, proxies=proxy)
        response.raise_for_status()  # Raise an error for bad responses
        
        return xmltodict.parse(response.content), response.text
    
    except requests.RequestException as e:
        logging.error(f"Error fetching MPD data: {e}")
        return None


# Parse MPD data for PSSH maps
def parse_mpd_data(mpd_per: dict) -> tuple:
    rid_kid = {}
    pssh_kid = {}
    logging.info("Parsing MPD data")

    def read_content_prot(rid, cp):
        _pssh = None
        if cp[1]["@schemeIdUri"].lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
            logging.info("Found PSSH")
            _pssh = cp[1]["cenc:pssh"]

        if _pssh:
            if _pssh not in pssh_kid:
                pssh_kid[_pssh] = set()

            if cp[0]['@value'].lower() == "cenc":
                _kid = cp[0]["@cenc:default_KID"].replace("-", "")  # Cleanup
                logging.info("Found KID")

                rid_kid[rid] = {
                    "kid": _kid,
                    "pssh": _pssh
                }
                pssh_kid[_pssh].add(_kid)

    for ad_set in mpd_per['AdaptationSet']:
        resp = ad_set['Representation']
        if isinstance(resp, list):
            for res in resp:
                if 'ContentProtection' in res:
                    read_content_prot(res['@id'], res['ContentProtection'])
        else:
            if 'ContentProtection' in resp:
                read_content_prot(resp['@id'], resp['ContentProtection'])

    return rid_kid, pssh_kid


# Perform Handshake with Widevine Server for License
def get_widevine_license(license_url: str, challenge: bytes, token: str, playback_id: str = None) -> bytes:
    if not playback_id:
        playback_id = "27349583-b5c0-471b-a95b-1e1010a901cb"

    drm_headers = {
        "authority": "key-jio.voot.com",
        "accesstoken": token,
        "appname": "RJIL_JioCinema",
        "devicetype": "androidstb",
        "os": "android",
        "uniqueid": "1957805b-8c2a-4110-a5d9-767da377ffce",
        "x-platform": "fireOS",
        "x-feature-code": "ytvjywxwkn",
        "x-playbackid": playback_id
    }
    
    drm_headers.update(headers)

    try:
        response = session.post(license_url, data=challenge, headers=drm_headers, proxies=proxy)
        response.raise_for_status()  # Raise an error for bad responses
        
        return response.content
    
    except requests.RequestException as e:
        logging.error(f"Error fetching Widevine license: {e}")
        return None


# Jio Cinema Downloader Bot Created By Aryan Chaudhary





