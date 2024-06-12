# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 18:33:29 2021

@author: Fernando

decorator_functions

ar_decorator usados por API_ROBOT (hay decorators en ar_task_functions y en ar_mongodb pero son específicos de esas librerías)

"""
GLOBAL_EXCEPTION = False

# --- *          * PERFORMANCE TIMING DECORATOR
import functools
import time
import sys
import pprint

import os
import platform
import traceback

import copy

import builtins
try:
    access = builtins.access
except:
    access = {}

import seachad.common_libraries.IPL
# access = IPL.get_access()

# import ar_db
import seachad.common_libraries.terminal_colors as tc  

stop = False

# import common

""" definición de custom excpetion 

    API_ROBOT_custom_exception
    
    se utiliza en flush_error para determinar si hay que parar el programa, porque el error sea realmente grave
    
"""

catch_exceptions_external_function = None

def set_catch_exceptions_external_function(f):
    global catch_exceptions_external_function
    catch_exceptions_external_function = f

import os
class OuterScopeGetter(object):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    OuterScopeGetter
    
    Va hacia atrás hasta que encuentra una variable con el nombre que se quiere usar (rastrea en los locals de las funciones caller)
    From: https://stackoverflow.com/questions/15608987/how-can-i-access-variables-from-the-caller-even-if-it-isnt-an-enclosing-scope
    
    Extended Description:
    ---------------------
    Nos sirve para simplificar el uso de scoped_sessions.
    La función get_scoped_session necesita ir llenando un diccionario para acceder a las sesiones creadas y cerrarlas en la salida del scope
    de llamadas
    Para ello antes había que pasar un parametro en la función decorada con scoped_sessions (que crea un diccionario precisamente para ello)
    y la función get_scoped_session tenía que recibir ese diccionario. Esto complica el uso del decorator y la función que crea las sessions.
    Con esta clase sólo tenemos que poner el decorator a la función y get_scoped_sessions intentará encontrar el diccionario que se encarga del
    inventario de sesiones, por nombre.
    
    No se podrá usar get_scoped_session en una función que no tenga el decorator scoped_sessions
    
    Ejemplo de uso:

    En este ejemplo vemos cómo hacer tres sesiones, usar una de ellas para modificar un valor en un registro y, al salir de la función,
    mágicamente, todas las sesiones se cierran (incluso aunque se produzca un error de código)

    >>> @scoped_sessions
    >>> def ATOMIC_add_register(configuration):
    >>>    session_1 = get_scoped_session(bind="Auth",custom_schema="public") # obtiene una sesion para trabajar con la base de datos
    >>>    session_2 = get_scoped_session(bind="abmc",custom_schema="public") # obtiene una sesion para trabajar con la base de datos
    >>>    session_3 = get_scoped_session(bind="dashboards_apirobot",custom_schema="SEACHAD") # obtiene una sesion para trabajar con la base de datos
    >>>    session_4 = get_scoped_session(User) # obtiene una sesion para trabajar con la tabla User
    >>>    session_5 = get_scoped_session(xxx_active_licenses) # obtiene una sesion para trabajar con la tabla xxx_active_licenses y usuario logged
    >>>    session_6 = get_scoped_session(xxx_active_licenses,schema="SEACHAD") # obtiene una sesion para trabajar con la tabla xxx_active_licenses en el schema "SEACHAD"
    >>>    # trabajamos con las sesiones en lo que sea necesario
    >>>    r = session_1.query(User).filter_by(User.id == 1).first()
    >>>    r.username = "user name de prueba)
    >>>    session_1.commit() 
    >>>    return True 

    Args:
    -----
        - object (_type_): _description_
    """    

    def __getattribute__(self, name):
        import inspect
        frame = inspect.currentframe()
        if frame is None:
            raise RuntimeError('cannot inspect stack frames')
        sentinel = object()
        frame = frame.f_back
        while frame is not None:
            value = frame.f_locals.get(name, sentinel)
            if value is not sentinel:
                return value
            frame = frame.f_back
        
        raise AttributeError(repr(name) + ' not found in any outer scope')


def globals_set(key, value, tag = "unknown"):
    """
    (c) Seachad - FGV
    
    Description:
    ---------------------- 
        globals_set
        Pone valor en key, y con el tag de agregación tag
    
    Extended Description:
    ---------------------
        _extended_summary_
    
    Args:
    -----
            - key (_type_): _description_
            - value (_type_): _description_
            - tag (str, optional): _description_. Defaults to "unknown".
    """    
    o = OuterScopeGetter()
    try:
        __globals = o.__globals
        __globals.set(key, value,tag)
    except Exception as e:
        pass

def globals_get(key, default_value = None):
    """
    (c) Seachad - FGV
    
    Description:
    ---------------------- 
        globals_get
        Devuelve el contenido de key o default_value si no lo encuentra
    
    Extended Description:
    ---------------------
        _extended_summary_
    
    Args:
    -----
            - key (_type_): _description_
            - default_value (_type_, optional): _description_. Defaults to None.
    """    
    o = OuterScopeGetter()
    try:
        __globals = o.__globals
        return __globals.get(key, default_value)
    except Exception as e:
        return default_value

def globals_serialize(key = None, subdirectory = "", build_prefix = True):
    """
    (c) Seachad - FGV
    
    Description:
    ---------------------- 
        globals_serialize
        serializa globals
    
    Extended Description:
    ---------------------
        _extended_summary_
    
    Args:
    -----
            - key (_type_, optional): _description_. Defaults to None.
            - subdirectory (str, optional): _description_. Defaults to "". Si se le pasa un subdirectorio, se creará dentro de globals
            - build_prefix (bool, optional): _description_. Defaults to True. Si es True, se construye el prefix con la fecha y hora actual
    """

    o = OuterScopeGetter()
    try:
        __globals = o.__globals    
        __globals.serialize(key, subdirectory = subdirectory, build_prefix = build_prefix)
    except Exception as e:
        tc._print(f"{e}")
        
    pass


def get_globals():
    """
    (c) Seachad - FGV
    
    Description:
    ---------------------- 
        get_globals
        Devuelve una referencia a __globals, que es dónde se guarda toda la información de variables globales del thread que está corriendo
    
    Extended Description:
    ---------------------
        _extended_summary_
    
    Returns:
    --------
            _type_: _description_
    """    
    try:
        o = OuterScopeGetter()
        __globals = o.__globals
        return __globals    
    except Exception as e:
        return None

# =============================================================================
# Se carga información de contexto global lógico para "escupirlo" en caso de error, así facilita el seguimiento
# =============================================================================
class API_ROBOT_global_context():
    def __init__(self):
        self._dict = {}
    
    def __str__(self):
        return self._dict
        
    def __repr__(self):
        return self._dict

global_api_robot_context = None

""" excepción genérica de API_ROBOT """
class API_ROBOT_Exception(Exception):
    def __init__(self, message, stop_program = False):
        self.message = message
        self._stop_program = stop_program
        GLOBAL_EXCEPTION = True

    def __str__(self):
        if self.message:
            return f"API_ROBOT_Exception: {self.message} {self._stop_program}"
        else:
            return f"API_ROBOT_Exception: raised"

# claves conocidas del diccionario de integridad
exception_information_known_keys = ["SYSTEM", "ITEM", "ITEM_EXTENDED_INFORMATION", "ERROR_WARNING_CODE", "CLIENT", "TIMESTAMP", "ADDITIONAL_INFORMATION"]

