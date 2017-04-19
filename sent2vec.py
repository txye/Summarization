#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gensim
import os
import numpy as np
import logging
import cluster
import math

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

clsList = None

def sent2vec(Dir,tokenlist):
    #sentlist
    #sentlist = [["one", "child", "in"], ["which", "six", "from"]]
    #s,w,tokenlist = cluster.processCluster(Dir)
    model = gensim.models.Word2Vec.load('vec_model')
    global clsList
    clsList = []
    for sent in tokenlist:
        sentVec = np.zeros(300)
        cnt = 0
        for word in sent:
            sentVec = sentVec + model.wv[word]
            cnt += 1
        sentVec = sentVec/cnt
        #print len(sentVec.tolist())
        clsList.append(sentVec.tolist())
    simList = []
    for i in range(len(clsList)):
        print "calculating sentence " + str(i) + "..."
        clsSim = []
        for j in range(len(clsList)):
            innerPro = 0
            len1 = 0
            len2 = 0
            for k in range(len(clsList[i])):
                innerPro += clsList[i][k] * clsList[j][k]
                len1 += clsList[i][k] * clsList[i][k]
                len2 += clsList[j][k] * clsList[j][k]
            res = innerPro / (math.sqrt(len1) * math.sqrt(len2))
            clsSim.append(res)
        simList.append(clsSim)
    return simList



#if __name__ == "__main__":
 #   sent2vec()	    
