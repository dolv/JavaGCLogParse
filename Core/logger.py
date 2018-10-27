import os

class Logger(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    INFO = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    LightGray = "\033[37m"
    DarkGray = "\033[90m"
    LightRed = "\033[91m"
    LightGreen = "\033[92m"
    LightYellow = "\033[93m"
    LightBlue = "\033[94m"
    LightMagenta = "\033[95m"
    LightCyan = "\033[96m"
    White = "\033[97m"

    logfile = None
    newline = '\n'

    def __init__(self, logfile='server.log', output_dir='output', newline=os.linesep):
        self.logfile = logfile
        self.output_dir = output_dir
        self.newline = newline

    def echo(self, message='', color=ENDC, mtype='', newline=newline):
        print("{color}{message}{endc}{newline}".format(color=color, message=message, endc=self.ENDC, newline=newline)),
        self.log(message=message, mtype=mtype, newline=newline)

    def log(self, message='', mtype="*", newline=newline):
        if self.logfile:
            import datetime
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            with open(os.path.join(self.output_dir, self.logfile), 'a') as f:
                f.writelines("{time} [{type}] {message}{newline}".format(time=datetime.datetime.now(),
                                                                         type=mtype, message=message, newline=newline))

    def info(self, message='', color=INFO, newline='\n'):
        self.echo(message=message, color=color, mtype='I', newline=newline)

    def debug(self, message='', newline='\n'):
        self.echo(message=message, color=self.OKBLUE, mtype='D', newline=newline)

    def error(self, message='', newline='\n'):
        self.echo(message=message, color=self.FAIL, mtype='E', newline=newline)

    def fatal(self, message='', code=0, newline='\n'):
        self.echo(message=message, color=self.FAIL, mtype='F', newline=newline)
        exit(code=code)

    def warning(self, message='', newline='\n'):
        self.echo(message=message, color=self.WARNING, mtype='W', newline=newline)


logger = Logger()
