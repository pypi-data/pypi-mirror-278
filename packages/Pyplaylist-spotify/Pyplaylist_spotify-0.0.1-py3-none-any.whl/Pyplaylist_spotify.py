import datetime as dt
import warnings
warnings.filterwarnings('ignore')
import requests
from bs4 import BeautifulSoup
date=input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
def playlist():
    url = f"https://www.billboard.com/charts/hot-100/{date}"
    response = requests.get(url)
    #status=response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    song_name = soup.select("li ul li h3")
    list_of_song_name = [x.getText().strip() for x in song_name]


    import spotipy as sp
    from spotipy.oauth2 import SpotifyOAuth
    import config
    #spotify user authentication 
    sp = sp.Spotify(
        auth_manager=SpotifyOAuth(
            scope="playlist-modify-private",
            redirect_uri="http://localhost:8501",
            client_id=config.client_id,
            client_secret=config.client_secret,
            show_dialog=True,
            cache_path="./token.txt",
            username=config.username,
        )
    )
    user_id = sp.current_user()["id"]


    song_uris = []
    year = date.split("-")[0]
    for song in list_of_song_name:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        #print(result)
        #st.write(result)
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
            
    #Creating a new private playlist in Spotify
    playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
    #print(playlist)
    #st.write(playlist)

    #Adding songs found into the new playlist
    sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
