import pymysql
import scholarly
import sys

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and paassword as mentioned in variable 'connection'



connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

word = input('Enter Your Keyword: \n')

search_query = scholarly.search_pubs_query(word)


try:
    with connection.cursor() as cursor:
        print('connected')
        for x in range(2):
            papers = next(search_query)
            title = (papers.bib['title'])
            abstract = (papers.bib['abstract'])
            author = (papers.bib['author'])
            url = (papers.bib['url'])
            #citedby = (papers.bib['citedby'])

            print(title)
            print(abstract)
            print(author)
            print(url)
            #print(citedby)

            split_auth = author.split('and')

            size_auth = len(split_auth);



            try:
                auth1 = split_auth[0]
                auth2 = split_auth[1]
                print(auth1)
                print(auth2)

                for x in range(size_auth):
                    if auth1 and auth2 in split_auth:
                        split_auth.remove(auth1)
                        split_auth.remove(auth2)

            except:
                auth1 = split_auth[0]
                print(auth1)

                for x in range(size_auth):
                    if auth1 in split_auth:
                        split_auth.remove(auth1)


            authors = str(split_auth)
            authors_new = authors.split('['']')


            sqlQuery = "INSERT INTO paper (title,citation,abstract) VALUES (%s,0,%s);"

            cursor.execute(sqlQuery, (title, abstract))

            try:
                sqlQuery2 = "INSERT INTO author (AUTH_1, AUTH_2, AUTH_3_5, AUTH_COUNT ) VALUES (%s,%s,%s,%s);"

                cursor.execute(sqlQuery2, (auth1, auth2, authors_new, size_auth))

            except:
                sqlQuery2 = "INSERT INTO author (AUTH_1, AUTH_2, AUTH_3_5, AUTH_COUNT ) VALUES (%s,'0','0',%s);"

                cursor.execute(sqlQuery2, (auth1, size_auth))


    connection.commit()

except pymysql.err.InternalError as e:
    print('{}'.format(e))


# This section is used to remove redundant data in database once the paper is entered

try:
    with connection.cursor() as cursor_new:

        sqlQuery3 = 'DELETE c1, c3 FROM paper c1 INNER JOIN paper c2 INNER JOIN author c3 WHERE c1.paper_id > c2.paper_id AND c1.title = c2.title AND c1.paper_id =  c3.author_id  ;'

        cursor_new.execute(sqlQuery3)

        connection.commit()

except pymysql.err.InternalError as e:
    print('{}'.format(e))
