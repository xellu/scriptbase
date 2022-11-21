import json
import os
import pyfiglet
from colorama import Fore as c

def get_config():
    return json.loads(open("config.json", "r").read())

def announce(text):
    print(f"{c.BLUE}[INFO] {c.WHITE}{text}")

def __init__():
    f = open(get_config()["basename"]+".py", "w", encoding="utf-8")
    
    #Injecting packages
    for p in os.listdir("packages"):
        f.write(open(f"packages/{p}", "r").read() + "\n")
        announce(f"Injected packages '{p}'")
        
    #Loading scripts
    scripts = []
    for x in os.listdir("scripts"):
        scripts.append({"code": open(f"scripts/{x}", "r", encoding="utf-8").read(), "display": x.replace(".py", "")})
    announce("Loaded scripts")
        
    #Loading template
    template = open("template.py", "r", encoding="utf-8").read()
    template = template.replace("[[CFG]]", str(get_config()))
    template = template.replace("[[SCRIPT_DICT]]", str(scripts))
    announce("Injected scripts")
    announce("Loaded template")

    
    #Injecting template
    f.write(template)
    announce("Injected template")
    
    announce("Your ScriptBase tool was successfully constructed")
    
__init__()