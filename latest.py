import pymysql
import scholarly
from urllib.request import Request, urlopen
import re
import random
import hashlib

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and password as mentioned in variable 'connection'
connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

ai = ['"neural network"','CNN','RNN','SVM',
      '"reinforcement learning"']
security = ['Antivirus','firewall','"cyber Security"','cybersecurity','"network Security"','"internet Security"',
            '"computer Security"','"web Security"','"intrusion detection"','"anomaly detection"','"iot security"']

publication = ['RAID','"ACM CCS"','"IEEE S&P" ','ACSAC','NDSS','DSN','USENIX','KDD','ESORICS','"INTERNATIONAL WORLD WIDE WEB CONF"','DIMVA']

comb = [[i,j,k] for i in ai
                for j in security
                for k in publication]

d = []
for m in range (len(comb)):
    d.append(comb[m])
print(len(d))

count1 = 0
print(d[count1])

word = '{} {} source:{} "Deep Learning" OR AI OR ML OR "Machine Learning"'.format(d[count1][1],d[count1][0],d[count1][2])
print(word)

search_query = scholarly.search_pubs_query(word)


data = []

for x in range(100):
    try:
        papers = next(search_query)
        data.append(papers)
        print(papers.bib['title'])

    except:
        continue

# try:
with connection.cursor() as cursor:
    print('connected')
    for y in range(len(data)):
        print(y)

        try:
            title = (data[y].bib['title'])
            abstract = (data[y].bib['abstract'])
            author = (data[y].bib['author'])
            url = (data[y].bib['url'])
            citedby = data[y].citedby
        except:
            print("Paper data incomplete")
            continue

        print("citations", citedby)


        split_auth = author.split(' and ')
        size_auth = len(split_auth)
        print(title)

        print("url",url)

        hash_abs = hashlib.md5(str(str(title)+str(size_auth)).encode())
        hash_paper = hash_abs.hexdigest()

        # get year
        try:
            req = Request(data[y].url_scholarbib, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            new_webpage = str(webpage)
            split_year = new_webpage.split()
            constraint = re.sub('[^0-9]', '', new_webpage)
            year = constraint[:4]
        except:
            year = 0

        q_insert_conference = "INSERT INTO conference (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM conference WHERE name = %s)"
        rows = cursor.execute(q_insert_conference, (d[count1][2], d[count1][2]))
        conf_id = connection.insert_id()
        # if id == 0, duplicate
        print("conf read", conf_id)

        # if duplicate, get id
        if conf_id == 0:
            q_duplicate_conf = "SELECT id FROM conference WHERE name = %s;"
            cursor.execute(q_duplicate_conf, d[count1][2])
            conf_id = cursor.fetchone()['id']
            print("conf duplicate id", conf_id)

        q_insert_keyword = "INSERT INTO keyword (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM keyword WHERE name = %s)"
        rows = cursor.execute(q_insert_keyword, (d[count1][0], d[count1][0]))
        keyword_id_1 = connection.insert_id()
        # if id == 0, duplicate
        print("keyword 1 read", keyword_id_1)

        rows = cursor.execute(q_insert_keyword, (d[count1][1], d[count1][1]))
        keyword_id_2 = connection.insert_id()
        # if id == 0, duplicate
        print("keyword 2 read", keyword_id_2)

        try:
            q_insert_paper = "INSERT IGNORE INTO papers (conference_id, title,year,search_term,citation,url,abstract,author_count,hash,date) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,NOW());"
            row_insert = cursor.execute(q_insert_paper, (conf_id, title, year, word, citedby, url, abstract, size_auth, hash_paper))
            paper_id = connection.insert_id()
        except:
            row_insert = 0

        print("Row insert", row_insert)
        # if paper == 0, duplicate
        print("paper read", paper_id)

        # If there is duplicate, insert only new keyword relationship (if new keyword)
        if row_insert == 0:
            # Insert keyword relationship
            q_insert_keyword_paper = "INSERT IGNORE INTO keyword_paper (paper_id, keyword_id) VALUES (%s, %s);"
            if keyword_id_1 != 0:
                cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id_1))
                print("inserting relationship p-k 1")
            if keyword_id_2 != 0:
                cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id_2))
                print("inserting relationship p-k 2")

        # Else if new paper = insert authors and all relationship
        elif row_insert != 0:
            print("paper new id", paper_id)

            # Get duplicate keyword_id
            q_duplicate_keyword = "SELECT id FROM keyword WHERE name = %s;"
            cursor.execute(q_duplicate_keyword, d[count1][0])
            keyword_id_1 = cursor.fetchone()['id']
            print("keyword paper id", keyword_id_1)
            cursor.execute(q_duplicate_keyword, d[count1][1])
            keyword_id_2 = cursor.fetchone()['id']
            print("keyword paper id", keyword_id_2)

            # Insert keyword relationship
            q_insert_keyword_paper = "INSERT IGNORE INTO keyword_paper (paper_id, keyword_id) VALUES (%s, %s);"
            cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id_1))
            print("inserting relationship p-k")
            cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id_2))
            print("inserting relationship p-k")

            # Insert authors table and junction table
            for x in range(size_auth):
                # Insert author
                q_insert_author = "INSERT INTO authors (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM authors WHERE name = %s)"
                cursor.execute(q_insert_author, (split_auth[x], split_auth[x]))
                author_id = connection.insert_id()
                print("author read", author_id)

                # if duplicate, get id
                if author_id == 0:
                    q_duplicate_author = "SELECT id FROM authors WHERE name = %s;"
                    cursor.execute(q_duplicate_author, split_auth[x])
                    author_id = cursor.fetchone()['id']
                    print("author duplicate id", author_id)

                # Insert author-paper
                q_insert_author_paper = "INSERT INTO author_paper (paper_id, author_id) VALUES (%s,%s)"
                cursor.execute(q_insert_author_paper, (paper_id, author_id))
                print('new author', paper_id, author_id)
        else:
            print("do nothing")

connection.commit()

# except pymysql.err.InternalError as e:
#     print('{}'.format(e))
