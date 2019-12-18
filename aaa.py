import pymysql
import scholarly
from urllib.request import Request, urlopen
import re
import random

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and password as mentioned in variable 'connection'
connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

ai = ['robotics','technology','CRM','machine learning','neural networks','data mining','internet of things','artificial intelligence',
                  'Deep Learning','reinforcement learning','computer vision', 'Natural language processing', 'recommender system', 'Algorithm Game Theory',
                  'Computational Design']
security = ['Antivirus','Anti_Virus','firewall','cyber','network','internet','information','computer'
                        'it','network firewall', 'data','cryptography','cyber threats','web']

comb = [[i,j] for i in ai
              for j in security]

d = []

for m in range (len(comb)):
    d.append(comb[m])
print(len(d))
const = ' Security "Artificial Intelligence" OR AI OR "Machine Learning"'
count1 = 5
word = d[count1][0] + " " + d[count1][1] + const
print(word)
search_query = scholarly.search_pubs_query(word)

data = []
for x in range(10):
    papers = next(search_query)
    data.append(papers)
    print(x)

try:
    with connection.cursor() as cursor:
        print('connected')
        for y in range(len(data)):
            print(y)

            title = (data[y].bib['title'])
            abstract = (data[y].bib['abstract'])
            author = (data[y].bib['author'])
            url = (data[y].bib['url'])
            try:
                citedby = data[y].citedby
            except:
                citedby = 0
            print("citations", citedby)
            split_auth = author.split(' and ')
            size_auth = len(split_auth)
            print(title)

            print("url",url)

            # get year
            try:
                req = Request(data[y].url_scholarbib, headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                new_webpage = str(webpage)
                split_year = new_webpage.split()
                constraint = re.sub('[^0-9]', '', new_webpage)
                year = constraint[:4]
            except:
                year = random.randint(1997, 2014)

            q_insert_keyword = "INSERT INTO keyword (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM keyword WHERE name = %s)"
            rows = cursor.execute(q_insert_keyword, (d[count1][0], d[count1][0]))
            keyword_id = connection.insert_id()
            # if id == 0, duplicate
            print("keyword read", keyword_id)


            q_insert_keyword = "INSERT INTO keyword (name) SELECT %s WHERE NOT EXISTS (SELECT name FROM keyword WHERE name = %s)"
            rows = cursor.execute(q_insert_keyword, (d[count1][1], d[count1][1]))
            keyword_id = connection.insert_id()
            # if id == 0, duplicate
            print("keyword read", keyword_id)


            q_insert_paper = "INSERT IGNORE INTO papers (title,year,keyword,citation,url,abstract,author_count) VALUES (%s,%s,%s,%s,%s,%s,%s);"
            cursor.execute(q_insert_paper, (title, year, word, citedby, url, abstract, size_auth))
            paper_id = connection.insert_id()
            # if paper == 0, duplicate
            print("paper read", paper_id)

            # If there is duplicate, insert only new search term relationship (if new search term)
            if paper_id == 0 and keyword_id != 0:
                # Insert keyword relationship
                q_insert_keyword_paper = "INSERT INTO keyword_paper (paper_id, keyword_id) VALUES (%s, %s);"
                cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id))
                print("inserting relationship p-k")

            # Else if new paper = insert authors and all relationship
            elif paper_id != 0:
                print("paper new id", paper_id)

                # Get duplicate keyword_id
                # q_duplicate_keyword = "SELECT id FROM keyword WHERE name = %s;"
                # cursor.execute(q_duplicate_keyword, word)
                # keyword_id = cursor.fetchone()['id']
                # print("keyword paper id", keyword_id)

                # Insert keyword relationship
                q_insert_keyword_paper = "INSERT INTO keyword_paper (paper_id, keyword_id) VALUES (%s, %s);"
                cursor.execute(q_insert_keyword_paper, (paper_id, keyword_id))
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
                        print("author duplicate id", keyword_id)

                    # Insert author-paper
                    q_insert_author_paper = "INSERT INTO author_paper (paper_id, author_id) VALUES (%s,%s)"
                    cursor.execute(q_insert_author_paper, (paper_id, author_id))
                    print('new author', paper_id, author_id)
            else:
                print("do nothing")

    connection.commit()

except pymysql.err.InternalError as e:
    print('{}'.format(e))
