from sys import argv
from os import path
from requests import get, put, post, delete
from settings import URL

method = argv[1]

print(get(''.join(URL, 'test/')).text)

if method in ['post','get', 'put', 'delete']:

    try:
        file_path = argv[2]
        file = path.basename(file_path)
        title,ext = path.splitext(file)
        url = ''.join(URL,'config/', title)
    except IndexError:
        print('No file path.')
        exit(1)

    if method == 'get':
        try:
            with open(file_path, 'wb') as f:
                f.write(get(url).text)
        except Exception as e:
            print(e)

    elif method == 'put':
        try:
            with open(file_path, 'r') as f:
                print(put(url, data={'logfile':(file, f.read)}).text)
        except Exception as e:
            print(e)

    elif method == 'delete':
        try:
            print(delete(url).text)
        except Exception as e:
            print(e)
    else:
        url = ''.join(URL,'config/')
        with open(file_path, 'r') as f:
            r = post(url, data={'title':(title,''), 'logfile':(file, f.read)})
            print(r.text)

elif method == 'get':
    url = ''.join(URL,'config/')
    print(get(url).text)