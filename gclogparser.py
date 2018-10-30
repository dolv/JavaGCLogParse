import os
import time
from pprint import pprint
from Core.helper_functions import parse_script_commandline_arguments as parse_args
from Core.java_gc_log import JavaGCLog
from Core.gc_log_line import GCLogLine, Watcher
from Core.logger import logger
from urllib import request
import subprocess

tomcat_hosts = []

def read_log_file(log):
    while True:
        for line in log.get_lines():
            yield line

        try:
            if os.stat(log.filename).st_ino != log.inode:
                new = open(log.path, "r")
                log.descriptor.close()
                log.descriptor = new
                log.inode = os.fstat(log.descriptor.fileno()).st_ino
        except IOError:
            pass
        time.sleep(1)

def get_health_status(url):
   return True if request.urlopen(url).getcode() == 200 else False

def collect_health_checks():
    with open('inventory.yml') as inventory:
        host={}
        for line in inventory.readlines():
            host['address'] = line
            host['address'] += ":8080"
            host['is_healthy'] = None
            tomcat_hosts.append(host)

    for host in tomcat_hosts:
        host['is_healthy'] = get_health_status(host['address'])

def restart_tomcat():
    if len([i for i in tomcat_hosts if i['is_healthy']]) - 1 > 0:
        logger.info("Restart tomcat")
        subprocess.call('systemctl restart tomcat', shell=True)

def send_alert():
    logger.info("Sending Alert")

def debug():
    logger.info(message=l)
    w.add_line(GCLogLine(l))
    print(len(w.events))
    pprint(w.counters)

if __name__ == '__main__':

    args = parse_args()

    w = Watcher(timeframe_minutes=args.timeframe)
    gc_log = JavaGCLog(args.logfile, args.dir)
    for l in read_log_file(gc_log):
        if args.debug:
            debug()
        if w.counters['Full_GC_free_below_20'] > 10:
            logger.warning('During a 5 min window, number of FullGC events in which the memory being freed is below 20% \
is too high [{}]'.format(w.counters['Full_GC_free_below_20']))
            send_alert()
            restart_tomcat()
        if len(w.events) > 5 and w.counters['Full_GC_time_percent'] > 0.15:
            logger.warning('Total FullGC time during a 5min window is greater than 15%')
            send_alert()
            restart_tomcat()