class API_ROBOT_INTEGRITY_Exception(Exception):
    import datetime
    SYSTEM = "API_ROBOT"        #(realmente es el nombre del programa - script - que está generando la excepción )
    ITEM = "API_CALL"           # (item que está generando la excepción - puede ser una llamada a un API, carga de una BBDD, lo que sea)
    ITEM_EXTENDED_INFORMATION = {}          # (diccionario que contiene información extendida del item que está generando la excepción, si procede) (para una llamada API sería el Proveedor/Tenant/Subscription,..., para una carga de BBDD sería el nombre de la BBDD/SCHEMA/Tabla,...)
    ERROR_WARNING_CODE = ""     # (código de error o warning que se está generando) por ejemplo, códigos de error por debajo de 1000 son WARNINGS - OJO, no están normalizados, cada programa puede tener los suyos (por eso es un STRING)
    CLIENT = ""                 # (nombre o identificación del cliente en la forma en que lo conoce el programa) - el programa de gestión de integridad se encargará de intentar chequear la información con el cliente que se le pase
    TIMESTAMP = datetime.datetime.now()            # (timestamp de la excepción)
    ADDITIONAL_INFORMATION = {}     # - (como siempre, un diccionario con cualquier otra información que quiera pasarse y que es un saco para ampliar info en el futuro) - es LIBRE
    f_to_call = None # función a la que se llamará con el diccionario de información para meterlo en AUDIT, o para escribir un fichero o lo que corresponda (se puede inyectar una función desde otro script)
    
    
    def __init__(self, 
                 namesystem = "API_ROBOT", # SYSTEM que ocasiona el problema de integridad
                 message = "Error o Warning", # mensaje personalizado que podemos mostrar en el log
                 stop_program = False, # se debe parar el programa?
                 f_to_call = None, # función a la que llamar (se le pasará ) 
                 exception_information = {}, # diccionario con la información que enviamos para integridad, en as_dict se especifica qué información contedrá el diccionario que se envíe, claves no conocidas en exception_information se meterán dentro de ADDITIONAL_INFORMATION para no perder información
                 **kwargs # reservado para el futuro
                 ):
        self.namesystem = namesystem
        self.message = message
        self._exception_information = self.as_dict(exception_information)
        self._stop_program = stop_program
        self.f_to_call = f_to_call
        GLOBAL_EXCEPTION = True

    def as_dict(self, exception_information):
        import datetime
        
        # convierte la información que le llega en un diccionario, por si es necesario usarse después en este formato
        if not isinstance(exception_information, dict):
            raise API_ROBOT_Exception("exception_information must be a dict. No integrity information will be sent")
        
        """ el diccionario interno y, por tanto, las variables internas, se inicializan con valores por defecto en la medida de lo posible, algunas se cogen de variables globales si no viene la información en __init__ """        
        dic = {}
        self.SYSTEM         = exception_information.get("SYSTEM", "Unknown") 
        self.ITEM           = exception_information.get("ITEM", "Unknown") # puede ser API, BBDD, ... de dónde pretendo coger la información
        self.ITEM_EXTENDED_INFORMATION  = exception_information.get("ITEM_EXTENDED_INFORMATION", {})
        self.ERROR_WARNING_CODE         = exception_information.get("ERROR_WARNING_CODE", "TRAZA")
        self.CLIENT         = exception_information.get("CLIENT", global_client_name)
        self.TIMESTAMP      = exception_information.get("TIMESTAMP", datetime.datetime.now())
        self.ADDITIONAL_INFORMATION     = exception_information.get("ADDITIONAL_INFORMATION", {})
        
        dic["SYSTEM"]       = self.SYSTEM
        dic["ITEM"]         = self.ITEM
        dic["ITEM_EXTENDED_INFORMATION"]    = self.ITEM_EXTENDED_INFORMATION
        dic["ERROR_WARNING_CODE"]           = self.ERROR_WARNING_CODE
        dic["CLIENT"]       = self.CLIENT
        dic["TIMESTAMP"]    = self.TIMESTAMP
        dic["ADDITIONAL_INFORMATION"]       = self.ADDITIONAL_INFORMATION
        
        # toda las claves no conocidas, se meten como claves dentro de ADDITIONAL_INFORMATION
        for k,v in exception_information.items():
            if not k in exception_information_known_keys:
                dic["ADDITIONAL_INFORMATION"][k] = v
        return dic
  

   
""" cualquier programa que sea un SOURCE puede levantar una excepción de este tipo y acabará en el CSV de errores de integridata para flask_dashboards """    
class API_ROBOT_SOURCE_Exception(API_ROBOT_INTEGRITY_Exception):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    API_ROBOT_SOURCES_Exception
    
    Gestión de Excepción específica para SOURCES e INTEGRITY de datos a obtener para cualquier cliente (o proceso)
    
    Extended Description:
    ---------------------
    Cualquier programa podrá lanzar este tipo de excepción para que sea procesada posteriormente por util_integrity_manager.py
        
    Args:
    -----
        - Exception (_type_): _description_
    
    Raises:
    -------
        API_ROBOT_Exception: _description_
    
    Returns:
    --------
        _type_: _description_
    """    
 
    def __init__(self, namesystem = "API_ROBOT", message = "Error o Warning", stop_program = False, f_to_call = None, exception_information = {},**kwargs):
        API_ROBOT_INTEGRITY_Exception.__init__(self, namesystem = namesystem, message = message, stop_program = stop_program, f_to_call = f_to_call, exception_information = exception_information, **kwargs)
 
    def __str__(self):
        if self.message:
            return f"API_ROBOT_SOURCE_Exception: {self.namesystem} {self.message} {self._stop_program} {self._exception_information}"
        else:
            return f"API_ROBOT_SOURCE_Exception: raised {self.namesystem} {self._exception_information}"    
    
class API_ROBOT_SETUP_Exception(API_ROBOT_INTEGRITY_Exception):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    API_ROBOT_SOURCES_Exception
    
    Gestión de Excepción específica para SOURCES e INTEGRITY de datos a obtener para cualquier cliente (o proceso)
    
    Extended Description:
    ---------------------
    Cualquier programa podrá lanzar este tipo de excepción para que sea procesada posteriormente por util_integrity_manager.py
        
    Args:
    -----
        - Exception (_type_): _description_
    
    Raises:
    -------
        API_ROBOT_Exception: _description_
    
    Returns:
    --------
        _type_: _description_
    """    
    def __init__(self, namesystem = "API_ROBOT", message = "Error o Warning", stop_program = False, f_to_call = None, exception_information = {},**kwargs):
        API_ROBOT_INTEGRITY_Exception.__init__(self, namesystem = namesystem, message = message, stop_program = stop_program, f_to_call = f_to_call, exception_information = exception_information, **kwargs)
    def __str__(self):
        if self.message:
            return f"API_ROBOT_SETUP_Exception: {self.namesystem} {self.message} {self._stop_program} {self._exception_information}"
        else:
            return f"API_ROBOT_SETUP_Exception: raised {self.namesystem} {self._exception_information}"    
    
class API_ROBOT_INTERACTIVE_Exception(API_ROBOT_INTEGRITY_Exception):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    API_ROBOT_SOURCES_Exception
    
    Gestión de Excepción específica para SOURCES e INTEGRITY de datos a obtener para cualquier cliente (o proceso)
    
    Extended Description:
    ---------------------
    Cualquier programa podrá lanzar este tipo de excepción para que sea procesada posteriormente por util_integrity_manager.py
        
    Args:
    -----
        - Exception (_type_): _description_
    
    Raises:
    -------
        API_ROBOT_Exception: _description_
    
    Returns:
    --------
        _type_: _description_
    """    
    def __init__(self, namesystem = "API_ROBOT", message = "Error o Warning", stop_program = False, f_to_call = None, exception_information = {},**kwargs):
        API_ROBOT_INTEGRITY_Exception.__init__(self, namesystem = namesystem, message = message, stop_program = stop_program, f_to_call = f_to_call, exception_information = exception_information, **kwargs)
    def __str__(self):
        if self.message:
            return f"API_ROBOT_INTERACTIVE_Exception: {self.namesystem} {self.message} {self._stop_program} {self._exception_information}"
        else:
            return f"API_ROBOT_INTERACTIVE_Exception: raised {self.namesystem} {self._exception_information}"    
    
 
def _flask_dashboards_error(namesystem, dic):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    _flask_dashboards_error
    
    Genera una traza de error para que el procedimiento de gestión e información de errores posterior lo pueda leer
    
    Extended Description:
    ---------------------
    Necesitamos saber desde qué API ha dado el error concreto
        
    Args:
    -----
        -   namesystem (str): nombre del sistema que lo genera (encabezará el fichero)
        -   dic (_type_): diccionario conteniendo la información del error
    
    Returns:
    --------
        _type_: _description_
    """    
    # de momento no hace nada, pero tendrá que escribir un ficherito con el error que se ha producido
    pass

# =============================================================================
# saca un "shot" de error en un archivo
# =============================================================================
def _error_flush(cadena, 
                 auto_destroy = False,
                 namefile = "ERR_", # le añadimos algo antes del nombre del fichero (que si no se le dice nada, sería el timestamp?
                 timestamp_tf = True,
                 # stop = False,
                 ):
    _flush_error(cadena, auto_destroy = auto_destroy, namefile = namefile, timestamp_tf = timestamp_tf, stop = stop)
    
