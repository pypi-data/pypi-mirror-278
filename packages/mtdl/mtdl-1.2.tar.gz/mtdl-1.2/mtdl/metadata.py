import sys
import platform

__version__ = "1.2"
__author__ = "Bill Loic"
__author_email__ = "billloic6@gmail.com"
__release_time__ = "2024/06/09T08:12:00"
__operating_system__ = platform.platform()
python_ver = sys.version

def format_metadata():
    return "\n".join([f"Multi-Thread downloader version {__version__} by {__author__}, release {__release_time__}", 
    f"Python Ver. {python_ver}", 
    f"OS Ver. {__operating_system__}"])
