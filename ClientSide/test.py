from requests import get
from settings import URL

url = URL+'test/'

def simple_test():
   print get(url).text
