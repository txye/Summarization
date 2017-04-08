import os
import re

def preprocess():
    dirlist = os.listdir("docs")
    for d in dirlist:
        if d == ".DS_Store":
            continue
        filelist = os.listdir("docs/" + d)
        for fil in filelist:
            with open("docs/" + d + '/' + fil) as f:
                text = f.read()
                if '<TEXT>' in text:
                    res_tr = r'<TEXT>(.*?)</TEXT>'
                    m_tr = re.findall(res_tr,text,re.S|re.M)
                    text = m_tr[0]
                if "<P>" in text:
                    text = text.replace('<P>','')
                if '</P>' in text:
                    text = text.replace('</P>','')
                if(not os.path.exists("newdocs/" + d)):
                    os.makedirs("newdocs/" + d)
                with open("newdocs/" + d + '/' + fil, 'a') as fw:
                    fw.write(text)
if __name__ == '__main__':
    preprocess()
