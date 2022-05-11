import logging
# import datetime
import time
import os
import pprint

#dtime = datetime.datetime.now().strftime(r"%H-%M;%Y-%m-%d")
check_time = time.time()
path_ = r"./logs"
file_ = f'logfile_{int(check_time)}.log'


logging.basicConfig(filename=os.path.join(path_,file_),
                    format='%(asctime)s\\%(levelname)s: %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO,
                    filemode="w")

main_log = logging.getLogger("main_log")
module_log = logging.getLogger('module_log')


def info_log(message):
     return main_log.info(f'{message}')

def debug_log(message):
     return main_log.debug(f'{message}')
     
def warning_log(message):
     return main_log.warning(f'{message}')
     
def error_log(message):
     return main_log.error(f'{message}')


def search_files(filetype='.log', path=r'.'):
    list_files=[File for File in os.listdir(path) if File.endswith(filetype)]
    return list_files

def remove_old_logs(days = 7, path_=r'../logs'):
     time_delete = days*86400
     list_logs = search_files(path=path_)
     for i in list_logs:
          time_create = int(i[:-4].split('_')[1])
          time_now = int(time.time())
          if time_create < time_now - time_delete:
               os.remove(os.path.join(path_,i))

if __name__ == '__main__':
     pprint.pprint(search_files(path=r'../logs'))
     print(len(search_files(path=r'../logs')))
     remove_old_logs()
     pprint.pprint(search_files(path=r'../logs'))
     print(len(search_files(path=r'../logs')))
