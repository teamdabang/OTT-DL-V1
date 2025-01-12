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


# Request guest token from JioCine Server
def fetchGuestToken():
    """Fetches a guest token from JioCinema server.

    Returns:
        str: Guest token on success, None otherwise.
    """

    guestTokenUrl = "https://auth-jiocinema.voot.com/tokenservice/apis/v4/guest"
    guestData = {
        "appName": "RJIL_JioCinema",
        "deviceType": "fireTV",
        "os": "android",
        "deviceId": "1464251119",
        "freshLaunch": False,
        "adId": "1464251119",
        "appVersion": "4.1.3"
    }

    try:
        r = session.post(guestTokenUrl, json=guestData, headers=headers, proxies=proxy)
        r.raise_for_status()  # Raise exception for non-200 status codes

        result = r.json()
        if not result.get('authToken'):
            logging.error("Guest token not found in response")
            return None

        return result['authToken']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching guest token: {e}")
        return None



def getContentDetails(content_id, session, headers, proxy=None):
    """Fetches content details from the server."""
    logging.info(f"Fetching details for content ID: {content_id}")
    assetQueryUrl = (
        "https://content-jiovoot.voot.com/psapi/voot/v1/voot-web//content/query/asset-details?"
        f"&ids=include:{content_id}&responseType=common&devicePlatformType=desktop"
    )

    try:
        r = session.get(assetQueryUrl, headers=headers, proxies=proxy)
        r.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = r.json()

        if not data.get("result"):  # More robust check for missing 'result'
            logging.warning(f"No 'result' key found in response for ID: {content_id}")
            return None

        results = data["result"]
        if not results: # Check if result list is empty.
            logging.warning(f"Empty result list in response for ID: {content_id}")
            return None

        return results[0]

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for ID {content_id}: {e}")
        return None  # Return None instead of re-raising, caller can handle

    except (ValueError, KeyError, IndexError) as e: # Catch JSON errors
        logging.error(f"Error parsing JSON response for ID {content_id}: {e}")
        return None



# Fetch Video URl details using Token
def fetchPlaybackData(content_id, token, headers=None, proxy=None):
  """Fetches playback data for a content using the provided access token.

  Args:
      content_id (str): The ID of the content to fetch playback data for.
      token (str): The access token for authorization.
      headers (dict, optional): Additional headers to include in the request. Defaults to None.
      proxy (dict, optional): Dictionary containing proxy settings if needed. Defaults to None.

  Returns:
      dict: Playback data dictionary on success, None otherwise.

  Raises:
      Exception: If an unexpected error occurs during the request or parsing.
  """

  logging.info(f"Fetching playback data for content: {content_id}")

  playbackUrl = f"https://apis-jiovoot.voot.com/playback/v1/{content_id}"

  playData = {
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
      "x-apisignatures": "REPLACE_WITH_YOUR_X_APISIGNATURES",  # Placeholder for actual value
      "deviceRange": "",
      "networkType": "4g",
      "deviceMemory": 4096
  }

  playHeaders = {
      "authority": "apis-jiovoot.voot.com",
      "accesstoken": token,
      "x-platform": "androidweb",
      "x-platform-token": "web",
      "appname": "RJIL_JioCinema",
      "jc-user-agent": "JioCinema/2411044 (web; mweb/10; tablet; Chrome Android)",
      "uniqueid": "0a97cbb8e9a871ba2ae6fde431e24efe",
      "versioncode": "2411044",
      "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
      "sec-ch-ua-platform": "\"Android\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "cross-site"
  }

  # Update headers if provided
  if headers:
      playHeaders.update(headers)

  try:
      r = session.post(playbackUrl, json=playData, headers=playHeaders, proxies=proxy)
      r.raise_for_status()  # Raise exception for non-200 status codes

      result = r.json()
      if not result.get('data'):
          logging.warning(f"No 'data' key found in response for content ID: {content_id}")
          return None

      return result['data']

  except requests.exceptions.RequestException as e:
      logging.error(f"Error fetching playback data for ID {content_id}: {e}")
      return None
  except (ValueError, KeyError, IndexError) as e:
      logging.error(f"Error parsing JSON response for ID {content_id}: {e}")
      return None

# Remember to replace "REPLACE_WITH_YOUR_X_APISIGNATURES" with the actual value before using

    


# Fetch Series Episode List from Server
def getSeriesEpisodes(content_id):
    episodeQueryUrl = "https://content-jiovoot.voot.com/psapi/voot/v1/voot-web//content/generic/series-wise-episode?" + \
                    f"sort=episode:asc&id={content_id}"

    r = session.get(episodeQueryUrl, headers=headers, proxies=proxy)
    if r.status_code != 200:
        return None

    result = r.json()
    if not result['result'] or len(result['result']) < 1:
        return None

    return result['result']



