import pymysql
import scholarly
from urllib.request import Request, urlopen
import re
import requests
import hashlib

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and password as mentioned in variable 'connection'
connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)
# AI keywords
kw = ['"artificial intelligence"','"deep learning"','"machine learning"','"neural network"','"recurrent neural networks"','"support vector machine"',
      '"convolutional neural network"','"decision tree"','"reinforcement learning"',
      '"supervised learning"','"unsupervised learning"','"genetic algorithm"','"k fold"','"neural architecture"']
# Security keywords
# kw = ['antivirus','firewall','"cyber security" OR cybersecurity','"network security"','"internet security"',
#         '"computer security"','"web security"','"intrusion detection"','"anomaly detection"','"iot security"',
#         '"mobile security"','"threat identification"','malware','spyware','ransomware','"data leak prevention"',
#         '"data leak protection"']
publication = ['European Symposium on Research in Computer Security']
pub_type = "Security"
keyword_type = "AI"
pub_src = []
for n in range (len(publication)):
    pub = publication[n]
    src = " source:"
    pub_src.append(src + src.join(pub.split()))

# data
comb_1 = [[i,k] for i in kw
                for k in publication]
d = []
for m in range (len(comb_1)):
    d.append(comb_1[m])
# search
comb_2 = [[i,k] for i in kw
                for k in pub_src]
search = []
for m in range (len(comb_2)):
    search.append(comb_2[m])

print("total combination:"+str(len(d)))
count1 = 0
search_term = "{}{}".format(search[count1][0],search[count1][1])

print("combination of keyword is :" + d[count1][0],d[count1][1])
print("the search term is:" + search_term)
search_query = scholarly.search_pubs_query(search_term)
data = []

for x in range(0):
    try:
        papers = next(search_query)
        data.append(papers)
        print(papers.bib['title'])

    except:
        print('fail')
        continue

# try:
with connection.cursor() as cursor:
    print('connected')
    for y in range(len(data)):
        print(y)

        try:
            bib = data[y].url_scholarbib
        except:
            bib = "None"
        try:
            title = (data[y].bib['title'])
        except:
            title = "None"
        try:
            abstract = (data[y].bib['abstract'])
        except:
            abstract = "None"
        try:
            author = (data[y].bib['author'])
        except:
            author = "None"
        try:
            url = (data[y].bib['url'])
        except:
            url = "None"
        try:
            eprint = (data[y].bib['eprint'])
        except:
            eprint = "None"
        try:
            citedby = data[y].citedby
        except:
            citedby = 0

        print("citations", citedby)

        if '…' in author:
            author = author[0:-1]
        split_auth = author.split(' and ')
        authors=[]
        for y in range(len(split_auth)):
            authors.append(split_auth[y].split(' '))
        size_auth = len(authors)

        print(title)
        print("url",url)

        hash_abs = hashlib.md5(str(str(title)+str(d[count1][1])).encode())
        hash_paper = hash_abs.hexdigest()

        # get year
        try:
            req = Request(bib, headers={'User-Agent': 'Mozilla/5.0'})
            sbib = str(urlopen(req).read())
            start = sbib.find('year={')+len('year={')
            year = sbib[start:-7]
        except:
            year = 0

        q_insert_conference = "INSERT INTO conference (name,type) SELECT %s,%s WHERE NOT EXISTS (SELECT name,type FROM conference WHERE name = %s AND type = %s)"
        rows = cursor.execute(q_insert_conference, (d[count1][1],pub_type, d[count1][1],pub_type))
        conf_id = connection.insert_id()
        # if id == 0, duplicate
        print("conf read", conf_id)

        # if duplicate, get id
        if conf_id == 0:
            q_duplicate_conf = "SELECT id FROM conference WHERE name = %s;"
            cursor.execute(q_duplicate_conf, d[count1][1])
            conf_id = cursor.fetchone()['id']
            print("conf duplicate id", conf_id)

        q_insert_keyword = "INSERT INTO keyword (name,type) SELECT %s,%s WHERE NOT EXISTS (SELECT name,type FROM keyword WHERE name = %s AND type = %s)"
        rows = cursor.execute(q_insert_keyword, (d[count1][0],keyword_type, d[count1][0],keyword_type))
        keyword_id_1 = connection.insert_id()
        # if id == 0, duplicate
        print("keyword 1 read", keyword_id_1)
        if keyword_id_1 == 0:
            # Get duplicate keyword_id
            q_duplicate_keyword = "SELECT id FROM keyword WHERE name = %s;"
            cursor.execute(q_duplicate_keyword, d[count1][0])
            keyword_id_1 = cursor.fetchone()['id']
            print("keyword paper id", keyword_id_1)

        try:
            q_insert_paper = "INSERT IGNORE INTO papers (conference_id, title,year,citation,url,eprint,bibtex,abstract,author_count,hash,date) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,NOW());"
            row_insert = cursor.execute(q_insert_paper, (conf_id, title, year, citedby, url, eprint, bib, abstract, size_auth, hash_paper))
            paper_id = connection.insert_id()
        except:
            row_insert = 0

        print("Row insert", row_insert)
        # if paper == 0, duplicate
        print("paper read", paper_id)

        # If there is duplicate, insert only new keyword relationship
        if row_insert == 0:
            # Get duplicate keyword_id
            q_duplicate_paper = "SELECT id FROM papers WHERE title = %s;"
            cursor.execute(q_duplicate_paper, title)
            paper_id = cursor.fetchone()['id']
            print("paper id", paper_id)
            # Insert keyword relationship
            q_insert_keyword_paper = "INSERT IGNORE INTO keyword_paper (paper_id, keyword_id) VALUES (%s, %s);"
            cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id_1))
            print("inserting relationship p-k 1")

        # Else if new paper = insert authors and all relationship
        elif row_insert != 0:
            print("paper new id", paper_id)

            # Insert keyword relationship
            q_insert_keyword_paper = "INSERT IGNORE INTO keyword_paper (paper_id, keyword_id) VALUES (%s, %s);"
            cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id_1))
            print("inserting relationship p-k")

            # Insert authors table and junction table
            for x in range(size_auth):
                # Insert author
                q_insert_author = "INSERT INTO authors (firstname,lastname) SELECT %s,%s WHERE NOT EXISTS (SELECT firstname,lastname FROM authors WHERE firstname = %s AND lastname = %s)"
                cursor.execute(q_insert_author, (authors[x][0],authors[x][1], authors[x][0],authors[x][1]))
                author_id = connection.insert_id()
                print("author read", author_id)

                # if duplicate, get id
                if author_id == 0:
                    q_duplicate_author = "SELECT id FROM authors WHERE firstname = %s AND lastname = %s;"
                    cursor.execute(q_duplicate_author, (authors[x][0],authors[x][1]))
                    author_id = cursor.fetchone()['id']
                    print("author duplicate id", author_id)

                # Insert author-paper
                q_insert_author_paper = "INSERT IGNORE INTO author_paper (paper_id, author_id) VALUES (%s,%s)"
                cursor.execute(q_insert_author_paper, (paper_id, author_id))
                print('new author', paper_id, author_id)
        else:
            print("do nothing")

connection.commit()

# except pymysql.err.InternalError as e:
#     print('{}'.format(e))
