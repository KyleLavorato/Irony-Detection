## Final Project Elec 880 --Pretraining- Using Glove_Word Embeddings
#load packages
import tensorflow as tf
import csv
import random
import sys
import os
from keras import layers
#from keras.preprocessing.text import one_hot
from keras.layers import Dense,Input,GlobalMaxPooling1D
from keras.layers import Flatten, Dropout
from keras.layers.embeddings import Embedding
from keras.initializers import Constant
from tensorflow.keras import backend as K
import numpy as np # linear algebra
#import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from keras.layers import LSTM, SpatialDropout1D,Conv1D, MaxPooling1D,Activation
from keras.models import Sequential
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
#from keras.utils.np_utils import to_categorical
#from keras.callbacks import EarlyStopping

#read in data files
def parseDataset(fp):
    corpus = []
    y = []
    with open(fp, "r", encoding='utf-8') as f:
        fileData = csv.reader(f, delimiter="|")
        for row in fileData:
            y.append(row[0])
            corpus.append(row[1])
    return corpus, y

##main
#load data
corpus_random, y_random = parseDataset("/Users/monicarao/Desktop/Twitter-Dataset/corpus-irony-processed.txt")
corpus_irony, y_irony = parseDataset("/Users/monicarao/Desktop/Twitter-Dataset/pretrain_random_small.txt")
corpus = corpus_random + corpus_irony
y = y_random + y_irony
a_tweet_array=[]
b_score_array=[]

for i in range(0, len(corpus)):
    index = random.randint(0, len(corpus))
    tweet = corpus.pop(index)
    score = y.pop(index)
    print(tweet,score)
    a_tweet_array.append(tweet)
    b_score_array.append(score)

#Extract Word Embeddings 
embeddings_index = dict()
f = open('/Users/monicarao/Desktop/Twitter-Dataset/...')
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

#Embedding matrix
vocabulary_size = 15000
embedding_matrix = np.zeros((vocabulary_size, 100))
for word, index in Tokenizer.word_index.items():
    if index > vocabulary_size - 1:
        break
    else:
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector

## create model
model_glove = Sequential()
model_glove.add(Embedding(vocabulary_size, 100, input_length=50, weights=[embedding_matrix], trainable=False))
model_glove.add(Dropout(0.2))
model_glove.add(Conv1D(64, 5, activation='relu'))
model_glove.add(MaxPooling1D(pool_size=4))
#model_glove.add(LSTM(100))
model_glove.add(Dense(1, activation='sigmoid'))
model_glove.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
## Fit train data
model_glove.fit(a_tweet_array, np.array( b_score_array), validation_split=0.2, epochs = 3)

## Get weights
glove_embds = model_glove.layers[0].get_weights()[0]

##Summary of model
print(model_glove.summary())


    