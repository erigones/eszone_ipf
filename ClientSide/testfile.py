from sys import argv
from os import path
from requests import get, put, post, delete

URL = 'http://127.0.0.1:8000/api_ipf/'
method = argv[1]

print(get(''.join([URL, 'test/'])).text)

if method in ['post','get', 'put', 'delete']:

    try:
        file_path = argv[2]
        file_name = path.basename(file_path)
        url = ''.join([URL, 'config/', file_name, '/'])
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
                print(put(url, files={'title':(file_name,''),
                                      'logfile':(file_name, f.read())}).text)
        except Exception as e:
            print(e)

    elif method == 'delete':
        try:
            delete(url)
        except Exception as e:
            print(e)
    else:
        url = ''.join([URL,'config/'])
        try:
            with open(file_path, 'r') as f:
                print(post(url, files={'title':(file_name,''),
                                       'logfile':(file_name, f.read())}).text)
        except Exception as e:
            print(e)

elif method == 'all':
    url = ''.join([URL,'config/'])
    print(get(url).text)