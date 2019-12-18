import scholarly
from itertools import combinations
from urllib.request import Request, urlopen
import re
import pymysql


ai = ['robotics','technology','CRM','machine learning','neural networks','data mining','internet of things','artificial intelligence',
                  'Deep Learning','reinforcement learning','computer vision', 'Natural language processing', 'recommender system', 'Algorithm Game Theory',
                  'Computational Design']
security = ['Antivirus','Anti_Virus','security','firewall','cyber security','network security','internet security','information security','computer security'
                        'it security','network firewall', 'data security','cryptography','cyber threats','web security']


comb = [[i,j] for i in ai
              for j in security]

d = []

for x in range (len(comb)):
    d.append(comb[x])

titles = []
abstracts = []
authors = []
urls = []
years = []

keyword = str(d[0])
print(keyword)
search_query = scholarly.search_pubs_query(keyword)

for z in range(1):

    papers = next(search_query)


    #retrive title
    title = papers.bib['title']
    titles.append(title)

    #retrieve abstract
    abstract = (papers.bib['abstract'])
    abstracts.append(abstract)

    #retrieve author
    author = (papers.bib['author'])
    authors.append(author)

    #retrieve url
    url = (papers.bib['url'])
    urls.append(url)

    #retrieve year
    req = Request(papers.url_scholarbib, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    new_webpage = str(webpage)
    split_year = new_webpage.split()
    constraint = re.sub('[^0-9]', '', new_webpage)
    year = constraint[:4]
    years.append(year)



connection = pymysql.connect(host='37.59.55.185', user='ZejMYc2nXj', port=3306, password='TtEI93o66O', db='ZejMYc2nXj', cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        for x in range (1):

            sqlQuery2 = "Enter suming"

    connection.commit()

except pymysql.err.InternalError as e:
    print('{}'.format(e))




