# Usage

```
from myanonamouse import MamApi

api = MamApi("your mam_id here")

api.set_seedbox_ip()

print(api.load_user_data(snatch_summary=True))

torrents = api.torrent_search("", tor={
    "main_cat": 13,
}, limit=1000)

total_size = 0
for i, torrent in enumerate(torrents):
    size = human_read_to_byte(torrent["size"])
    total_size += size
    print(i, torrent["title"], torrent["size"], f"total size: {total_size / 1024 / 1024 / 1024:.2f} GB")

```