import os
from json import dumps, loads
from sys import argv
from subprocess import Popen
from requests import get, put, post, delete

version = 'v1'
IP = '10.10.10.10'
port = '8000'
URL = 'http://{}:{}/{}/api_ipf/'.format(IP, port, version)
editor = '/usr/bin/vim'


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
        self.form = 'ipf'

    def show(self):
        """
        Method that prints content of a requested configuration file.

        Linux method print(get(self.url).text).
        For Solaris is used pretty_print function.
        """
        try:
            pretty_print(get(self.url)) 
        except Exception as e:
            print(e)

    def create(self):
        """
        Method that request file creation with a specific title and form.
        """
        try:
            self.form = raw_input('form(ipf/ipf6/ipnat/ippool)? ')
            with open(self.path, 'r') as f:
                files={'title': (self.title, ''), 'form': (self.form, ''),
                       'directory': (self.title, f.read())}
            pretty_print(post(self.URL, files=files))
        except Exception as e:
            print(e)

    def download(self):
        """
        Method that downloads copy of a requested configuration file.
        """
        try:
            response = get(self.url)
            with open(self.path, 'wb') as f:
                for line in response.text[1:-1].split('\\n'):
                    f.write(line + '\n')
            print('Status: {} '.format(response.status_code)),
            
            if os.stat(self.path).st_size != 0:
                print('Downloaded.')
            else:
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
                files={'title': (self.title, ''),
                       'directory': (self.title, f.read())}
            pretty_print(put(self.url, files=files))
        except Exception as e:
            print(e)

    def remove(self):
        """
        Method that requests delete of a specific configuration file.
        """
        try:
            pretty_print(delete(self.url)) 
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
            self.update()
        except Exception as e:
            print(e)

    def activate(self):
        """
        Method that requests activation of a specific configuration file.
        """
        try:
            pretty_print(get(''.join([self.URL, 'activate/', self.title, '/'])))
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
            pretty_print(get(self.url))
        except Exception as e:
            print(e)

    def create(self):
        """
        Method that request log creation with a specific title.
        """
        try:
            pretty_print(post(self.URL, data={'title': self.title}))
        except Exception as e:
            print(e)

    def remove(self):
        """
        Method that requests delete of a specific log.
        """
        try:
            pretty_print(delete(self.url))            
        except Exception as e:
            print(e)


def JSON_print(JSONresponse):
    """
    Function that takes JSON response from server response and translates it
    into more readable form.
    """
    print('Status: {}'.format(JSONresponse.status_code))
    print dumps(loads(JSONresponse.text), indent=4)


def pretty_print(response):
    """
    Function that takes string response from server respose and
    translates '/n' characters.
    """
    print('Status: {}'.format(response.status_code)),
    
    if len(response.text) >= 80:
        print('')
    
    for line in response.text[1:-1].split('\\n'):
        print(line)


try:
    if argv[1] == 'config':
        try:
            handler = ConfigHandler(argv[3])
            handler.func[argv[2]]()
        except IndexError:
            # show all configuration files
            try:
                if argv[2] in ['show', 'get', 'post', 'put', 'delete', 'modify']:
                    print('Function needs an argument.')
                else:
                    print('Error: Unknown command.')
            except IndexError:
                JSON_print(get(''.join([URL, 'config/'])))
        except Exception as e:
            print(e)

    elif argv[1] == 'log':
        try:
            handler = LogHandler(argv[3])
            handler.func[argv[2]]()
        except IndexError:
            # show all logs
            try:
                if argv[2] in ['show', 'post', 'delete']:
                    print('Function needs an argument.')
                else:
                    print('Error: Unknown command.')
            except IndexError:
                JSON_print(get(''.join([URL, 'log/'])))
        except Exception as e:
            print(e)

    elif argv[1] == 'update':
        # update IP blacklist
        pretty_print(get(''.join([URL, 'update/'])))

    elif argv[1] in ['enable', 'disable', 'restart', 'refresh']:
        # enable, disable, restart or refresh IPFilter
        try:
            pretty_print(get(''.join([URL, 'svcadm/{}/'.format(argv[1])])))
        except Exception as e:
            print(e)

    elif argv[1] in ['ipf', 'ipnat', 'ippool', 'ipmon']:
        # other IPFilter basic commands
        try:
            if argv[2]:
                pretty_print(
                    get(''.join([URL, argv[1], '/', ' '.join(argv[2:]), '/'])))
        except IndexError as e:
            print('{} needs argument.'.format(argv[1]))
        except Exception as e:
            print(e)

    elif argv[1] == 'ipfstat':
        # ipfstat is separated due to workability without arguments
        try:
            if argv[2]:
                pretty_print(
                    get(''.join([URL, argv[1], '/', ' '.join(argv[2:]), '/'])))
        except IndexError as e:
            pretty_print(get(''.join([URL, argv[1], '/'])))
        except Exception as e:
            print(e)

    elif argv[1] == 'help':
        with open('usage', 'r') as f:
            print(f.read())
    
    else:
        print('Error: Unknown command.\nUse help by running with "help" argument')

except Exception as e:
    print e
