#!/usr/bin/env python
# coding: utf-8

# # Cifar 10 dataset from keras
# 
# <img src="https://production-media.paperswithcode.com/datasets/4fdf2b82-2bc3-4f97-ba51-400322b228b1.png" width="300" height="200" />

# # Plan :
#  > Importing libraries
#  
#  > Data analysis
#  
#  > Plotting
#  
#  > Building CNN model
#  
#  > Deploying model

# # 1 

# In[2]:


from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization, Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Activation
from keras.callbacks import Callback
import random
from tensorflow import keras
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import json


# # 2

# In[4]:


(x_train,y_train),(x_test,y_test) = keras.datasets.cifar10.load_data()


# In[15]:


print("train_data : ",x_train.shape,y_train.shape,"\n\n",'test_data:',x_test.shape,y_test.shape)


# # 3

# In[6]:


label=['airplane','automobile','bird','cat','deer','dog','frog','horse','ship','truck']
plt.figure(figsize=(22,10))
z = random.randint(1,len(y_train))
plt.title(f"this is a/an {label[y_train[z][0]]}\n")
print()
plt.imshow(x_train[z])
plt.show()


# # 4

# In[19]:


model =Sequential([
    keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
    keras.layers.experimental.preprocessing.RandomWidth(0.1),
    keras.layers.experimental.preprocessing.RandomZoom(0.1),
])
# We use Random function which multiplies our datas by changing the position of photo like zooming it or rotating


# In[20]:


# Callback function is used to avoid time wasting.It stops the training of our model if it's loss or accuracy reaches the point
# which we need we ourselves give the  border to stop
class myCallback(Callback):
    def on_epoch_end(self,epoch,logs={}):
        if (logs.get("loss")<0.1):
            print("\n accuracy reached the highest point,cancelling session")
            self.model.stop_training=True
callback = myCallback()


# In[21]:


model.add(Sequential([
    Conv2D(32,(3,3),padding='same',input_shape=(32,32,3)),
    Activation('relu'),
    BatchNormalization(),
    MaxPooling2D((3,3)),
    Dropout(0.2),
    
    Conv2D(64,(3,3),padding='same'),
    Activation('relu'),
    BatchNormalization(-1),
    
    Conv2D(64,(3,3),padding='same'),
    Activation('relu'),
    BatchNormalization(-1),
    MaxPooling2D((2,2)),
    Dropout(0.25),
    
    Conv2D(128,(3,3),padding='same'),
    Activation('relu'),
    BatchNormalization(),
    
    Conv2D(128,(3,3),padding='same'),
    Activation('relu'),
    BatchNormalization(-1),
    MaxPooling2D((2,2)),
    
    Conv2D(256,(3,3),padding='same'),
    Activation('relu'),
    BatchNormalization(),
    
    Flatten(),
    Dense(256),
    Activation('relu'),
    Dense(128),
    Activation('relu'),
    Dense(64),
    Activation('relu'),
    Dense(32),
    Activation('relu'),
    Dense(10),
    Activation("softmax")
]))
l_r=0.001
batch_size=64
epochs=20
op=Adam(learning_rate=l_r)
model.compile(optimizer=op,loss='sparse_categorical_crossentropy',metrics=['accuracy'])
hist = model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=epochs, batch_size=batch_size,callbacks=callback)


# In[23]:


model.evaluate(x_test,y_test)


# In[24]:


model.summary()


# In[25]:


def plotting(hist):
    plt.plot(hist.history["accuracy"])
    plt.plot(hist.history["val_accuracy"])
    plt.title("model accuracy")
    plt.ylabel("accuracy")
    plt.xlabel("epoch")
    plt.legend(["train", "validation"], loc="best")
    plt.show()
plotting(hist)

