import csv
import math
from sklearn.metrics import f1_score

row_list = []
with open('train.tsv') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    row_list.append(row)

positive_list = []
negative_list = []
score_list =[]
original_score_list = []
predicted_score_list = []
for row in row_list:
    score_list.append(row[2])
    if row[2] == "0":
        positive_list.append(row)
    elif row[2] == "1":
        negative_list.append(row)

list_of_ps = []
list_of_ns = []

for lst in positive_list:
    list_of_ps.append(lst[1])
for lst in negative_list:
    list_of_ns.append(lst[1])

positive_big_string = "".join(list_of_ps)
negative_big_string = "".join(list_of_ns)

positive_bag_of_words = positive_big_string.split()
negative_bag_of_words = negative_big_string.split()
TOTAL = len(positive_bag_of_words)+len(negative_bag_of_words)

p_y_positive = len(positive_list)/len(row_list)
p_y_negative = len(negative_list)/len(row_list)

def count_words(words):
    dic = {}
    for word in words:
        if word not in dic:
            dic[word] = 1
        else:
            dic[word] += 1
    return (dic)

positive_dict = count_words(positive_bag_of_words)
negative_dict = count_words(negative_bag_of_words)
large_dict = count_words((positive_big_string+negative_big_string).split())

#turn string into words
def tokenize(string):
    list_of_words = string.split()
    return list_of_words

#==========WRITE BETTER TOKENIZE FUNCTION==============
#def better_tokenize

#shape is dimension of tuple or array

alpha = 1
def train(l_dic, p_dic, n_dic, smothing_alpha = alpha):
    out_dict = {}
    p_x_y_pdict = {}
    p_x_y_ndict = {}
    for word in l_dic.keys():
        out_dict[word] = []
        pxi = large_dict[word]/TOTAL
        out_dict[word].append(pxi)

    for word in p_dic.keys():
        p_x_y_positive = ((p_dic[word]+smothing_alpha)/(len(positive_bag_of_words)+len(negative_bag_of_words)+smothing_alpha))/p_y_positive
        p_x_y_pdict[word] = p_x_y_positive
        out_dict[word].append(p_x_y_positive)

    for word in l_dic.keys():
        if word not in p_x_y_pdict:
            p_x_y_positive = ((0+smothing_alpha)/(len(positive_bag_of_words)+len(negative_bag_of_words)+smothing_alpha))/p_y_positive
            out_dict[word].append(p_x_y_positive)

    for word in n_dic.keys():
        p_x_y_negative = ((n_dic[word]+smothing_alpha)/(len(positive_bag_of_words)+len(negative_bag_of_words)+smothing_alpha))/p_y_negative
        p_x_y_ndict[word] = p_x_y_negative
        out_dict[word].append(p_x_y_negative)

    for word in l_dic.keys():
        if word not in p_x_y_ndict:
            p_x_y_negative = ((0+smothing_alpha)/(len(positive_bag_of_words)+len(negative_bag_of_words)+smothing_alpha))/p_y_negative
            out_dict[word].append(p_x_y_negative)
    return out_dict
out_dict = train(large_dict, positive_dict, negative_dict)

def classify(px_total, p_x_y_positive, p_x_y_negative):#calculat pyx
    p_y_x_positive = (p_y_positive*p_x_y_positive)/(p_y_positive*p_x_y_positive+p_y_negative*p_x_y_negative)
    p_y_x_negative = 1-p_y_x_positive
    return (p_y_x_positive, p_y_x_negative)

#==========COMPARE PERFORMACE=================
for row in row_list:
    list_of_sentence_words = row[1].split()
    p_y_x_stnce_positive = 0
    p_y_x_stnce_negative = 0
    for word in list_of_sentence_words:
        try:
             p_y_x_stnce_positive = p_y_x_stnce_positive + math.log(classify(out_dict[word][0],out_dict[word][1],out_dict[word][2])[0])
             p_y_x_stnce_negative = p_y_x_stnce_negative +  math.log(classify(out_dict[word][0],out_dict[word][1],out_dict[word][2])[1])
        except:
            pass
    if p_y_x_stnce_positive < p_y_x_stnce_negative:
        p_score = 1
    else:
        p_score = 0
    predicted_score_list.append(p_score)

# print(type(predicted_score_list[0]))

for i in score_list:
    try:
        i = int(float(i))
        original_score_list.append(i)
    except:
        pass

print(len(original_score_list))
print(len(predicted_score_list))
f1 = f1_score(original_score_list, predicted_score_list[1:], average='macro')
print(f1)
