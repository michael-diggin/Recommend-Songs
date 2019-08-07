import Spotify as spot
from MLClassifier import predictions       
from Training import trained_model




disc_weekly_songs = spot.user_playlist_by_name('Discover Weekly')
disc_weekly_features = spot.song_features(disc_weekly_songs)

predictions = predictions(trained_model, disc_weekly_features)

recommended = []
rec_ids = []
for i in range(len(disc_weekly_songs)):
    if predictions[i] >= 0.9:
        recommended.append(disc_weekly_songs[i]['track']['name'])
        rec_ids.append(disc_weekly_songs[i]['track']['id'])

if recommended is not None:
    print('The following songs are recommeneded based on your saved songs:')
    print('\n')
    for song in recommended:
        print(song)
else:
    print('No songs matched your likes by over 80%')

if rec_ids is not None:
    spot.add_tracks(rec_ids, 'Recommended')






