import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.stem import SnowballStemmer


senlist = None    #the list of sentence of the article cluster
toklist = None    #the list of sentence after tokenlizing and stemming
wordnum = None	  #the list of word after tokenlizing
senvec = None     #the vector of sentence

# remove some unecessary signals
def filterDoc(doc):
    doc = doc.replace('\n',' ')
    doc = doc.replace("-LRB-",' ')
    doc = doc.replace("-RRB-",' ')
    doc = doc.replace("-LCB-",' ')
    doc = doc.replace("-RCB-",' ')
    doc = doc.replace("\"",' ')
    doc = doc.replace("_", ' ')
    doc = doc.replace("--",' ')
    doc = doc.replace("''", ' ')
    doc = doc.replace("-",' ')
    doc = doc.replace("`",' ')
    doc = doc.replace("``",' ')
    doc = doc.replace("\t", ' ')
    doc = doc.replace("     ",' ')
    doc = doc.replace("    ",' ')
    doc = doc.replace("   ",' ')
    doc = doc.replace("  ",' ')
    return doc

def processCluster(Dir):
    global senlist
    global toklist
    global senvec
    global wordnum
    senlist = []
    toklist = []
    wordnum = []
    filelist = os.listdir(Dir)
    articles = ""
    for fil in filelist:
        with open(Dir + "/" + fil) as f:
            text = f.read()
            if '<text>' in text:
                res_tr = r'<text>(.*?)</text>'
                m_tr = re.findall(res_tr, text, re.S|re.M)
                text = m_tr[0]
            articles += " " + text
    articles = filterDoc(articles)
    senStart = []
    senEnd = []
    lenth = len(articles)
    isStart = True
    for i in range(lenth):
        if isStart and articles[i] != ' ':
            senStart.append(i)
            isStart = False
        if articles[i] == '.' or articles[i] == '?' or articles[i] == '!':
            senEnd.append(i)
            isStart = True
    for i in range(len(senEnd)):
        senlist.append(articles[senStart[i]:senEnd[i] + 1])
    stemmer = SnowballStemmer("english") 
    for s in senlist:
        wordnum.append(len(s.split(' ')))
    tmplist = []
    siglist = ['.', ':', '?', '!', "'s", '"']
    for s in senlist:
        s = s.lower()
        for sig in siglist:
            s = s.replace(sig, '')
        s = s.split(' ')
        tempsen = [stemmer.stem(w) for w in s]
        toklist.append(tempsen)
    
    #vectorizer = TfidfVectorizer(stop_words='english')
    #senvec = vectorizer.fit_transform(tmplist)
    
    #toklist = vectorizer.inverse_transform(toklist)
    #senvec = senvec.toarray()
    #print list(senvec[1])
    #print len(senvec[1])
    '''
    with open("test",'w') as fw:
        fw.write(str(len(senlist)))
        fw.write('\n')
       # fw.write(str(len(toklist)) + '\n')        
        fw.write(str(toklist) + '\n')
    '''
    return (senlist,wordnum,toklist)
    
#if __name__ == '__main__':
#    processCluster('data/cv/docs/d307b')
