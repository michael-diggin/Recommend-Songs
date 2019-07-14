import Spotify as spot
from MLClassifier import ml_model

     

#Train the model here


sp = spot.user_log_in()

liked_songs = spot.user_liked_songs()
bad_songs = spot.user_playlist_by_name('squarebrush')
features = spot.song_features(liked_songs, target=1)
bad_features = spot.song_features(bad_songs, target=0)
features.extend(bad_features)

model = ml_model(features)
