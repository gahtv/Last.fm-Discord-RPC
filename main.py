import asyncio
import importlib
import json
from io import BytesIO
from os import getenv
from time import sleep

import lastfmpy
from dotenv import load_dotenv
from PIL import Image
from pypresence import Presence
from requests import get
from tidal_unofficial import TidalUnofficial

load_dotenv()
key = getenv("LASTFM_API_KEY")
config = json.load(open("config.json"))  # Read config file


async def getlastfm():  # Get lastfm data
    lastfm = await lastfmpy.LastFM(key)
    return lastfm


async def recents():  # Get recent tracks
    # Change line 8 in config.json to your lastfm username
    recent = await lastfm.user.get_recent_tracks(config["lastfmuser"])
    return recent


def wtf(track, artist, album, imgurl):  # Write to file (a great acronym)
    with open("title.txt", "w") as f:
        f.write(f"Listening to {track}")
    with open("artist.txt", "w") as f:
        f.write(f"by {artist}")
    with open("album.txt", "w") as f:
        f.write(f"from {album}")
    response = get(imgurl)
    img = Image.open(BytesIO(response.content)).resize((300, 300))  # Get image from url
    img.save("art.png")  # Save image


rpc = Presence("909117969014083684")  # Change this to your discord app id
rpc.connect()
lastfm = asyncio.run(getlastfm())
def main():
    try:
        try:
            recent = asyncio.run(recents())  # Get recent tracks
        except lastfmpy.exceptions.OperationFailedError:  # If lastfm is down
            rpc.clear()  # Clear discord rich presence
            sleep(300)  # Wait 5 minutes
            recent = asyncio.run(recents())  # Try again
        most_recent = recent.items[0]
        tidal_track = None
        if most_recent.now_playing:  # If the track is currently playing
            if config["stream"]["tidal"]:
                import tidal
                tidal_track = tidal.tidalTrack(most_recent)  # Get tidal track
            if config["stream"]["spotify"]:
                import spotify
                spotify_track = spotify.spotifytrack(most_recent) # Get spotify track
            if config["stream"]["applemusic"]:
                import apple
                apple_track = apple.appletrack(most_recent)
            # Discord RPC Buttons
            buttons = []
            imgurl = None
            if spotify_track:
                # If the track is on spotify, add a button to listen on spotify
                buttons.append({"label": "Listen on Spotify",
                                "url": spotify_track[0]})
                imgurl = spotify_track[1]  # Get the album art url from spotify
            if tidal_track:
                # If the track is on tidal, add a button to listen on tidal
                buttons.append({"label": "Listen on TIDAL",
                                "url": tidal_track[0]})
                imgurl = tidal_track[1] # Get the album art url if the track is on tidal
            if apple_track:
                # If the track is on apple music, add a button to listen on apple music
                buttons.append({"label": "Listen on Apple Music",
                                "url": apple_track[0]})
                if imgurl is None: # DON'T OVERWRITE THE ALBUM ART URL IF IT'S ALREADY SET BECAUSE APPLE MUSIC ALBUM ART IS CRAP
                    imgurl = apple_track[1]  # Get the album art url if all else fails (A much nicer way to say the above)
            if buttons == []:
                # If the track is not on any other streaming, get the lastfm album art url
                imgurl = most_recent.image[3].url
            buttons.append({"label": "Last.FM link", "url": f"{most_recent.url}"})  # Add a button to the lastfm page
            rpc.update(details=f"🎵{most_recent.name}🧍{most_recent.artist}",  # Update discord rich presence
                       state=f"💿{most_recent.album}",
                       large_image="lastfm",
                       buttons=buttons[0:2]) # Only show the first two buttons (Discord only allows 2 buttons)
            if config["streaming"]:# If you are a streamer, enable streaming in json to make widget in OBS
                wtf(most_recent.name, most_recent.artist,most_recent.album, imgurl)  # Write to file
        else:
            rpc.clear()  # If the track is not currently playing, clear discord rich presence
        sleep(5)  # Wait 5 seconds for api rate limit
    except KeyboardInterrupt:  # If you press ctrl+c to exit
        rpc.close()
        exit()
if __name__ == "__main__":
    while True:
        main()        