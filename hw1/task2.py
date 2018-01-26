import csv
import math
import numpy as np
from numpy import exp
import pandas as pd
from sklearn.metrics import f1_score
import re
import codecs
from collections import Counter
from scipy.sparse import csr_matrix


row_list = []
with codecs.open('train.tsv',"r", encoding = 'utf-8',errors = 'ignore') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  next(reader, None)
  for row in reader:
    row_list.append(row)

def test_patterns(text, pattern):
    pattern=re.compile(pattern)
    st = " ".join(pattern.findall(text))
    return st

word_list = []
score_list =[]
sentence_list = word_list
list_of_words = []
original_score_list = []
predicted_score_list = []
for row in row_list:
    word_list.append(row[1])
    score_list.append(row[2])

big_string = "".join(word_list)
lower_big_string = big_string.lower()
cleaned_string = test_patterns(lower_big_string,'([a-zA-Z]*)')

def count_words(words):
    dic = {}
    for word in words:
        if word not in dic:
            dic[word] = 1
        else:
            dic[word] += 1
    return (dic)

large_dict = count_words(cleaned_string.split())
list_cleaned_sentence = []
for sentence in sentence_list:
    sentence = sentence.lower()
    cleaned_sentence = test_patterns(sentence,'([a-zA-Z]*)')
    list_cleaned_sentence.append(cleaned_sentence)

#==========BUILD MATRIX===========
indptr = [0]
indices = []
data = []
vocabulary = {}
for sentence in list_cleaned_sentence:
    for term in sentence.split():
        index = vocabulary.setdefault(term, len(vocabulary))
        indices.append(index)
        data.append(1)
    indptr.append(len(indices))
X = csr_matrix((data, indices, indptr), dtype=int).toarray()
lst=[]
for score in score_list:
    lst.append(int(float(score)))
score_array = np.array(lst)
# print(X)
#===================================

#print(large_dict)

sigmoid = np.vectorize(lambda x: 1 / (1 + math.exp(-x)))
a = np.array([[1,2,3,3,5],[1,2,3,4,5]])

#vfunc([1, 2, 3, 4], 2) 针对array进行同时运算
theta = np.zeros((58693,))
# print(X.shape)
# print(theta.shape)
# print(score_array.shape)

def log_likelihood(theta,X,y):
    ll = 0
    for i in range(len(y)):
        ll+=y[i]*np.dot(theta.T,X[i])-math.log(1 + math.exp(np.dot(theta.T,X[i])))
        print(i)
    return ll

def compute_gradient(alpha,i,X,Y):
    global theta
    Y_predict = sigmoid(np.dot(theta.T, X[i]))
    theta = theta + alpha*np.dot((Y-Y_predict)[i],X[i])

def logistic_regression(X,Y,learning_rate,num_step):
    global theta
    # X = X.stack(np.ones(35603),axis = 1)#ADD intercept coefficient
    for i in range(num_step):
        compute_gradient(learning_rate,i,X,Y)#should be 300,000
        print(i)
        print(log_likelihood(theta,X,Y))

logistic_regression(X,score_array,5e-5, 300)
def predict(X):
    for X[i]:

# ========NEED TO ADD BIAS TERM TO X=========
