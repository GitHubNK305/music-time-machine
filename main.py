from os.path import isfile

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

CLIENT_ID ="081c809d38714ccba3b3a1b048974b0b"
CLIENT_SECRET = "9e722b93bf2947b6bcfbea54709c5857"
REDIRECT_URL = "http://example.com"

scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URL, scope=scope))
user_id = sp.current_user()["id"]
# print(sp.current_user())

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
# print(year)
hot_100_on_that_date_url = f"{BILLBOARD_URL}{date}"

# print(hot_100_on_that_date_url)

response = requests.get(hot_100_on_that_date_url)
web_site_content = response.text

soup = BeautifulSoup(web_site_content, "html.parser")

best_songs = soup.select("li ul li h3")
best_song_100 = [song.getText().strip() for song in best_songs]
# print(best_song_100)
song_uris = []

if not isfile(f"{year} Billboard 100.txt"):

    for name in best_song_100:
        result = sp.search(q=f"track: {name} year: {year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{name} is not exist in Spotify. Skipped.")

    with open(f"{year} Billboard 100.txt", "w") as file:
        for song in song_uris:
            file.write(f"{song}\n")
else:
    with open(f"{year} Billboard 100.txt", "r") as file:
        song_uris = file.read()
        song_uris_list = song_uris.split("\n")
        print(len(song_uris_list))
        print(song_uris_list[:-2])

# print(song_uris)
# song_uris = [sp.search(q=f"track: {name} year: {year}", type="track")["tracks"]["items"][0]["uri"] for name in best_song_100]

play_list = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False, description=f"{year} Billboard top 100 songs")
# print(play_list)
# for song_uri in song_uris:
songs_exm = ['spotify:track:6rPO02ozF3bM7NnOV4h6s2', 'spotify:track:1OAh8uOEOvTDqkKFsKksCi', 'spotify:track:0KKkJNfGyhkQ5aFogxQAPU']
sp.playlist_add_items(playlist_id=play_list["id"], items=song_uris_list[:-2])
print(sp.playlist(playlist_id=play_list["id"]))
# print(song_uris)
# print(len(song_uris))