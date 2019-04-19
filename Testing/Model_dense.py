## Final Project Elec 880 --LSTM Dense Model
#load packages
import tensorflow as tf
import csv
import random
import sys
import os
import glob
import errno
from keras import layers
from keras.models import model_from_json
from keras.layers import Dense,Input,GlobalMaxPooling1D
from keras.layers import Flatten, Dropout
from keras.layers.embeddings import Embedding
from keras.initializers import Constant
from tensorflow.keras import backend as K
import numpy as np 
from keras.layers import LSTM, SpatialDropout1D,Conv1D, MaxPooling1D,Activation
from keras.models import Sequential
from sklearn.feature_extraction.text import CountVectorizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras.callbacks import EarlyStopping

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

def score(input_dir, output_dir):
    # unzipped submission data is always in the 'res' subdirectory
    submission_dir = os.path.join(input_dir, 'res')
    submission_file = []
    for el in os.listdir(submission_dir):
        if el.startswith('predictions'):
            submission_file.append(el)
    if not len(submission_file) == 1:
       #print ("Warning: the submission folder should only contain 1 file ('predictions-taskA.txt' or 'predictions-taskB.txt'). Process terminated.")
       sys.exit()
    submission_file_name = submission_file[0]
    submission_path = os.path.join(submission_dir, submission_file_name)
    if any (name in submission_file_name.lower() for name in ['taska', 'task-a', 'task_a']):
        task = "A"
    elif any (name in submission_file_name.lower() for name in ['taskb', 'task-b', 'task_b']):
        task = "B"
    else:
        #message = "Task not found. Please check the name of your submission file."
        sys.exit()
    with open(submission_path) as submission_file:
        submission = submission_file.readlines()

    # unzipped reference data is always in the 'ref' subdirectory
    if task == "A":
        with open(os.path.join(input_dir, 'ref', 'goldstandard_train_A.txt')) as truth_file:
            truth = truth_file.readlines()
    elif task == "B":
        with open(os.path.join(input_dir, 'ref', 'goldstandard_train_B.txt')) as truth_file:
            truth = truth_file.readlines()

    true = []
    predicted = []
    for s,t in zip(submission, truth):
        if s.strip() and t.strip():
            true.append(int(t.strip()))
            predicted.append(int(s.strip()))

    if task == "A":
        for el in list(set(true+predicted)):
            if not el in [0,1]:
                sys.exit()
    elif task == "B":
        for el in list(set(true+predicted)):
            if not el in [0,1,2,3]:
                sys.exit()

    with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
        acc = calc_accuracy(true, predicted)
        if task == "A":
            p, r, f = precision_recall_fscore(true, predicted, beta=1, labels=[0,1], pos_label=1)
        elif task == "B":
            p, r, f = precision_recall_fscore(true, predicted, beta=1, labels=[0,1,2,3])
        output_file.write("Accuracy:{0}\nPrecision:{1}\nRecall:{2}\nF1-score:{3}\n".format(acc, p,r,f))


def calc_accuracy(true, predicted):
    return sum([t==p for t,p in zip(true, predicted)]) / float(len(true))


def precision_recall_fscore(true, predicted, beta=1, labels=None, pos_label=None, average=None):
    # Build contingency table as ldict
    ldict = {}
    for l in labels:
        ldict[l] = {"tp": 0., "fp": 0., "fn": 0., "support": 0.}

    for t, p in zip(true, predicted):
        if t == p:
            ldict[t]["tp"] += 1
        else:
            ldict[t]["fn"] += 1
            ldict[p]["fp"] += 1
        ldict[t]["support"] += 1

    # Calculate precision, recall and F-beta score per class
    beta2 = beta ** 2
    for l, d in ldict.items():
        try:
            ldict[l]["precision"] = d["tp"]/(d["tp"] + d["fp"])
        except ZeroDivisionError: ldict[l]["precision"] = 0.0
        try: ldict[l]["recall"]    = d["tp"]/(d["tp"] + d["fn"])
        except ZeroDivisionError: ldict[l]["recall"]    = 0.0
        try: ldict[l]["fscore"] = (1 + beta2) * (ldict[l]["precision"] * ldict[l]["recall"]) / (beta2 * ldict[l]["precision"] + ldict[l]["recall"])
        except ZeroDivisionError: ldict[l]["fscore"] = 0.0

    # If there is only 1 label of interest, return the scores. No averaging needs to be done.
    if pos_label:
        d = ldict[pos_label]
        return (d["precision"], d["recall"], d["fscore"])
    # If there are multiple labels of interest, macro-average scores.
    else:
        for label in ldict.keys():
            avg_precision = sum(l["precision"] for l in ldict.values()) / len(ldict)
            avg_recall = sum(l["recall"] for l in ldict.values()) / len(ldict)
            avg_fscore = sum(l["fscore"] for l in ldict.values()) / len(ldict)
        return (avg_precision, avg_recall, avg_fscore)   
    
