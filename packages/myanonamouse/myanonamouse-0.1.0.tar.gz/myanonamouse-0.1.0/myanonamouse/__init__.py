import requests
import math


class MamApi:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.myanonamouse.net/"

    def set_seedbox_ip(self):
        """
        This sets the dynamic seedbox IP to your current IP address.
        """
        res = requests.get(
            self.base_url + "json/dynamicSeedbox.php", cookies={"mam_id": self.api_key}
        )
        return res.ok()

    def load_user_data(self, user_id=None, notif=False, snatch_summary=False):
        """
        Loads data for a user. If the user_id is not specified, load it for yourself
        """
        data = {}
        if user_id:
            data["id"] = user_id
        if notif:
            data["notif"] = True
        if snatch_summary:
            data["snatch_summary"] = True

        res = requests.get(
            self.base_url + "jsonLoad.php",
            cookies={"mam_id": self.api_key},
            params=data,
        )
        return res.json()

    def torrent_search(self, text="", tor={}, limit=100):
        """
        Search for torrents. You can use the parameters as per
        https://www.myanonamouse.net/api/endpoint.php/1/tor/js/loadSearchJSONbasic.php

        Additional note: The library performs pagination and iteration automatically,
        you do not need to implement it in your code.
        """

        MAX_PER_PAGE = 100
        current_count = 0
        result_count_for_search = 1000000  # We lower this later. Do this so we don't keep trying to paginate when we run out of data

        while current_count < min(limit, result_count_for_search):
            print("making request")
            req_json = {
                "text": text,
                "tor": tor,
                "limit": 100,
            }
            req_json["tor"]["startNumber"] = current_count
            print(req_json)
            res = requests.post(
                self.base_url + "tor/js/loadSearchJSONbasic.php",
                # "https://webhook.site/ceb57673-b663-4223-9036-4f20bd7992ca",
                cookies={"mam_id": self.api_key},
                json=req_json,
            )
            print(f"Current count: {current_count}")
            data = res.json()
            result_count_for_search = data["found"]
            if not data:
                break
            for torrent in data["data"]:
                if current_count >= limit:
                    break
                current_count += 1
                yield torrent
