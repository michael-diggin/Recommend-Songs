import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials 

#global variables
cid = CLIENT_ID
secret = CLIENT_SECRET
redirect_uri = URI_PROVIDED_ON_SPOTIFY
username = ""
scope = 'user-library-read playlist-read-private'
user = USERNAME


def user_log_in():
    """
    prompt for log in and return a spotipy instance using the access token
    """ 
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    try:
        token = util.prompt_for_user_token(username, scope, client_id=cid, client_secret=secret, redirect_uri=redirect_uri)
    except:
            print("Can't get token for", username)
            sys.exit()
    
    sp = spotipy.Spotify(auth=token)
    return sp

sp=user_log_in()


def user_liked_songs():
    """
    returns list of the users saved/liked songs
    """
    results = sp.current_user_saved_tracks()
    liked_songs = results['items']
    while results['next']:
        results = sp.next(results)
        liked_songs.extend(results['items'])
        
    return liked_songs

def user_playlist_by_name(playlist_name):
    """
    returns songs from a user playlist of given name if one exists,
    None is returned else
    """
    playlists = sp.user_playlists(user)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            play_id = playlist['id']
            songs = songs_from_playlist(play_id)
            return songs
    print('No playlist found matching that name')
    return None
    
    
def song_ids(songs):
    """
    returns list of ids of songs in a given list,
    song ids are needed to get the audio features
    """
    ids = []
    for song in songs:
        ids.append(song['track']['id'])
    
    return ids

def songs_from_playlist(play_id):
    """
    returns list of songs from a playlist given the playlist id
    """
    playlist = sp.user_playlist(user, play_id)
    tracks = playlist['tracks']
    songs = tracks['items']
    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks['items']:
            songs.append(item)
    
    return songs

def song_features(songs, target=1):
    """
    returns list of audio features for a list of songs
    """
    s_ids = song_ids(songs)
    features = []
    for i in range(0,len(s_ids),50):
        audio_features = sp.audio_features(s_ids[i:i+50])
        for track in audio_features:
            features.append(track)
            features[-1]['target'] = target
            
    return features