def _flush_error(cadena, 
                 auto_destroy = False,
                 namefile = "ERR_", # le añadimos algo antes del nombre del fichero (que si no se le dice nada, sería el timestamp?
                 timestamp_tf = True, 
                 **kwargs,
                 # stop = False
                 
                 ): 
    """
    "escupe" un fichero en el directorio CM_err_folder o crea una directorio "C:/API_ROBOT_ERR" 

    Parameters
    ----------
    cadena : TYPE
        DESCRIPTION.
    auto_destroy : TYPE, optional
        DESCRIPTION. The default is False. Si está a True, el fichero no persistirá

    Returns
    -------
    None.

    """
    global global_context_name, global_process_name, global_process_reference, global_trace_execution 
    global global_client_name, global_provider_name
    global global_api_robot_context

    import ar_managers
    from pathlib import Path
    timestamp = ""

    if timestamp_tf:
        timestamp = IPL.timestamp()
    filename = f"{namefile}{timestamp}.txt"
    name = f"{namefile}{timestamp}"
    log_path = access.get("CM_err_folder", "C:/API_ROBOT_ERR") # si no existe esta clave, lo creo siempre en el directorio del disco por defecto
    filename = Path(log_path) / Path(filename)
    
    if not global_api_robot_context == None:
        cadena = cadena + "\n\nCONTEXTO DE EJECUCION:\n\n"
        aro = global_api_robot_context._dict["aro"]
        cadena = cadena + f"{aro}"

    
    # ! grabación en disco en la clave de apirobot_json CM_err_folder
    m = ar_managers._persistence_manager_raw(_name = name, _filename = str(filename), _auto_destroy = auto_destroy)   
    m._put(cadena)
    
    # pendiente conseguir el client_name y el provider_name
    # ! grabación en bbdd
    # if global_trace_execution:
    #     if False:
    #         ar_db.trace_execution(  process_name = global_process_name, 
    #                                 process_instance = global_process_reference, 
    #                                 standarized_code = ar_db.SC_ERROR, 
    #                                 standarized_sub_code = -1, 
    #                                 standarized_type = "ERROR!!!", # para APIs                              
    #                                 title = f"{namefile}{timestamp}",
    #                                 text = cadena,
    #                                 application_name = "apirobot",
    #                                 client_name = global_client_name,
    #                                 provider_name = global_provider_name 
    #                                 )                               
    

# --- *          * DECORATORS -------------------------------------------------

def time_control(func): # <- DECORATOR 
    @functools.wraps(func)    
    def call(*args, **kwargs): # <- FUNC 
    
        st = time.perf_counter()
        value = func(*args, **kwargs)
        et = time.perf_counter()
        
        tc._print(f"--------> elapsed time in func {func.__name__} : {et-st} sgs")
        
        return value, et-st
    
    return call

global_context_name = "ERR_"

global_process_name = None
global_process_reference = None
global_trace_execution = True

unknown = "unknown"

global_client_name = unknown
global_provider_name = unknown


def locals_on_error():
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    locals_on_error
    
    Coge todas las variables LOCALES de la función que ha producido el error y las devuelve como un diccionario
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Returns:
    --------
        _type_: _description_
    """    
    import sys
    import traceback    
    exc_type, exc_value, exc_tb = sys.exc_info()
    return exc_tb.tb_next.tb_frame.f_locals


""" funcion por defecto para trazar excepciones de integridad, por si catch_integrity_information == True y no se proporciona función de proceso """
def integrity_information_function(integrity_information = {}, f_integrity_factory = None):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    integrity_information_function
    
    Función por defecto de proceso de función de information de integridad
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - dic (_type_): _description_
    """   
    # tenemos en el espacio globals() una función de integridad
    
    
    if len(integrity_information):
        # f_integrity_factory = globals_get("f_integrity_factory_function", None)
        if f_integrity_factory != None:
            retorno = f_integrity_factory(integrity_information=integrity_information, error = False)
    
    
    pass

""" función por defecto para trazar excepciones de integridad, por si flag_integrity_exception == True y no se proporciona función de proceso """
def integrity_exception_function(exception_information = {}):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    integrity_exception_function
    
    Función por defecto de proceso de función de exception de integridad
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - dic (_type_): _description_
    """    
    
    f_integrity_factory = globals_get("f_integrity_factory_function", None)
    if f_integrity_factory != None:
        retorno = f_integrity_factory(exception_information=exception_information, error = True)

    if False:    
        with open(access.get("CM_err_folder", "C:/API_ROBOT_ERR") + f"/{exception_information['SYSTEM']}_EXCEPTIONS.csv", "a") as f:
            # escribo los valores
            f.write(f"{exception_information['TIMESTAMP']},{exception_information['ITEM']},{exception_information['ITEM_EXTENDED_INFORMATION']},{exception_information['ERROR_WARNING_CODE']},{exception_information['CLIENT']},{exception_information['ADDITIONAL_INFORMATION']}\n")
    

class _OuterScopeGetter(object):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    OuterScopeGetter
    
    Va hacia atrás hasta que encuentra una variable con el nombre que se quiere usar (rastrea en los locals de las funciones caller)
    From: https://stackoverflow.com/questions/15608987/how-can-i-access-variables-from-the-caller-even-if-it-isnt-an-enclosing-scope
    
    Extended Description:
    ---------------------
    Nos sirve para simplificar el uso de scoped_sessions.
    La función get_scoped_session necesita ir llenando un diccionario para acceder a las sesiones creadas y cerrarlas en la salida del scope
    de llamadas
    Para ello antes había que pasar un parametro en la función decorada con scoped_sessions (que crea un diccionario precisamente para ello)
    y la función get_scoped_session tenía que recibir ese diccionario. Esto complica el uso del decorator y la función que crea las sessions.
    Con esta funcionalidad sólo tenemos que poner el decorator a la función y get_scoped_sessions intentará encontrar el diccionario que se encarga del
    inventario de sesiones, por nombre.
    
    No se podrá usar get_scoped_session en una función que no tenga el decorator scoped_sessions
    
    Ejemplo de uso:

    En este ejemplo vemos cómo hacer tres sesiones, usar una de ellas para modificar un valor en un registro y, al salir de la función,
    mágicamente, todas las sesiones se cierran (incluso aunque se produzca un error de código)

    >>> @scoped_sessions
    >>> def ATOMIC_add_register(configuration):
    >>>    session_1 = get_scoped_session(bind="Auth",custom_schema="public") # obtiene una sesion para trabajar con la base de datos
    >>>    session_2 = get_scoped_session(bind="abmc",custom_schema="public") # obtiene una sesion para trabajar con la base de datos
    >>>    session_3 = get_scoped_session(bind="dashboards_apirobot",custom_schema="SEACHAD") # obtiene una sesion para trabajar con la base de datos
    >>>    session_4 = get_scoped_session(User) # obtiene una sesion para trabajar con la tabla User
    >>>    session_5 = get_scoped_session(xxx_active_licenses) # obtiene una sesion para trabajar con la tabla xxx_active_licenses y usuario logged
    >>>    session_6 = get_scoped_session(xxx_active_licenses,schema="SEACHAD") # obtiene una sesion para trabajar con la tabla xxx_active_licenses en el schema "SEACHAD"
    >>>    # trabajamos con las sesiones en lo que sea necesario
    >>>    r = session_1.query(User).filter_by(User.id == 1).first()
    >>>    r.username = "user name de prueba)
    >>>    session_1.commit() 
    >>>    return True 

    Args:
    -----
        - object (_type_): _description_
    """    
    def __init__(self, f=None, first_appearance = True):
        self.f = f
        self.first_appearance = first_appearance # se queda con la primera variable local que se llame así o sigue en el stack hasta el principio de los tiempos?

    def __getattribute__(self, name):
        import inspect
        frame = inspect.currentframe()
        if frame is None:
            raise RuntimeError('cannot inspect stack frames')
        sentinel = object()
        frame = frame.f_back
        while frame is not None:
            value = frame.f_locals.get(name, sentinel)
            if value is not sentinel:
                return value
            frame = frame.f_back
        return None
        
        # raise AttributeError(repr(name) + ' not found in any outer scope')

