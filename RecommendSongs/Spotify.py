import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials 

cid ="f39a5b4873c644798153b1b2e064622a" 
secret = "ff2eae50bf1e4a53a9efb9fef2675f9b"
redirect_uri = "http://localhost:8888/callback/"
username = ""

#log in to spotify via spotipy
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-library-read playlist-read-private'

try:
    token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)
except:
    print("Can't get token for", username)
    sys.exit()
    
sp = spotipy.Spotify(auth=token)

def song_ids(songs):
    ids = []
    for song in songs:
        ids.append(song['track']['id'])
    
    return ids

def songs_from_playlist(play_id):
    playlist = sp.user_playlist('michaeldiggin', play_id)
    tracks = playlist['tracks']
    songs = tracks['items']
    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks['items']:
            songs.append(item)
    
    return songs

def song_features(ids, target=1):
    features = []
    for i in range(0,len(ids),50):
        audio_features = sp.audio_features(ids[i:i+50])
        for track in audio_features:
            features.append(track)
            features[-1]['target'] = target
            
    return features

#Use the saved songs as songs I like
results = sp.current_user_saved_tracks()
liked_songs = results['items']
while results['next']:
    results = sp.next(results)
    liked_songs.extend(results['items'])

liked_ids = song_ids(liked_songs)
    

#songs I don't like
#for now its just a playlist of about 340 songs of a certain genre I don't like    
#bad playlist id '7iqH15fAnuVPsP48WxhNxz' 

bad_songs = songs_from_playlist('7iqH15fAnuVPsP48WxhNxz')
bad_ids = song_ids(bad_songs)   

        
#get the audio features
features = song_features(liked_ids, target=1)
bad_features = song_features(bad_ids, target=0)
features.extend(bad_features)

#features are danceablity, energy, key, loudness, mode, speechiness, acousticness 
#instrumentalness, liveness, valence, tempo
           
#lets use the discover weekly playlist to see how good the model is at prediction
#playlist id is 37i9dQZEVXcM5yWwSfkc97

disc_weekly_songs = songs_from_playlist('37i9dQZEVXcM5yWwSfkc97')
disc_weekly_ids = song_ids(disc_weekly_songs)
disc_weekly_features = song_features(disc_weekly_ids)

     
         
                 
    
