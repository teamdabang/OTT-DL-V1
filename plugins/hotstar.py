import json
import re
from typing import Dict, Optional, Tuple

class ContentData:
    def __init__(
        self,
        rid_map: Dict,
        name: str,
        has_drm: bool,
        license_url: str,
        url: str,
        video_ids: Optional[Tuple[str, str, str]] = None,
        formats: Optional[str] = None,
        language: Optional[str] = None,
    ):
        self.rid_map = rid_map
        self.name = name
        self.has_drm = has_drm
        self.license_url = license_url
        self.url = url
        self.video_ids = video_ids
        self.formats = formats
        self.language = language

    @classmethod
    def from_json(cls, json_data: str) -> "ContentData":
        try:
            data = json.loads(json_data)
            url = data.get("url", "")

            video_url_regex = r"https?://(?:www\.)?hotstar\.com/(?:[a-z]{2}/)?(?:tv|movies|sports|shows|news|clips|premium)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)"
            match = re.match(video_url_regex, url)
            video_ids = match.groups() if match else None

            return cls(
                data["rid_map"],
                data["name"],
                data["has_drm"],
                data["license_url"],
                url,
                video_ids,
                data.get("formats"),
                data.get("language"),
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing JSON: {e}") #Print error for debug
            return None #Return None if error occure

    def to_json(self) -> Optional[str]:
        try:
            return json.dumps(self.__dict__, indent=2)
        except TypeError as e: #Handle TypeErrors that might occur during serialization
            print(f"Error serializing to JSON: {e}")
            return None

