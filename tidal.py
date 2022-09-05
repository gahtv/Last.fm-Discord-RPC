from tidal_unofficial import TidalUnofficial

def tidalTrack(track, tidal): # Get tidal track
    search=tidal.search(query=track.name+" "+track.artist.name, search_type='tracks')['items'] # Search for the track on tidal
    for ltrack in search: 
        if ltrack["album"]['title'].capitalize() in track.album.name.capitalize(): # Check if the album is the same
            return ltrack # If it is, return the track
    return None # If it isn't, return None