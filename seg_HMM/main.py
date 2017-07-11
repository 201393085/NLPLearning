import codecs
import random
from train import train
from test import test

if __name__ == '__main__':
    trainSet = []
    testSet = []

    trainFile = codecs.open('train.tag','r',encoding='utf-8')
    testFile = codecs.open('test.tag','r',encoding='utf-8')
    output =     output = codecs.open('output_original.tag','w+','utf-8')


    for line in trainFile:
        line = line.strip()
        r = random.random()
        if r < 0.8:
            trainSet.append(line)
        else:
            testSet.append(line)



    model = train(trainSet)
    model.train()

    solve = test(testSet)
    solve.test(model)
