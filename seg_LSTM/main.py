import codecs
import random

import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, TimeDistributed, Activation, Dropout

trainSet = []
testSet = []

trainFile = codecs.open('train.tag','r',encoding='utf-8')
testFile = codecs.open('test.tag','r',encoding='utf-8')


for line in trainFile:
    line = line.strip()
    trainSet.append(line)

def pos2vec(pos):
    if pos == 'B':
        return [1,0,0,0]
    elif pos == 'M':
        return [0,1,0,0]
    elif pos == 'E':
        return [0,0,1,0]
    elif pos == 'S':
        return [0,0,0,1]
    else:
        return [0,0,0,0]

sentLength = 375

vocab = {}
vocabSize = 0

def word2num(word):
    if word in vocab:
        return vocab[word]
    else:
        return 0

trainData = {}
trainData['X'] = []
trainData['Y'] = []
validData = {}
validData['X'] = []
validData['Y'] = []

for line in trainSet:
    line = line.strip().split()
    r = random.random()
    sent = []
    poses = []

    for pairs in line:
        pairs = pairs.split('/')
        word = pairs[0]
        pos = pairs[1]
        if word not in vocab:
            vocabSize += 1
            vocab[word] = vocabSize
        sent.append(word2num(word))
        poses.append(pos2vec(pos))
    sent += [0 for i in range(sentLength - len(sent))]
    poses += [pos2vec('N') for i in range(sentLength - len(poses))]
    if r < 0.8:
        trainData['X'].append(sent)
        trainData['Y'].append(poses)
    else:
        validData['X'].append(sent)
        validData['Y'].append(poses)

X_train = np.array(trainData['X'])
Y_train = np.array(trainData['Y'])
X_valid = np.array(validData['X'])
Y_valid = np.array(validData['Y'])
print("data shape (#_batches, batch_size, vector_size)")
print("X_train", X_train.shape)
print("Y_train", Y_train.shape)
print("X_dev", X_valid.shape)
print("Y_dev", Y_valid.shape)

model = Sequential()
model.add(Embedding(vocabSize+1, 128,  mask_zero=True))
model.add(LSTM(128, return_sequences=True))
# model.add(Dropout(0.1))
model.add(TimeDistributed(Dense(4)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
        optimizer='rmsprop', # or sgd
        #optimizer='sgd', # or sgd
        metrics=['accuracy'])
print(model.summary())

hist = model.fit(X_train, Y_train, nb_epoch=5, validation_data=(X_valid, Y_valid))
print(hist.history)
model.save('_model.h5')
