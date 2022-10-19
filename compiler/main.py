import json
import time
import os

start = 0

def get_time():
    return time.strftime("%H:%M:%S", time.localtime())

def log(text: str, silent = False):
    x = f"[{get_time()}] {text}"
    if not silent:
        print(x)
    open("latest_log.txt", "a").write("\n"+x)

def fatal(e: str):
    end = time.time()
    log(e, silent=True)
    print(f"[FATAL] {e}")
    print(f"[SCRIPTBASE] BUILD FAILED IN {abs(end-start):.5f}s")
    os._exit(0)

def validate_script(name):
    try:
        data = json.loads(open(f"data/scripts/{name.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    except:
        return False
    
    for var in ["packages", "update_url", "display_name"]:
        try: data[var]
        except:
            log(f"Failed to validate a script '{name}' (Invalid meta data)")
            return False
    return True

def get_script_meta(na):
    if validate_script(na):
        return json.loads(open(f"data/scripts/{na.replace('.py', '')}.meta.json", "r", encoding="utf-8").read())
    else:
        return {
    "packages": [""],
    "update_url": "https://github.com/xellu/scriptbase/wiki/Meta-data-&-configs#script-meta-data",
    "display_name": "Invalid meta data"}

def validate_package(p):
    try: open(f"data/packages/{p}.pack.py")
    except Exception as e:
        log(f"Failed to validate a package '{p}.pack.py'")
        return False
    return True



def build():
    global start
    start = time.time()
    log(f"Build process started")
    
    #Getting the needed files
    try: base = open("data/base.py", "r", encoding="utf-8").read()
    except Exception as e: fatal(e)
    log("Base loaded")
    try: cfg = json.loads(open("data/config.json", "r").read())
    except Exception as e: fatal(e)
    log("Config loaded")
    
    base = base.replace("[BASENAME]", base_name)
    base = base.replace("""figlet_format(base_name, font=font)""", """figlet_format(base_name, font=font)+"\\nPowered by ScriptBase " """)
    log("Build Name Changed")
    
    script_dict = []
    packages = []
    try:
        for s in os.listdir("data/scripts"):
            if validate_script(s):
                meta = get_script_meta(s)
                code = open("data/scripts/"+s, "r", encoding="utf-8").read()
                display = meta["display_name"]
                for p in meta["packages"]:
                    if p not in packages:
                        if validate_package(p):
                            base = open(f"data/packages/{p}.pack.py", "r", encoding="utf-8").read()+"\n"+base
                            log(f"Injected a package into the build ({p})")
                            packages.append(p)
                script_dict.append({"code": code, "display": display})
                log(f"Injected a script into the build ({s})")
                
    except Exception as e: fatal(e)
        
    base = base.replace("[SCRIPT_DICT]", str(script_dict))
    log("Script injection was finished")
    
    final = f"""
cfg = {str(cfg)}

{base}
    """
    log("Build constructed")
    open(f"{base_name}.py", "w", encoding="utf-8").write(final)
    log("Build Saved")
    
    log(f"Build Successful in {abs(time.time()-start):.5f}s")
    

open("latest_log.txt", "w").write("")
base_name = input(f"[{get_time()}] Base Name> ")
build()