def fetchPlaybackDataold(content_id, token):
    playbackUrl = f"https://apis-jiovoot.voot.com/playbackjv/v5/{content_id}"

    playData = {
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
                    "frameRateSupport": "50fps",
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
        "deviceMemory": 4096  # Web: o668nxgzwff, FTV: 38bb740b55f, JIOSTB: e882582cc55, ATV: d0287ab96d76
    }
    playHeaders = {
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
    playHeaders.update(headers)

    r = session.post(playbackUrl, json=playData, headers=playHeaders, proxies = proxy)
    if r.status_code != 200:
        return None
        print("problem in playback")

    result = r.json()
    if not result['data']:
        return None

    return result['data']



# Fetch Video URl details using Token

def getMPDData(mpd_url,is_hs=False):
    headerhs = {
    "Origin": "https://www.hotstar.com",
    "Referer": "https://www.hotstar.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    headerjcs = {
    "Origin": "https://www.jiocinema.com",
    "Referer": "https://www.jiocinema.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    if is_hs:
        r = session.get(mpd_url, headers=headerhs, proxies=proxy)
    else:
        r = session.get(mpd_url, headers=headers, proxies=proxy)
    if r.status_code != 200:
        return None

    try:
        import logging
        logging.info(r.content)
        return xmltodict.parse(r.content), r.text
    except Exception as e:
        print(f"[!] getMPDData: {e}")
        return None


# Parse MPD data for PSSH maps
def parseMPDData(mpd_data):
  """Parses MPD data to extract PSSH and KID information.

  Args:
      mpd_data (dict): The MPD data dictionary.

  Returns:
      tuple: A tuple containing two dictionaries:
          - rid_kid (dict): Maps Representation IDs to their corresponding KID and PSSH data.
          - pssh_kid (dict): Maps PSSH data to sets of KIDs associated with that PSSH.

  Raises:
      ValueError: If the expected structure of the MPD data is not found.
  """

  logging.info("Parsing MPD data")

  rid_kid = {}
  pssh_kid = {}

  def readContentProt(rid, cp):
      pssh = None
      if cp.get("@schemeIdUri", "").lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed":
          logging.info(f"Found PSSH for Representation ID: {rid}")
          pssh = cp.get("cenc:pssh")

      if pssh:
          if pssh not in pssh_kid:
              pssh_kid[pssh] = set()

          if cp.get("@value", "").lower() == "cenc":
              kid = cp.get("@cenc:default_KID", "").replace("-", "")
              logging.info(f"Found KID for Representation ID: {rid}")

              rid_kid[rid] = {
                  "kid": kid,
                  "pssh": pssh
              }
              pssh_kid[pssh].add(kid)

  # Iterate through AdaptationSet and Representations
  for ad_set in mpd_data.get('AdaptationSet', []):
      for resp in ad_set.get('Representation', []):
          if 'ContentProtection' in resp:
              readContentProt(resp['@id'], resp['ContentProtection'])

  if not rid_kid:
      raise ValueError("No PSSH and KID information found in MPD data")

  return rid_kid, pssh_kid



# Perform Handshake with Widevine Server for License
def getWidevineLicense(license_url, challenge, token, playback_id=None, headers=None, proxy=None):
  """Fetches a Widevine license for playback.

  Args:
      license_url (str): The URL to request the license from.
      challenge (str): The challenge data needed for the license request.
      token (str): The access token for authorization.
      playback_id (str, optional): The playback ID. Defaults to None.
      headers (dict, optional): Additional headers to include in the request. Defaults to None.
      proxy (dict, optional): Dictionary containing proxy settings if needed. Defaults to None.

  Returns:
      str: The Widevine license content on success, None otherwise.

  Raises:
      Exception: If an unexpected error occurs during the request or parsing.
  """

  logging.info(f"Fetching Widevine license for: {license_url}")

  drmHeaders = {
      "authority": "key-jio.voot.com",
      "accesstoken": token,
      "appname": "RJIL_JioCinema",
      "devicetype": "androidstb",  # Consider making configurable
      "os": "android",  # Consider making configurable
      "uniqueid": "1957805b-8c2a-4110-a5d9-767da377ffce",  # Consider making configurable
      "x-platform": "fireOS",
      "x-feature-code": "ytvjywxwkn",
  }

  if playback_id:
      drmHeaders["x-playbackid"] = playback_id

  # Update headers if provided
  if headers:
      drmHeaders.update(headers)

  try:
      r = session.post(license_url, data=challenge, headers=drmHeaders, proxies=proxy)
      r.raise_for_status()  # Raise exception for non-200 status codes

      return r.content

  except requests.exceptions.RequestException as e:
     logging.error(f"Error fetching Widevine license: {e}")
      return None

  except Exception as e:  # Catch other potential errors
     logging.error(f"Unexpected error: {e}")
      return None




#Jio Cinema Downloader Bot Created By Aryan Chaudhary
