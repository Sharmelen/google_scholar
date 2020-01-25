#import pymysql
#import scholarly
from urllib.request import Request, urlopen
import re
import random
#import hashlib
import string

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and password as mentioned in variable 'connection'connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

ai = ['"neural network"','RNN','SVM','"convolution network"','""decision tree"','"support vector machine"',
      '"reinforcement learning"','"supervised learning"','"unsupervised learning"','"genetic algorithm"',
      'kfold','k-fold','"k fold"','"neural architecture"']

publication = ['ESORICS','"INTERNATIONAL WORLD WIDE WEB CONF"']

publication_sliced = [['ESORICS'],['INTERNATIONAL','WORLD','WIDE','WEB']]

count1 = 1

comb = [[g,h] for g in ai
                for h in publication]
c = []
for m in range (len(comb)):
    c.append(comb[m])

keyword_1 = c[count1][0]
pub_1 = c[count1][1]


comb_1 = [[i,k] for i in ai
                for k in publication_sliced]

d = []
for m in range (len(comb_1)):
    d.append(comb_1[m])


#print(len(d))

keyword_2 = d[count1][0]
pub = d[count1][1]
#print(len(pub))


if len(pub) > 2 :
    #print(pub)
    app = []
    for y in range (len(pub)):
        add = ''+pub[y]+''
        add_src = 'source:'+add

        app.append(add_src)


else:
    add = ' "'+str(pub)+'"'
    app = 'source:'+add

search = str(app)
symbol = "[']"
symbol_2 = '[],[]'
new_search_1 = re.sub(symbol,'',search)
new_search_2 = re.sub(symbol_2,'',new_search_1)

keyword = str(keyword_1)+" "+str(pub_1)
search_term = "{} {}".format(keyword_2,new_search_2)

print("combination of keyword is :" + keyword)#before entering the keyword into database please change the type to string
print("")
print("the search term is :" +search_term)
