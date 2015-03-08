from os import path
from sys import argv
from requests import post
from settings import URL
from test import simple_test

simple_test()

try:
    file_path = argv[1]
    file = path.basename(file_path)
    title, ext = path.splitext(file)
    url = URL+'upload/'
except IndexError:
    print('No file path.')
    exit(1)

f = open(file_path, 'r')
data = f.read()

r = post(url, files={'title':(title,''), 'logfile':(file, data)})
print(r.text)

"""
Simple

file = path.basename(argv[1])

r = post(URL+'upload/',
         data={'title':str(path.splitext(file)[0)]},
         files={'docfile':(file, open(argv[1], 'r').read())})
print(r.text)
"""