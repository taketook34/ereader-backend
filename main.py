import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
soup = BeautifulSoup()
book = epub.read_epub('Worth_the_Candle.epub')
book.get_metadata('DC', 'coverage')

