# Last.FM Discord RPC
**A Discord Rich Presence client for Last.FM with support for Spotify, Tidal, and Apple Music**
## How it works
The program works by grabbing the details of your Now Playing scrobble, and sends that info to any of the 3 music streaming platforms that you choose search APIs. It then records those urls and places all of the info into a now playing discord box. The program also records the music played to a 3 different text file, `album.txt`, `artist.txt`, and `title.txt`, as well as `art.png`, these are here for if you are a streamer for example, and want to custom make your widget a little bit.
## Modules 
Using lastfmpy, dotenv, PIL/Pillow, pypresence, requests, tidal_unofficial, and spotipy
## Setup
1. Clone repository
2. Make .env file in the root folder like this 
```
LASTFM_API_KEY=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```
3. Fill in with your API keys
4. Change `config.json` file with your 2 letter country code, Last.FM username and what streaming services the program sends scrobbled info to
5. Run `main.py`
## Known Bugs
Nothing right now, however tell me if you experience any.
## Improvements
May make a GUI version to allow for more ease of use, and there may be clunky code in use that I'll fix up.