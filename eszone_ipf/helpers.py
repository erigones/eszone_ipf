from eszone_ipf.settings import CONF_DIR, LOG_DIR
from os.path import exists
from os import makedirs


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