# GLOBAL_SHARED_INTEGRITY_exception_information = {}
# posibles valores para el sistema de INGEGRITY



def look_backwards_for_variable(var_name):
    """
    (c) Seachad - FGV
    
    Description:
    ---------------------- 
        look_backwards_for_variable
        Hace lo mismo que _OuterScopeGetter pero busca hacia atrás hasta encontrar, en el stack, la primera definición de var_name
    
    Extended Description:
    ---------------------
        _extended_summary_
    
    Args:
    -----
            - var_name (_type_): _description_
    
    Returns:
    --------
            _type_: _description_
    """
    import inspect
    found = False
    retorno = None
    # miro hacia atrás hasta que me encuentre el valor de la primera vez que se definión el parámetro
    frame = inspect.currentframe()
    while frame:
        frame_vars = frame.f_locals
        estado = frame_vars.get(var_name, "-") # una variable que no exista... una variable no puede contener "-"
        if estado != "-":
            # tc._print(f"Valor de '{var_name}' encontrado en el stack de llamadas: {estado}", tc.G)
            found = True
            retorno = estado
            break
        frame = frame.f_back
    
    return found, retorno

# decorador para la integridad lógica de cargss de APIs, ficheros, etc... viniendo de las fuentes de datos API_ROBOT, PARSER, SETUP, INTERACTIVE
from functools import partial, wraps
def catch_integrity(func=None, # decorated function
                    *, # <- solo keyword arguments a partir de aquí y tienen que llamarse como se indica
                    integrity_information = {}
                    ):
    """
    (c) Seachad - FGV
    
    Description:
    ---------------------- 
        catch_integrity
        Este decorador se encarga de recoger la información de las funciones de integridad
    
    Extended Description:
    ---------------------
        _extended_summary_
    
    Args:
    -----
            - func (_type_, optional): _description_. Defaults to None.
    """    
    if func is None:
        return partial(catch_integrity, 
                        integrity_information = integrity_information
                       )     
    
    @functools.wraps(func)       
    def call(*args, **kwargs): # <- FUNC 
        try:            
            
            # si __globals no existe, lo creamos!
            # found, _ = look_backwards_for_variable("__globals")
            # if not found:
            #     __globals = Globals()
            # else:
            #     __globals = _
            
            # creamos un timestamp hasta el milisegundo en formato str
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S--%f")
             
            
            # integrity_information = globals_get("integrity_information", {})
            # globals_set("integrity_information", integrity_information)
            
            # from app import look_backwards_for_variable_not_empty
            # ? busco hacia atrás, así me permite encadenar funciones que contengan el decorador sin perder la información, yq eu si pongo el decorador vacío
            # ? como puede ser el caso de catch_exceptions, y no le envío los diccionarios, estos se pierden...
            # ii = look_backwards_for_variable_not_empty("integrity_information")
            
            ii = look_backwards_for_variable("integrity_information")
            found, l_integrity_information = ii
            if found:
                kwargs["integrity_information"] = l_integrity_information
            else:
                kwargs["integrity_information"] = integrity_information
            
            # si tiene timestamp, lo respetamos
            if not "timestamp" in kwargs["integrity_information"]:
                kwargs["integrity_information"]["timestamp"] = timestamp    

            # ? si tenemos client_id, provider_id y tenant_id lo metemos en el diccionario de integridad
            client_id_found, client_id = look_backwards_for_variable("client_id")
            provider_id_found, provider_id =look_backwards_for_variable("provider_id")
            tenant_id_found, tenant_id = look_backwards_for_variable("tenant_id")  
            str_tenant_found, str_tenant = look_backwards_for_variable("str_tenant") # podemos querer usarlos para crear un subdirectorio o cualquier otra información          
            if client_id_found:
                kwargs["integrity_information"]["client_id"] = client_id
            if provider_id_found:
                kwargs["integrity_information"]["provider_id"] = provider_id
            if tenant_id_found:
                kwargs["integrity_information"]["tenant_id"] = tenant_id
            if str_tenant_found:
                kwargs["integrity_information"]["str_tenant"] = str_tenant
            l_integrity_information = kwargs["integrity_information"]    

            # enviamos la función que encadena la información de integridad
            f_integrity_factory = kwargs["integrity_information"].get("f_integrity_factory", None)

            import inspect
            # Get the frame object of the calling function
            frame = inspect.stack()[1].frame

            # Get the module and function name from the frame object
            module = inspect.getmodule(func).__name__
            function_name = func.__name__
            kwargs["integrity_information"]["decorated_function"] = f"{module}.{function_name}"
                
            result = func(*args, **kwargs) # ahora puedo acceder desde func a globals_get("integrity_information") y siempre habrá un diccionario
            # llamamos por defecto a la función de integrity
            integrity_information_function(integrity_information = integrity_information, f_integrity_factory = f_integrity_factory)
            
            # ! TEARDOWN ?
            teardown = integrity_information.get("teardown", {}).get(func.__name__,{})
            if len(teardown):
                module = teardown.get("module", None)
                function = teardown.get("function", None)
                if module != None and function != None:
                    args =  teardown.get("args", [])
                    kwargs = teardown.get("kwargs", {})
                    # intento cargar el módulo
                    m = __import__(module)
                    f = getattr(m, function)
                    f(*args, **kwargs)
            
            return result  
        except Exception as e:
            # tc._print(f"inside_flask: no se ha podido crar el contexto de aplicación: Error reason {e}")
            tc._print(f"ERROR {e}")
            raise e        
        finally:
            a = 999
    return call     


# fuentes de tratamiento de información
Source_SETUP       = "SETUP" # lo que sea mantenimiento del sistema (setup, util, prueba, ...)
Source_API_ROBOT   = "API_ROBOT" # lo que sea api robot o ejecución de APIs (aquí tiene sentido controlar, por ejemplo, los schemas conocidos de JSON que nos vienen (mirar en ijson))
Source_INTERACTIVE = "INTERACTIVE" # lo queo se ejecute desde flask_dashboards
Source_PARSER      = "PARSER" # lo que se ejecute desde el parser de archivos 

# parámetros en el exception_information que es dónde se comunica toda la información de integrity
Integrity_KEY_SYSTEM          = "SYSTEM" # Setup, Interactive, Parser, API_Robot
Integrity_KEY_ITEM            = "ITEM" # item que se está procesando
Integrity_KEY_ADDITIONAL_INFORMATION     = "ADDITIONAL_INFORMATION" # lo queo se ejecute desde flask_dashboards

