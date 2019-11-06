import pymysql
import scholarly

#connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

#try:
    #with connection.cursor() as cursor:

        #sqlQuery = "SELECT title, year FROM papers"
        #cursor.execute(sqlQuery)
        #auth = cursor.fetchall()
        #print(auth)
#except:
    #print('not connected')

word = input('Enter Your Keyword')

search_query = scholarly.search_pubs_query(word)
papers = next(search_query)


for x in range (1):

    title = (papers.bib['title'])
    abstract = (papers.bib['abstract'])
    author = (papers.bib['author'])
    url = (papers.bib['url'])

    cite = (papers.citedby)

    # print(title)
    # print(abstract)
    # print(author)
    # print(url)
    print(cite)
