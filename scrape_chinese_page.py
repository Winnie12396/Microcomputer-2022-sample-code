import requests
from bs4 import BeautifulSoup

url = "https://travel.ettoday.net/category/%E6%A1%83%E5%9C%92/"
url2 = "https://travel.ettoday.net/category/桃園/"

r = requests.get(url2)
content = r.text
soup = BeautifulSoup(content,'lxml')
tags = soup.find('a')
#for tag in tags:
#    #print(tag.get("href",None))
#    print(tag)
print(type(tags))
print(tags)
    