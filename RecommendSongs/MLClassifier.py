from Spotify import features, disc_weekly_features
import pandas as pd

import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split


data = pd.DataFrame(features)

#split into training/testing data
train, test = train_test_split(data, test_size = 0.15)

#utility function to make a tf dataset
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('target')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds

#columns we want to use
feature_cols = []
for col in ['energy', 'danceability', 'loudness', 'speechiness', 'valence', 'key']:
    feature_cols.append(feature_column.numeric_column(col))

feature_layer = tf.keras.layers.DenseFeatures(feature_cols)

batch_size = 32
train_ds = df_to_dataset(train, batch_size=batch_size)
test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

#create and compile the model
model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(128, activation='relu'),
  layers.Dense(128, activation='relu'),
  layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'],
              run_eagerly=True)

model.fit(train_ds, epochs=10)

disc_data = pd.DataFrame(disc_weekly_features)
predict_ds = df_to_dataset(disc_data, shuffle=False, batch_size = 10)
predictions = model.predict(predict_ds)






