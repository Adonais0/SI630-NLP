#library from http://blog.csdn.net/u013719780/article/details/78388056
import csv
row_list = []
with open('train.tsv') as tsvfile:
  reader = csv.reader(tsvfile, delimiter='\t')
  for row in reader:
    row_list.append(row)

positive_list = []
negative_list = []
for row in row_list:
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

#shape is dimension of tuple or array
def train(l_dic, p_dic, n_dic, smothing_alpha = 5):
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

a = train(large_dict, positive_dict, negative_dict)
print(a)
a3 = 0
a2 = 0
a1 = 0
for i in a.keys():
    if len(a[i])==3:
        a3 += 1
    elif len(a[i])==2:
        a2 += 1
    else:
        a1 += 1
print("a3: "+str(a3))
print("a2: "+str(a2))
print("a1: "+str(a1))
def classify(px, py, pxy):#calculat pyx
    pyx = (py*pxy)/(py)
