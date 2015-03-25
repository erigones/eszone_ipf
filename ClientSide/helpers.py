from requests import get

URL = 'http://127.0.0.1:8000/api_ipf/'
editor = '/usr/bin/vim.tiny'

def help():
    print('Soon.')

def test():
    try:
        print get(''.join([URL,'test/'])).text
    except Exception as e:
        print(e)

def ipf_stat(arg):
    try:
        if arg:
            print get(''.join([URL, 'stats/', arg, '/'])).text
        else:
            print ''.join([URL, 'stats/'])
            #print get(''.join([URL, 'stats/'])).text
    except Exception as e:
        print(e)