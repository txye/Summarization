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
                if '<HEADLINE>' in text:
                    res_tr = r'<HEADLINE>(.*?)</HEADLINE>'
                    m_tr = re.findall(res_tr,text,re.S|re.M)
                    text = m_tr[0]
                elif '<HEAD>' in text:
                    res_tr = r'<HEAD>(.*?)</HEAD>'
                    m_tr = re.findall(res_tr,text,re.S|re.M)
                    text = ""
                    for i in m_tr:
                        text += i + " " 
                else:
                    text = ""
                if(not os.path.exists("headline/" + d)):
                    os.makedirs("headline/" + d)
                with open("headline/" + d + '/' + fil, 'a') as fw:
                    fw.write(text)
if __name__ == '__main__':
    preprocess()
