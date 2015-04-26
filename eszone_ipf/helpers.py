from eszone_ipf.settings import CONF_DIR, LOG_DIR
from os.path import exists
from os import makedirs, remove, rename
from wget import download
import schedule
import time
import zipfile

def check_dirs():
    print('Checking directories.')
    if exists(CONF_DIR):
        print('CONF_DIR.............................................OK')
    else:
        makedirs(CONF_DIR)
        print('CONF_DIR has been created............................OK')

    if exists(LOG_DIR):
        print('LOG_DIR..............................................OK')
    else:
        makedirs(LOG_DIR)
        print('LOG_DIR has been created.............................OK')

def check_config():
    print('Checking configuration files.')
    path = ''.join([CONF_DIR, 'ipf.conf'])
    if exists(path):
        print('ipf.conf.............................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#filter configuration')
        print('ipf.conf has been created............................OK')

    path = ''.join([CONF_DIR, 'ipnat.conf'])
    if exists(path):
        print('ipnat.conf...........................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#NAT configuration')
        print('ipnat.conf has been created..........................OK')

    path = ''.join([CONF_DIR, 'ippool.conf'])
    if exists(path):
        print('ippool.conf..........................................OK')
    else:
        with open(path, 'a') as f:
            f.write('#ippool configuration')
        print('ippool.conf has been created.........................OK')

    print('Startup configuration done.\n')

def upload_blacklist():
    url = 'http://myip.ms/files/blacklist/general/full_blacklist_database.zip'
    dir = '/tmp/'
    zip_file = ''.join([dir, 'blacklist.zip'])
    txt_file = ''.join([dir, 'blacklist.txt'])

    try:
        print('Downloading updates.')
        download(url, zip_file)
    except Exception as e:
        print(e)

    try:
        with zipfile.ZipFile(zip_file, 'r') as file:
            file.extractall(dir)
            rename(''.join([dir, 'full_blacklist_database.txt']), txt_file)
        print('\nUnzip file...........................................OK')
    except Exception as e:
        print(e)

    try:
        with open(txt_file, 'r') as database:
            with open(''.join([CONF_DIR, 'ippool.conf']), 'w') as ippool:
                ippool.write('blacklist role = ipf type = tree number = 1\n{\n')
                for line in database.readlines()[15:]:
                    ippool.write(line.split()[0]+',\n')
                ippool.write('}')
        print('Blacklist update.....................................OK')
    except Exception as e:
        print(e)

    try:
        remove(zip_file)
        remove(txt_file)
    except Exception as e:
        print(e)

def start():
    check_dirs()
    check_config()
    upload_blacklist()
    schedule.every().day.do(upload_blacklist)

    while True:
        schedule.run_pending()
        time.sleep(3600)