from functools import partial, wraps
def catch_exceptions(
                    func=None, # decorated function
                    *, # <- solo keyword arguments a partir de aquí y tienen que llamarse como se indica
                    external_callback_function = None, # función inyectada que se llamará si se produción una excepción solamente
                    # ! integrity errors in code
                    exception_information = {}, # diccionario con información lógica, todo lo que no venga se llenará por defecto
                    catch_integrity_information = False,  # trazamos esta función para integrity?
                    # f_integrity_information = None, # función de traza para integrity
                    # f_integrity_exception = None, # función de excepción para integrity
                    # SYSTEM = None, # sistema (API,BBDD,POWERBI,...)
                    # ITEM = None, # item (API, BBDD, POWERBI,...)
                    # ITEM_EXTENDED_INFORMATION = None, # información adicional que se quiera incluir, por defecto llevará el módulo y la función
                    # ERROR_WARNING_CODE = None, # ERROR, WARNING, TRAZA, PRUEBA
                    # CLIENT = None, # cliente tal y como lo conoce SYSTEM
                    # ADDITIONAL_INFORMATION = None, # información adicional que se quiera enviar...
                    # SHARED_INTEGRITY_exception_information = {}  
                    ): # <- WRAPPER 
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    catch_exceptions
    
    Esta función se encarga de capturar cualquier error que se produzca en el código
    Específicamente y si la excepción es una de tipo API_ROBOT_INTEGRITY_Exception llamará a la función que tiene proporcionada en la clase
    para "escupir" toda la información de lo que ha ido mal desde el punto de vista de integridad (SOURCE, SETUP, INTERACTIVE)
    
    Extended Description:
    ---------------------
    La información de INTEGRITY ha de venir en un diccionario con las siguientes claves y explicación. (Si no se propociona información para una clave, se rellena por defecto)

    >>> SYSTEM                          # sistema (API,BBDD,POWERBI,...)
    >>> ITEM                            # item (API, BBDD, POWERBI,...)
    >>> ITEM_EXTENDED_INFORMATION       # cualquier información extendida de ITEM que queramos enviar (se procesa en la función custom que se pueda enviar, por defecto va a ADDITIONAL_INFORMATION)
    >>> ERROR_WARNING_CODE              # ERROR, WARNING, TRAZA, PRUEBA
    >>> CLIENT                          # cliente tal y como lo conoce SYSTEM
    >>> TIMESTAMP                       # por si se quiere un timestamp diferente al que tomaría el decorador por defecto
    >>> ADDITIONAL_INFORMATION          # información adicional que se envía
    
    Adicionalmente, este parámetro SHARED_INTEGRITY_exception_information no se envía (únicamente se recibe por la función decorada)
    # COMUNICACION CON EL DECORATOR CATCH_INTEGRITY
    si quiero comunicar cualquier información interna de mi función (variables locales, por ejemplo: podríamos enviar desde SETUP todo el diccionario configuration de cualquier función, que tiene lo que quiero hacer), 
    de cara a que aparezca en la clave con el diccionario ADDITIONAL_INFORMATION 
    obtengo la referencia a SHARED_INTEGRITY_exception_information (que también me podría venir en kwargs, pero esta manera es más sencilla y no obliga a cambiar la rúbrica de la función, porque
    puede que originalmente no tuviera kwargs)
    SHARED_INTEGRITY_exception_information es un diccionario interno del decorator catch_integrity que nos entrega a cualquier función decorada y trabaja con él de vuelta para integrarlo en 
    ADDITIONAL_INFORMATION dentro de la clave SHARED_INTEGRITY_exception_information. De esta manera si tengo una función de proceso para integrity, recibirá información de proceso de la función decorada, que puede ser necesaria para emeitir algún tipo de información
    particular, tomar decisiones, escribirlo en AUDIT, etc...
    
    Args:
    -----
        - func (_type_, optional): _description_. Defaults to None.
        - external_callback_function (_type_, optional): _description_. Defaults to None.
    
        - exception_information (_type_, optional): _description_. Defaults to {}. Diccionario conteniendo información lógica para las funciones de información y de excepción de integridad
        - catch_integrity_information (_type_, optional): _description_. Defaults to False. Queremos que esta función se informe como traza en el sistema de INTEGRITY?
        
        # - f_integrity_information (_type_, optional): _description_. Defaults to None. Función a la que llamar para informar de que se va a hacer algo en el sistema de INTEGRITY. Solo se llamará si catch_integrity_information = True
        # - f_integrity_exception (_type_, optional): _description_. Defaults to None. Función a la que llamar para informar de que algo ha ido mal en el sistema de INTEGRITY. 	
        # - SYSTEM (_type_, optional): _description_. Defaults to None. Sistema que genera la información de INTEGRITY
        # - ITEM (_type_, optional): _description_. Defaults to None. Item que genera la información de INTEGRITY
        # - ITEM_EXTENDED_INFORMATION (_type_, optional): _description_. Defaults to None. Información extendida del ITEM que genera la información de INTEGRITY
        # - ERROR_WARNING_CODE (_type_, optional): _description_. Defaults to None. Código de error o warning que se genera en el sistema de INTEGRITY
        # - CLIENT (_type_, optional): _description_. Defaults to None. Cliente que genera la información de INTEGRITY
        # - ADDITIONAL_INFORMATION (_type_, optional): _description_. Defaults to None. Información adicional que se envía en el sistema de INTEGRITY
        #     Puede contener las siguientes claves:
        #     - ITEM_EXTENDED_INFORMATION -> el contenido de ITEM_EXTENDED_INFORMATION
        #     - ERROR -> contenido del error de catch_exceptions (cadena) - sólo es útil si se produce un error, se usa en flag_integrity_exception
        #     - ADDITIONAL_KEYS -> diccionario con las claves que no se han usado en el diccionario de información de INTEGRITY
        #     - SHARED_INTEGRITY_exception_information -> cualquier información que la función decorada quiera compartir con el decorador (sólo útil en la parte de flag_integrity_exception)
        #     - INJECTED KWARGS - en el caso específico de que setup.py se esté usando como librería, el decorador inject_kwargs inyecta los kwargs que se le pasan a la función _input, y aparecerían en este diccionario
    
    Returns:
    --------
        _type_: _description_
    """    
    
    if func is None:
        
        return partial(catch_exceptions, external_callback_function = external_callback_function,
                        exception_information = exception_information,
                        catch_integrity_information = catch_integrity_information,
                        # f_integrity_information = f_integrity_information,
                        # f_integrity_exception = f_integrity_exception,
                        # SYSTEM = SYSTEM,
                        # ITEM = ITEM,
                        # ITEM_EXTENDED_INFORMATION = ITEM_EXTENDED_INFORMATION,
                        # ERROR_WARNING_CODE = ERROR_WARNING_CODE,
                        # CLIENT = CLIENT,
                        # ADDITIONAL_INFORMATION = ADDITIONAL_INFORMATION, 
                        # SHARED_INTEGRITY_exception_information = SHARED_INTEGRITY_exception_information                          
                       )        
        
        
        
    @functools.wraps(func)       
    def call(*args, **kwargs): # <- FUNC 
      
        global global_context_name, global_process_name, global_process_reference, global_trace_execution 
        try:
            SHARED_INTEGRITY_exception_information = {}
            mem_args = []
            mem_kwargs = {}
            try:
                mem_args = args
                # mem_kwargs = copy.deepcopy(kwargs)
            except Exception as e:
                print(f"Error en catch exceptions : {e}")
                pass
            if catch_integrity_information == True: # si queremos capturar problemas de integrity se usan solamente dos cosas       
                import inspect
                import datetime
                """ cogemos la información enviada en el exception_information """
                dic = {}
                dic["SYSTEM"]                       = exception_information.get("SYSTEM", unknown) 
                dic["ITEM"]                         = exception_information.get("ITEM", unknown)    # proceso lógico ejecutándose
                dic["ERROR_WARNING_CODE"]           = exception_information.get("ERROR_WARNING_CODE", unknown)
                dic["CLIENT"]                       = exception_information.get("CLIENT", unknown)
                dic["TIMESTAMP"]                    = exception_information.get("TIMESTAMP", datetime.datetime.now())
                dic["ADDITIONAL_INFORMATION"]       = exception_information.get("ADDITIONAL_INFORMATION", {})
                dic["ADDITIONAL_INFORMATION"]["ITEM_EXTENDED_INFORMATION"]    = exception_information.get("ITEM_EXTENDED_INFORMATION", {}) # información adicional sobre el proceso que se está ejecutando
           
                # ! información adicional sobre el frame en que se produce la traza o el error                
                current_script_path = inspect.getsourcefile(func)
                current_script_name = os.path.basename(current_script_path)           
                module = inspect.getmodule(func)
                module_name = module.__name__ if module else "Unknown"            
                dic["PYTHON_INFORMATION"] = {  # información del programa y función que se está ejecutando   
                    "PATH" : current_script_path,
                    "FILE" : current_script_name,
                    "MODULE" : module_name,
                    "FUNCTION" : func.__name__,
                    "ARGS" : mem_args,
                    # "KWARGS" : mem_kwargs,
                }

                # # permitimos cambios en el diccionario enviado                
                # if SYSTEM != None:
                #     dic["SYSTEM"] = SYSTEM
                # if ITEM != None:
                #     dic["ITEM"] = ITEM
                # if ITEM_EXTENDED_INFORMATION != None:
                #     dic["ADDITIONAL_INFORMATION"]["ITEM_EXTENDED_INFORMATION"] = ITEM_EXTENDED_INFORMATION
                # if ERROR_WARNING_CODE != None:
                #     dic["ERROR_WARNING_CODE"] = ERROR_WARNING_CODE
                # if CLIENT != None:
                #     dic["CLIENT"] = CLIENT
                # if ADDITIONAL_INFORMATION != None:
                #     dic["ADDITIONAL_INFORMATION"] = ADDITIONAL_INFORMATION
                
                # ! toda las claves no conocidas, se meten como claves dentro de ADDITIONAL_INFORMATION
                dic["ADDITIONAL_INFORMATION"]["ADDITIONAL_KEYS"] = {}                
                for k,v in exception_information.items():
                    if not k in exception_information_known_keys:
                        dic["ADDITIONAL_INFORMATION"]["ADDITIONAL_KEYS"][k] = v                   
                
                # if f_integrity_information != None:
                #     f_integrity_information(dic) # llamamos a la función de traza de integridad para informar de una tarea que pretendemos realizar
                # else:
                #     integrity_information_function(dic) # función por defecto de gestión de información (traza) de integridad
                SHARED_INTEGRITY_exception_information = dic
                kwargs["exception_information"] = dic
            value = func(*args, **kwargs)
            return value
        except Exception as e:
            # buscamos si en el stack hay una primera función decorada que ha establecido que hay que hacer el control de INTEGRITY
            mem_catch_integrity_information = catch_integrity_information
            found, retorno = look_backwards_for_variable("catch_integrity_information")
            if found:
                mem_catch_integrity_information = retorno
            
            # detailed error
            exc_type, exc_value, exc_tb = sys.exc_info()
            cadena = f"{exc_type} :-: {exc_value} :-: {exc_tb}"
            just_the_string = traceback.format_exc()
            cadena = just_the_string + "\n" + cadena            
            
            # * metemos información de la página y dónde se puede haber producido el error, si es que existe esa información
            dispatched = ""
            dispatched_formatted = ""
            
            # información de página si el error viene de una última interactuación con el usuario	
            __have_page_information = False
            __page = ""
            __user_logged = ""
            __user_impersonated = ""            
            o = OuterScopeGetter()
            try:
                from app import globals_get
                dispatched = globals_get("dispatched", {})
                if len(dispatched) != 0:
                    dispatched_formatted = f"{tc.Y}{dispatched}\n: \t"
                # información de la página    
                __page = dispatched.get("page", "")
                __user_logged = dispatched.get("user_logged", "")
                __user_impersonated = dispatched.get("user_impersonated", "")
                
                __have_page_information = True
                
            except Exception as e1:
                a = 999
            
            tc._print(f"{dispatched_formatted}from ar_decorator_functions.catch_exceptions: \n{cadena}", tc.R) # imprimo el error  

            """ INTEGRITY ERRORS - Exceptions """
            """ control de errores de integridad de flask_dashboards, de todos los programas que se supone que tienen que obtener datos para clientes (SOURCES) """
            if mem_catch_integrity_information == True: # si queremos hacer traza de la función       
                # new 
                import inspect
                import datetime
                # OJO! no se pueden asignar valores a variables que se hayan recibido por el decorador desde dentro de esta zona, da ERROR de variable local no existe
                mem_exception_information = exception_information # me quedo con el valor que tenía exception_information cuando se ha producido el error
                found, retorno = look_backwards_for_variable("exception_information") # miro si hay una deficinión más profunda en el stack
                if found:
                    mem_exception_information = retorno

                """ cogemos la información enviada en el exception_information """
                dic = {}
                dic["SYSTEM"]                       = mem_exception_information.get("SYSTEM", unknown) 
                dic["ITEM"]                         = mem_exception_information.get("ITEM", unknown)    # proceso lógico ejecutándose
                dic["ERROR_WARNING_CODE"]           = mem_exception_information.get("ERROR_WARNING_CODE", "ERROR")
                dic["CLIENT"]                       = mem_exception_information.get("CLIENT", unknown)
                dic["TIMESTAMP"]                    = mem_exception_information.get("TIMESTAMP", datetime.datetime.now())
                dic["ADDITIONAL_INFORMATION"]       = mem_exception_information.get("ADDITIONAL_INFORMATION", {})
                dic["ADDITIONAL_INFORMATION"]["ITEM_EXTENDED_INFORMATION"]    = mem_exception_information.get("ITEM_EXTENDED_INFORMATION", {}) # información adicional sobre el proceso que se está ejecutando
                
                
             
                # ! información adicional sobre el frame en que se produce la traza o el error                
        
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback_details = traceback.extract_tb(exc_traceback)[-1]
                module_name = traceback_details.filename
                function_name = traceback_details.name
                line_number = traceback_details.lineno
                error_message = str(exc_value)

                error_information = {
                    "module": module_name,
                    "function": function_name,
                    "line_number": line_number,
                    "error_message": error_message
                }        
        
                module = inspect.getmodule(func)
                module_name = module.__name__ if module else "Unknown"            
                dic["PYTHON_INFORMATION"] = {  # información del programa y función que se está ejecutando   
                    "FILE" : __file__,
                    "FUNCTION" : func.__name__,
                    "ARGS" : mem_args,
                    "error_information" : error_information,
                }

                integrity_exception_function(dic) # función por defecto de gestión de excepciones de integridad

            # ! FUNCIONES DE PROCESO y PERSISTENCIA DE LA EXCEPCION

            """ FUNCTION DE CAPTURA DE EXCEPTION EXTERNA no integrity """
            # en flask_dashboards lo mete en AUDIT
            # ! GLOBAL FUNCTION para todo el sistema
            global catch_exceptions_external_function
            if not catch_exceptions_external_function == None:
                catch_exceptions_external_function(cadena) # llama a la función de proceso externa con la cadena construida con el error
            # ----------------------------------------------------------------------
            # nuevo, si se le manda una función a la instancia del decorator (sólo para esa ejecución de la función concreta), 
            # llamará a esa función con el contenido de todas las varables locales de la función que ha producido el error MAGIA POTAGIA
            # ----------------------------------------------------------------------
            # ! LOCAL FUNCTION, sólo para esta función
            if not external_callback_function == None:
                dic = locals_on_error() # dic contiene todas las variables locales de la función que ha producido el error
                dic["resultado"] = "ERROR"
                dic["additional_information"] = cadena
                external_callback_function(dic)

            # debemos detener el script????
            stop_programa = False

            # ! EXCEPCIONES específicas que pueden llevar una función de proceso
            """ API_ROBOT_INTEGRITY_Exception """
            # cualquier función puede hacer raise de una excepción de integridad...
            if isinstance(e, API_ROBOT_INTEGRITY_Exception):
                dic = e._exception_information
                tc._print(f"API_ROBOT_INTEGRITY_Exception: {e.message} - {dic}", tc.R)
                f_to_call = e.f_to_call             
                   
                if f_to_call != None:
                    f_to_call(exception_information = dic) # llamamos a la función de traza de integridad para informar de una tarea que pretendemos realizar
                    
                # en cualquier caso siempre llamamos a la función factory de integrity    
                integrity_exception_function(exception_information = dic) # por defecto la función de API_ROBOT (lo mete en el fichero y directorio de API_ROBOT)
                    
                if e._stop_program:
                    stop_programa = True # por si obligamos a que se detenga el programa ante un error grave!
            
            """ DEBE PARARSE EL PROGRAMA??? """            
            if isinstance(e, API_ROBOT_Exception):
                if e._stop_program:
                    stop_programa = True # por si obligamos a que se detenga el programa ante un error grave!

            """ fichero de traza de error con toda la información y bbdd """
            # ! ERROR en la clave CM_err_folder del fichero de configuración apirobot.json
            dispatched_info = f"{__page}_{__user_logged}_{__user_impersonated}"
            _flush_error(cadena, 
                        namefile = f"{global_context_name}_{dispatched_info}_{func.__name__}_", # esta es la parte PRE del nombre del fichero, si no digo nada le va a meter, además, el timestamp
                        ) 
            
            if stop_programa:
                sys.exit(-1)    
    
    return call  
# return decorate(external_func_to_call) if callable(external_func_to_call) else decorate

# def catch_exceptions(
#                     func=None, # decorated function
#                     *, # <- solo keyword arguments a partir de aquí y tienen que llamarse como se indica
#                     external_callback_function = None, # función inyectada que se llamará si se produción una excepción solamente
#                     exception_information = {}, # diccionario con información lógica, todo lo que no venga se llenará por defecto
#                     catch_integrity_information = None,  # trazamos esta función para integrity?
#                     f_integrity_information = None, # función de traza para integrity
#                     f_integrity_exception = None, # función de excepción para integrity
#                     SYSTEM = None, # sistema (API,BBDD,POWERBI,...)
#                     ITEM = None, # item (API, BBDD, POWERBI,...)
#                     ITEM_EXTENDED_INFORMATION = None, # información adicional que se quiera incluir, por defecto llevará el módulo y la función
#                     ERROR_WARNING_CODE = None, # ERROR, WARNING, TRAZA, PRUEBA
#                     CLIENT = None, # cliente tal y como lo conoce SYSTEM
#                     ADDITIONAL_INFORMATION = None, # información adicional que se quiera enviar...
#                     SHARED_INTEGRITY_exception_information = {}  
#                     ): # <- WRAPPER 
#     """
#     (c) Seachad
    
