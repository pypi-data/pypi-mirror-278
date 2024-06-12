import logging

'''
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
'''
class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""
    green = "\x1b[32m"  # Green color for DEBUG level
    white = "\x1b[37m"  # White color for INFO level
    yellow = "\x1b[33m"
    yellow_bold = "\x1b[33;1m"  # Bold yellow
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"  # Bold red
    reset = "\x1b[0m"  # Reset to default
    formatLog = '%(levelname)s %(asctime)s - %(name)s %(message)s'

    FORMATS = {
        logging.DEBUG: green + f'%(levelname)s %(asctime)s [%(name)s]{white}%(message)s' + reset,
        logging.INFO: yellow + f'%(levelname)s %(asctime)s [%(name)s]{white}%(message)s' + reset,
        logging.WARNING: yellow_bold + f'%(levelname)s %(asctime)s [%(name)s]{white}%(message)s' + reset,
        logging.ERROR: red + f'%(levelname)s %(asctime)s [%(name)s]{white}%(message)s' + reset,
        logging.CRITICAL: bold_red + f'%(levelname)s %(asctime)s [%(name)s]{white}%(message)s' + reset,
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    


class ULogger:
    # Singleton instance
    __instance = None

    @staticmethod
    def getInstance():
        if ULogger.__instance == None:
            ULogger()
            ULogger.__instance.doInit()
        return ULogger.__instance

    def __init__(self):
        if ULogger.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            ULogger.__instance = self
            self.isSaveLog = False
            self.pathLog = "/tmp/cyborgai.log"

    def doInit(self,_level=10):
        logger = logging.getLogger(__name__)
        
       
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)

        c_handler.setFormatter(CustomFormatter())

        logger.addHandler(c_handler)
        logger.setLevel(_level)#logging.DEBUG)
       
        self.logger = logger
        
    def saveToLog(self, message):
        if self.isSaveLog:
            with open(self.pathLog, 'a') as file:
                file.write(message + '\n')