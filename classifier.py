#OpenDaylight_Controller    not sure about all these nulls<comma> would at least add TODO for refactoring   [TodoComment]   opendaylight/md-sal/sal-dom-broker/src/main/java/org/opendaylight/controller/sal/dom/broker/ConsumerContextImpl.java+refs-changes-63-8463-5 58

import sys
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
import sys
import nltk
nltk.download('punkt')

from change_from_gumtree import changeFromGumTree
#Vaadin     "Javadoc is missing actual explanation of what \""responsive layout capabilities\"" means. "    [JavadocType]   server/src/com/vaadin/server/Responsive.java+refs-changes-63-2863-1 23

reload(sys)
sys.setdefaultencoding('utf8')

#check_family_map.txt
threshold_dict=make_dictionary('sim_vals_correct.txt')
threshold_arg=float(sys.argv[1])
for x,y in threshold_dict.iteritems():
    threshold_dict[x]=threshold_arg

num_keywords=15
num_close_matches=1
missing_files=file_opener.myopen('missing_files.txt','w+')

check_family_dict={}
def make_check_family_dict():
    check_fam_file=file_opener.myopen("check_family_map.txt",'r')
    for line in check_fam_file:
        check=line.split('\t')[0].rstrip()
        family=line.split('\t')[1].rstrip()
        check_family_dict[check]=family

make_check_family_dict()

def median(lst):
    return numpy.median(numpy.array(lst))

dictionary = corpora.Dictionary.load('all_comm.dict')
corpus = corpora.MmCorpus('bow_corpus.mm')
dictionary_dict=dict(dictionary.items())

accuracy_list=[]
tfidf = models.TfidfModel(corpus) #  initialize a model
op_tfidf_warn={}
all_comm=[]
all_warning=[]
CSDesc=[]
CSWarn=[]
check_unsplitted_split_dict={}
# with file_opener.myopen('/Users/xxx/Desktop/notes/CSDescriptions.txt') as CSFile:
#     for line in CSFile:
#         CSDesc.append(line.split('\t')[1])
#         CSWarn.append(line.split('\t')[0])

repeated_comm_warn=[]

# with file_opener.myopen('sorted_correct.txt','r') as qual_comm:#all_info_comm_insuff_desc_added_Vaadin
with file_opener.myopen('new_oracle.txt','r') as qual_comm:

    for line in qual_comm:
        # line=preprocess_SWy.preprocess(line)
        line=line.rstrip()
       
        all_comm.append(line)


# with file_opener.myopen('repeated_comm_qual_insuff_added.txt') as repeated_comm:   #NEED TO REVERT AFTER CHANGING FILE
line_count=0
with file_opener.myopen('new_oracle.txt','r') as repeated_comm:#final,  all_info_oracle
    for line in repeated_comm:
        line=line.strip()
        repeated_comm_warn.append(line)

warning_file=open('warning_result.txt','w')

extra_desc_list=[]

warning_acc_dict={}
# print 'repeated_comm_warn',repeated_comm_warn
comments_size=len(all_comm)
window_size=comments_size/50
matched=0.0

incorrect_match_file=file_opener.myopen('incorrect_match_file.txt','w+')
with open('num_comments.txt','r')as num_comments_file:
    line_count=int(num_comments_file.readline().replace('\n',''))

