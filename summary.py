import article
import math
import os
import numpy as np

def calsim(line1, line2):
    innerPro = 0
    len1 = 0
    len2 = 0
      
    for i in range(len(line1)):
        if line1[i] == 0.0 or line2[i] == 0.0:
            innerPro += 0
        else:
            innerPro += line1[i] * line2[i]
        len1 += line1[i] * line1[i]
        len2 += line2[i] * line2[i]
    return innerPro / (np.sqrt(len1) * np.sqrt(len2) + 1)
    
   # return len(line1)

'''
def calscore(unsel, sel, lamb):
    score = 0
    score1 = 0
    redundancy = 0
    for i in unsel:
        for j in sel:
            score1 += calsim(i,j)
    score1 = lamb * score1
    for i in sel:
        for j in sel:
            if i != j:
                redundancy += calsim(i,j)
    redundancy += (1 - lamb) * redundancy
    score = score1 - redundancy
    return score
'''

def deltaScore(sen, unsel, sel ,lamb, p, index, tokenlist):
    score = 0
    red = 0
    for i in unsel:
        score += calsim(sen,i)
    score = lamb * score
    for i in sel:
        red += calsim(i, sen)
    return (score - red) / math.pow(len(tokenlist[index]), p)

def getSummary(inputDir, maxlen, lamb, p):
    senlist, toklist, senvec = article.processCluster(inputDir)
    chosen = [0 for i in range(len(senlist))]
    lenth = 0
    while(True):
        for i in range(len(senlist)):
            maxId = ""
            maxInc = -1000000
            if not chosen[i] and lenth + len(toklist[i]) < maxlen:
                selected = [senvec[k] for k in range(len(chosen)) if chosen[k] == 1]
                chosen[i] = 1
                unselected = [senvec[k] for k in range(len(chosen)) if chosen[k] == 0]
                chosen[i] = 0
                inc = deltaScore(senvec[i], unselected, selected, lamb, p, i, toklist)
                if inc > maxInc:
                    maxInc = inc
                    maxId = i
        if maxId == "":
            break
        chosen[maxId] = 1
        lenth += len(toklist[maxId])
        if lenth > maxlen:
            break
    return (chosen, senlist)

def printSummary(inputDir, maxlen, lamb, p, outputDir):
    chosed, senlist = getSummary(inputDir, maxlen, lamb, p)
    summ = ""
    for i in range(len(chosed)):
        if chosed[i]:
            summ += senlist[i] + " "
    with open(outputDir, 'w') as fw:
        fw.write(summ)

if __name__ == '__main__':
    inputDir = 'data/cv/docs/d307b'
    maxlen = 250
    lamb = 0.7
    p = 1
    outputDir = inputDir.split('/')[-1]
    printSummary(inputDir, maxlen, lamb, p, outputDir)



