import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "081c809d38714ccba3b3a1b048974b0b"
CLIENT_SECRET = "9e722b93bf2947b6bcfbea54709c5857"

scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://example.com", scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
