from requests import get
from json import load
market = load(open("config.json"))["country"]
def appletrack(most_recent):
    search = get("https://itunes.apple.com/search?term="+most_recent.artist.name+"+"+most_recent.name+"+"+most_recent.album.name+"&country="+market+"&limit=1&media=music&entity=musicTrack&attribute=mixTerm")
    try:
        return [search.json()["results"][0]["trackViewUrl"], search.json()["results"][0]["artworkUrl100"]]
    except:
        return None