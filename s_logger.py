import os,inspect
import logging

log = None

def Init(filename):
    global log
    if (log == None):
        # create log
        log = logging.getLogger("")
        log.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
#        ch = logging.FileHandler(filename,mode='w')
        ch.setLevel(logging.DEBUG)
      
        # create formatter
        formatter = logging.Formatter('%(asctime)s \t| %(levelname)s \t| %(filename)s \t| %(funcName)s:%(lineno)d \t| %(message)s',"%Y-%m-%d %H:%M:%S")
    
        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to log
        log.addHandler(ch)    

(frame, filename, line_number,function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
Init(os.path.basename(filename) + ".log")

