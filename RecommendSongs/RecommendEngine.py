from Spotify import disc_weekly_songs
from MLClassifier import predictions        

recommended = []
for i in range(len(disc_weekly_songs)):
    if predictions[i][0] >= 0.9:
        recommended.append(disc_weekly_songs[i]['track']['name'])

if recommended is not None:
    print('The follwoing songs are recommeneded based on your saved songs:')
    print('\n')
    for song in recommended:
        print(song)
else:
    print('No songs matched your likes by over 90%')
