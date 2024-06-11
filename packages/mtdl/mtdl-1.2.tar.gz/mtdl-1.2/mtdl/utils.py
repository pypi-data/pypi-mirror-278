import traceback
import colorama
import time
from threading import current_thread
import sys
import os

debug_log = open(".\\debug.log", "w")

def abort_if_exception(func):
    def wrapped(*args, **kwds):
        global debug_log
        try:
            #print(f"Thread {current_thread()} :running function {func.__qualname__} with {vars()}", end="\n")
            result = func(*args, **kwds)
            #print(f"Thread {current_thread()} :{func.__qualname__} returned {result}.", end="\n")
            return result
        except BaseException as error:
            print(f"[{time.ctime(time.time())}] - E: ", current_thread(), func, error.__class__.__qualname__,  error, file=debug_log)
            print(traceback.format_exc(), file=debug_log)
            print(colorama.Fore.RED + F"Error: See the message below or the log file {os.path.abspath(debug_log.name)}:\n", colorama.Fore.RESET, traceback.format_exc(), "\n\n\n")
            debug_log.close()
            print("Program aborted.")
            os._exit(1)
    return wrapped

def print_on_lastline(string):
    sys.stdout.write(f"\r{string}")
    sys.stdout.flush()
    
def abort_with_exception(msg, stat):
    print(msg)
    os._exit(stat)
