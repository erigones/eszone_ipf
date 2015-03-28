from sys import argv
from os import remove, stat
from os.path import basename
from subprocess import Popen
from requests import put, post, delete
from helpers import *


class FileHandler():

    def __init__(self, file_path):
        self.URL = ''.join([URL, 'config/'])
        self.path = file_path
        self.func = {
            'show':   self.show_one,
            'get':    self.download,
            'put':    self.upload,
            'post':   self.create,
            'delete': self.remove,
            'modify': self.modify}
        self.name = basename(self.path)
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
                           files={'title':   (self.name, ''),
                                  'logfile': (self.name, f.read())}).text)
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
                          files={'title':   (self.name, ''),
                                 'logfile': (self.name, f.read())}).text)
        except Exception as e:
            print(e)

    def remove(self):
        try:
            delete(self.url)
        except Exception as e:
            print(e)

    def modify(self):
        try:
            self.download()
            Popen([editor, self.path]).wait()
            self.upload()
        except Exception as e:
            print(e)

try:
    if argv[1] in ['show', 'get', 'put', 'post', 'delete', 'modify']:
        h = FileHandler(argv[2])
        h.func[argv[1]]()

    elif argv[1] == 'all':
        try:
            print get(''.join([URL, 'config/'])).text
        except Exception as e:
            print(e)

    elif argv[1] == 'test':
        try:
            print get(''.join([URL, 'test/'])).text
        except Exception as e:
            print(e)

    elif argv[1] == 'ipf':
        try:
            print get(''.join([URL, ''.join(argv[1:3]), '/'])).text
        except Exception as e:
            print(e)

    elif argv[1] == 'log':
        try:
            print post(''.join([URL, 'log/']), data={'title':argv[2]}).text
        except IndexError:
            print get(''.join([URL, 'log/'])).text
        except Exception as e:
            print(e)

    elif argv[1] in ['ipfstat', 'ipnat', 'ippool', 'ipmon']:
        try:
            print get(''.join([URL, 'command/', ' '.join(argv[1:]), '/'])).text
        except Exception as e:
            print(e)

    else:
        print('Error: Unknown command.')

except IndexError:
    print('Error: No file entered.')
except Exception as e:
    print(e)