from tidal_unofficial import TidalUnofficial
from json import load
market = load(open("config.json"))["country"]
tidalapi = TidalUnofficial({'country_code': market})
def tidalTrack(track): # Get tidal track
    search=tidalapi.search(query=track.name+" "+track.artist.name, search_type='tracks')['items'] # Search for the track on tidal
    for ltrack in search: 
        if ltrack["album"]['title'].capitalize() in track.album.name.capitalize(): # Check if the album is the same
            return [ltrack["url"], tidalapi.album_art_to_url(ltrack['album']['cover'])["xxl"]]  # If it is, return the track and the album art
    return None # If it isn't, return None