import requests
import re
import pymysql

db = pymysql.connect(host = '127.0.0.1',
 user='root',passwd='1581339',db='spider',charset='utf8')
cursor = db.cursor()

def getMovieList(page):
    res = requests.get('https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'.format(page))
    res.encoding = 'gb2312'
    result = res.text
    reg = r'<a href="(.*?)" class="ulink">(.*?)</a>'
    reg = re.compile(reg)
    return re.findall(reg,result)

def getMovieContent(url,title):
    res = requests.get('https://www.dytt8.net{}'.format(url))
    res.encoding = 'gb2312'
    result = res.text
    reg = r'<div class="co_content8">(.*?)<strong>' #.无法识别换行符
    reg = re.compile(reg,re.S) #re.S匹配多行
    try:
        content = re.findall(reg,result)[0]

    except:
        print(title,'出现错误，已忽略')
        return

    sql = "insert into movie(title,content) values('{}','{}')".format(title, content.replace("'", "\\'"))
    print(title,'已保存')
    cursor.execute(sql)
    db.commit()

# def getMovieDownload(url):
#     res = requests.get('https://www.dytt8.net{}'.format(url))
#     res.encoding = 'gb2312'
#     result = res.text
#     reg2 = r'thunderrestitle="(.*?)"kzbpiylr '
#     reg2 = re.compile(reg2)
#     link = re.findall(reg2,result)
#     print(link)
for page in range(1,166):
    for url,title in getMovieList(page):
        getMovieContent(url,title)
        # getMovieDownload(url)

db.close()