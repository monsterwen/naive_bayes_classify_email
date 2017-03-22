# -*- coding: utf-8 -*-
'''Name: Menglan Wen. NetID: mxw163130
this is the naive_bayes implementation,which is used to classify emails into ham or spam. It will print out the classification accuracy with/wo stopwords'''
import numpy as np
import os
import io
import math


stop_words_list=[]
'''this function return a word dictionary where the key is the word, the value is the occurence of each word
input training sets path, return dictionary of words, all words of ham/spam are stored in each dictionary'''
def prepare_word(path):

    files=os.listdir(path)
    s=[]
    word_dict={}
    num_files=0
    cond_prob_ham=0
    cond_prob_apam=0

    for file in files:
        num_files+=1
        if not os.path.isdir(file):
            f=io.open(path+"/"+file,encoding="ISO_8859_1")
            iter_f= iter(f)
            for line in iter_f:
                currentline=line.split()
                for a in currentline:
                    a.encode('UTF-8')
                    s.append(a)
    for word in s:
        if word not in word_dict:
            word_dict[word]=1
        else:
            word_dict[word]=word_dict[word]+1

    return word_dict,num_files
'''input: a word(from test file). Output: the conditional probability of the word'''
def calculate_cond(word):
    cond_prob_ham=0
    cond_prob_spam=0
    if word not in word_dict_ham:
        cond_prob_ham=math.log10(float(1)/(sum(word_dict_ham.values())+len(word_dict_ham.keys())+len(word_dict_spam.keys())))
    else:
        cond_prob_ham=math.log10(float((word_dict_ham[word])+1)/(sum(word_dict_ham.values())+len(word_dict_ham.keys())+len(word_dict_spam.keys())))
    if word not in word_dict_spam:
        cond_prob_spam=math.log10(float(1)/(sum(word_dict_spam.values())+len(word_dict_ham.keys())+len(word_dict_spam.keys())))
    else:
        cond_prob_spam=math.log10(float(word_dict_spam[word]+1)/(sum(word_dict_spam.values())+len(word_dict_ham.keys())+len(word_dict_spam.keys())))

    '''this will return a two element list containing two probabilities'''

    return cond_prob_ham,cond_prob_spam

def calculate_cond_wo_stop(word):
    cond_prob_ham=0
    cond_prob_spam=0
    if word not in ham_dict_wostop:
        cond_prob_ham=math.log10(float(1)/(sum(ham_dict_wostop.values())+len(ham_dict_wostop.keys())+len(spam_dict_wostop.keys())))
    else:
        cond_prob_ham=math.log10(float((ham_dict_wostop[word])+1)/(sum(ham_dict_wostop.values())+len(ham_dict_wostop.keys())+len(spam_dict_wostop.keys())))
    if word not in spam_dict_wostop:
        cond_prob_spam=math.log10(float(1)/(sum(spam_dict_wostop.values())+len(ham_dict_wostop.keys())+len(spam_dict_wostop.keys())))
    else:
        cond_prob_spam=math.log10(float(spam_dict_wostop[word]+1)/(sum(spam_dict_wostop.values())+len(ham_dict_wostop.keys())+len(spam_dict_wostop.keys())))

    '''this will return a two element list containing two probabilities'''

    return cond_prob_ham,cond_prob_spam
'''input: a word list(each file from test file), output: the classlable of the word list/file'''
def classify(word_list,function):
    cond_prob_ham=0
    cond_prob_spam=0
    prob_ham=math.log(float(num_ham)/(num_ham+num_spam))
    prob_spam=math.log(float(num_spam)/(num_ham+num_spam))
    for word in word_list:
        cond_prob_ham+=function(word)[0]
        cond_prob_spam+=function(word)[1]
    total_prob_ham=prob_ham+cond_prob_ham
    total_prob_spam=prob_spam+cond_prob_spam
    if total_prob_spam>total_prob_ham:
        return "spam"
    else:
        return "ham"
    '''input: test folder. output: the number of files are classifies correctly and incorrectly'''
def test(test_folder,stopwordflag):
    correct_counter_ham=0
    wrong_counter_ham=0
    correct_counter_spam=0
    wrong_counter_spam=0
    if "ham" in test_folder:
        ham_files=os.listdir(test_folder)
        for file in ham_files:
            file_str_list=[]
            if not os.path.isdir(file):
                f=io.open(test_folder+"/"+file,encoding="ISO_8859_1")
                iter_f= iter(f)
                for line in iter_f:
                    currentline=line.split()
                    file_str_list=file_str_list+currentline
                new_file_str_list1=[x for x in file_str_list if x not in stop_words_list ]
                if stopwordflag:
                    class_lable=classify(new_file_str_list1,calculate_cond_wo_stop)
                    if class_lable == 'ham':
                        correct_counter_ham+=1
                    else:
                        wrong_counter_ham+=1
                else:
                    class_lable=classify(file_str_list,calculate_cond)
                    if class_lable == 'ham':
                        correct_counter_ham+=1
                    else:
                        wrong_counter_ham+=1
        return correct_counter_ham,wrong_counter_ham
    if "spam" in test_folder:
        spam_files=os.listdir(test_folder)
        for file in spam_files:
            file_str_list=[]
            if not os.path.isdir(file):
                f=io.open(test_folder+"/"+file,encoding="ISO_8859_1")
                iter_f= iter(f)
                for line in iter_f:
                    currentline=line.split()
                    file_str_list=file_str_list+currentline
                new_file_str_list2=[x for x in file_str_list if x not in stop_words_list]
                if stopwordflag:
                    class_lable=classify(new_file_str_list2,calculate_cond_wo_stop)
                    if class_lable == 'spam':
                        correct_counter_spam+=1
                    else:
                        wrong_counter_spam+=1
                else:
                    class_lable=classify(file_str_list,calculate_cond)
                    if class_lable == 'spam':
                        correct_counter_spam+=1
                    else:
                        wrong_counter_spam+=1
        return correct_counter_spam,wrong_counter_spam
def read_stopwords():
    file_name=io.open('stopwords_en.txt',encoding="ISO_8859_1")
    iter_file=iter(file_name)
    for f in iter_file:
        f=f.strip('\n')
        stop_words_list.append(f)
    return stop_words_list
def word_optimize(word_list_map):
    temp_word_list={x:y for x,y in word_list_map.iteritems() if x not in stop_words_list}
    return temp_word_list
if __name__ == "__main__":

    read_stopwords()
    '''word dictionary with stopwords'''
    word_dict_spam,num_spam=prepare_word("train/spam")
    word_dict_ham,num_ham=prepare_word("train/ham")
    '''word dictionary with out stopwords'''
    ham_dict_wostop=word_optimize(word_dict_ham)
    spam_dict_wostop=word_optimize(word_dict_spam)
    '''classify test files with stopwords'''
    ham_counters=test("test/ham",True)
    spam_counters=test("test/spam",True)
    accuracy_wo_stopwords=float(ham_counters[0]+spam_counters[0])/(ham_counters[0]+ham_counters[1]+spam_counters[0]+spam_counters[1])
    '''classfy test files without stopwords'''
    ham_counters=test("test/ham",False)
    spam_counters=test("test/spam",False)
    accuracy_with_stopwords=float(ham_counters[0]+spam_counters[0])/(ham_counters[0]+ham_counters[1]+spam_counters[0]+spam_counters[1])

    print accuracy_with_stopwords,accuracy_wo_stopwords





