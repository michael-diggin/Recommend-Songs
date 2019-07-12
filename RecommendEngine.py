import Spotify as spot
from MLClassifier import ml_model , predictions       

"""
    -load the spotify data
    -load the model and train it
    -run on the new data
    -print out the predictions
"""

sp = spot.user_log_in()

liked_songs = spot.user_liked_songs()
bad_songs = spot.user_playlist_by_name('squarebrush')
features = spot.song_features(liked_songs, target=1)
bad_features = spot.song_features(bad_songs, target=0)
features.extend(bad_features)

model = ml_model(features)

disc_weekly_songs = spot.user_playlist_by_name('Discover Weekly')
disc_weekly_features = spot.song_features(disc_weekly_songs)

predictions = predictions(model, disc_weekly_features)

recommended = []
for i in range(len(disc_weekly_songs)):
    if predictions[i] >= 0.8:
        recommended.append(disc_weekly_songs[i]['track']['name'])

if recommended is not None:
    print('The follwoing songs are recommeneded based on your saved songs:')
    print('\n')
    for song in recommended:
        print(song)
else:
    print('No songs matched your likes by over 80%')
