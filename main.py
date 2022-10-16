import os
from colorama import Fore as c
from discord import User
import pyfiglet
import json
import sys

#CONFIGURATION-------------
primary = c.LIGHTBLUE_EX
secondary = c.LIGHTWHITE_EX

base_name = "ScriptBase"
font = "slant"
#--------------------------

#TODO: add custom library support

class script:
    def __init__(self):
        self.index = 0
        self.path = ""
        self.display = ""
        self.code =""

def get_title():
    return pyfiglet.figlet_format(base_name, font=font)

def get_packages(script):
    try:
        data = json.loads(open(f"scripts/{script.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    except FileNotFoundError: raise Exception(f"Unable to load packages for {script}, {script.replace('.py', '')}.meta.json is missing")
    except Exception as err: raise UserWarning(f"Caught an unknown error ({err})") 
    
    packages = ""
    
    for p in data["packages"]:
        try:
            c = open(f"packages/{p}.pack.py", "r", encoding="utf-8").read()
        except FileNotFoundError: raise UserWarning(f"Package '{p}.pack.py' was not found")
        except Exception as err: raise UserWarning(f"Caught an unknown error ({err})") 

        packages += c+"\n"

    
    return packages

def load_scripts():
    scripts = []
    i = 0
    for x in os.listdir("scripts"):
        if x.endswith(".py"):
            packages = get_packages(x)
            if packages == None: packages = ""
            
            i +=1
            s = script()
            s.index = i
            s.path = "scripts/"+x
            s.display = x.replace(".py", "")
            s.code = packages+"\n"+open(f"scripts/{x}", "r", encoding="utf-8").read()
            scripts.append(s)

    return scripts

def get_script(na):
    for x in load_scripts():
        if x.display == na:
            return x
        
def is_script_index(n: int):
    try: int(n)
    except: return False
    
    if len(load_scripts()) >= int(n):
        return True
    return False

def process_builtin_commands(s):
    if s in ["exit", "quit", "shutdown", "0", "x"]:
        os._exit(0)
    if s in ["reload", "reboot", "restart"]:
        print(f" {primary}[x] {secondary}Reloading")
        os.system(str(os.path.basename(sys.argv[0])))
        os._exit(0)

def __init__():
    os.system("cls")
    scripts = load_scripts()
    
    #Menu
    print(f"""{primary}\n{get_title()}""", end="")
    print(secondary+"─"*os.get_terminal_size().columns)
    print(f" {primary}[x] {secondary}Exit")
    for x in scripts:
        print(f" {primary}[{x.index}] {secondary}{x.display}")
    print("")
    #----
    
    while True:
        selection = input(f" {primary}[>] {secondary}").lower()
        script = get_script(selection)
    
        process_builtin_commands(selection)
        
        if script != None:
            exec(script.code)
        if is_script_index(selection):
            for x in scripts:
                if x.index == int(selection):
                    exec(x.code)
        else:
            print(f" {primary}[!] {secondary}invalid selection")
        
__init__()