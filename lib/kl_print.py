from colorama import init,Fore, Back, Style

init(autoreset=True)

def print_blue(str):
    print(Fore.BLUE + str)

def print_red(str):
    print(Fore.RED + str)

def print_green(str):
    print(Fore.GREEN + str)

def print_bg_blue(str):
    print(Back.BLUE + str)

def print_bg_red(str):
    print(Back.RED + str)

def print_bg_green(str):
    print(Back.GREEN +str)
