import Spotify as spot
import pandas as pd
from matplotlib import pyplot as plt

sp = spot.user_log_in()
liked_songs = spot.ser_liked_songs()
bad_songs = spot.user_playlist_by_name('squarebrush')

features = spot.song_features(liked_songs, target=1)
bad_features = spot.song_features(bad_songs, target=0)
features.extend(bad_features)

data = pd.DataFrame(features)


def plot_pos_neg(data, feature):
    
    """
    function to plot the positive/negative song values 
    of a certain feature
    features are:
    danceablity, energy, key, loudness, mode, speechiness,
    acousticness, instrumentalness, liveness, valence,
    tempo
    """
    if feature not in list(features[0].keys()):
        print('Cannot plot a feature that is not an audio features')
        return None
    else:
        pos = data[data['target'] == 1][feature]
        neg = data[data['target'] == 0][feature]
        
        fig = plt.figure(figsize=(12,8))
        plt.title(f"{feature.capitalize()} distribution for liked/disliked songs")
        pos.hist(alpha=0.7, bins=30, label='positive')
        neg.hist(alpha=0.7, bins=30, label='negative')
        plt.legend(loc='upper right')
        
    return fig

#example plot
fig = plot_pos_neg('energy')
        
    
    
    
    
