import requests
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("channel_id", help="A valid channel ID")
args = parser.parse_args()

channel_id = args.channel_id

YT_API_TOKEN = os.getenv("YT_API_TOKEN")


# This should work fine as of currently, it still needs an API key from Google Cloud console but it's good enough
# might rewrite this tho to avoid exceeding the quota using an automated web browser
def abomination():
    _channel_url = "https://www.googleapis.com/youtube/v3/channels"
    _params = {
        "part": "snippet",
        "id": channel_id,
        "key": YT_API_TOKEN
    }

    with requests.Session() as sesh:
        resp = sesh.get(_channel_url, params=_params)
        resp.raise_for_status()

    snippet = resp.json()["items"][0]["snippet"]
    
    channel_name, avatar_url = snippet["title"], snippet["thumbnails"]["high"]["url"]

if __name__ == "__main__":
    abomination()
