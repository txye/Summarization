# Summarization
## data
存放cv和train数据  
cv和train里面，docs里为输入的多文档集合(已去除标签)，model里为对应每个文档集合的ground truth， headline为对应每篇文档的headline（从原来的<HEADLINE>或<HEAD>标签里提取出来的）  
## article.py  
整合cluster里面的文章，过滤一些乱七八糟的符号，去掉多余空格，然后进行分句，再计算每一句的向量（tf-isf，使用sklearn里面计算tfidf的包）  
## getSummary.py  
主要利用了SubModular的方法进行摘要  