def main():
    [_, input_dir, output_dir] = sys.argv
    score(input_dir, output_dir)
    
    
if __name__ == "__main__":
    main()

#main
    
#load data text files 
#corpus_random, y_random = parseDataset("/Users/monicarao/Desktop/Twitter-Dataset/pretrain.txt")
#corpus_irony, y_irony = parseDataset("/Users/monicarao/Desktop/Twitter-Dataset/pretrain.txt")
#corpus = corpus_random + corpus_irony
#y = y_random + y_irony
#a_tweet_array=[]
#b_score_array=[]

#for i in range(0, len(corpus)):
#    index = random.randint(0, len(corpus))
#    tweet = corpus.pop(index)
#    scores = y.pop(index)
#    print(tweet,scores)
#    a_tweet_array.append(tweet)
#    b_score_array.append(scores)
        
#load json (pretrained Glove Model) 
json_file = open('model.pretraining_glove', 'r')
loaded_model_json = json_file.read('/Users/monicarao/Desktop/ELEC 880/pretraining_glove.py')
json_file.close()
loaded_model = model_from_json(loaded_model_json)
        
# loading train and test files and pretraining text files
path = ('/Users/monicarao/Desktop/Model_Data/Task_A/*.txt')
#path = ('/Users/monicarao/Desktop/Model_Data/Task_B/*.txt')
files = glob.glob(path)
for name in files:
    try:
        with open(name) as f:
            for line in f:
                print(line.split())

MAX_SEQUENCE_LENGTH = 128
MAX_NUM_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.2
print ('Indexing word vectors.')

tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(tweet)
sequences = tokenizer.texts_to_sequences(tweet)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)

labels = to_categorical(np.asarray(score))
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)

indices = np.arange(data.shape[0])
np.random.shuffle(indices)
data = data[indices]
labels = labels[indices]
num_validation_samples = int(VALIDATION_SPLIT * data.shape[0])

#Embedding matrix
embedding_matrix = np.zeros((MAX_NUM_WORDS, MAX_SEQUENCE_LENGTH))
for word, index in Tokenizer.word_index.items():
    if index > MAX_NUM_WORDS - 1:
        break
    else:
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector

##define model
model = Sequential()
model.add(Embedding(MAX_NUM_WORDS, MAX_SEQUENCE_LENGTH, input_length=50, weights=[embedding_matrix], trainable=False))
model.add(Dropout(0.2))
model.add(Conv1D(64, 5, activation='relu'))
model.add(MaxPooling1D(pool_size=4))
model.add(Dense(1, activation='sigmoid')
model.add(SpatialDropout1D(0.7))
model.add(LSTM(64, dropout=0.7, recurrent_dropout=0.7))
model.add(LSTM(64, dropout=0.7, recurrent_dropout=0.7))
model.add(Dense(1, activation='sigmoid'))
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

## Fit train data
model.fit(data, labels, validation_split=0.2, epochs = 15)

##Summary of model
print(model.summary())
model.summary()
#Model Evaluation
#if TASK.lower() == 'a':
#        score = metrics.f1_score(y, predicted, pos_label=1)
#    elif TASK.lower() == 'b':
#        score = metrics.f1_score(y, predicted, average="macro")
#    print ("F1-score Task", TASK, score)
#    for p in predicted:
#        PREDICTIONSFILE.write("{}\n".format(p))
#    PREDICTIONSFILE.close()