#     Description:
#     ---------------------- 
#     catch_exceptions
    
#     Esta función se encarga de capturar cualquier error que se produzca en el código
#     Específicamente y si la excepción es una de tipo API_ROBOT_INTEGRITY_Exception llamará a la función que tiene proporcionada en la clase
#     para "escupir" toda la información de lo que ha ido mal desde el punto de vista de integridad (SOURCE, SETUP, INTERACTIVE)
    
#     Extended Description:
#     ---------------------
#     La información de INTEGRITY ha de venir en un diccionario con las siguientes claves y explicación. (Si no se propociona información para una clave, se rellena por defecto)

#     >>> SYSTEM                          # sistema (API,BBDD,POWERBI,...)
#     >>> ITEM                            # item (API, BBDD, POWERBI,...)
#     >>> ITEM_EXTENDED_INFORMATION       # cualquier información extendida de ITEM que queramos enviar (se procesa en la función custom que se pueda enviar, por defecto va a ADDITIONAL_INFORMATION)
#     >>> ERROR_WARNING_CODE              # ERROR, WARNING, TRAZA, PRUEBA
#     >>> CLIENT                          # cliente tal y como lo conoce SYSTEM
#     >>> TIMESTAMP                       # por si se quiere un timestamp diferente al que tomaría el decorador por defecto
#     >>> ADDITIONAL_INFORMATION          # información adicional que se envía
    
