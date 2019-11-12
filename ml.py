import pymysql
import scholarly
import sys

# login to this url: https://remotemysql.com/phpmyadmin/sql.php?db=ZejMYc2nXj&table=papers&pos=0
# Use the username and paassword as mentioned in variable 'connecton'



connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

word = input('Enter Your Keyword')

search_query = scholarly.search_pubs_query(word)


try:
    with connection.cursor() as cursor:
        print('connected')
        for x in range(4):
            papers = next(search_query)
            title = (papers.bib['title'])
            abstract = (papers.bib['abstract'])
            author = (papers.bib['author'])
            url = (papers.bib['url'])

            print(title)
            print(abstract)
            print(author)
            print(url)

            sqlQuery = "INSERT INTO papers (title,author,year,keyword,citation,url,abstract,citedby,source) VALUES (%s,%s,2,%s,2,%s,%s,'citedby','source');"

            #sqlQuery = "SELECT title, COUNT(url) FROM papers GROUP BY title HAVING COUNT(url) > 1"

            cursor.execute(sqlQuery, (title,author,word,url,abstract))

    connection.commit()

except pymysql.err.InternalError as e:
    print('{}'.format(e))


# This section is used to remove redundant data in database once the paper is entered

try:
    with connection.cursor() as cursor_new:

        sqlQuery2 = "DELETE c1 FROM papers c1 INNER JOIN papers c2 WHERE c1.id > c2.id AND c1.title = c2.title;"

        cursor_new.execute(sqlQuery2)

        connection.commit()

except pymysql.err.InternalError as e:
    
    print('{}'.format(e))
