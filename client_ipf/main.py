import os
from sys import argv
from subprocess import Popen
from requests import get, put, post, delete

version = 'v1'
IP = '127.0.0.1'
port = '8000'
URL = 'http://{}:{}/{}/api_ipf/'.format(IP, port, version)
editor = '/usr/bin/vim.tiny'
help = '''
IPF firewall @MikuskaTomas

Usage:
    -h | --help
    config [[show, get, put, post, delete, modify] [file_path]]
    log [[show, post, delete] [file_title]]
    state
    ipf [start, stop]
    ipfstat [valid ipfstat params]
    ipnat [valid ipnat params]
    ippool [valid ippool params]
    ipmon [valid ipmon params]
'''


class ConfigHandler():
    """
    A class that operates with a specific configuration file.

    List of accessible methods:
    - show (GET content)
    - create (POST)
    - download (GET content to file)
    - update (PUT)
    - delete (DELETE)
    - modify (GET, change, PUT)
    - activate (activate created file)
    """
    def __init__(self, file_path):
        """
        Initialization method that processes necessary parameters.

        :param file_path: path to the configuration file
        """
        self.URL = ''.join([URL, 'config/'])
        self.path = file_path
        self.func = {
            'show':     self.show,
            'get':      self.download,
            'put':      self.update,
            'post':     self.create,
            'delete':   self.remove,
            'modify':   self.modify,
            'activate': self.activate}
        self.title = os.path.basename(self.path)
        self.url = ''.join([self.URL, self.title, '/'])
        self.type = 'ipf'

    def show(self):
        """
        Method that prints content of a requested configuration file.
        """
        try:
            print get(self.url).text
        except Exception as e:
            print(e)

    def create(self):
        """
        Method that request file creation with a specific title and form.
        """
        try:
            with open(self.path, 'r') as f:
                self.form = raw_input('form(ipf/ipf6/nat/ippool)? ')
                print(post(self.URL,
                           files={'title':     (self.title, ''),
                                  'form':      (self.form, ''),
                                  'directory': (self.title, f.read())}).text)
        except Exception as e:
            print(e)

    def download(self):
        """
        Method that downloads copy of a requested configuration file.
        """
        try:
            with open(self.path, 'w+') as f:
                f.write(get(self.url).text)
            if os.stat(self.path).st_size == 0:
                os.remove(self.path)
                raise Exception('No file.')
        except Exception as e:
            print(e)

    def update(self):
        """
        Method that requests update of a specific configuration file.
        """
        try:
            with open(self.path, 'r') as f:
                print(put(self.url,
                          files={'title':     (self.title, ''),
                                 'directory': (self.title, f.read())}).text)
        except Exception as e:
            print(e)

    def remove(self):
        """
        Method that requests delete of a specific configuration file.
        """
        try:
            print(delete(self.url).text)
        except Exception as e:
            print(e)

    def modify(self):
        """
        Method that firstly downloads a specific configuration file, opens it
        for a rewrite and requests its update.
        """
        try:
            self.download()
            Popen([editor, self.path]).wait()
            self.upload()
        except Exception as e:
            print(e)

    def activate(self):
        """
        Method that requests activation of a specific configuration file.
        """
        try:
            print(get(''.join([self.URL, 'activate/', self.title])).text)
        except Exception as e:
            print(e)


class LogHandler():
    """
    A class that operates with a specific log.

    List of accessible methods:
    - show (GET content)
    - create (POST)
    - delete (DELETE)
    """
    def __init__(self, title):
        self.URL = ''.join([URL, 'log/'])
        self.title = title
        self.func = {
            'show':   self.show,
            'post':   self.create,
            'delete': self.remove}
        self.url = ''.join([self.URL, self.title, '/'])

    def show(self):
        """
        Method that prints content of a requested log.
        """
        try:
            print get(self.url).text
        except Exception as e:
            print(e)

    def create(self):
        """
        Method that request log creation with a specific title.
        """
        try:
            print(post(self.URL, data={'title': self.title}).text)
        except Exception as e:
            print(e)

    def remove(self):
        """
        Method that requests delete of a specific log.
        """
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
            # show all configuration files
            if not argv[2]:
                print(get(''.join([URL, 'config/'])).text)
            else:
                print help
        except Exception as e:
            print(e)

    elif argv[1] == 'log':
        try:
            handler = LogHandler(argv[3])
            handler.func[argv[2]]()
        except IndexError:
            # show all logs
            if not argv[2]:
                print(get(''.join([URL, 'log/'])).text)
            else:
                print help
        except Exception as e:
            print(e)

    elif argv[1] == 'update':
        # update IP blacklist
        get(''.join([URL, 'update/']))

    elif argv[1] in ['enable', 'disable', 'restart', 'refresh', 'state']:
        # enable, disable, restart and refresh IPFilter or get its state
        try:
            state = get(''.join([URL, 'state/'])).text
            if argv[1] == 'state':
                print(state)
            elif argv[1] == 'enable' and state == 'online':
                print('Firewall is already enabled.')
            elif argv[1] == 'disable' and state == 'disabled':
                print('Firewall is already disabled.')
            else:
                get(''.join(
                    [URL, 'command/svcadm {} ipfilter/'.format(argv[1])]))
        except Exception as e:
            print(e)

    elif argv[1] in ['ipf', 'ipfstat', 'ipnat', 'ippool', 'ipmon']:
        # other IPFilter basic commands
        try:
            print get(''.join([URL, ' '.join(argv[1:]), '/'])).text
        except Exception as e:
            print(e)

    elif argv[1] == 'help':
        print help

    else:
        print('Error: Unknown command.\nUse help by running with -h or --help')

except Exception as e:
    print e, help