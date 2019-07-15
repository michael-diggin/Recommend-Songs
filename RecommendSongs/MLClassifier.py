import pandas as pd

import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split


#utility function to make a tf dataset
def df_to_dataset(dataframe, shuffle=True, batch_size=32):
  dataframe = dataframe.copy()
  labels = dataframe.pop('target')
  ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
  if shuffle:
    ds = ds.shuffle(buffer_size=len(dataframe))
  ds = ds.batch(batch_size)
  return ds



def ml_model(data, batch_size=32):
    """
    returns a tf model trained on the song data provided
    """
    
    #set up the data
    df = pd.DataFrame(data)
    train, test = train_test_split(df, test_size = 0.15)
    
    feature_cols = []
    for col in ['energy', 'danceability', 'loudness', 'speechiness', 'valence', 
            'mode', 'key', 'acousticness', 'instrumentalness', 'liveness',
            'tempo'
            ]:
        feature_cols.append(feature_column.numeric_column(col))

    feature_layer = tf.keras.layers.DenseFeatures(feature_cols)
    
    train_ds = df_to_dataset(train, batch_size=batch_size)
    test_ds = df_to_dataset(test, shuffle=False, batch_size=batch_size)

    #create the model
    model = tf.keras.Sequential([
             feature_layer,
             layers.Dense(128, activation='relu'),
             layers.Dense(128, activation='relu'),
             layers.Dense(1, activation='sigmoid')
    ]) 
    
    #compile it
    model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'],
              run_eagerly=True)
    
    #train the model
    model.fit(train_ds, epochs=5)
    
    #evalaue the model
    loss, accuracy = model.evaluate(test_ds)
    print(f"Model is accurate to {accuracy*100}%")
    
    return model



def predictions(model, data):
    df = pd.DataFrame(data)
    ds = df_to_dataset(df, shuffle=False, batch_size=10)
    pred = model.predict(ds).flatten()
    return pred
    
    