#     Adicionalmente, este parámetro SHARED_INTEGRITY_exception_information no se envía (únicamente se recibe por la función decorada)
#     # COMUNICACION CON EL DECORATOR CATCH_INTEGRITY
#     si quiero comunicar cualquier información interna de mi función (variables locales, por ejemplo: podríamos enviar desde SETUP todo el diccionario configuration de cualquier función, que tiene lo que quiero hacer), 
#     de cara a que aparezca en la clave con el diccionario ADDITIONAL_INFORMATION 
#     obtengo la referencia a SHARED_INTEGRITY_exception_information (que también me podría venir en kwargs, pero esta manera es más sencilla y no obliga a cambiar la rúbrica de la función, porque
#     puede que originalmente no tuviera kwargs)
#     SHARED_INTEGRITY_exception_information es un diccionario interno del decorator catch_integrity que nos entrega a cualquier función decorada y trabaja con él de vuelta para integrarlo en 
#     ADDITIONAL_INFORMATION dentro de la clave SHARED_INTEGRITY_exception_information. De esta manera si tengo una función de proceso para integrity, recibirá información de proceso de la función decorada, que puede ser necesaria para emeitir algún tipo de información
#     particular, tomar decisiones, escribirlo en AUDIT, etc...
    
#     Args:
#     -----
#         - func (_type_, optional): _description_. Defaults to None.
#         - external_callback_function (_type_, optional): _description_. Defaults to None.
    
#         - exception_information (_type_, optional): _description_. Defaults to {}. Diccionario conteniendo información lógica para las funciones de información y de excepción de integridad
#         - catch_integrity_information (_type_, optional): _description_. Defaults to False. Queremos que esta función se informe como traza en el sistema de INTEGRITY?
#         - flag_integrity_exception (_type_, optional): _description_. Defaults to False. Queremos que esta función se informe cuando algo va mal en el sistema de INTEGRITY?
#         - f_integrity_information (_type_, optional): _description_. Defaults to None. Función a la que llamar para informar de que se va a hacer algo en el sistema de INTEGRITY. Solo se llamará si catch_integrity_information = True
#         - f_integrity_exception (_type_, optional): _description_. Defaults to None. Función a la que llamar para informar de que algo ha ido mal en el sistema de INTEGRITY. Solo se llamará si flag_integrity_exception = True	
#         - SYSTEM (_type_, optional): _description_. Defaults to None. Sistema que genera la información de INTEGRITY
#         - ITEM (_type_, optional): _description_. Defaults to None. Item que genera la información de INTEGRITY
#         - ITEM_EXTENDED_INFORMATION (_type_, optional): _description_. Defaults to None. Información extendida del ITEM que genera la información de INTEGRITY
#         - ERROR_WARNING_CODE (_type_, optional): _description_. Defaults to None. Código de error o warning que se genera en el sistema de INTEGRITY
#         - CLIENT (_type_, optional): _description_. Defaults to None. Cliente que genera la información de INTEGRITY
#         - ADDITIONAL_INFORMATION (_type_, optional): _description_. Defaults to None. Información adicional que se envía en el sistema de INTEGRITY
#             Puede contener las siguientes claves:
#             - ITEM_EXTENDED_INFORMATION -> el contenido de ITEM_EXTENDED_INFORMATION
#             - ERROR -> contenido del error de catch_exceptions (cadena) - sólo es útil si se produce un error, se usa en flag_integrity_exception
#             - ADDITIONAL_KEYS -> diccionario con las claves que no se han usado en el diccionario de información de INTEGRITY
#             - SHARED_INTEGRITY_exception_information -> cualquier información que la función decorada quiera compartir con el decorador (sólo útil en la parte de flag_integrity_exception)
#             - INJECTED KWARGS - en el caso específico de que setup.py se esté usando como librería, el decorador inject_kwargs inyecta los kwargs que se le pasan a la función _input, y aparecerían en este diccionario
    
#     Returns:
#     --------
#         _type_: _description_
#     """    
    
#     if func is None:
        
#         return partial(catch_exceptions, external_callback_function = external_callback_function,
#                         exception_information = exception_information,
#                         catch_integrity_information = catch_integrity_information,
#                         f_integrity_information = f_integrity_information,
#                         f_integrity_exception = f_integrity_exception,
#                         SYSTEM = SYSTEM,
#                         ITEM = ITEM,
#                         ITEM_EXTENDED_INFORMATION = ITEM_EXTENDED_INFORMATION,
#                         ERROR_WARNING_CODE = ERROR_WARNING_CODE,
#                         CLIENT = CLIENT,
#                         ADDITIONAL_INFORMATION = ADDITIONAL_INFORMATION, 
#                         SHARED_INTEGRITY_exception_information = SHARED_INTEGRITY_exception_information                          
#                        )        
        
        
        
#     @functools.wraps(func)       
#     def call(*args, **kwargs): # <- FUNC 
      
#         global global_context_name, global_process_name, global_process_reference, global_trace_execution 
#         try:
#             """ cogemos la información enviada en el exception_information """
#             if catch_integrity_information == 1 or catch_integrity_information == 3: # si queremos hacer traza de la función       
#                 import inspect
#                 import datetime
#                 """ cogemos la información enviada en el exception_information """
#                 dic = {}
#                 dic["SYSTEM"]                       = exception_information.get("SYSTEM", "Unknown") 
#                 dic["ITEM"]                         = exception_information.get("ITEM", "Unknown")    # proceso lógico ejecutándose
#                 dic["ERROR_WARNING_CODE"]           = exception_information.get("ERROR_WARNING_CODE", "TRAZA")
#                 dic["CLIENT"]                       = exception_information.get("CLIENT", global_client_name)
#                 dic["TIMESTAMP"]                    = exception_information.get("TIMESTAMP", datetime.datetime.now())
#                 dic["ADDITIONAL_INFORMATION"]       = exception_information.get("ADDITIONAL_INFORMATION", {})
#                 dic["ADDITIONAL_INFORMATION"]["ITEM_EXTENDED_INFORMATION"]    = exception_information.get("ITEM_EXTENDED_INFORMATION", {}) # información adicional sobre el proceso que se está ejecutando
            
            
#             if exception_information:
#                 tc._print(f"exception_information has content: {exception_information}")
#             else:
#                 tc._print("exception_information is empty.")            
            
