import requests
import argparse
import os
import pathlib
from typing import Any
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

load_dotenv(os.path.join(os.getcwd(), ".env"))

parser = argparse.ArgumentParser(description="Extracts channel avatar")
parser.add_argument(
    "channels", help="A valid channel ID or a handle starting with `@`", nargs="*")
# parser.add_argument("--save-dir", help="Specify a save directory", type=str)
args = parser.parse_args()

channel_list_args = args.channels

_yt_token = os.environ.get("YT_API_KEY")


def __fetch(url: str, params: dict[str, Any] | None = None):
    with requests.Session() as sesh:
        resp = sesh.get(url, params=params)
        resp.raise_for_status()
        print("[debug] took {}".format(resp.elapsed.total_seconds()))
        return resp

# This should work fine as of currently, it still needs an API key from Google Cloud console but it's good enough
# might rewrite this tho to avoid exceeding the quota using an automated web browser


def abomination(dynamic_channel_id):
    if not _yt_token:
        raise Exception("An API key is required lol")

    _params = {
        "part": "snippet,id",
        "key": _yt_token
    }

    if dynamic_channel_id.startswith("UC"):
        _params.update({"id": dynamic_channel_id})

    if dynamic_channel_id.startswith("@"):
        _params.update({"forHandle": dynamic_channel_id})

    api_resp = __fetch("https://www.googleapis.com/youtube/v3/channels", _params)  # noqa

    try:
        json_res = api_resp.json()["items"][0]

        channel_id_res = json_res["id"]
        snippet = json_res["snippet"]

        channel_name, avatar_url = snippet["title"], str(snippet["thumbnails"]["high"]["url"])  # noqa

        # override the params of avatar_url to get the highest quality possible
        avatar_url = f"{avatar_url.split('=')[0]}=s4096"

        print("Found", channel_name)

        img_content = BytesIO(__fetch(avatar_url).content)

        img = Image.open(img_content)

        img.save(f"{channel_name} - {channel_id_res}.png", "png")
        print("saved lol")

    except KeyError:
        print("Cannot not found due to it being removed or something idk")


if __name__ == "__main__":
    for ch in channel_list_args:
        abomination(ch)
