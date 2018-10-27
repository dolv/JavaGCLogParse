import os


class JavaGCLog(object):
    filename = "gc.log"
    dir = "logs"
    path = "./logs/gc.log"
    newLine = "/n"
    descriptor = None
    inode = None

    def __init__(self, logfile='gc.log', log_dir='logs', newline=os.linesep):
        self.filename = logfile
        self.dir = log_dir
        self.path = os.path.join(self.dir, self.filename)
        self.newline = newline
        self.open()

    def open(self):
        self.descriptor = open(self.path, "r")
        self.inode = os.fstat(self.descriptor.fileno()).st_ino

    def get_lines(self):
        return self.descriptor.readlines()

