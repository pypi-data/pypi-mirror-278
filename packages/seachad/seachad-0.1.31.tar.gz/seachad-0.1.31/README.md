
to create the library
1) first delete /dist
2) change TOML version
3) python -m build
4) twine upload dist/*

with this the library is updated and uploaded
in order to refresh en environments
5) pip install --upgrade --no-cache-dir nombre_del_paquete



terminal_colors
---------------

Allows print with colors

Very easy!!!

    >>> import terminal_colors as tc

    tc._print(f"{tc.Y}Print in rellow, {tc.G}print in green, {tc.B}, print in blue")
    tc._print(f"print in yellow", tc.Y)
    tc._print(f"print without marks", time_and_module_mark=False)


    def test_print():
        # utilizando el HELPER
        tc._print("Hola mundo", tc.B) # imprimirá por defecto en CYAN con BRIGHT (así sabemos que se está usando esta función por defecto)
        tc._print(f"{tc.Y}Hola {tc.R}mundo") # imprimirá en AZUL sobre ROJO en BRIGHT
        tc._print("Hola mundo", tc.W) # vuelve a imprimir en CYAN con BRIGHT (así sabemos que se está usando esta función por defecto)
        
        # utilizando las primitivas
        tc.print_in_color(tc.fg.BLUE+tc.bg.RED+tc.style.BRIGHT)
        tc.print("Show me your color")    
        tc.print_in_color(tc.fg.WHITE)    
        tc.print( "All following prints will be WHITE ...")
        tc.print( "continues WHITE...")
        tc.print_in_color()    
        tc.print( "Now default color")

cache_REDIS
-----------

Usage of REDIS

functionallities:
- seamless communication with REDIS
- encrypted information
- allow to store in a singleton in memory (for fastest access) only alive during execution, no persistence


common
------

incluida
soporte a diversas funcionaliades para la plataforma


ar_decorator_functions
----------------------

incluida
soporte a control automático de errores avanzado y controles de integridad, básicamente
