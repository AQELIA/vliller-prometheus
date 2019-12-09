import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

# DATASET_PATH = 'dataset/station-1_2019-09-15_to_2019-10-15.csv'
DATASET_PATH = 'dataset/station-1-2_2019-09-25_to_2019-10-10.csv'

def load_dataset():
  dataset = pd.read_csv(DATASET_PATH).copy()

  # removes id column for now (only station 1)
  # dataset.pop('id')

  # split set into train/test
  train_dataset = dataset.sample(frac=0.8,random_state=0)
  test_dataset = dataset.drop(train_dataset.index)

  return train_dataset, test_dataset

def normalize_dataset(dataset, mean, std):
  def norm(x):
    return (x - mean) / std

  return norm(dataset)

def build_model(train_dataset_size):
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[train_dataset_size]),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(
    loss='mse',
    optimizer=optimizer,
    metrics=['mae', 'mse']
  )

  return model

def train_model(model, train_data, train_labels, epochs = 1000):
  # The patience parameter is the amount of epochs to check for improvement
  early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

  early_history = model.fit(
    train_data,
    train_labels,
    epochs=epochs,
    validation_split=0.2,
    verbose=0,
    callbacks=[
      early_stop,
      tfdocs.modeling.EpochDots()
    ]
  )

  return early_history

def evaluate_model(model, test_data, test_labels):
  loss, mae, mse = model.evaluate(
    test_data,
    test_labels,
    verbose=2
  )

  print('Testing set Mean Abs Error: {:5.2f} usage'.format(mae))

  return loss, mae, mse

###################
#  Main
#
train_dataset, test_dataset = load_dataset()

# compute stats on dataset
train_stats = train_dataset.describe()
train_stats.pop('usage')
train_stats = train_stats.transpose()

# split 'labels' (value modal gonna predict) from features data
train_labels = train_dataset.pop('usage')
test_labels = test_dataset.pop('usage')

normed_train_data = normalize_dataset(train_dataset, train_stats['mean'], train_stats['std'])
normed_test_data = normalize_dataset(test_dataset, train_stats['mean'], train_stats['std'])

# lets build and train the model !
train_dataset_size = len(train_dataset.keys())
model = build_model(train_dataset_size)
model.summary()

history = train_model(model, normed_train_data, train_labels, epochs = 1000)

# evaluation
evaluate_model(model, normed_test_data, test_labels)

# # model prediction
test_predictions = model.predict(normed_test_data).flatten()

# display prediction
a = plt.axes(aspect='equal')
plt.scatter(test_labels, test_predictions)
plt.xlabel('True Values [usage]')
plt.ylabel('Predictions [usage]')
lims = [0, 1]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims, lims)

plt.show()