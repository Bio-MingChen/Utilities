import colorama

def make_colors():
"""
make some colors in command line
"""
    colors = {}
    colorama.init()
    colors['red'] = colorama.Fore.RED
    colors['green'] = colorama.Fore.GREEN
    colors['green_ex'] = colorama.Fore.LIGHTGREEN_EX
    colors['white'] = colorama.Fore.LIGHTWHITE_EX
    colors['magenta_ex'] = colorama.Fore.LIGHTMAGENTA_EX
    colors['magenta'] = colorama.Fore.MAGENTA
    colors['cyan'] = colorama.Fore.CYAN
    colors['cyan_ex'] = colorama.Fore.LIGHTCYAN_EX
    colors['yellow'] = colorama.Fore.YELLOW
    colors['bright'] = colorama.Style.BRIGHT
    colors['back'] = colorama.Style.RESET_ALL
    return colors
    
if __name___ == "__main__":
    colors_dict = make_colors()
    print('{green}Using colorama to print {red}colorful {back}'.format(**colors_dict))
