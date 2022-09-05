from json import load
from os import getenv
from time import sleep

from dotenv import load_dotenv
from spotipy import Spotify, SpotifyException
from spotipy.oauth2 import SpotifyClientCredentials

market = load(open("config.json"))["country"]
load_dotenv()

auth_manager = SpotifyClientCredentials(client_id=getenv("SPOTIFY_CLIENT_ID"),
                                        client_secret=getenv("SPOTIFY_CLIENT_SECRET"))
sp = Spotify(client_credentials_manager=auth_manager)

def spotifytrack(track):
    search = None
    while search is None:
        try:
            search = sp.search(q=f"artist:{track.artist} track:{track.name} album:{track.album.name}", market=market,
                           type="track", limit=1)
        except SpotifyException as e:
            if e.http_status == 404:
                return None
            sleep(2)
    return [search["tracks"]["items"][0]["external_urls"]["spotify"], search["tracks"]["items"][0]["album"]["images"][0]["url"]]