for shuffle_ind in range(1):
    # shuffle(all_comm)
    Javadoc_Comments=0
    for fold_i in range(line_count):#,911,531,574,#586,480,260 with non-repeating comments, no extra info added of where comment is present
        file_name=all_comm[fold_i].split('\t')[3]
        if file_name=='no_file':
            continue
        print '### fold ',fold_i
        # train=[]
        test=[]
        test.append(all_comm[fold_i])
        test_data=test[0]
        # train=all_comm.pop(fold_i)
        warn_comm_dict={}
        # print 'test ',test
        train=[x for x in all_comm if (x not in test)]
        # print 'train ',train
        # print 'train ',train
        
        
        for i in range(767+line_count):#767,768,655 #(len(repeated_comm_warn)):
            # print train[i]
            if(repeated_comm_warn[i] in test):
                continue
            comment=repeated_comm_warn[i].split('\t')[1]
            comment=preprocess_SWy.preprocess(comment)
            warning=repeated_comm_warn[i].split('\t')[2]
            # warning=preprocess_SWy.preprocess(warning)
            warning=warning.replace('[','')
            warning=warning.replace(']','')
            if(warning=="not_related_to_checkstyle" or warning=="NA"):
                continue
            if (warning in warn_comm_dict):
                warn_comm_dict[warning]=warn_comm_dict[warning] + ' | ' + comment
            else:
                 warn_comm_dict[warning]=comment

        matched=0.0
        # print 'warn_comm_dict',warn_comm_dict
        # for group_key,group_comment in warn_comm_dict.iteritems():
            # print 'group key=',group_key
        for i in range(len(test)):
            cs_warning_for_refinement=""
            possible_right_warnings=[]
            preprocess_SWy.preprocessed_splitted_cs_warning_for_refinement=[]
            splitted_test=test[i].split('\t')
            file_name=splitted_test[3]
            full_file=file_name
            split_file_name=file_name.split('/')
            file_name=split_file_name[len(split_file_name)-1]
            project_name=splitted_test[0]
            # cs_file_loc= findloc(project_name,full_file.strip())

            # if cs_file_loc=='no':
            #     cs_file_loc='/Users/xxx/Desktop/own_code_extraction/consolidated/'+file_name
            cs_file_loc="cs_op/"+file_name+".java.txt"
            print('trying to open '+cs_file_loc)
            if os.path.isfile(cs_file_loc):
                with file_opener.myopen(cs_file_loc,'r') as cs_op_file:
                    try:
                        print 'file opened', cs_file_loc
                        for line in cs_op_file:
                            if (not '[' in line):
                                continue
                            # print 'line in cs_op_file',line
                            splitted_line=line.split(" ")
                            error_info=splitted_line[1]
                            # if(len(error_info.split(':'))<1):
                            #     continue
                            line_num=error_info.split(':')[1]
                            line_num_gerrit_comm=splitted_test[4]
                            # print 'line_num_gerrit_comm',line_num_gerrit_comm
                            if(abs(int(line_num) - int(line_num_gerrit_comm))>0):#4
                                continue
                            print 'error_info ',error_info
                            print 'line_num in cs_op',line_num
                            cs_warning_for_refinement=splitted_line[len(splitted_line)-1]
                            print 'cs_warning_for_refinement',cs_warning_for_refinement
                            cs_warning_for_refinement=cs_warning_for_refinement.replace('\n','')
                            cs_warning_for_refinement=cs_warning_for_refinement.replace('[','')
                            cs_warning_for_refinement=cs_warning_for_refinement.replace(']','')
                            possible_right_warnings.append(cs_warning_for_refinement)
                            splitted_cs_warning_for_refinement=re.sub('([a-z])([A-Z])', r'\1 \2', cs_warning_for_refinement).split()
                            cs_warning_for_refinement=' '.join(splitted_cs_warning_for_refinement)
                            preprocess_SWy.preprocessed_cs_warning_for_refinement=preprocess_SWy.preprocess(cs_warning_for_refinement)
                            preprocess_SWy.preprocessed_splitted_cs_warning_for_refinement=preprocess_SWy.preprocessed_cs_warning_for_refinement.split()
                            print 'cs_warning_for_refinement',cs_warning_for_refinement
                            # add cs_warning_for_refinement to comment only if the 2 checks from same family. ok for now
                            #Also multiple warnings in same line. code for that
                    except Exception as e:
                        print 'exception while reading cs file',e

                    
            else:
                print 'checkstyle op file not present',cs_file_loc
                full_file_name=file_name#+'.txt'
                missing_files.write(full_file_name)
                missing_files.write('\n')
            
            print 'test data= ',test[i]
            test_comm=test[i].split('\t')[1]
            
            # print 'test_comm before processing',test_comm
            test_comm=preprocess_SWy.preprocess(test_comm)
            test_comm=test_comm.replace('$','')#!!!!!!!
            test_warn=test[i].split('\t')[2]
            test_warn=test_warn.rstrip()
            test_warn=test_warn.replace('[','')
            test_warn=test_warn.replace(']','')
            if (test_warn in check_family_dict):
                if(check_family_dict[test_warn]=='Javadoc_Comments'):
                     Javadoc_Comments+=1
           
            test_comm=test_comm
            sim_val_warn_list=[]
            groupTFIDF_warn_list=[]
            
            print 'possible right checks for this comment= '
            for x in possible_right_warnings:
                print x
            print 'test_warn',test_warn
            if test_warn in possible_right_warnings:
                
                print 'test_warn in possible_right_warnings'
            else:
                print 'test_warn not in possible_right_warnings'

            
            # test_warn=preprocess_SWy.preprocess(test_warn)
            test_comm_bow=dictionary.doc2bow(test_comm.split())   
            test_comm_tfidf=tfidf[test_comm_bow]
            # print 'test_comm'
            for x,y in test_comm_tfidf:
                    if len(dictionary_dict[x])==1 and dictionary_dict[x].isalpha():
                        test_comm_tfidf=[(a,b) for (a,b) in test_comm_tfidf if (a,b)!=(x,y)]
           
            for x,y in test_comm_tfidf:
                    if dictionary_dict[x] in preprocess_SWy.preprocessed_splitted_cs_warning_for_refinement:
                            print dictionary_dict[x], 'in splitted_cs_warning_for_refinement'
                            test_comm_tfidf[test_comm_tfidf.index((x,y))]=(x,1)  
           
            # print 'test comm bow= ',test_comm_bow
            test_comm_tfidf.sort(key=lambda tup:tup[1], reverse=True)
            # if(len(test_comm_tfidf)>num_keywords):
            #     test_comm_tfidf=test_comm_tfidf[:num_keywords]        
            groupTFIDF_warn_list={}
            for group_key,group_comment in warn_comm_dict.iteritems():
            #     print 'group key=',group_key

                # group_comment=warn_comm_dict[group_key]
                # group_comment=group_comment.replace(test_comm,'')
                # print 'group comment= ',group_comment
                # group_comment=group_comment.replace('$','')
                new_group_key=group_key.replace('[','')
                new_group_key=new_group_key.replace(']','')
                splitted_check=re.sub('([a-z])([A-Z])', r'\1 \2', new_group_key).split()
                for x in splitted_check:
                    if x.lower() in settings_SWy.stoplist:
                        splitted_check[splitted_check.index(x)]=x+'$'
                # print 'splitted check b4 process',splitted_check
                splitted_check_str=' '.join(splitted_check)
                # print 'splitted_check_str=',splitted_check_str
                processed_splitted_check=preprocess_SWy.preprocess(splitted_check_str)

                # print processed_splitted_check,'processed_splitted_check'
                processed_splitted_check=processed_splitted_check.replace('$','')
                processed_splitted_check=processed_splitted_check.split()
                for blah in processed_splitted_check:
                 # if blah not in stoplist:######!!!!!!!!!!!!!!
                    group_comment=group_comment+' '+blah
                group_comment_bow=dictionary.doc2bow(group_comment.split())  
                group_comment_tfidf=tfidf[group_comment_bow]

                for x,y in group_comment_tfidf:
                    # if dictionary_dict[x] in processed_splitted_check:
                    #     # if dictionary_dict[x].lower() not in stoplist :
                    #     #     # print dictionary_dict[x],' in splitted check',new_group_key,' in stoplist'

                    #         group_comment_tfidf[group_comment_tfidf.index((x,y))]=(x,1)  
                    if dictionary_dict[x]=='|':
                         group_comment_tfidf=[(a,b) for (a,b) in group_comment_tfidf if (a,b)!=(x,y)]
                for x,y in group_comment_tfidf:
                    if len(dictionary_dict[x])==1 and dictionary_dict[x].isalpha():
                        # print 'len 1 b4 remove',  dictionary_dict[x] 
                        # del group_comment_tfidf[group_comment_tfidf.index((x,y))]   
                        # group_comment_tfidf.remove((x,y))
                        group_comment_tfidf=[(a,b) for (a,b) in group_comment_tfidf if (a,b)!=(x,y)]
                    

                # for x,y in group_comment_tfidf:
                    # if len(dictionary_dict[x])==1:
                    #     print 'len 1 after remove',  dictionary_dict[x]        
                group_comment_tfidf.sort(key=lambda tup:tup[1], reverse=True)
                # if(len(group_comment_tfidf)>num_keywords):
                #     group_comment_tfidf=group_comment_tfidf[:num_keywords]
                
                
                 
                # print 'splitted check ', group_key
                # for x in splitted_check:
                #     print x,
                splitted_check_bow=dictionary.doc2bow(splitted_check)  
                splitted_check_tfidf=tfidf[splitted_check_bow]
                # group_comment_tfidf  = group_comment_tfidf +  splitted_check_bow   
                
                # print 'group_comment_tfidf= ',   group_comment_tfidf    
                # print 'splitted check bow'                                                                   
                # print group_key, group_comment, group_comment_tfidf
                # sim_val=cosine_sim(test_comm_tfidf,group_comment_tfidf)
                sim_val=cosine_sim(test_comm_tfidf,group_comment_tfidf)
                sim_val_warn_list.append((sim_val,group_key))
               
                groupTFIDF_warn_list[group_key]=group_comment_tfidf
                # print 'keyword from group ',group_key, 'gr comm', group_comment
                # for x,y in group_comment_tfidf:
                #     print dictionary_dict[x],'>',y,
            
            sim_val_warn_list.sort(key=lambda x:x[0], reverse=True)
            # print 'sim_val_warn ',sim_val_warn_list
            matched_warning=[]
            # print '\n'
            warning_matched_b4_CS=""
            for j in range(num_close_matches):
                # print '|test comment= ', test_comm, 

                # print '|test warning= ', test_warn,
                # print 'sim_val_warn_list[j][1]',sim_val_warn_list[j][1]
                # print '|matched comment= ',warn_comm_dict[sim_val_warn_list[j][1]] ,
                warning_matched_b4_CS=sim_val_warn_list[j][1]
                print '\n|matched warning before using checkstyle = ', warning_matched_b4_CS, 
                real_warning_matched_b4_CS=warning_matched_b4_CS
                
                # print '|max similarity val= ',sim_val_warn_list[j][0]
                matched_warning.append(sim_val_warn_list[j][1].rstrip())

                ## if matched warning and 

                # print 'test comment tfidf keywords= ', test_comm_tfidf
                # print 'group comment tfidf keywords= ', group_comment_tfidf

                # print 'keywords from test'
                # for item in test_comm_tfidf:
                    # print dictionary_dict[item[0]] , 'tfidf-score ',item[1]
                # print 'keywords from train'
                # for item in groupTFIDF_warn_list[sim_val_warn_list[j][1]]:
                    # print dictionary_dict[item[0]] ,'tfidf-score ',item[1]
            # change comment appending checkstyle error if from same family, possible right warnings are already stored only if from same line`
            # print '\n'
            warning_matched_b4_CS=warning_matched_b4_CS.replace('[','')
            warning_matched_b4_CS=warning_matched_b4_CS.replace(']','')


            # print 'warning_matched_b4_CS',warning_matched_b4_CS
            warn_after_using_cs=warning_matched_b4_CS
            CS_warn_added_test_comm=test_comm
            if(1==1):# if (warning_matched_b4_CS in check_family_dict):
                warning_common_words_count_dict={}
                for indiv_possible_right_warnings in possible_right_warnings:
                    indiv_possible_right_warnings=indiv_possible_right_warnings.replace('[','')
                    indiv_possible_right_warnings=indiv_possible_right_warnings.replace(']','')
                    # print 'indiv_possible_right_warnings',indiv_possible_right_warnings
                    splitted_indiv_possible_right_warnings=re.sub('([a-z])([A-Z])', r'\1 \2', indiv_possible_right_warnings).split()
                    #check if there are common words in possible right warning and warning b4 use of CS. If so, add possible right warning to comment
                    splitted_warning_matched_b4_CS=re.sub('([a-z])([A-Z])', r'\1 \2', warning_matched_b4_CS).split()
                    common_words_set=set(splitted_warning_matched_b4_CS) & set(splitted_indiv_possible_right_warnings)
                    # print splitted_warning_matched_b4_CS,'splitted_warning_matched_b4_CS'
                    # print splitted_indiv_possible_right_warnings,'splitted_indiv_possible_right_warnings'
                    common_words_present=len(common_words_set)

                    # print 'common_words_present',common_words_present
                    if(1==1):# if (indiv_possible_right_warnings in check_family_dict):
                        if(common_words_present>=1):
                            matched_warning.append(indiv_possible_right_warnings)
                            warning_common_words_count_dict[indiv_possible_right_warnings]=common_words_present
                # for x in warning_common_words_count_dict.iteritems():
                #     print x
                common_words_count=1
                count_list=[]
                for x,y in warning_common_words_count_dict.iteritems():
                    print 'common words count'
                    print x,y
                    count_list.append(y)
                    if (y>=common_words_count):
                        common_words_count=y
                        warn_after_using_cs=x
            #     if (len(set(count_list))!=len(count_list)):
            #         if(set(count_list)!={0}):
            #             print 'multiple prospective warnings share common word'            
                
            # print 'after using CS op\n'
            for j in range(num_close_matches):
                warning_matched_b4_CS=""
                print test[i]
                print '|cs op added test comment= ', "NA", 
                print '|test warning= ', test_warn
                # print '|matched comment= ',warn_comm_dict[sim_val_warn_list[j][1]] ,
                warning_matched_b4_CS=warn_after_using_cs#sim_val_warn_list[j][1]
                print 'comparision:','threshold',threshold_arg,'similarity',sim_val_warn_list[j][0]
                if(warn_after_using_cs.strip() in threshold_dict):
                    print 'sim_val_warn_list[j][0]<float(threshold_dict[warn_after_using_cs.strip()])',sim_val_warn_list[j][0],float(threshold_dict[warn_after_using_cs.strip()])
                    # if(sim_val_warn_list[j][0]<float(threshold_dict[warn_after_using_cs.strip()])):
                    res_from_gumtree=''
                    if(float(threshold_arg) >sim_val_warn_list[j][0]):
                    # if(1==1):

                        print('usename... sim lt threshold')
                        if(changeFromGumTree(test_data) !=''):
                            res_from_gumtree=changeFromGumTree(test_data)
                            print('usename... change extracted from gumtree')

                        if (res_from_gumtree==''):
                            warn_after_using_cs='not_related_to_checkstyle'
                            print('usename... no res from gumtree')
                        else:
                            warn_after_using_cs=res_from_gumtree

                            print('gumtree got warning '+warn_after_using_cs)
                        print 'sim_val less than threshold','matched to',warn_after_using_cs,
                print '\n|matched warning  = ', warn_after_using_cs,#warning_matched_b4_CS,
                if (test_warn.strip() == warn_after_using_cs.strip()):
                    print 'match is found',
                
                print '|max similarity val= ',sim_val_warn_list[j][0]
                # matched_warning.append(sim_val_warn_list[j][1].rstrip()) #actual line. correct. may need to uncomment
                matched_warning.append(warn_after_using_cs);

                # if(warning_matched_b4_CS!=real_warning_matched_b4_CS):
                #     print 'warning matched changed after use of CS'

                

                # print 'keywords from test'
                # for item in test_comm_tfidf:
                #     print dictionary_dict[item[0]] , 'tfidf-score ',item[1]
                # print 'keywords from train'
                # for item in groupTFIDF_warn_list[sim_val_warn_list[j][1]]:
                #     print dictionary_dict[item[0]] ,'tfidf-score ',item[1]

                
                ########

                matched_warning=warn_after_using_cs
            # if (test_warn in matched_warning):
            print 'flag:','test_warn',test_warn , 'matched_warning',matched_warning
            warning_file.write(matched_warning+'\n')
            
            if (test_warn.strip() == matched_warning.strip()):
                matched+=1
                print 'match found'
                if(test_warn in warning_acc_dict):
                    warning_acc_dict[test_warn].append(1)
                else:
                    warning_acc_dict[test_warn]=[1]
            else:
                # if os.path.isfile(cs_file_loc):
                    # incorrect_match_file.write('cs_file=y')
                # else:
                    # incorrect_match_file.write('cs_file=n')
                # line_from_oracle="line from oracle \t"+test[i]+"\t"
                # incorrect_match_file.write(line_from_oracle)
                # op_test_warn='test warning= '+test_warn
                # incorrect_match_file.write(op_test_warn)
               
                # incorrect_match_file.write(str(fold_i))
                # incorrect_match_file.write('\t')
                # incorrect_match_file.write(full_file)
                # incorrect_match_file.write('\t')
                # incorrect_match_file.write(line_num_gerrit_comm)
                # incorrect_match_file.write('\t')
                # incorrect_match_file.write(test_warn)
                # incorrect_match_file.write('\t')
                # incorrect_match_file.write(test_comm)
                # incorrect_match_file.write('\t')
                op_matched_warn='matched warning= '+ sim_val_warn_list[j][1]+" "+matched_warning #sim_val_warn_list[j][1]
                # incorrect_match_file.write(op_matched_warn)
                # incorrect_match_file.write('\t')
                # incorrect_match_file.write(str(sim_val_warn_list[j][0]))
                # incorrect_match_file.write('\t')
                # incorrect_match_file.write(' '.join(possible_right_warnings))


                # op_test_com='test comment=  '+test_comm
                # incorrect_match_file.write(op_test_com)
                # incorrect_match_file.write('\t')
                # op_test_com_modified='test comment after CS =  '+CS_warn_added_test_comm
                # incorrect_match_file.write(op_test_com_modified)
                # incorrect_match_file.write('\t')
                # op_matched_com='matched comment= '+warn_comm_dict[sim_val_warn_list[j][1]]
                # incorrect_match_file.write(op_matched_com)
                # incorrect_match_file.write('\t')
                # op_test_key='test keyword= '+' '.join([dictionary_dict[x] for x,y in test_comm_tfidf] ) 
                # incorrect_match_file.write(op_test_key)
                # incorrect_match_file.write('\t')
                # op_matched_com_key='matched comment keywords= '+' '.join([dictionary_dict[x] for x,y in groupTFIDF_warn_list[sim_val_warn_list[j][1]]] ) 
                # incorrect_match_file.write(op_matched_com_key)
                incorrect_match_file.write('\n')
                print 'match not found'
                if(test_warn in warning_acc_dict):
                    warning_acc_dict[test_warn].append(0)
                else:
                    warning_acc_dict[test_warn]=[0]
            

            print '\n---'
            
        
        accuracy=matched/len(test)
        accuracy*=100
        accuracy_list.append(accuracy)
        print '### fold ',fold_i, 'accuracy ',accuracy
print 'accuracy= ',accuracy_list
print 'average acc ', sum(accuracy_list)/len(accuracy_list)
print 'minimum acc ', min(accuracy_list)
print 'maximum acc ', max(accuracy_list)
print 'median acc', median(accuracy_list)

# for x,y in warn_comm_dict.iteritems():
#     print x,y

with file_opener.myopen('group_tfidf.txt','w+') as op_file:
    for key,val in op_tfidf_warn.iteritems():
        op_file.write(key)
        op_file.write('\t')
        op_file.write(val)
        op_file.write('\n')
        # print 'written'

for x,y in warning_acc_dict.iteritems():
    # ac=100*sum(warning_acc_dict[x])/float(len(warning_acc_dict[x]))
    ac=100*sum(y)/float(len(y))
    print x,'\t',len(y),'\t',ac
warning_file.close()

# for x,y in dictionary_dict.iteritems():
#     print x,y

# for x,y in check_family_dict.iteritems():
#     print x,y


# print '# of Javadoc_Comments warnings',Javadoc_Comments







