import numpy as np
import matplotlib.pyplot as plt

import sys
reload(sys)
sys.setdefaultencoding('utf8')

sys.path.insert(0, r'modules')
import os.path
import re
import math
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
from collections import defaultdict
from random import shuffle
import numpy
import settings_SWy
import file_opener

import preprocess_SWy
from cosine_similarity import cosine_sim
from make_dictionary import make_dictionary
from find_loc import findloc
import nltk
nltk.download('punkt')

dictionary = corpora.Dictionary.load('all_comm.dict')
corpus = corpora.MmCorpus('bow_corpus.mm')
tfidf = models.TfidfModel(corpus)


#group warn:comments dict

dict_warn_comments={}
with open('../sim_between_warns/oracle_couchbase.txt')as ip:
	for line in ip:
		line = line.encode('utf-8', 'ignore').decode('utf-8')
		splitted=line.split('\t')
		warn=splitted[2]
		comm=splitted[1]
		comm=preprocess_SWy.preprocess(comm)
		if warn not in dict_warn_comments:
			dict_warn_comments[warn]=comm
		else:
			dict_warn_comments[warn]=dict_warn_comments[warn] + ' | '+ comm +' '
list_warn_bow=[]
for x,y in dict_warn_comments.iteritems():
	comment_bow=dictionary.doc2bow(y.split())  
	# print(x,tfidf[comment_bow])
	list_warn_bow.append((x,tfidf[comment_bow]))

# for x in list_warn_bow:
# 	print(x)


check_family_map=make_dictionary('check_family_map.txt')
# print(check_family_map)

count=0
mat=[]
for i in range(len(list_warn_bow)):
	count+=1
	# print("checking warn ",list_warn_bow[i][0])
	sim_list=[]
	max_sim=0
	sim_warn=""
	row=[]
	for j in range(len(list_warn_bow)):

		sim=cosine_sim(list_warn_bow[i][1],list_warn_bow[j][1])
		if sim>max_sim and list_warn_bow[i][0]!=list_warn_bow[j][0] :
			max_sim=sim
			sim_warn=list_warn_bow[j][0]
			
			# if check_family_map[list_warn_bow[i][0].replace('[','').replace(']','')]==check_family_map[list_warn_bow[j][0].replace('[','').replace(']','')]:
				
			# 	# print('same_family')
			# 	pass
		# print(list_warn_bow[j][0]+" "+str(sim)),
		row.append(round(sim,2))
	mat.append(row)

data=[]
for i in range(len(mat)):
	for j in range(len(mat)):
		if j<i:
			print(mat[i][j]),
			data.append(mat[i][j])			

fig1, ax1 = plt.subplots()
ax1.set_title('Warning similarity in Couchbase')

ax1.boxplot(data)
plt.show()

