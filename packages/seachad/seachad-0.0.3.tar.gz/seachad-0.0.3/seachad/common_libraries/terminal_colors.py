# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:15:34 2021

@author: Fernando

Description:

    
    terminal_colors.py
    imprimir colores en pantalla

"""

import sys
import pprint

global_external_function = None

# =============================================================================
# ---- IMPRIMIR EN COLORES EN LA PANTALLA
# =============================================================================
# RED   = "\033[1;31m"  
# BLUE  = "\033[1;34m"
# CYAN  = "\033[1;36m"
# GREEN = "\033[1;32m"
# RESET = "\033[0;0m"
# BOLD    = "\033[;1m"
# REVERSE = "\033[;7m"

# Terminal color definitions

import os
import platform

# permite ANSI Colorize en Windows y Powershell
# source: https://gist.github.com/RDCH106/6562cc7136b30a5c59628501d87906f7
if os.name == 'nt' and platform.release() == '10' and platform.version() >= '10.0.14393':
    # Fix ANSI color in Windows 10 version 10.0.14393 (Windows Anniversary Update)
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


ESC = '\033'


class fg:
    BLACK   = ESC+'[30m'
    RED     = ESC+'[31m'
    GREEN   = ESC+'[32m'
    YELLOW  = ESC+'[33m'
    BLUE    = ESC+'[34m'
    MAGENTA = ESC+'[35m'
    CYAN    = ESC+'[36m'
    WHITE   = ESC+'[37m'
    RESET   = ESC+'[39m'

class bg:
    BLACK   = ESC+'[40m'
    RED     = ESC+'[41m'
    GREEN   = ESC+'[42m'
    YELLOW  = ESC+'[43m'
    BLUE    = ESC+'[44m'
    MAGENTA = ESC+'[45m'
    CYAN    = ESC+'[46m'
    WHITE   = ESC+'[47m'
    RESET   = ESC+'[49m'

class style:
    BRIGHT    = ESC+'[1m'
    DIM       = ESC+'[2m'
    NORMAL    = ESC+'[22m'
    RESET     = ESC+'[0m'


# REESCRITO EN COLORAMA A VER SI CONSIGO LOS COLORES EN TERMINAL...
 
import colorama
from colorama import Fore, Back, Style

# Initialize Colorama to make it work on Windows as well
colorama.init(autoreset=True)

class fg:
    BLACK   = Fore.BLACK
    RED     = Fore.RED
    GREEN   = Fore.GREEN
    YELLOW  = Fore.YELLOW
    BLUE    = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN    = Fore.CYAN
    WHITE   = Fore.WHITE
    RESET   = Fore.RESET

class bg:
    BLACK   = Back.BLACK
    RED     = Back.RED
    GREEN   = Back.GREEN
    YELLOW  = Back.YELLOW
    BLUE    = Back.BLUE
    MAGENTA = Back.MAGENTA
    CYAN    = Back.CYAN
    WHITE   = Back.WHITE
    RESET   = Back.RESET

class style:
    BRIGHT    = Style.BRIGHT
    DIM       = Style.DIM
    NORMAL    = Style.NORMAL
    RESET     = Style.RESET_ALL


# ACELERADORES - colores de salida
B = fg.BLUE + style.BRIGHT    
G = fg.GREEN + style.BRIGHT    
R = fg.RED + style.BRIGHT    
Y = fg.YELLOW + style.BRIGHT 
C = fg.CYAN + style.BRIGHT 
W = fg.WHITE + style.BRIGHT

# sin BRIGHT
b = fg.BLUE
g = fg.GREEN
r = fg.RED
y = fg.YELLOW
c = fg.CYAN
w = fg.WHITE

# fondos
Bb = bg.BLUE
Bg = bg.GREEN
Br = bg.RED
By = bg.YELLOW
Bc = bg.CYAN
Bw = bg.WHITE

# foreground + background
B_b = B + Bb
B_g = B + Bg
B_r = B + Br
B_y = B + By
B_c = B + Bc
B_w = B + Bw

G_b = G + Bb
G_g = G + Bg
G_r = G + Br
G_y = G + By
G_c = G + Bc
G_w = G + Bw

R_b = R + Bb
R_g = R + Bg
R_r = R + Br
R_y = R + By
R_c = R + Bc
R_w = R + Bw

Y_b = Y + Bb
Y_g = Y + Bg
Y_r = Y + Br
Y_y = Y + By
Y_c = Y + Bc
Y_w = Y + Bw

C_b = C + Bb
C_g = C + Bg
C_r = C + Br
C_y = C + By
C_c = C + Bc
C_w = C + Bw

W_b = W + Bb
W_g = W + Bg
W_r = W + Br
W_y = W + By
W_c = W + Bc
W_w = W + Bw


def print_in_color(col=style.RESET):
    try:
        sys.stdout.write(col)
    except:
        sys.stdout.write(fg.RESET+bg.RESET+style.RESET)
        
# =============================================================================
# Imprime con colores!!!!
# =============================================================================
def __trace(message, color = fg.CYAN+style.BRIGHT, func = None, byscreen = True):
    _print(message, color, func, byscreen)

def clean_screen():
    import os
    os.system('cls')


def _print(message, color = fg.CYAN+style.BRIGHT, func = None, byscreen = True, time_and_module_mark = True):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    _print
    
    imprime con colores en la pantalla
    Si se le envía una función se encarga de ejecutarla y mostrar el resultado
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - message (_type_): _description_
        - color (_type_, optional): _description_. Defaults to fg.CYAN+style.BRIGHT.
        - func (_type_, optional): _description_. Defaults to None.
            por si queremos grabar en disco, por ejemplo (habría que pasarle como parámetro common._print("mensaje", common.Y, lambda: funcion(param1, param2, ...)))
        - byscreen (bool, optional): _description_. Defaults to True.

    Posibles combinaciones de colores:
        # ACELERADORES - colores de salida
        B = fg.BLUE + style.BRIGHT    
        G = fg.GREEN + style.BRIGHT    
        R = fg.RED + style.BRIGHT    
        Y = fg.YELLOW + style.BRIGHT 
        C = fg.CYAN + style.BRIGHT 
        W = fg.WHITE + style.BRIGHT

        # sin BRIGHT
        b = fg.BLUE
        g = fg.GREEN
        r = fg.RED
        y = fg.YELLOW
        c = fg.CYAN
        w = fg.WHITE

        # fondos
        Bb = bg.BLUE
        Bg = bg.GREEN
        Br = bg.RED
        By = bg.YELLOW
        Bc = bg.CYAN
        Bw = bg.WHITE

        # foreground + background
        B_b
        B_g
        B_r
        B_y
        B_c
        B_w

        G_b
        G_g
        G_r
        G_y
        G_c
        G_w

        R_b
        R_g
        R_r
        R_y
        R_c
        R_w

        Y_b
        Y_g
        Y_r
        Y_y
        Y_c
        Y_w

        C_b
        C_g
        C_r
        C_y
        C_c
        C_w

        W_b
        W_g
        W_r
        W_y
        W_c
        W_w

    """

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    class bcolors:
        HEADER = Fore.MAGENTA
        OKBLUE = Fore.BLUE
        OKCYAN = Fore.CYAN
        OKGREEN = Fore.GREEN
        WARNING = Fore.YELLOW
        FAIL = Fore.RED
        ENDC = Style.RESET_ALL
        BOLD = Style.BRIGHT
        # UNDERLINE = Style.UNDERLINE


    # if isinstance(message, dict):
    #     message = pretty_dict(message) 
    
    # imprimir la fecha y hora hasta con milisegundos
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    module_name = sys._getframe(1).f_globals["__name__"]
    funcion_name = sys._getframe(1).f_code.co_name
    num_linea = sys._getframe(1).f_lineno
 
    if byscreen: # puede que sólo quiera ejecutar la función y no pintar en la pantalla   
        m_color = color
        print_in_color(m_color)
        if not isinstance(message, (str, int)):
            if time_and_module_mark:
                print(f"{fg.WHITE}{timestamp}: {fg.BLUE}{module_name}  --> {funcion_name} [{num_linea}] :")
            print_in_color(m_color)
            pprint.pprint(message)
        else:
            # añadimos nombre del módulo y nombre de la función
            if time_and_module_mark:
                print(f"{fg.WHITE}{timestamp}: {fg.BLUE}{module_name} --> {funcion_name} [{num_linea}] : {m_color}{message}")
            else:
                print(f"{m_color}{message}")
        print_in_color()
    
    # por si queremos grabar en disco, por ejemplo (habría que pasarle como parámetro common._print("mensaje", common.Y, lambda: funcion(param1, param2, ...)))
    if func:
        func()        

    if not global_external_function == None:
        # significa que nos han pasado una función global para escribir en disco
        trace_message = f"{timestamp}: {module_name} --> {funcion_name} [{num_linea}] : {message}"
        global_external_function(trace_message)
        return

def test_print():
    # utilizando el HELPER
    _print("Hola mundo", B) # imprimirá por defecto en CYAN con BRIGHT (así sabemos que se está usando esta función por defecto)
    _print(f"{Y}Hola {R}mundo") # imprimirá en AZUL sobre ROJO en BRIGHT
    _print("Hola mundo", W) # vuelve a imprimir en CYAN con BRIGHT (así sabemos que se está usando esta función por defecto)
    
    # utilizando las primitivas
    print_in_color(fg.BLUE+bg.RED+style.BRIGHT)
    print("Show me your color")    
    print_in_color(fg.WHITE)    
    print( "All following prints will be WHITE ...")
    print( "Esto sigue siendo WHITE")
    print_in_color()    
    print( "Ahora normal")

def print_to_disc(filename, cadena):
    with open(filename, "a") as myfile:
        myfile.write(cadena)
    pass

if __name__ == "__main__":
    test_print()

