import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials 

cid ="f39a5b4873c644798153b1b2e064622a" 
secret = "ff2eae50bf1e4a53a9efb9fef2675f9b"
redirect_uri = "http://localhost:8888/callback/"
username = ""



client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = 'user-library-read playlist-read-private'

try:
    token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)
except:
    print("Can't get token for", username)
    sys.exit()
    

sp = spotipy.Spotify(auth=token)

#Use the saved songs as songs I liked
results = sp.current_user_saved_tracks()
liked_songs = results['items']
while results['next']:
    results = sp.next(results)
    liked_songs.extend(results['items'])

#get the song ids
liked_ids = []
for i in range(len(liked_songs)):
    liked_ids.append(liked_songs[i]['track']['id'])
    

#songs I don't like
#for now its just a playlist of about 340 songs of a certain genre I don't like    
#bad playlist id '7iqH15fAnuVPsP48WxhNxz'    
bad_playlist = sp.user_playlist('michaeldiggin', '7iqH15fAnuVPsP48WxhNxz')
bad_tracks = bad_playlist['tracks']
bad_songs = bad_tracks['items']
while bad_tracks['next']:
    bad_tracks = sp.next(bad_tracks)
    for item in bad_tracks['items']:
        bad_songs.append(item)
        
#get bad song ids
bad_ids = []
for i in range(len(bad_songs)):
    bad_ids.append(bad_songs[i]['track']['id'])
    
#want to analyse the song features
features = []
for i in range(0,len(liked_ids),50):
    audio_features = sp.audio_features(liked_ids[i:i+50])
    for track in audio_features:
        features.append(track)
        features[-1]['target'] = 1 #this is a song we like

for i in range(0,len(bad_ids),50):
    audio_features = sp.audio_features(bad_ids[i:i+50])
    for track in audio_features:
        features.append(track)
        features[-1]['target'] = 0 #this is a song we don't like
        

#features are danceablity, energy, key, loudness, mode, speechiness, acousticness, instrumentalness
#liveness, valence, tempo
           
        
         
                 
    
