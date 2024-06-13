import os
import sys
import time

def print_slow(s, delay=0.01):
    if s:
        for c in s:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
def cls():
    if os.name == 'nt':
        os.system('cls')
    # Unix/Linux/MacOS/BSD
    else:
        os.system('clear')


def clear_screen():
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Unix/Linux/MacOS/BSD
    else:
        os.system('clear')

