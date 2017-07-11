
from math import log2
from train import *

class viterbiNode:
    log2Prob = 0
    path = []
    def __init__(self,log2Prob,path):
        self.log2Prob = log2Prob
        self.path = path

class test:
    testSet = []

    def __init__(self,testSet):
        self.testSet = testSet

    def test(self,model):
        print('testing...............')
        correctNum = 0
        sumNum = 0

        i = 1
        for line in self.testSet:
            print('testing...............',i,'/',len(self.testSet))
            i += 1

            path = []
            pathFound = []
            line = line.strip().split()

            index = -1
            prenodes = {}
            nownodes = {}

            for pairs in line:
                index += 1

                pairs = pairs.split('/')
                word = pairs[0]
                pos = pairs[1]
                path.append(pos)
                if index == 0:
                    for pos,prob in model.posHeadProb.items():
                        temp = model.getPosToWordProb(pos,word)
                        temp = float('-Inf') if temp == 0 else log2(temp)
                        temp += log2(prob)
                        nownodes[pos] = viterbiNode(temp,[pos])
                else:
                    for prepos,prenode in prenodes.items():
                        for pos,prob in model.posTransProb[prepos].items():
                            if pos in nownodes:
                                temp = model.getPosToWordProb(pos, word)
                                temp = float('-Inf') if temp == 0 else log2(temp)
                                temp += log2(prob)
                                temp += prenode.log2Prob

                                if temp > nownodes[pos].log2Prob:
                                    nowpath = [i for i in prenode.path]
                                    nowpath.append(pos)
                                    nownodes[pos] = viterbiNode(temp, nowpath)

                            else:
                                temp = model.getPosToWordProb(pos, word)
                                temp = float('-Inf') if temp == 0 else log2(temp)
                                temp += log2(prob)
                                temp += prenode.log2Prob

                                nowpath = [i for i in prenode.path]
                                nowpath.append(pos)
                                nownodes[pos] = viterbiNode(temp,nowpath)
                prenodes = nownodes
                nownodes = {}

            maxLog2Prob = float('-Inf')
            for pos,node in prenodes.items():
                if node.log2Prob >= maxLog2Prob:
                    maxLog2Prob = node.log2Prob
                    pathFound = node.path
            # print(pathFound,'\n',path,'\n',sent)
            if len(path) != len(pathFound):
                print(line)
                print(path)
                print(pathFound)
                print(len(path),' ',len(pathFound))
                print("!!!!!!")
                break
            for ii in range(len(path)):
                if pathFound[ii] == path[ii]:
                    correctNum += 1
                sumNum += 1
        print('correct:',correctNum,' ','sum:',sumNum,' ','rate:',1.0*correctNum/sumNum)
