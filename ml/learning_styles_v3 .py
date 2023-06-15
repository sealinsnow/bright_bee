# -*- coding: utf-8 -*-
"""Learning Styles_v3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RkdtnJHcaFV3E0zu8ixGlntn7T4fok2x
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/CAPSTONE/learning_styles.csv')
df.head()

df['Learner'] = df['Learner'].replace({'K': '0_K', 'A': '1_A', 'V': '2_V'})
df.head()

types = df['Learner'].unique()
num_types = len(types)

df = pd.get_dummies(df, columns=['Learner'])
df.head()

dummy_type = ['Learner_0_K', 'Learner_1_A', 'Learner_2_V']
print(dummy_type)

#Split the dataset for training (85%)
from sklearn.model_selection import train_test_split

train_df, valid_df = train_test_split(df, test_size=0.15, random_state=1)

print(train_df)

print(f"training examples: {train_df.shape[0]}")
print(f"validation examples: {valid_df.shape[0]}")

y_train = pd.concat([train_df.pop(dc) for dc in dummy_type], axis=1)
y_valid = pd.concat([valid_df.pop(dc) for dc in dummy_type], axis=1)

y_train.head()

y_valid.head()

# Scaling dataset
stats = train_df.describe().transpose()
x_train = (train_df-stats['mean'])/stats['std']
x_valid = (valid_df-stats['mean'])/stats['std']
x_train.head()

print(stats)

# Converting to numpy
train_features = x_train.to_numpy()
valid_features = x_valid.to_numpy()

train_labels = y_train.to_numpy()
valid_labels = y_valid.to_numpy()

print(train_features)

def create_train_valid (features, labels, batch, shuffle_buffer):
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))
    dataset = dataset.shuffle(shuffle_buffer)
    dataset = dataset.batch(batch).prefetch(1)
    return dataset

batch_size = 32
buffer = 50
training = create_train_valid(train_features, train_labels, batch_size, buffer)
validation = create_train_valid(valid_features, valid_labels, batch_size, buffer)

# Build Model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='relu'),
    tf.keras.layers.Dense(num_types, activation='softmax')
])


model.compile(
    loss=tf.keras.losses.categorical_crossentropy,
    optimizer=tf.keras.optimizers.SGD(),
    metrics=['accuracy', 'mae']
)

history = model.fit(
    training,
    epochs=100,
    validation_data=validation
)

model.summary()

# plotting Graphs
plots = ['accuracy', 'mae', 'loss']
for plot in plots:
    metric = history.history[plot]
    val_metric = history.history[f"val_{plot}"]
    epochs = range(len(metric))

    plt.figure(figsize=(15, 10))
    plt.plot(epochs, metric, label=f"Training {plot}")
    plt.plot(epochs, val_metric, label=f"Validation {plot}")
    plt.legend()
    plt.title(f"Training and Validation for {plot}")
    plt.show()

X_test2 = np.array([[5,	4,	4,	4,	3,	3,	2,	4,	3,	4	,3,	4,	3,	4,	4	]]) #audio
y_pred2 = model.predict(X_test2)
y_pred2

print(np.argmax(y_pred2,axis=1))
#0 = kinetik | 1 = audio | 2 = visual

from tensorflow.keras.models import load_model

model.save('/content/model/modelfinal.h5')

#import joblib
#joblib.dump(model,'conten/lr_model.pkl')

#import pickle

#pickle.dump(model, open('model.pkl', 'wb'))
#pickled_model = pickle.load(open('model.pkl', 'rb'))
#pickled_model.predict(X_test2)

print(tf.__version__)

pip install tensorflow tensorflow-lite

model.save('model pb','pb')

convert_model = tf.lite.TFLiteConverter.from_saved_model('model pb')

convert_model.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
    tf.lite.OpsSet.SELECT_TF_OPS # enable TensorFlow ops.
]

test_lite = convert_model.convert()

# Save the model.
with open('modelfinal.tflite', 'wb') as f:
  f.write(test_lite)
