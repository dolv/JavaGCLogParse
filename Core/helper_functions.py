import argparse

def parse_script_commandline_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('logfile', default="gc.log", help="filename of the tomcat GC log")
    p.add_argument('-d', '--dir', default="", help="tomcat logs folder path", action="store")
    p.add_argument('-i', '--inventory', default="./inventory.yml", help="inventory containing tomcat hosts", action="store", required=True)
    p.add_argument('-t', '--timeframe', default=5, type=int, help="time frame to monitor", action="store", required=True)
    p.add_argument('--debug', default=False, help="debug output", action="store_true")
    args = p.parse_args()
    return args