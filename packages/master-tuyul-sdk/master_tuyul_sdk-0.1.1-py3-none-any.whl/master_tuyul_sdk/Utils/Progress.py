import time
from .Color import Color
import random

class ProgressBar:
    
    def __init__(self, iteration: int, total: int, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r", ending = '\n') -> None:        
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        color = [Color.WHITE, Color.RED, Color.GREEN, Color.BLUE, Color.CYAN, Color.MAGENTA, Color.YELLOW]
        normal = ' ' * (length - filledLength)
        bar = f'{color[random.randint(0, len(color) - 1)]}{fill * filledLength}{normal}'
        print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}Progress', end='\r') if printEnd == '\r' else print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}Progress', end='\n')
        if iteration == total: 
            bar = f'{Color.GREEN}{fill * filledLength}{normal}'
            print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}{suffix}', end='\r') if ending == '\r' else print(f'\r{prefix} |{bar}{Color.WHITE}| {Color.GREEN}{percent}% {Color.WHITE}{suffix}', end='\n')

class ProgressWait:
    
    def __init__(self, Random: bool, Start = 1, End = 60) -> None:
        if Random is True: items = list(range(0, random.randint(Start, End)))
        else: items = list(range(Start, End))
        ProgressBar(0, len(items), prefix = 'Please wait:', suffix = 'Complete', length = 25, ending = '\r')
        for i, item in enumerate(items):
            ProgressBar(i + 1, len(items), prefix = 'Please wait:', suffix = 'Complete', length = 25, ending = '\r')
            time.sleep(1)