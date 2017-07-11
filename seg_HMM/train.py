
class train:
    trainSet = []
    trainSetSize = 0

    posHeadProb = {}
    posTransProb = {}
    posToWordProb = {}

    posHeadFreq = {}
    posTransFreq = {}
    posToWordFreq = {}

    posSum = {}

    def __init__(self,trainSet):
        self.trainSet = trainSet
        self.trainSetSize = len(trainSet)

        self.posHeadFreq['sum'] = 0


    def insertPosHeadFreq(self,pos):
        self.posHeadFreq['sum'] += 1
        if pos in self.posHeadFreq:
            self.posHeadFreq[pos] += 1
        else:
            self.posHeadFreq[pos] = 1



    def insertPosTransFreq(self,prepos,pos):
        if prepos in self.posTransFreq:
            self.posTransFreq[prepos]['sum'] += 1
            if pos in self.posTransFreq[prepos]:
                self.posTransFreq[prepos][pos] += 1
            else:
                self.posTransFreq[prepos][pos] = 1
        else:
            self.posTransFreq[prepos] = {}
            self.posTransFreq[prepos]['sum'] = 1
            self.posTransFreq[prepos][pos] = 1

    def insertPosToWordFreq(self,pos,word):
        if pos in self.posToWordFreq:
            self.posToWordFreq[pos]['sum'] += 1
            if word in self.posToWordFreq[pos]:
                self.posToWordFreq[pos][word] += 1
            else:
                self.posToWordFreq[pos][word] = 1
        else:
            self.posToWordFreq[pos] = {}
            self.posToWordFreq[pos]['sum'] = 1
            self.posToWordFreq[pos][word] = 1

    def getPosToWordProb(self,pos,word):
        if word in self.posToWordProb[pos]:
            return self.posToWordProb[pos][word]
        else:
            return 0


    def train(self):
        print('taining..............')
        i = 1
        for line in self.trainSet:
            print('training..............', i, '/', len(self.trainSet))
            i += 1

            line = line.strip().split()
            prepos = ''
            index = -1
            for pairs in line:
                pairs = pairs.split('/')
                word = pairs[0]
                pos = pairs[1]
                index += 1
                if index == 0:
                    self.insertPosHeadFreq(pos)
                else:
                    self.insertPosTransFreq(prepos,pos)
                self.insertPosToWordFreq(pos,word)
                prepos = pos
        for pos,freq in self.posHeadFreq.items():
            if pos != 'sum':
                self.posHeadProb[pos] = 1.0*freq/self.posHeadFreq['sum']

        for prepos,dic in self.posTransFreq.items():
            self.posTransProb[prepos] = {}
            for pos,freq in dic.items():
                if pos != 'sum':
                    self.posTransProb[prepos][pos] = 1.0*freq/dic['sum']

        for pos,dic in self.posToWordFreq.items():
            self.posToWordProb[pos] = {}
            for word,freq in dic.items():
                if word != 'sum':
                    self.posToWordProb[pos][word] = 1.0*freq/dic['sum']

        return