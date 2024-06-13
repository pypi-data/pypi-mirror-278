class Input:
    
    @staticmethod
    def _string(message: str):
        while True:
            try:
                Result = input(message).strip()
                if len(Result) > 5: return Result
            except KeyboardInterrupt:exit()
            except:pass
    
    @staticmethod
    def _integer(message: str):
        while True:
            try:
                return int(input(message).strip())
            except KeyboardInterrupt:exit()
            except:pass
    
    @staticmethod
    def _continue():
        try:
            input('Press enter to continue...')
            return
        except KeyboardInterrupt:exit()
        except:pass