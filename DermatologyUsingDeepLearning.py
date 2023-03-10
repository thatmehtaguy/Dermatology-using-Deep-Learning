# -*- coding: utf-8 -*-
"""Copy of Copy of IPD_VGG.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vTGFBcWyXFgZKh7DUY5jAQ6u_tmc7b5O
"""

import numpy as np
import pandas as pd
import pathlib
import os

from google.colab import drive
drive.mount('/content/drive')

data_dir='/content/drive/MyDrive/skin disease'
data_dir = pathlib.Path(data_dir)
data_dir

Acne= list(data_dir.glob('Acne/*'))
Eczema= list(data_dir.glob('Eczema/*'))
Psoriasis= list(data_dir.glob('Psoriasis_and_LP/*'))
Ringworm= list(data_dir.glob('Ringworm/*'))

# Contains the images path
df_images = {
'Acne':Acne,
'Eczema':Eczema,
'Psoriasis':Psoriasis,
'Ringworm':Ringworm,
}

# Contains numerical labels for the categories
df_labels = {
'Acne':0,
'Eczema':1,
'Psoriasis':2,
'Ringworm':3,
}

import cv2 as cv
X=[]
y=[]
for label, images in df_images.items():
    for image in images:
        img=cv.imread(str(image))
        img=cv.resize(img,(224,224))
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        X.append(img)
        y.append(df_labels[label])

import matplotlib.pyplot as plt
plt.hist(y)
plt.show()

y = np.array(y)

X = np.array(X)

y.shape

X.shape

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y, train_size=0.7,random_state=42)

X_train.shape

from tensorflow.keras.applications.vgg16 import VGG16
res = VGG16(weights ='imagenet', include_top = False, input_shape = (224, 224, 3))

from tensorflow.keras import layers
import tensorflow as tf
import keras
from keras.layers import (Conv2D, MaxPooling2D, Dense, Flatten, Dropout, Input,GlobalAveragePooling2D,BatchNormalization)
from tensorflow.keras import Sequential, Model

res.trainable = False


x= res.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
# x = Dropout(0.5)(x) 
x = Dense(512, activation ='relu')(x)
x = BatchNormalization()(x)
# x = Dropout(0.5)(x)

x = Dense(256, activation ='relu')(x)
x = BatchNormalization()(x)

x = Dense(4, activation ='softmax')(x)
model = Model(res.input, x)

model.compile(optimizer =tf.keras.optimizers.RMSprop(learning_rate=0.0001),  #'Adam'
              loss ="sparse_categorical_crossentropy",  #sparse_categorical_crossentropy
              metrics =["sparse_categorical_accuracy"])  #sparse_categorical_accuracy

model.summary()

X_train = np.array(X_train)
y_train = np.array(y_train)
X_test = np.array(X_test)
y_test = np.array(y_test)

from keras.callbacks import ModelCheckpoint, EarlyStopping
custom_early_stopping = EarlyStopping(
    monitor='val_loss', 
    patience=10, 
    min_delta=0.001, 
    mode='min'
)

vgghist = model.fit(X_train,y_train, validation_data = (X_test,y_test), epochs = 50)

from sklearn.metrics import accuracy_score
y_pred=model.predict(X_test).argmax(axis=1)
accuracy_score(y_test,y_pred)

from sklearn import metrics
confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)

cm_display.plot()
plt.show()



from keras.applications.inception_v3 import InceptionV3
base_model=InceptionV3(include_top=False, weights='imagenet',input_shape=(224,224,3))

for i in base_model.layers:
    i.trainable=False

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Flatten()(x)
x = Dense(128, activation ='relu')(x)
#x=Dropout(0.5)(x)
x = Dense(64, activation ='relu')(x)
pred=Dense(4,activation='softmax')(x)
model=Model(inputs=base_model.input,outputs=pred)

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics='accuracy')

model.summary()

InceptionVRHist = model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs = 100)

from sklearn.metrics import accuracy_score
y_pred=model.predict(X_test).argmax(axis=1)
accuracy_score(y_test,y_pred)

from sklearn import metrics
confusion_matrix = metrics.confusion_matrix(y_test, y_pred)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = confusion_matrix)

cm_display.plot()
plt.show()