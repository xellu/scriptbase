import os
from colorama import Fore as c
import pyfiglet
import json
import requests
import random
import string
import sys

#CONFIGURATION-------------
primary = c.LIGHTBLUE_EX
secondary = c.LIGHTWHITE_EX

base_name = "[BASENAME]"
font = "slant"
debug = False

#--------------------------

class script:
    def __init__(self):
        self.index = 0
        self.display = ""
        self.code = ""

def load_compiled_scripts():
    scripts_dict = [SCRIPT_DICT]
    scripts = []
    i = 0
    for sc in scripts_dict:
        i += 1
        s = script()
        s.code = sc["code"]
        s.display = sc["display"]
        s.index = i
        scripts.append(s)
    return scripts        

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


def validate_script(name):
    try:
        data = json.loads(open(f"scripts/{name.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    except:
        return False
    
    for var in ["packages", "update_url", "display_name"]:
        try: data[var]
        except: return False
    return True
    
def load_scripts():
    # scripts = []
    # i = 0
    # for x in os.listdir("scripts"):
    #     if validate_script(x):
    #         packages = get_packages(x)
    #         if packages == None: packages = ""
    #         meta = get_script_meta(x)
            
    #         i +=1
    #         s = script()
    #         s.index = i
    #         s.path = "scripts/"+x
    #         s.display = meta["display_name"]
    #         s.code = packages+"\n"+open(f"scripts/{x}", "r", encoding="utf-8").read()
    #         s.update_url = meta["update_url"]
    #         scripts.append(s)
            
    #     elif debug and x.endswith(".py"):
    #         print(f"[WARN] Failed to load '{x}' - meta data is missing or is corrupted")
            
    return load_compiled_scripts()

def get_script_meta(na):
    if validate_script(na):
        return json.loads(open(f"scripts/{na.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    else:
        return {
    "packages": [""],
    "update_url": "https://github.com/xellu/scriptbase/wiki/Getting-Started#metajson-files",
    "display_name": "Invalid meta data" 
}

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

def update_scripts():
    for s in load_scripts():
        if s.update_url != "":
            r = requests.get(s.update_url)
            if r.status_code in [200, 201, 202]:
                if r.content != s.code:
                    open(s.path, "wb").write(r.content)
                    print(f" {primary}[i] {secondary}Updated {s.display}")


def get_config():
    return cfg



def process_builtin_commands(s):
    if get_config()["allow_integrated_commands"] == False: return
    if s in ["exit", "quit", "shutdown", "0", "x"]:
        os._exit(0)
    if s in ["reboot", "restart"]:
        print(f" {primary}[x] {secondary}Restarting")
        os.system(str(os.path.basename(sys.argv[0])))
        os._exit(0)
    if s in ["rel", "reload"]:
        print(f" {primary}[x] {secondary}Restarting")
        __init__()
    if s in ["commands", "help"]:
        print(f"""
   {primary}[i] {secondary}Command list
    {primary}|  Restart{secondary} Restarts the app
    {primary}|  Reload{secondary} Reloads the app
    {primary}|  Exit{secondary} Quits the {base_name}
    {primary}|  Help{secondary} Shows the command list
              """)
        return True
        
        
def __init__():
    os.system("cls")
    scripts = load_scripts()
    
    #Menu
    print(f"""{primary}\n{get_title()}""", end="")
    print(secondary+"─"*(os.get_terminal_size().columns-len("\\nPowered by ScriptBase ")))
    
    if get_config()["show_exit_button"]: print(f" {primary}[x] {secondary}Exit")
    
    for x in scripts:
        print(f" {primary}[{x.index}] {secondary}{x.display}")
    print("")
    #----
    
    while True:
        selection = input(f" {primary}[>] {secondary}").lower()
        script = get_script(selection)
    
        if not process_builtin_commands(selection):
            
            if script != None:
                exec(script.code)
            if is_script_index(selection):
                for x in scripts:
                    if x.index == int(selection):
                        exec(x.code)
            else:
                print(f" {primary}[!] {secondary}invalid selection")
        
__init__()
