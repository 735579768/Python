from colorama import init,Fore, Back, Style

init(autoreset=True)

def print_blue(s_str):
    print(Fore.BLUE + str(s_str))

def print_red(s_str):
    print(Fore.RED + str(s_str))

def print_green(s_str):
    print(Fore.GREEN + str(s_str))

def print_bg_blue(s_str):
    print(Back.BLUE + str(s_str))

def print_bg_red(s_str):
    print(Back.RED + str(s_str))

def print_bg_green(s_str):
    print(Back.GREEN +str(s_str))

if __name__ == '__main__':
    print_red('asdfasdf');
    print_bg_red('asdfasdf');
    print_green('asdfasdf');
    print_bg_green('asdfasdf');
