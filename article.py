import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer

senlist = None    #the list of sentence of the article cluster
toklist = None    #the list of sentence after tokenlizing

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
    senlist = []
    toklist = []
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
    vectorizer = TfidfVectorizer(stop_words='english')
    toklist = vectorizer.fit_transform(senlist)
    #for s in senlist:
    #    toklist.append(s.split(' '))
    
    #toklist = vectorizer.inverse_transform(toklist)
    toklist = toklist.toarray()
    #print list(toklist[1])
    '''
    with open("test",'w') as fw:
        fw.write(str(len(senlist)))
        fw.write('\n')
       # fw.write(str(len(toklist)) + '\n')        
        fw.write(str(toklist) + '\n')
    '''
    return (senlist, toklist)
    
#if __name__ == '__main__':
 #   processCluster('data/cv/docs/d307b')


