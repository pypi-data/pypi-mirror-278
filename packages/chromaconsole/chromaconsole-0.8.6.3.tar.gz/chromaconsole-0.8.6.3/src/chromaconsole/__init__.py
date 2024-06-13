#https://en.wikipedia.org/wiki/ANSI_escape_code

from .styling import Styling
from .Color import Color
from .Console import Console
from .Style import Style
from .ColorBackground import Background as background
from .ColorText import Text as text
import argparse

__all__ = ['Styling', 'Color', 'Style', 'Console']

def setup():
    try:
        import sys, os, platform
        from pkg_resources import get_distribution
        
        try:
            import requests

            current_version = get_distribution("chromaconsole").version
            latest_version = requests.get(f'https://pypi.org/pypi/chromaconsole/json').json()['info']['version']

            if tuple(map(int, current_version.split('.'))) < tuple(map(int, latest_version.split('.'))):
                os.system("pip install chromaconsole -U")
        except:
            pass

        def FixWinConsoleColors():
            if platform.system() == "Windows" and sys.stdout and hasattr(sys.stdout, "fileno"):
                try:
                    import ctypes
                    ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11), 7)
                except Exception:
                    pass

        FixWinConsoleColors()
    except:
        pass

setup()

def check_ver():
    try:
        from pkg_resources import get_distribution
        import requests
        print(f"current: {get_distribution('chromaconsole').version}\n latest: {requests.get(f'https://pypi.org/pypi/chromaconsole/json').json()['info']['version']}")
    except:
        print(f"Something went wrong")
