def say(text):
    print(f" [>] {text}")
    
def get_input(text):
    return input(f" [>] {text}: ")
    
def get_int_input(text, fail_msg="Please enter a valid integer"):
    while True:
        a = input(f" [>] {text}: ")
        try: int(a)
        except: say(fail_msg)
        else: return int(a)

def cls():
    __init__()