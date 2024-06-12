
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

deal with dates -> ejemplos

    >>> # significa ahora
    cadena = "@D:NOW@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}", Y)
    
    cadena = "@D:NOW-6MONTH:LASTDAY@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")
   
    # current year
    cadena = "@D:CY@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")
    # current month
    cadena = "@D:CM@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")
    # current H
    cadena = "@D:CH@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")
    # current quarter
    cadena = "@D:CQ@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    # ejemplos:

    cadena = "@D:NOW@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    cadena = "@D:NOW-100DAY@" # -> esto sería START-SIGN-NUMBER-DATAFRAME
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    cadena = "@D:NOW-3DAY@" # -> esto sería START-SIGN-NUMBER-DATAFRAME
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    cadena = "@D:NOW-3DAY:LASTDAY@" # -> esto sería START-SIGN-NUMBER-DATAFRAME y MODIFIER
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    cadena = "@D:NOW:LFEB-35DAY@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    cadena = "@D:2030:FFEB-35DAY@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    #cadenas de fechas para producción en Cloudmore
    cadena = "@D:NOW-6MONTH:LASTDAY@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")

    cadena = "@D:NOW:LASTDAY@"
    _print( f"cadena {cadena} = {dealWithDates(cadena)}")


encriptación y desencriptación (funciones básicas)

generación de claves de encriptación

    >>> CACHE_KEY = common.get_user_env("CM_ENCRYPTION_PASSWORD")
    # estas claves son estáticas y no permiten su modificación en el tiempo
    # encriptación por defecto en base a lo que nos venga dado
    ENCRYPTION_METHOD = common.encryption_get_method_to_encrypt()
    CACHED_GENERATED_KEY = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = ENCRYPTION_METHOD)
    CACHED_GENERATED_KEY_fernet = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = common.ENCRYPTION_METHOD_FERNET) 
    CACHED_GENERATED_KEY_aes = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = common.ENCRYPTION_METHOD_AES)
    CACHED_GENERATED_KEY_chacha20 = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = common.ENCRYPTION_METHOD_CHACHA20)
    CACHED_GENERATED_KEY_obfuscate_base64 = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = common.ENCRYPTION_METHOD_OBFUSCATE_BASE64)

encriptación y desencriptación de información

    >>> common.encryption_set_temporal_include_encryption_prefix(True)

    encryption_support = common.get_user_env("CM_ENCRYPTION_SUPPORT", "False")
    if encryption_support.lower() == "true":
        encryption_support = True
    else:
        encryption_support = False
    from common import ENCRYPTION_PREFIX_MARK    
    # encryption_mark = os.getenv("CM_ENCRYPTION_MARK", ENCRYPTION_PREFIX_MARK)
    encryption_mark = ENCRYPTION_PREFIX_MARK
    encrytion_mark = eval(f"b'{encryption_mark}'")           
    
    string_to_encrypt = "Hello, World from Seachad!"

    # ? vamos a encriptar y desencriptar
    common.encryption_set_temporal_support("xxx_zzzz", True)

    # ! NO ENCRYPTED STRING DECRYPTED OK
    encrypted_strings = {}
    original = string_to_encrypt
    decrypted = string_to_encrypt
    encrypted_strings["no_encryption"] = {
        "original": original, 
        "encrypted" : original, 
        "decrypted" : decrypted,
        "check" : original == decrypted
        }
    
    # ! ENCRYPTED STRING USING FERNET DECRYPTED OK
    CACHED_GENERATED_KEY = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = "fernet")        
    common.encryption_set_temporal_encryption_method(common.get_encryption_method_by_name("fernet"))
    original = string_to_encrypt
    encrypted = common.encrypt(string_to_encrypt, CACHED_GENERATED_KEY, returns_string = True)
    decrypted = common.decrypt(encrypted, CACHED_GENERATED_KEY, returns_string = True)
    encrypted_strings["fernet"] = {
        "original": original, 
        "encrypted" : encrypted, 
        "decrypted" : decrypted,
        "check" : original == decrypted
        }        
    
    # ! ENCRYPTED STRING USING AES DECRYPTED OK
    CACHED_GENERATED_KEY = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = "aes")        
    common.encryption_set_temporal_encryption_method(common.get_encryption_method_by_name("aes"))
    original = string_to_encrypt
    encrypted = common.encrypt(string_to_encrypt, CACHED_GENERATED_KEY, returns_string = True)
    decrypted = common.decrypt(encrypted, CACHED_GENERATED_KEY, returns_string = True)        
    encrypted_strings["aes"] = {
        "original": original, 
        "encrypted" : encrypted, 
        "decrypted" : decrypted, 
        "check" : original == decrypted
        }           
    
    # ! ENCRYPTED STRING USING CHACHA20 DECRYPTED OK
    CACHED_GENERATED_KEY = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = "chacha20")        
    common.encryption_set_temporal_encryption_method(common.get_encryption_method_by_name("chacha20"))
    encrypted = common.encrypt(string_to_encrypt, CACHED_GENERATED_KEY, returns_string = True)
    decrypted = common.decrypt(encrypted, CACHED_GENERATED_KEY, returns_string = True)         
    encrypted_strings["chacha20"] = {
        "original": original, 
        "encrypted" : encrypted, 
        "decrypted" : decrypted, 
        "check" : original == decrypted
        }           
    
    # ! ENCRYPTED STRING USING OBFUSCATE BASE64 DECRYPTED OK
    CACHED_GENERATED_KEY = common.generateEncryptionKey(password = CACHE_KEY, encryption_method = "obfuscation_base64")        
    common.encryption_set_temporal_encryption_method(common.get_encryption_method_by_name("obfuscate_base64"))
    encrypted = common.encrypt(string_to_encrypt, CACHED_GENERATED_KEY, returns_string = True)
    decrypted = common.decrypt(encrypted, CACHED_GENERATED_KEY, returns_string = True)         
    encrypted_strings["obfuscate_base64"] = {
        "original": original, 
        "encrypted" : encrypted, 
        "decrypted" : decrypted, 
        "check" : original == decrypted
        }           





ar_decorator_functions
----------------------

incluida
soporte a control automático de errores avanzado y controles de integridad, básicamente

incluye decoradores para control de errores y para control de integridad. Se proporcionarán ejemplos más adelante (pendiente de pruebas)

