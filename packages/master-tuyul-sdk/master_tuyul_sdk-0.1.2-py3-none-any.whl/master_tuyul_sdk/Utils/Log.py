import logging, datetime
from .Color import Color

#logging.basicConfig(level=logging.INFO)

class Log:
    
    @staticmethod
    def info(message: str):
        date = f" {Color.YELLOW}" + str(datetime.datetime.now()).split('.')[0].split(' ')[1] + f"{Color.RESET} "
        print(f'INFO:{date}: {Color.GREEN}{message}{Color.RESET}')
        
    @staticmethod
    def error(message: str):
        date = f" {Color.YELLOW}" + str(datetime.datetime.now()).split('.')[0].split(' ')[1] + f"{Color.RESET} "
        print(f'ERROR:{date}: {Color.RED}{message}{Color.RESET}')
        
    @staticmethod
    def debug(message: str):
        date = f" {Color.YELLOW}" + str(datetime.datetime.now()).split('.')[0].split(' ')[1] + f"{Color.RESET} "
        print(f'DEBUG:{date}: {Color.RESET}{message}{Color.RESET}')