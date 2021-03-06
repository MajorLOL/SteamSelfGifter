import datetime
import json
import logging
import requests

logger = logging.getLogger(__name__)


class SteamGame:
    def __init__(self, steamid):
        self.steamid = steamid

    def _update_data(self):
        data = ""
        try:
            r = requests.get(f"https://store.steampowered.com/api/appdetails?appids={self.steamid}&json=1")
            data = r.json()
            if not data[self.steamid]["success"]:
                raise TypeError(f"Giveaway is a bundle, let's skip")
            self.name = data[self.steamid]["data"]["name"]
            self.type = data[self.steamid]["data"]["type"]
            self.release_date = data[self.steamid]["data"]["release_date"]["date"]
        except Exception as e:
            raise Exception(f"Could not get steam game data: {str(e)} for {r.url}")

    def _update_review_data(self):
        data = ""
        try:
            r = requests.get(f"https://store.steampowered.com/appreviews/{self.steamid}?json=1")
            data = r.json()
            if not data["success"]:
                raise Exception(f"Giveaway is a bundle, let's skip")
            self.review_score = int(data["query_summary"]["review_score"])
            self.total_positive = int(data["query_summary"]["total_positive"])
            self.total_negative = int(data["query_summary"]["total_negative"])
            self.total_reviews = int(data["query_summary"]["total_reviews"])
        except Exception as e:
            raise Exception(f"Could not get steam score: {str(e)} for {r.url}")

    def refresh(self):
        self._update_data()
        self._update_review_data()
        self.modified_at = datetime.datetime.utcnow()
        logger.info(f"[SteamGame][Refresh] Done refreshing {self.name}")
