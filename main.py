import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

xhtml_doc = open('worth/Worth the Candle_split_000.xhtml')
soup = BeautifulSoup(xhtml_doc, 'html.parser')
for href in soup.find_all('link'):
    print(href)


