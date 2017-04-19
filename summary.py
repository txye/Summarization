import article
import math
import os
import math
import cluster
import sent2vec

def calsim(line1, line2):
    innerPro = 0
    len1 = 0
    len2 = 0
      
    for i in range(len(line1)):
        innerPro += line1[i] * line2[i]
        len1 += line1[i] * line1[i]
        len2 += line2[i] * line2[i]
    return innerPro / (math.sqrt(len1) * math.sqrt(len2))
    
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

def deltaScore(simlist,unsel, sel ,lamb, p, index, num):
    score = 0
    red = 0
    for i in unsel:
        score += simlist[index][i]
    score = lamb * score
    for i in sel:
        red += simlist[index][i]
    return (score - red) / math.pow(num[index], p)

def getSummary(inputDir, maxlen, lamb, p):
    senlist, wordnum, toklist = cluster.processCluster(inputDir)
    simlist = sent2vec.sent2vec(inputDir, toklist)
    chosen = [0 for i in range(len(senlist))]
    lenth = 0
    while(True):
        maxId = ''
        maxInc = -1000000
        for i in range(len(senlist)):
            if not chosen[i] and lenth + wordnum[i] < maxlen:
                selected = [k for k in range(len(chosen)) if chosen[k] == 1]
                chosen[i] = 1
                unselected = [k for k in range(len(chosen)) if chosen[k] == 0]
                chosen[i] = 0
                inc = deltaScore(simlist, unselected, selected, lamb, p, i, wordnum)
                if inc > maxInc:
                    maxInc = inc
                    maxId = i
        if maxId == "":
            break
        chosen[maxId] = 1
        lenth += wordnum[maxId]
        if lenth > maxlen:
            break
    return (chosen, senlist)

def printSummary(inputDir, maxlen, lamb, p, outputDir):
    chosed, senlist = getSummary(inputDir, maxlen, lamb, p)
    summ = ""
    for i in range(len(chosed)):
        if chosed[i] == 1:
            summ += senlist[i] + " "
    with open(outputDir, 'w') as fw:
        fw.write(summ)

if __name__ == '__main__':
    rootpath = 'data/test/docs/'
    dirs = os.listdir(rootpath)
    for d in dirs:
        if d == ".DS_Store":
            continue
        inputDir = rootpath + d
        maxlen = 250
        lamb = 0.65
        p = 0.5
        outputDir = "peers/2/" + d[:-1].upper() + ".M.250." + d[-1].upper() + ".6"
        printSummary(inputDir, maxlen, lamb, p, outputDir)
        print d + " cluster solved!"

