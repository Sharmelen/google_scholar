import pymysql
import scholarly
from urllib.request import Request, urlopen
import re
import random
import hashlib

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and password as mentioned in variable 'connection'


ai = ['"neural networks"','"data mining"','CNN','RNN','SVM',
      '"reinforcement learning"', '"recommender system"','Computational Design']

security = ['Antivirus','firewall','"cyber Security"','"network Security"','"information Security"',
            '"computer Security"','"cyber threats"','"web Security"']

publication = ['RAID','ACM','CSS','IEEE','ACSAC','NDSS','DSN','USENIX','KDD','ESORICS','IEEE','WWW','DIMWA']

comb = [[i,j,k] for i in ai
                for j in security
                for k in publication]

d = []

for m in range (len(comb)):
    d.append(comb[m])

print(len(d))

count1 = 1


print(d[count1])


word = '{} {} source:{} "Deep Learning" OR AI OR ML OR "Machine Learning"'.format(d[count1][1],d[count1][0],d[count1][2])


print(word)
search_query = scholarly.search_pubs_query(word)
print(search_query)

data = []

for x in range(100):
    try:
        papers = next(search_query)
        data.append(papers)
        print(papers.bib['title'])

    except:
        continue



