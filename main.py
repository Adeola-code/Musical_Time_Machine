import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from decouple import config

SPOTIPY_CLIENT_ID = config('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = config('SPOTIPY_CLIENT_SECRET')
DATE=input("What year you would like to travel to? Type in YYY-MM-DD format.")
URL_ENDPOINT=f"https://www.billboard.com/charts/hot-100/{DATE}"
print(URL_ENDPOINT)
response=requests.get(URL_ENDPOINT)
billboard=(response.text)
soup = BeautifulSoup(billboard,"html.parser")
songs = soup.select("li ul li h3")
songs_titles = [song.getText().strip() for song in songs]
print(songs_titles)



sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="31v6xz42743sf4egskx5fhwsgqua"
    )
)
user_id = sp.current_user()["id"]

# songs_titles = ["The list of song", "titles from your", "web scrape"]

song_uris = []
year = DATE.split("-")[0]
for song in songs_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
playlist = sp.user_playlist_create(user=user_id, name=f"{DATE} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)