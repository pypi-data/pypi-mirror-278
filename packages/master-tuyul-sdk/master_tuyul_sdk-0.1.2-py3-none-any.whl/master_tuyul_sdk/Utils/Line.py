import shutil, os

class Line:
    
    @staticmethod
    def Normal():
        try: Size = os.get_terminal_size()
        except: Size = shutil.get_terminal_size(fallback=(120, 50))
        Length = int((Size.columns))
        print('-' * Length)
        
    @staticmethod
    def Bold():
        try: Size = os.get_terminal_size()
        except: Size = shutil.get_terminal_size(fallback=(120, 50))
        Length = int((Size.columns))
        print('=' * Length)
        
    @staticmethod
    def Clear():
        try: Size = os.get_terminal_size()
        except: Size = shutil.get_terminal_size(fallback=(120, 50))
        Length = int((Size.columns))
        print(' ' * Length, end='\r')