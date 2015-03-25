from sys import argv
from os import remove, stat
from os.path import basename
from requests import get, put, post, delete
from webbrowser import open as wb_open
from helpers import *

class FileHandler():

    def __init__(self, file_path):
        self.URL = ''.join([URL,'config/'])
        self.path = file_path
        self.func = {
            'show'   : self.show_one,
            'get'    : self.download,
            'put'    : self.upload,
            'post'   : self.create,
            'delete' : self.remove,
            'change' : self.change}
        self.name = basename(self.file_path)
        self.url = ''.join([self.URL, self.name, '/'])

    def show_one(self):
        try:
            print get(self.url).text
        except Exception as e:
            print(e)

    def create(self):
        try:
            with open(self.path, 'r') as f:
                print(post(self.URL,
                           files={'title':(self.name,''),
                                  'logfile':(self.name, f.read())}).text)
        except Exception as e:
            print(e)

    def download(self):
        try:
            with open(self.path, 'w+') as f:
                f.write(get(self.url).text)
            if stat(self.path).st_size == 0:
                remove(self.path)
                raise Exception('No file.')
        except Exception as e:
            print(e)

    def upload(self):
        try:
            with open(self.path, 'r') as f:
                print(put(self.url,
                          files={'title':(self.name,''),
                                 'logfile':(self.name, f.read())}).text)
        except Exception as e:
            print(e)

    def remove(self):
        try:
            delete(self.url)
        except Exception as e:
            print(e)

    def change(self):
        try:
            self.download()
            wb_open(self.path)
            self.upload()
        except Exception as e:
            print(e)

try:
    if argv[1] in ['show', 'get', 'put', 'post', 'delete', 'change']:
        h = FileHandler(argv[2])
        h.func[argv[1]]()

    elif argv[1] == 'all':
        try:
            print get(''.join(URL, 'config/')).text
        except Exception as e:
            print(e)

    elif argv[1] == 'test':
        try:
            print get(''.join([URL, 'test/'])).text
        except Exception as e:
            print(e)

    elif argv[1] == 'stat':
        try:
            print get(''.join([URL, 'stats', argv[2]], '/')).text
        except IndexError:
            print get(''.join([URL, 'stats/'])).text
        except Exception as e:
            print(e)

    elif argv[1] == 'ipf':
        try:
            print put(''.join([URL, 'ipf', argv[2], '/'])).text
        except IndexError:
            print get(''.join([URL, 'ipf/'])).text
        except Exception as e:
            print(e)

except IndexError:
    print('Error: No file entered.')
except Exception as e:
    print(e)