import urllib.request
import json
import time

headers = {'User-Agent': 'PartyGamesHub/1.0 (https://partygameshub.com; contact@example.com) Python/3'}

names = ["Shah_Rukh_Khan", "Deepika_Padukone", "Amitabh_Bachchan"]

for name in names:
    url = f"https://en.wikipedia.org/w/api.php?action=query&titles={name}&prop=pageimages&format=json&pithumbsize=400"
    try:
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req, timeout=10)
        data = json.loads(res.read().decode())
        pages = data.get("query", {}).get("pages", {})
        for pid, pdata in pages.items():
            thumb = pdata.get("thumbnail", {}).get("source", "NOT FOUND")
            print(f"{name}: {thumb}")
    except Exception as e:
        print(f"{name}: ERROR - {e}")
    time.sleep(1)
