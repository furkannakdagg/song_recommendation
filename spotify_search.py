import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# https://developer.spotify.com/dashboard/
cid = "eb018f76e1bb427caf2857fccc6cc719"
secret = "74dc7173c9e34e03aab2b6dad04f2aa8"
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_pic(song_name, artist_name):
    find = song_name + " " + artist_name
    song = sp.search(find, limit=5)
    if len(song["tracks"]["items"]) != 0:
        album_pic_url = song["tracks"]["items"][0]["album"]["images"][1]["url"]
        preview_song = song["tracks"]["items"][0]["preview_url"]
        return album_pic_url, preview_song
    else:
        return -1



def audio_features(song_name, artist_name):
    find = song_name + " " + artist_name
    song = sp.search(find, limit=5)
    popularity = song["tracks"]["items"][0]["popularity"]
    explicit = 1 if song["tracks"]["items"][0]["explicit"] else 0
    release_date = pd.to_datetime(pd.Series(song["tracks"]["items"][0]["album"]["release_date"])).dt.year[0]
    danceability = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["danceability"]
    energy = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["energy"]
    key = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["key"]
    loudness = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["loudness"]
    mode = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["mode"]
    speechiness = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["speechiness"]
    acousticness = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["acousticness"]
    instrumentalness = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["instrumentalness"]
    liveness = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["liveness"]
    valence = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["valence"]
    tempo = sp.audio_features(song["tracks"]["items"][0]["id"])[0]["tempo"]

    song_analysis = pd.Series(data=[popularity, explicit, release_date, danceability, energy, key, loudness,
                    mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo])
    return song_analysis


def info(song_name, artist_name):
    find = song_name + " " + artist_name
    song = sp.search(find, limit=5)
    art_info = song["tracks"]["items"][0]["artists"][0]["name"]
    song_info = song["tracks"]["items"][0]["name"]
    release_date = song["tracks"]["items"][0]["album"]["release_date"]
    explicit = "Evet" if song["tracks"]["items"][0]["explicit"] == True else "Hayır"
    song_spot = song["tracks"]["items"][0]["external_urls"]["spotify"]
    art_spot = song["tracks"]["items"][0]["album"]["artists"][0]["external_urls"]["spotify"]
    return art_info, song_info, release_date, explicit, song_spot, art_spot

def rec_song(df, rec_song):
    rec_list = df.corrwith(rec_song, axis=1, numeric_only=True).sort_values(ascending=False).head(11)
    rec_list = rec_list[1:]
    rec_df = df.loc[rec_list.index, ["name", "artists"]]
    rec_df.to_csv("rec_df.csv")

