from sys import argv
from os import remove, stat
from os.path import basename
from subprocess import Popen
from requests import get, put, post, delete

version = 'v1'
URL = 'http://192.168.0.104:8000/{0}/api_ipf/'.format(version)
editor = '/usr/bin/vim.tiny'
help='''
IPF firewall @MikuskaTomas

Usage:
    -h | --help
    config [[show, get, put, post, delete, modify] [file_path]]
    log [[show, post, delete] [file_title]]
    ipf [start, stop]
    ipfstat [valid ipfstat params]
    ipnat [valid ipnat params]
    ippool [valid ippool params]
    ipmon [valid ipmon params]
'''


class ConfigHandler():

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
        self.title = basename(self.path)
        self.url = ''.join([self.URL, self.title, '/'])
        self.type = 'ipf'

    def activate(self):
        if self.type in ['ipf', 'nat']:
            return(raw_input('activate(Y/N)? '))

    def show_one(self):
        try:
            print get(self.url).text
        except Exception as e:
            print(e)

    def create(self):
        try:
            with open(self.path, 'r') as f:
                self.type = raw_input('type(ipf/nat/ippool)? ')
                print(post(self.URL,
                           files={'title':     (self.title, ''),
                                  'type':      (self.type, ''),
                                  'activate':  (self.activate(), ''),
                                  'directory': (self.title, f.read())}).text)
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
                          files={'title':     (self.title, ''),
                                 'activate':  (self.activate(), ''),
                                 'directory': (self.title, f.read())}).text)
        except Exception as e:
            print(e)

    def remove(self):
        try:
            print(delete(self.url).text)
        except Exception as e:
            print(e)

    def modify(self):
        try:
            self.download()
            Popen([editor, self.path]).wait()
            self.upload()
        except Exception as e:
            print(e)


class LogHandler():

    def __init__(self, title):
        self.URL = ''.join([URL, 'log/'])
        self.title = title
        self.func = {
            'show':   self.show_one,
            'post':   self.create,
            'delete': self.remove}
        self.url = ''.join([self.URL, self.title, '/'])

    def show_one(self):
        try:
            print get(self.url).text
        except Exception as e:
            print(e)

    def create(self):
        try:
            print(post(self.URL, data={'title':self.title}).text)
        except Exception as e:
            print(e)

    def remove(self):
        try:
            print(delete(self.url).status_code)
        except Exception as e:
            print(e)


try:
    if argv[1] == 'config':
        try:
            handler = ConfigHandler(argv[3])
            handler.func[argv[2]]()
        except IndexError:
            print(get(''.join([URL, 'config/'])).text)
        except Exception as e:
            print(e)

    elif argv[1] == 'log':
        try:
            handler = LogHandler(argv[3])
            handler.func[argv[2]]()
        except IndexError:
            print(get(''.join([URL, 'log/'])).text)
        except Exception as e:
            print(e)

    elif argv[1] in ['enable', 'disable', 'restart', 'refresh', 'status']:
        try:
            status = get(''.join([URL, 'command/', 'svcs ipfilter | tail -n 1 |'
                                                   ' cut -d " " -f1/'])).text
            if argv[1] == 'status':
                print(status)
            elif argv[1] == 'enable' and status == 'online':
                print('Firewall is already enabled.')
            elif argv[1] == 'disable' and status == 'disabled':
                print('Firewall is already disabled.')
            else:
                get(''.join(
                    [URL, 'command/svcadm {} ipfilter/'.format(argv[1])]))
        except Exception as e:
            print(e)

    elif argv[1] in ['ipf', 'ipfstat', 'ipnat', 'ippool', 'ipmon']:
        try:
            print get(''.join([URL, 'command/', ' '.join(argv[1:]), '/'])).text
        except Exception as e:
            print(e)

    elif argv[1] in ['-h', '--help']:
        print help

    else:
        print('Error: Unknown command.\nUse help by running with -h or --help')

except Exception as e:
    print e, help