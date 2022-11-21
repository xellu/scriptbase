import json
import os
import pyfiglet
from colorama import Fore as c

cfg = [[CFG]]

class script:
    def __init__(self):
        self.index = 0
        self.display = ""
        self.code = ""

def fancy():
    return pyfiglet.figlet_format(cfg["basename"], font="Slant")

def scripts():
    scripts_dict = [[SCRIPT_DICT]]
    ascripts = []
    i = 0
    for sc in scripts_dict:
        i += 1
        s = script()
        s.code = sc["code"]
        s.display = sc["display"]
        s.index = i
        ascripts.append(s)
    return ascripts        

def __init__():
    print(f"""{c.BLUE}
{fancy()}
{c.RESET}
        """)
    for x in scripts():
        print(f" {c.BLUE}[{x.index}] {c.LIGHTBLUE_EX}{x.display}")
    
    while True:
        s = input(f"{c.BLUE}> {c.RESET}")
        for script in scripts():
            if s.lower() == script.display.lower() or s == str(script.index):
                exec(script.code)
    
    
__init__()