#             value = func(*args, **kwargs)
#             return value
#         except Exception as e:
#             # buscamos si en el stack hay una primera función decorada que ha establecido que hay que hacer el control de INTEGRITY
#             # found, retorno = look_backwards_for_variable("catch_integrity_information")
#             # if found:
#             #     catch_integrity_information = retorno
            
            
#             # detailed error
#             exc_type, exc_value, exc_tb = sys.exc_info()
#             cadena = f"{exc_type} :-: {exc_value} :-: {exc_tb}"
#             just_the_string = traceback.format_exc()
#             cadena = just_the_string + "\n" + cadena            
            
#             tc._print(cadena, tc.R) # imprimo el error  

#             """ INTEGRITY ERRORS - Exceptions """
#             """ control de errores de integridad de flask_dashboards, de todos los programas que se supone que tienen que obtener datos para clientes (SOURCES) """
#             # new 
#             import inspect
#             import datetime
#             if catch_integrity_information == 2 or catch_integrity_information == 3: # si queremos hacer traza de la función       
#                 tc._print(f"EN ERROR -> {exception_information}")
#             #     # new 
#             #     import inspect
#             #     import datetime
#                 found, retorno = look_backwards_for_variable("exception_information")
#                 if found:
#                     exception_information = retorno

#             #     """ cogemos la información enviada en el exception_information """
#                 dic = {}
#                 dic["SYSTEM"]                       = exception_information.get("SYSTEM", "Unknown") 
#                 dic["ITEM"]                         = exception_information.get("ITEM", "Unknown")    # proceso lógico ejecutándose
#                 dic["ITEM_EXTENDED_INFORMATION"]    = exception_information.get("ITEM_EXTENDED_INFORMATION", {}) # información adicional sobre el proceso que se está ejecutando
#                 dic["ERROR_WARNING_CODE"]           = exception_information.get("ERROR_WARNING_CODE", "ERROR")
#                 dic["CLIENT"]                       = exception_information.get("CLIENT", global_client_name)
#                 dic["TIMESTAMP"]                    = exception_information.get("TIMESTAMP", datetime.datetime.now())
#                 dic["ADDITIONAL_INFORMATION"]       = exception_information.get("ADDITIONAL_INFORMATION", {})
             
#             #     # información adicional sobre el frame en que se produce la traza o el error                
#             #     current_script_path = inspect.getsourcefile(func)
#             #     current_script_name = os.path.basename(current_script_path)           
#             #     module = inspect.getmodule(func)
#             #     module_name = module.__name__ if module else "Unknown"            
#             #     dic["PYTHON_INFORMATION"] = {  # información del programa y función que se está ejecutando   
#             #         "PATH" : current_script_path,
#             #         "FILE" : current_script_name,
#             #         "MODULE" : module_name,
#             #         "FUNCTION" : func.__name__,
#             #     }
            
#             tc._print(f"EN ERROR -> {exception_information}")

#             """ FUNCTION DE CAPTURA DE EXCEPTION EXTERNA """
#             global catch_exceptions_external_function
#             if not catch_exceptions_external_function == None:
#                 catch_exceptions_external_function(cadena) # llama a la función de proceso externa con la cadena construida con el error
#             # ----------------------------------------------------------------------
#             # nuevo, si se le manda una función a la instancia del decorator (sólo para esa ejecución de la función concreta), 
#             # llamará a esa función con el contenido de todas las varables locales de la función que ha producido el error MAGIA POTAGIA
#             # ----------------------------------------------------------------------
#             if not external_callback_function == None:
#                 dic = locals_on_error() # dic contiene todas las variables locales de la función que ha producido el error
#                 dic["resultado"] = "ERROR"
#                 dic["additional_information"] = cadena
#                 external_callback_function(dic)

#             # debemos detener el script????
#             stop_programa = False
            
#             # """ API_ROBOT_INTEGRITY_Exception """
#             # # cualquier función puede hacer raise de una excepción de integridad...
#             # if isinstance(e, API_ROBOT_INTEGRITY_Exception):
#             #     dic = e._exception_information
#             #     tc._print(f"API_ROBOT_INTEGRITY_Exception: {e.message} - {dic['SYSTEM']} {dic['ITEM']} {dic['ERROR_WARNING_CODE']} {dic['CLIENT']} {dic['ADDITIONAL_INFORMATION']}", tc.R)
#             #     f_to_call = e.f_to_call                
#             #     if f_to_call != None:
#             #         f_to_call(exception_information = dic) # llamamos a la función de traza de integridad para informar de una tarea que pretendemos realizar
#             #     else:
#             #         integrity_exception_function(exception_information = dic) # por defecto la función de API_ROBOT (lo mete en el fichero y directorio de API_ROBOT)
#             #     if e._stop_program:
#             #         stop_programa = True # por si obligamos a que se detenga el programa ante un error grave!
            
#             """ DEBE PARARSE EL PROGRAMA??? """            
#             if isinstance(e, API_ROBOT_Exception):
#                 if e._stop_program:
#                     stop_programa = True # por si obligamos a que se detenga el programa ante un error grave!

#             """ fichero de traza de error con toda la información """
#             _flush_error(cadena, 
#                         namefile = f"{global_context_name}_{func.__name__}_", # esta es la parte PRE del nombre del fichero, si no digo nada le va a meter, además, el timestamp
#                         ) 
            
#             if stop_programa:
#                 sys.exit(-1)    
    
#     return call  
# # return decorate(external_func_to_call) if callable(external_func_to_call) else decorate



# source: https://stackoverflow.com/questions/4214936/how-can-i-get-the-values-of-the-locals-of-a-function-after-it-has-been-executed
import sys
# =============================================================================
# Acceder a variables locales desde otra función
# =============================================================================
def call_function_get_frame(func, *args, **kwargs):
  """
  Calls the function *func* with the specified arguments and keyword
  arguments and snatches its local frame before it actually executes.
  """

  frame = None
  trace = sys.gettrace()
  def snatch_locals(_frame, name, arg):
    nonlocal frame
    if frame is None and name == 'call':
      frame = _frame
      sys.settrace(trace)
    return trace
  sys.settrace(snatch_locals)
  try:
    result = func(*args, **kwargs)
  finally:
    sys.settrace(trace)
  return frame, result

import types

def namespace_decorator(func):
  frame, result = call_function_get_frame(func)
  try:
    module = types.ModuleType(func.__name__)
    module.__dict__.update(frame.f_locals)
    return module
  finally:
    del frame
    
# fin Acceder a variables locales desde otra función


# =============================================================================
# StackTrace decorator
# =============================================================================
# nuevo stack_trace
# source: https://gist.github.com/socrateslee/4011475
        
class StackTrace(object):
    def __init__(self, with_call=True, with_return=False,
                       with_exception=False, max_depth=-1):
        self._frame_dict = {}
        self._options = set()
        self._max_depth = max_depth
        if with_call: self._options.add('call')
        if with_return: self._options.add('return')
        if with_exception: self._options.add('exception')

    def __call__(self, frame, event, arg):
        ret = []
        if event == 'call':
            back_frame = frame.f_back
            if back_frame in self._frame_dict:
                self._frame_dict[frame] = self._frame_dict[back_frame] + 1
            else:
                self._frame_dict[frame] = 0

        depth = self._frame_dict[frame]

        if event in self._options\
          and (self._max_depth<0\
               or depth <= self._max_depth):
            ret.append(frame.f_code.co_name)
            ret.append('[%s]'%event)
            if event == 'return':
                ret.append(arg)
            elif event == 'exception':
                ret.append(repr(arg[0]))
            ret.append('in %s line:%s'%(frame.f_code.co_filename, frame.f_lineno))
        if ret:
            tc._print("%s%s"%('  '*depth, '\t'.join([str(i) for i in ret])))

        return self

def stack_trace(**kw):
    def entangle(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            st = StackTrace(**kw)
            sys.settrace(st)
            try:
                return func(*args, **kwargs)
            finally:
                sys.settrace(None)
        return wrapper
    return entangle

@catch_exceptions
def catcheable_function(dic):
    d = dic.copy() # tiene que dar un error porque string no tiene copy()

@time_control
def test():
    a=0
    for n in range(0,10000000):
        a += 1
    
    pass

if __name__ == "__main__":
    dic = "hola mundo"
    catcheable_function(dic)
    
    # common._print("Hola")
    # common._print("Mundo", common.Y)
    # for i in range(1,100):
    #     common._print(f"{i}", common.G)
    
  



