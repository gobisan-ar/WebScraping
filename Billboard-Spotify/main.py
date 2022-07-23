import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100/"

SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()["id"]
date = input("Which year do you want to travel to? [YYY-MM-DD]: ")
response = requests.get(URL + date)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
song_headings = soup.find_all(name="h3",
                            id="title-of-a-story",
                            class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 "
                                   "lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 "
                                   "u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 "
                                   "u-max-width-230@tablet-only")

song_list = [song.getText().strip() for song in song_headings]

year = date.split("-")[0]
song_uris = []


for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# Create new private playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# Add songs to play list
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
