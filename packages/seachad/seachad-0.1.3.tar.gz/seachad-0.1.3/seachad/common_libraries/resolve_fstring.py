# -*- coding: utf-8 -*-
r"""
Created on Wed Jun 16 19:54:45 2021

@author: Fernando

Description:
------------

    Trabajos intensivos con fstrings construidas dinámicamente.
    Modificación de diccionarios y listas (JSON).
    Trabajo con cadenas


Functions:
----------

    - left : obtiene caracteres a la izquierda de una string 
    - rigt : obtiene caracteres a la derecha de una string
    - mid : obtiene una serie de caracteres desde una posición, en un string

"""
# from curses.ascii import isdigit
import sys

import seachad.common_libraries.terminal_colors as tc

import winreg
def get_user_env(name):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment")
    # ojo, cambiado el 4/9/2021 -> posibles e
    retorno = None
    try:
        retorno = winreg.QueryValueEx(key, name)[0]
    except:
        retorno = None
    return retorno


timestamp_ymd_format = "%Y-%m-%d"
# timestamp_hms_format = "%H-%M-%S-%f"
timestamp_hms_format = "%H-%M-%S"
timestamp_format = f"{timestamp_ymd_format}_{timestamp_hms_format}"

def timestamp(timestamp_format = timestamp_format):
    """
    Devuelve el timestamp del momento

    Returns
    -------
    ymd_hms : TYPE
        DESCRIPTION.

    """
    from datetime import datetime
    ymd_hms = datetime.now().strftime(timestamp_format)
    return ymd_hms   
    
# =============================================================================
# Devuelve YMD de un timestamp que se le envía en formato string, si no se le envía nada envía YMD de ahora mismo
# =============================================================================
def timestamp_ymd( str_timestamp = None, timestamp_format = timestamp_ymd_format):
    """
    Devuelve el timestamp sólo para YYMMDD

    Parameters
    ----------
    str_timestamp : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    ymd : TYPE str
        DESCRIPTION.

    """
    from datetime import datetime
    ymd = datetime.now().strftime(timestamp_format)
    # date = datetime.strptime(str_timestamp, timestamp_format)
    # ymd = date.strftime(timestamp_ymd_format)
    return ymd   

# =============================================================================
# Devuelve HMS de un timestamp que se le envía en formato string, si no se le envía nada envía HMS de ahora mismo
# =============================================================================
def timestamp_hms(str_timestamp = None, timestamp_format = timestamp_hms_format ):
    """
    Devuelve el timestamp para hhmmss

    Parameters
    ----------
    str_timestamp : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    hms : TYPE str
        DESCRIPTION.

    """
    
    
    from datetime import datetime
    hms = datetime.now().strftime(timestamp_format)    
    # date = datetime.strptime(str_timestamp, timestamp_format)
    # hms = datetime.strftime(timestamp_hms_format)
    return hms 



# ---- .
# ---- Resolución de fstrings dinámica 


def find_value(key: "clave a buscar - debe ser str" = "", 
               list_of_dictionaries: "lista de diccionarios o diccionario en el que buscar" = []):
    """
    encuentra, en modo recursivo, el valor de una clave, en una lista de diccionarios
    sólo busca hasta que encuentra una aparición de la clave
    en un JSON no buscará más allá del primer diccionario en que se encuentre la clave

    Parameters
    ----------
    key : TYPE string
        DESCRIPTION. clave de la que se desea encontrar el valor
    list_of_dictionaries : TYPE, optional
        DESCRIPTION. The default is []. diccionario o lista de diccionarios

    Returns
    -------
    None. nombre del parámetro, su valor (si no lo ha encontrado devolvera como valor = None) y el diccionario dónde se ha encontrado

    """
    found, valor, d = get_key_dictionary_in_dictionary(list_of_dictionaries, k = key)
    if found:
        return key, valor, d
    else:
        return key, None, None


# esta sección va a poder cogerse directamente desde IPL porque lo tiene allí cargado
def get_key_dictionary_in_dictionary(d, k = None):
    """ busca si la clave k está en d, si es así devuelve True, en otro caso devuelve False 
    devuelve también el valor encontrado
    opera en modo recursivo
    
    devuelve el valor y el diccionario que la contiene
    
    """
    
    retorno = False

    if not isinstance(k, str): # la clave tiene que ser un string!!!
        raise Exception(f"get_key_in_dictionary: {k} no es una clave válida (no es str!!!)")
        return None, None, None
        
    if isinstance(d, list): # si es una lista, rastreo todos los elementos
        for l in d:
            retorno, valor, dic = get_key_dictionary_in_dictionary(l, k)
            if retorno == True: # ha encontrado algo!
                return True, valor, dic
    
    if not isinstance(d, dict): # si no es un diccionario, no puedo seguir!
        return None, None, None

    if k in d: # si está la clave
        return True, d[k], d
    
    for lk,lv in d.items():
        if isinstance(lv,list):
            for i in lv: # cada i es un diccionario
                retorno, valor, dic = get_key_dictionary_in_dictionary(i, k)
                if retorno == True:
                    return True, valor, dic
        if isinstance(lv,dict): # si tengo un diccionario como valor, también busco
            retorno, valor, dic = get_key_dictionary_in_dictionary(lv, k)
            if retorno == True:
                return True, valor, dic               
        
    return retorno, None, None

# # crea f_strings dinámicas para resolver claves de diccionarios (del diccionario que recibe)
# # la orden de búsqueda es en el diccionario actual, en el diccionario padre o en access
def make_magic(current_dictionary = None,# diccionario desde el que he obtenido el valor
               target_dictionary = None, # diccionario en el que buscar
               key = None, # clave sobre la que he operado en el diccionario original
               magic = None,
               param_delimiter = "_PARAM_"): # clave que buscamos en el diccionario target
    res = -1
    
    # tenemos que evitar que una clave se esté dirigiendo a sí misma, por ejemplo
    # "client_id" : "{client_id}"

    l_params = {}
    

    if "{" in magic and "}" in magic: # si está entre {} hay que resolver la magia -> tiene que haber dos (cuidado si algún valor viene con cosas raras como UUID, secrets o algo que pueda traer estos caracteres porque podría dar un error, aunque no creo que se resuelva)     
    # en el caso de que magic sea una lista de campos entre {} (es decir, que lleve varios campos), los sacamos todos y limpiamos
        # 20200912 -> arreglado el control de si la clave se encuentra como parámetro o dentro de la lista de parametros cuando se busca dentro del mismo diccionario
        # si la clave aparece en la lista, entonces no es resoluble en este nivel    
        import re
        start_delimiter = "{"
        end_delimiter = "}"
        regex_patron = r"{start_delimiter}[\w\d+-:]+{end_delimiter}".format(
            start_delimiter = start_delimiter,
            end_delimiter = end_delimiter) # buscamos secuencias de palabras dígitos, signos + y menos y : entre @
        # quitar
        # key = "scope_base"
        # magic = "{scope_base}/{authority_uri}/{scope_end}"
        # fin quitar
        cadena = magic
        comandos = re.findall(regex_patron, cadena)
        is_in = False
        # limpiamos la lista
        for comando in comandos:
            comando = comando.replace(start_delimiter, "")
            comando = comando.replace(end_delimiter, "")
            if key == comando:
                is_in = True # está dentro, no podemos resolver...
                break
        
        # if current_dictionary == target_dictionary and key in magic: # si estoy buscando en el diccionario actual y la clave se corresponde con lo que busco entre {} (quiero evitar que se crea que lo ha encontrado cuando, por ejemplo: "scope_base" : "{scope_base}")
        if current_dictionary == target_dictionary and is_in: # si estoy buscando en el diccionario actual y la clave se corresponde con lo que busco entre {} (quiero evitar que se crea que lo ha encontrado cuando, por ejemplo: "scope_base" : "{scope_base}")
            magic = None
            res = -1                        
        else:
            lmagic = magic
            magic = magic.replace("{", "{target_dictionary[\"")
            magic = magic.replace("}", "\"]}")
            # common._print(magic)

            # intento recoger la lista de parámetros que puede venir            
            _,_,l_params = get_fstring_parameters(cadena = lmagic, 
                                                param_delimiter = param_delimiter,          
                                                start_delimiter = "{", 
                                                end_delimiter = "}", 
                                                identificador = "@", 
                                                limpiar_delimiters = False) 
            
            
            string = "f" + "'" + magic + "'"  # intento resolver un fstring con target_dictionary y la clave que me ha llegado
            try:     
                res = 0
                magic = eval(string)
                # si lo que obtengo contiene los delimiters, quiere decir que no es un valor, es algo a buscar en otro diccionario
                if "{" in magic and "}" in magic:
                    res = 2
                # common._print(magic, common.CYAN)    
            except: # notificamos que no se ha resuelto dentro del traget_dictionary
                res = -1
#                 cambio el 23/10/2020 - quiero que magic contenga el valor de string, aunque no haya encontrado nada...
                magic = None
#                magic = string
                # common._print(f"La clave {string} no existe", common.RED)
                pass                
    else: # como no está entre {} se supone que es un valor
        res = -1 # no hay cambio
        magic = current_dictionary[key]

    return res, magic, l_params

# =============================================================================
# # obtiene una lista de elementos contenidos entre los separadores (probablemente{}), se pueden limpiar los separadores (delimiters)
# # devuelve una lista conteniendo el elemento, y el identificador+elemento y, adicionalmente, la cadena original sustituyendo los elementos por identificador+elemento para posteriormente 
# # poder cambiar los valores    
# =============================================================================
def get_fstring_parameters(cadena = "{authority_host_uri}/_PARAM_{tenant_id}/_PARAM_{token_postfix}", # cadena que nos llega con elementos que deberían ser tratados como f-string
                           param_delimiter = "_PARAM_", # delimitador de parámetro para cargar la lista interna de parámetros de este API_call
                           start_delimiter = "{", # delimitador de comienzo de parámetro
                           end_delimiter = "}", # delimitador de fin de parámetro
                           identificador = "@", # en la cadena temporal de ubicación original del parámetro, qué voy a usar para identificarlo - produciría algo así @{authority_host_uri}/@{tenant_id}/@{token_postfix}
                           limpiar_delimiters = False, # cuando devuelvo los parámetros les quito los delimitadores? ({ y }, por ejemplo).
                           escupe = False,
                           ):
    """ devuelve una lista de parámetros (entendido como algo entre {}) en la forma:
        [parámetro, @+parametro]
        [@parametro]
        [_PARAM_parametro, _PARAM_@parametro]
        
        si se le manda limpiar_delimiters a True, quitará {} y _PARAM_
    """
    import re
    
    dict_params = {} # identificamos y devolvemos todo lo que sean _PARAM_, conteniendo su identificador y su valor
    
    cadena_cambiada = cadena # nos quedamos con la cadena original, donde sustituiremos lo que encontramos por algún tipo de identificador
    parameter = []
    lista_parameters = []

    if isinstance(cadena, str): # ojo, solo podemos operar con cadenas!
        _params = param_delimiter # obligamos a una búsqueda de _PARAM_
    
    
        """ _PARAM_ """
        start_delimiter_acumulado = f"{_params}{start_delimiter}"
        # buscamos primero con _PARAMS_, obtengo la información, y luego quito _PARAMS_
        patron_comando_params = r"{start_delimiter}[\w\d+-:]+{end_delimiter}".format(
                start_delimiter = start_delimiter_acumulado,
                end_delimiter = end_delimiter) # buscamos secuencias de palabras dígitos, signos + y menos y : entre @    
    
        regex_patron_params = patron_comando_params
        comandos = re.findall(regex_patron_params, cadena)
        if len(comandos)>0: # no es un comando
            for i in comandos:
                parameter = []
                if limpiar_delimiters:
                    i = i.replace(start_delimiter_acumulado,"")
                    i = i.replace(end_delimiter,"")
                else:
                    # construimos el identificador en la misma manera que se espera 
                    s_from = f"{_params}"
                    s_target = f"{_params}{identificador}"
                    i_con_identificador = i
                    i_con_identificador = i_con_identificador.replace(s_from, s_target)
                    # ahora le quito _params
                    i = i.replace(_params, "")
                    i_con_identificador = i_con_identificador.replace(_params, "")
                dict_params[i] = i_con_identificador # de momento lo dejamos vacío?
    
        """ LISTA DE COMANDOS """
        # obtenemos la lista de comandos    
        patron_comando = r"{start_delimiter}[\w\d+-:]+{end_delimiter}".format(
                start_delimiter = start_delimiter,
                end_delimiter = end_delimiter) # buscamos secuencias de palabras dígitos, signos + y menos y : entre @
    
        regex_patron = patron_comando
        comandos = re.findall(regex_patron, cadena)
        if len(comandos)>0: # no es un comando
            for i in comandos:
                parameter = []
                if limpiar_delimiters:
                    i = i.replace(start_delimiter,"")
                    i = i.replace(end_delimiter,"")
                parameter.append(i)
                parameter.append(identificador+i)
                lista_parameters.append(parameter)
                cadena_cambiada = re.sub(i,parameter[1],cadena_cambiada)
                # dict_params[i] = cadena_cambiada
    
    return lista_parameters, cadena_cambiada, dict_params

def clean_string(s, f, to = ""):
    """ cambia, en la cadena s
    los caracteres que aparecen en f (se entiende como una lista de caracteres)
    y lo cambia por los caracteres en to (por cada aparición de un caracter en f, lo cambia por la secuencia en to)
    """
    res = ""
    for c in f:
        res = s.replace(c, to)
        s = res

    return res

def update_list_of_params(l_params, params):
    """ coge la lista de parámetros y lo mete en la lista params, aún sin resolver """

    for k,v in l_params.items(): # estamos cambiando un parámetro?
        # l_params[i[0]] = valor # guardamos su valor correspondiente
        # limpiamos la clave de params porque contendrá { y }
        valor = v.replace("@","")
        s_key = clean_string(k, "{}")
        params[s_key] = valor # lo guardo en el diccionario global    
        
    return params
    pass

# =============================================================================
# Busqueda con profundidad en listas de diccionarios
# =============================================================================
def find_key_in_list_of_dictionaries(clave = None, list_of_dictionaries = None, current_dictionary = None):
    """
    busca recursiva de una clave en una lista de diccionarios

    Parameters
    ----------
    clave : TYPE, optional
        DESCRIPTION. The default is None.
    list_of_dictionaries : TYPE, optional
        DESCRIPTION. The default is None.
    current_dictionary : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    value : TYPE
        DESCRIPTION.
    m_current_dictionary : TYPE
        DESCRIPTION.

    """
    # si no me ha llegado una lista de diccionarios no puedo resolver nada    
    if len(list_of_dictionaries) > 0: # rastreo por los diferentes diccionarios intentando resolver la clave, pero para ello necesito que me haya llegado una lista de diccionarios...
        if not current_dictionary == None: # si no me indican por dónde comenzar, comienzo por el primer diccionario
            m_current_dictionary = current_dictionary            
        else:
            m_current_dictionary = list_of_dictionaries[0]
            
        if clave in m_current_dictionary: # está lo que busco en el diccionario?
            value = m_current_dictionary[clave]
            # if escupe:    
            #     common._print(f"valor encontrado = {value}", common.Y)            
        else: # si no está empiezao a buscar el diccionario dónde se contiene la clave que busco
            value = None
            # primero busco si la clave está en el diccionario en que me dicen que busque
            if not clave in m_current_dictionary: # si no está, tengo que buscar en todos los diccionarios
                for ld in list_of_dictionaries:
                    
                    # 20210519 - si el valor que tengo es otro diccionario o una lista, tengo que seguir buscando...
                    if isinstance(ld, (dict, list)):
                        value, m_current_dictionary = find_key_in_list_of_dictionaries(clave, ld, current_dictionary)
                        break # ya tengo el diccionario, dejo de buscar porque esta clave puede aparecer en otro diccionario superior y siempre tiene más prioridad el primer diccionario por orden
                    else:        
                        if clave in ld: # encontrada en este diccionario!
                            value = ld[clave] # consigo el valor
                            m_current_dictionary = ld # y apunto al diccionario en el que está
                            break # ya tengo el diccionario, dejo de buscar porque esta clave puede aparecer en otro diccionario superior y siempre tiene más prioridad el primer diccionario por orden
            else: # como está, cojo su valor                    
                value = m_current_dictionary[clave]    
    
    return value, m_current_dictionary


# =============================================================================
# Convierte una estructura profunda de diccionarios en una lista simple con diccionarios clave, valor
# así se prepara para resolve_f_string que sólo busca en primer nivel en diccioniarios
# =============================================================================
def convert_deep_dictionary_in_list_of_dictionaries(d, l = []):
    
    if not isinstance(d, (list, dict, str)):
        raise Exception(f"get_key_in_dictionary: {d} no es un diccionario ni una lista ni un string")
        return None
    
    if isinstance(d, dict):
        for lk,lv in d.items():
            if isinstance(lv,list):
                # for i in range(len(lv)): # cada i es un diccionario o un string
                #     if isinstance(lv[i], dict): # sólo lo mando a resolver si es un diccionario
                #         list_of_dictionaries = convert_deep_dictionary_in_list_of_dictionaries(lv[i], list_of_dictionaries)
                #         continue
                #     if isinstance(lv[i], str):
                #         ld = {}
                #         ld[lv[i]] = lv[i] # creo un diccionario con clave y valor iguales (transformo la lista en diccionario)
                #         list_of_dictionaries.append(ld.copy())                        
                #         continue
                l = convert_deep_dictionary_in_list_of_dictionaries(lv, l)
                continue
                    
                        
            if isinstance(lv,dict): # si tengo un diccionario como valor, también busco
                l = convert_deep_dictionary_in_list_of_dictionaries(lv, l)
                continue
       
            if isinstance(lv, str): 
                ld = {}
                ld[lk] = lv
                l.append(ld.copy())
                continue

            ld = {}
            ld[lk] = lv
            l.append(ld.copy())
                
    if isinstance(d, list):
        for i in range(len(d)): # cada i es un diccionario, string o lista
            if isinstance(d[i], dict): # sólo lo mando a resolver si es un diccionario
                l = convert_deep_dictionary_in_list_of_dictionaries(d[i], l)

            if isinstance(d[i], str):
                ld = {}
                ld[d[i]] = d[i] # lo convierto en clave, valor
                l.append(ld.copy())

            if isinstance(d[i],list):
                l = convert_deep_dictionary_in_list_of_dictionaries(d[i], l)



    return l    
    
    pass



# =============================================================================
# resuelve la API_CALL que le enviemos desde los diccionarios de descripción
# siempre empieza con SCOPE, de ahí resuelve SECURITY (un scope puede obligar a una resolución de TOKEN de seguridad distinta, o un API puede estar en STAGGER, etc...)    
# =============================================================================
      
def _resolve_dynamic_fstring_OLD(
                 
                 clave = None, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                 # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
                 list_of_dictionaries = None, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                 current_dictionary = None, # diccionario donde quiero que empiece a buscar
                 # context_query = None, # lista de diccionarios guardada en context y que se recupera por el logical_name
                 params = {},
                 param_delimiter = "_PARAM_", # identifico, dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API
                 escupe = 0, # escupo por pantalla info de rastreo?
                 force_until_all_resolved = False, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                 pending_resolution = None, # si el parámetro force_until_all_resolved está a True, en la salida tiene que mirar si le sigue quedando lo mismo por resolver que cuando entró en la función, en ese caso cesa de intentar resolver
                 # first_time = True, # es la primera vez que entra en la función?
                 ):
    """ objetivo, devolver contenido de una clave, buscando en una serie de diccionarios (query contexts) incluyendo la búsqueda en el área access (diccionario global)
    y resolver fstrings dinámicas (que pueden estar escritas en el propio diccionario - mediante la función magic)
    por diseño siempre busca la clave en el primer nivel (no hace búsquedas profundas) del diccionario que recibe
    """
#    logger = lg.arguments(currentframe(), verbose = g_lg_verbose) # si lleva información sensible obligo a que no la escriba (SALVO CUANDO ESTE EN GOD_MODE)
    # params = params # contiene un diccionario en el que se meterán los parámetros que detectemos (siempre empiezan por _PARAM_{})
    
    resultado = None
    res = 0
    valor = 0
    resultado_dict = {} # por si hemos de devolver un diccionario
    
    # 20210202
    # si no es una lista de diccionarios, lo convierto en una lista
    if not isinstance(list_of_dictionaries, list):
        list_of_dictionaries = [list_of_dictionaries]
    
    # # 20210615
    # if first_time:
    #     lld = list_of_dictionaries.copy()
    #     # aplano la lista con diccionarios que me llega (pueden ser diccionarios con cierta profundidad)
    #     # así permito que esta función trabaje hasta cualquier profundidad...
    #     list_of_dictionaries = convert_deep_dictionary_in_list_of_dictionaries(lld)
    #     first_time = False
    
    # la información para obtener el token de seguridad depende del PROVIDER y del SCOPE al que queramos llamar, por eso se tiene que obtener desde esta función
    cadena_cambiada = None
    """ si no llegan diccionarios creo una lista por defecto """
    # 26/11/2020
    # if list_of_dictionaries == None: # como este es el orden de búsqueda por defecto lo meto sin preguntar a nadie, aunque se pouede modificar pasándole otro orden de búsqueda
    #     query_context = ar_api_query_context(context_name = context.logical_name)        
    #     list_of_dictionaries = []
    #     d = query_context.create_query("Security")
    #     list_of_dictionaries.append(query_context.resolve_query(d))
    #     d = query_context.create_query("Scope")
    #     list_of_dictionaries.append(query_context.resolve_query(d)) 
    # 26/11/2020    
    # if not context == None:    
    #     d = context.getAccess()
    #     if not d == None:
    #         list_of_dictionaries.append(d) # siempre acabo buscando en el diccionario global en memoria
    #     d = context.get_configuration_machine() # !!!FIX - me está llegando un dic_context... y este no tiene información del context de configuration_machine, que sólo lo tiene ar_api_context
    #     if not d == None:
    #         list_of_dictionaries.append(d) # le añado la información confidencial del cliente


    # si no me ha llegado una lista de diccionarios no puedo resolver nada    
    if len(list_of_dictionaries) > 0: # rastreo por los diferentes diccionarios intentando resolver la clave, pero para ello necesito que me haya llegado una lista de diccionarios...
        if not current_dictionary == None: # si no me indican por dónde comenzar, comienzo por el primer diccionario
            m_current_dictionary = current_dictionary            
        else:
            m_current_dictionary = list_of_dictionaries[0]

        # if escupe:    
        #     common._print(f"diccionario a trabajar = {m_current_dictionary}", common.Y)

            
        if clave in m_current_dictionary: # está lo que busco en el diccionario?
            value = m_current_dictionary[clave]
            # if escupe:    
            #     common._print(f"valor encontrado = {value}", common.Y)            
        else: # si no está empiezao a buscar el diccionario dónde se contiene la clave que busco
        
            found, value, m_current_dictionary = get_key_dictionary_in_dictionary(m_current_dictionary, clave)
        
            # value = None
            # # primero busco si la clave está en el diccionario en que me dicen que busque
            # if not clave in m_current_dictionary: # si no está, tengo que buscar en todos los diccionarios
            #     for ld in list_of_dictionaries:
            #         if clave in ld: # encontrada en este diccionario!
            #             value = ld[clave] # consigo el valor
            #             m_current_dictionary = ld # y apunto al diccionario en el que está
            #             break # ya tengo el diccionario, dejo de buscar porque esta clave puede aparecer en otro diccionario superior y siempre tiene más prioridad el primer diccionario por orden
            # else: # como está, cojo su valor                    
            #     value = m_current_dictionary[clave]
        
        
        if value == None:
            return None, None # no se ha encontrado nada en los diccionarios, con lo que devolvemos precisamente que no hemos encontrado nada
        
        if not isinstance(value, dict): # he encontrado un valor, ya que no es un diccionario, veo qué contiene (valor en sí mismo, lista de parámetros a resolver,...)
            
            # si hay una lista de parámetros a resolver por magic, los obtengo y dejo marcada la cadena para luego hacer una sencilla sustitución
            lista_parameters, cadena_cambiada, l_params = get_fstring_parameters(cadena = value, 
                                                                       param_delimiter = param_delimiter,          
                                                                       start_delimiter = "{", 
                                                                       end_delimiter = "}", 
                                                                       identificador = "@", 
                                                                       limpiar_delimiters = False)   
            # 13/01/2021
            if len(l_params): # si tenemos parámetros
                params = update_list_of_params(l_params, params)
            
            
            # if escupe:    
            #     common._print(f"lista_parameters = {lista_parameters} cadena_cambiada = {cadena_cambiada}", common.B)
                
            if len(lista_parameters)==0: # no hay nada que cambiar
                resultado = cadena_cambiada
                
            for i in lista_parameters: # tengo lista de parámetros? - i contiene el parámetro a buscar y la identificación que habrá que cambiar por ese valor en la cadena original ('{scope_uri}', '@{scope_uri}')
                # i = ['{resellerid}', '@{resellerid}']
                # if escupe:
                #     common._print(f"-- lista_parameters = {lista_parameters}, cadena_cambiada = {cadena_cambiada}", common.B+common.style.BRIGHT)
                key = clave             
                magic_target = i[0] # lo que tengo que buscar siempre es el primer elemento del par i (lo devuelto en la lista de parámetros)

                for dic in list_of_dictionaries: # rastreo en todos los diccionarios, la lista de parámetros
                    # dic = list_of_dictionaries[0]
                    current_dictionary = m_current_dictionary
                    target_dictionary = dic
        
                    # busco dentro del diccionario en que me encuentro
                    res, valor, l = make_magic(current_dictionary = current_dictionary, target_dictionary = target_dictionary, key = key, magic = magic_target, param_delimiter = param_delimiter)
                    # 13/01/2021
                    if len(l): # si tenemos parámetros
                        params = update_list_of_params(l, params)                    
                    
                    """ Problema, cuando resuelve una cadena, deja de procesar parámetros """
                    
                    if res == 0: # encontrado
                        cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                        # 26/11/2020                        
                        if i[0] in l_params: # estamos cambiando un parámetro?
                            l_params[i[0]] = valor # guardamos su valor correspondiente
                            # limpiamos la clave de params porque contendrá { y }
                            s_key = clean_string(i[0], "{}")
                            params[s_key] = valor # lo guardo en el diccionario global
                            
                        resultado = cadena_cambiada
                        # if escupe:
                        #     common._print(f"res = {res}, valor = {valor}", common.fg.CYAN+common.style.BRIGHT)

                        break
                    if res == 2: # encontrado pero tenemos un campo todavía a resolver {})
                        #cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                        resultado = cadena_cambiada
                        # if escupe:
                        #     common._print(f"res = {res}, valor = {valor}", common.fg.CYAN+common.style.BRIGHT)

                        magic_target = valor
                        i[0] = magic_target # puede ocurrir el caso de que el parámetro no se resuelva... (por ejemplo {params} u otros parámetros que no estén en ninguna lista de diccionarios)

            # (23/10/2020) por si nos quedan elementos que no hemos podido cambiar
            for i in lista_parameters:
                cadena_cambiada = cadena_cambiada.replace(i[1], i[0]) # quitamos el identificador y lo dehamos como {parametro} para que vuelva a intentarlo después si procede (puede que no tengamos información suficiente ahora)
                # 26/11/2020
                if i[0] in l_params: # estamos cambiando un parámetro?
                    l_params[i[0]] = i[0] # guardamos su valor correspondiente
                    s_key = clean_string(i[0], "{}")                    
                    params[s_key] = i[0] # lo guardo en el diccionario global
                    
                    
            # if escupe:
            #     common._print(f"-- res {res}, valor = {valor}", common.B+common.style.BRIGHT)    
            #     common._print(f"-- lista_parameters = {lista_parameters}, cadena_cambiada = {cadena_cambiada}", common.B+common.style.BRIGHT)                    
            # if escupe:    
            #     common._print(f"cadena_cambiada = {cadena_cambiada}", common.Y+common.style.BRIGHT)
            # cuando ha terminado hago un último cambio por si han quedado parámetros sin cambiar
            for i in lista_parameters:
                cadena_cambiada = cadena_cambiada.replace(i[1], i[0]) 
                # 26/11/2020 antes de devolver el control, quitamos todos los identificadores de params                              
                cadena_cambiada = cadena_cambiada.replace(param_delimiter, "")                
                resultado = cadena_cambiada
                # 13/01/2021
                if i[0] in l_params: # estamos cambiando un parámetro?
                    l_params[i[0]] = i[0] # guardamos su valor correspondiente
                    s_key = clean_string(i[0], "{}")                    
                    params[s_key] = i[0] # lo guardo en el diccionario global                  
                
                
                
        if isinstance(value, dict): # si es un diccionario, itero y resuelvo todas sus claves
            for k,v in value.items():
                clave = k
                # common._print(f"Clave a trabajar - [{clave}]", common.fg.RED+common.style.BRIGHT)

                # ojo, no permitimos diccionarios de más nivel en esta versión (eixigiría una función recursiva) --- hay que cambiarlo
                if not isinstance(v,dict):                    
                # si hay una lista de parámetros a resolver por magic, los obtengo y dejo marcada la cadena para luego hacer una sencilla sustitución
                    lista_parameters, cadena_cambiada, l_params = get_fstring_parameters(cadena = v, 
                                                                               param_delimiter = param_delimiter,          
                                                                               start_delimiter = "{", 
                                                                               end_delimiter = "}", 
                                                                               identificador = "@", 
                                                                             limpiar_delimiters = False)   
                    # 13/01/2021
                    if len(l_params): # si tenemos parámetros
                        params = update_list_of_params(l_params, params)                    

                    if len(lista_parameters)>0:
                        for i in lista_parameters: 
                            # if escupe:
                            #     common._print(f"lista_parameters = {lista_parameters}, cadena_cambiada = {cadena_cambiada}", common.Y)
                            magic_target = i[0]                                 
                            key = clave   
                            current_dictionary = m_current_dictionary                                
                            for dic in list_of_dictionaries:  

                                # if escupe:
                                #     if LOGICAL_NAME in dic:
                                #         common._print(f"del dicionario [{dic[LOGICAL_NAME]}]", common.R)
                                #     common._print(dic, common.fg.RED+common.style.BRIGHT)                                    
                                target_dictionary = dic
       
                                # busco en el diccionario en que me encuentro
                                res, valor, l = make_magic(current_dictionary = current_dictionary, target_dictionary = target_dictionary, key = key, magic = magic_target, param_delimiter = param_delimiter)
                                if len(l_params): # si tenemos parámetros
                                    params = update_list_of_params(l_params, params)                                
                                # si me devuelve algo con los identificadores quiere decir que no lo ha podido resolver en el diccionario actual (está apuntando a una clave que vuelve a devolver algo que está en otro diccionario superior)
                                # ahora cambio en la cadena_cambiada los valores obtenidos
                                # if escupe:
                                #     common._print(f"key = {key}, i[0] = {i[0]}, res = {res}, valor = {valor}", common.Y)

                                if res == 0: # encontrado
                                    cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                                    resultado_dict[k] = cadena_cambiada
                                    # 13/01/2021
                                    if i[0] in l_params: # estamos cambiando un parámetro?
                                        l_params[i[0]] = valor # guardamos su valor correspondiente
                                        # limpiamos la clave de params porque contendrá { y }
                                        s_key = clean_string(i[0], "{}")
                                        params[s_key] = valor # lo guardo en el diccionario global
                                    
                                    # if escupe:
                                    #     common._print(f"res = {res}, valor = {valor}", common.C)
                                    break
                                if res == 2: # encontrado pero tenemos un campo todavía a resolver {})
                                    #cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                                    resultado_dict[k] = cadena_cambiada
                                    # if escupe:
                                    #     common._print(f"res = {res}, valor = {valor}", common.C)
                                    magic_target = valor
                                    i[0] = magic_target # añadido 23/10/2020 - por si hay parámetros que no se resuelven en la lista de diccionarios (el caso de {params}) - devolvemos lo que haya podido resolver
                        # por si nos quedan elementos que no hemos podido cambiar
                        for i in lista_parameters:
                            cadena_cambiada = cadena_cambiada.replace(i[1], i[0]) 
                            # 26/11/2020 antes de devolver el control, quitamos todos los identificadores de params                              
                            cadena_cambiada = cadena_cambiada.replace(param_delimiter, "")
                            resultado_dict[k] = cadena_cambiada
                            # 13/01/2021
                            if i[0] in l_params: # estamos cambiando un parámetro?
                                l_params[i[0]] = i[0] # guardamos su valor correspondiente
                                s_key = clean_string(i[0], "{}")                    
                                params[s_key] = i[0] # lo guardo en el diccionario global                            

                    else: # no hay nada que cambiar porque no tenemos lista_parameters
                        resultado_dict[k] = cadena_cambiada                             
            resultado = resultado_dict
        
    """ 
    29012021
    nuevo para intentar resolver a mayores profundidades, cuando llega aquí puede que se haya encontrado con un parámetro
    que se resolvería en otra pasada 
    """    
    if force_until_all_resolved: # si me piden que resuelva todo, es porque aún quedan parámetros por resolver
        if resultado == pending_resolution: 
            # esto quiere decir que no ha podido resolver nada más (puede que haya información que se resolverá después, cuando se carguen parámetros adicionales)
            # así que nos vamos
            return resultado, params
        else:
            # intentamos resolver nuevamente con una profundidad adicional y desde el principio
            # creo una clave temporal
            clave = str(timestamp())
            # copio lo que no hemos podido resolver
            valor = resultado
            # lo meto en la lista de diccionario para que intente resolver la clave con la información que ya tiene
            list_of_dictionaries.insert(0,{clave : valor})
            # y veo si se resuelve
            resultado, params = _resolve_dynamic_fstring(
                     clave = clave, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                     # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
                     params = params, # arrastro los parámetros para no perderlos
                     list_of_dictionaries = list_of_dictionaries, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                     current_dictionary = None, # diccionario donde quiero que empiece a buscar
                     # context_query = None, # lista de diccionarios guardada en context y que se recupera por el logical_name
                     param_delimiter = param_delimiter, # identifico, dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API
                     escupe = False, # escupo por pantalla info de rastreo?
                     force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                     pending_resolution = resultado, # si el parámetro force_until_all_resolved está a True, en la salida tiene que mirar si le sigue quedando lo mismo por resolver que cuando entró en la función, en ese caso cesa de intentar resolver
                     # first_time = False, # no es la primera vez que entra en la función, ...
                     )  
        
        
    return resultado, params



# cambio necesario, si no encuentra valor para la clave, tiene que devolver None, ahora está devolviendo "" (que podría ser una resolución válida en algún caso)
def _resolve_dynamic_fstring(
                 
                 clave = None, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                 # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
                 list_of_dictionaries = None, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                 current_dictionary = None, # diccionario donde quiero que empiece a buscar
                 # context_query = None, # lista de diccionarios guardada en context y que se recupera por el logical_name
                 params = {},
                 param_delimiter = "_PARAM_", # identifico, dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API
                 escupe = 0, # escupo por pantalla info de rastreo?
                 force_until_all_resolved = False, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                 pending_resolution = None, # si el parámetro force_until_all_resolved está a True, en la salida tiene que mirar si le sigue quedando lo mismo por resolver que cuando entró en la función, en ese caso cesa de intentar resolver
                 ):
    """ objetivo, devolver contenido de una clave, buscando en una serie de diccionarios (query contexts) incluyendo la búsqueda en el área access (diccionario global)
    y resolver fstrings dinámicas (que pueden estar escritas en el propio diccionario - mediante la función magic)
    por diseño siempre busca la clave en el primer nivel (no hace búsquedas profundas) del diccionario que recibe
    """
    
    resultado = None
    res = 0
    valor = 0
    resultado_dict = {} # por si hemos de devolver un diccionario
    
    # 20210202
    # si no es una lista de diccionarios, lo convierto en una lista
    if not isinstance(list_of_dictionaries, list):
        list_of_dictionaries = [list_of_dictionaries]
    
    # sólo puede contener diccionarios, en otro caso error
    # l = [x for x in list_of_dictionaries if not isinstance(x, dict)]    
    
    # if len(l)>0:
    #     raise Exception("sólo puede enviarse una lista conteniendo diccionarios")
    
    cadena_cambiada = None


    # si no me ha llegado una lista de diccionarios no puedo resolver nada    
    if len(list_of_dictionaries) > 0: # rastreo por los diferentes diccionarios intentando resolver la clave, pero para ello necesito que me haya llegado una lista de diccionarios...
        if not current_dictionary == None: # si no me indican por dónde comenzar, comienzo por el primer diccionario
            m_current_dictionary = current_dictionary            
        else:
            m_current_dictionary = list_of_dictionaries[0]

        # if escupe:    
        #     common._print(f"diccionario a trabajar = {m_current_dictionary}", common.Y)

            
        if clave in m_current_dictionary: # está lo que busco en el diccionario?
            value = m_current_dictionary[clave]
            # if escupe:    
            #     common._print(f"valor encontrado = {value}", common.Y)            
        else: # si no está empiezao a buscar el diccionario dónde se contiene la clave que busco
            value = None
            # primero busco si la clave está en el diccionario en que me dicen que busque
            if not clave in m_current_dictionary: # si no está, tengo que buscar en todos los diccionarios
                for ld in list_of_dictionaries:
                    if clave in ld: # encontrada en este diccionario!
                        value = ld[clave] # consigo el valor
                        m_current_dictionary = ld # y apunto al diccionario en el que está
                        break # ya tengo el diccionario, dejo de buscar porque esta clave puede aparecer en otro diccionario superior y siempre tiene más prioridad el primer diccionario por orden
                        """ quizá debería quitar este diccionario de esta posición y ponerle al principio??? """
            else: # como está, cojo su valor                    
                value = m_current_dictionary[clave]

        # if escupe:    
        #     common._print(f"_resolve_dynamic_fstring: \n\tm_current_dictionary {m_current_dictionary} \n\tcadena tiene = {value} \n\tclave {clave}", common.Y)
        
        
        if value == None:
            return None, None # no se ha encontrado nada en los diccionarios, con lo que devolvemos precisamente que no hemos encontrado nada
        
        if not isinstance(value, dict): # he encontrado un valor, ya que no es un diccionario, veo qué contiene (valor en sí mismo, lista de parámetros a resolver,...)
            
            # si hay una lista de parámetros a resolver por magic, los obtengo y dejo marcada la cadena para luego hacer una sencilla sustitución
            lista_parameters, cadena_cambiada, l_params = get_fstring_parameters(cadena = value, 
                                                                       param_delimiter = param_delimiter,          
                                                                       start_delimiter = "{", 
                                                                       end_delimiter = "}", 
                                                                       identificador = "@", 
                                                                       limpiar_delimiters = False)   
            # 13/01/2021
            if len(l_params): # si tenemos parámetros
                params = update_list_of_params(l_params, params)
            
            
            # if escupe:    
            #     common._print(f"lista_parameters = {lista_parameters} cadena_cambiada = {cadena_cambiada}", common.B)
                
            if len(lista_parameters)==0: # no hay nada que cambiar
                resultado = cadena_cambiada
                
            for i in lista_parameters: # tengo lista de parámetros? - i contiene el parámetro a buscar y la identificación que habrá que cambiar por ese valor en la cadena original ('{scope_uri}', '@{scope_uri}')
                # i = ['{resellerid}', '@{resellerid}']
                # if escupe:
                #     common._print(f"-- lista_parameters = {lista_parameters}, cadena_cambiada = {cadena_cambiada}", common.B+common.style.BRIGHT)
                key = clave             
                magic_target = i[0] # lo que tengo que buscar siempre es el primer elemento del par i (lo devuelto en la lista de parámetros)

                for dic in list_of_dictionaries: # rastreo en todos los diccionarios, la lista de parámetros
                    # dic = list_of_dictionaries[0]
                    current_dictionary = m_current_dictionary
                    target_dictionary = dic
        
                    # busco dentro del diccionario en que me encuentro
                    res, valor, l = make_magic(current_dictionary = current_dictionary, target_dictionary = target_dictionary, key = key, magic = magic_target, param_delimiter = param_delimiter)
                    # 13/01/2021
                    if len(l): # si tenemos parámetros
                        params = update_list_of_params(l, params)                    
                    
                    """ Problema, cuando resuelve una cadena, deja de procesar parámetros """
                    
                    if res == 0: # encontrado
                        cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                        # 26/11/2020                        
                        if i[0] in l_params: # estamos cambiando un parámetro?
                            l_params[i[0]] = valor # guardamos su valor correspondiente
                            # limpiamos la clave de params porque contendrá { y }
                            s_key = clean_string(i[0], "{}")
                            params[s_key] = valor # lo guardo en el diccionario global
                            
                        resultado = cadena_cambiada
                        # if escupe:
                        #     common._print(f"res = {res}, valor = {valor}", common.fg.CYAN+common.style.BRIGHT)

                        break
                    if res == 2: # encontrado pero tenemos un campo todavía a resolver {})
                        #cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                        resultado = cadena_cambiada
                        # if escupe:
                        #     common._print(f"res = {res}, valor = {valor}", common.fg.CYAN+common.style.BRIGHT)

                        magic_target = valor
                        i[0] = magic_target # puede ocurrir el caso de que el parámetro no se resuelva... (por ejemplo {params} u otros parámetros que no estén en ninguna lista de diccionarios)

            # (23/10/2020) por si nos quedan elementos que no hemos podido cambiar
            for i in lista_parameters:
                cadena_cambiada = cadena_cambiada.replace(i[1], i[0]) # quitamos el identificador y lo dehamos como {parametro} para que vuelva a intentarlo después si procede (puede que no tengamos información suficiente ahora)
                # 26/11/2020
                if i[0] in l_params: # estamos cambiando un parámetro?
                    l_params[i[0]] = i[0] # guardamos su valor correspondiente
                    s_key = clean_string(i[0], "{}")                    
                    params[s_key] = i[0] # lo guardo en el diccionario global
                    
                    
            # if escupe:
            #     common._print(f"-- res {res}, valor = {valor}", common.B+common.style.BRIGHT)    
            #     common._print(f"-- lista_parameters = {lista_parameters}, cadena_cambiada = {cadena_cambiada}", common.B+common.style.BRIGHT)                    
            # if escupe:    
            #     common._print(f"cadena_cambiada = {cadena_cambiada}", common.Y+common.style.BRIGHT)
            # cuando ha terminado hago un último cambio por si han quedado parámetros sin cambiar
            for i in lista_parameters:
                cadena_cambiada = cadena_cambiada.replace(i[1], i[0]) 
                # 26/11/2020 antes de devolver el control, quitamos todos los identificadores de params                              
                cadena_cambiada = cadena_cambiada.replace(param_delimiter, "")                
                resultado = cadena_cambiada
                # 13/01/2021
                if i[0] in l_params: # estamos cambiando un parámetro?
                    l_params[i[0]] = i[0] # guardamos su valor correspondiente
                    s_key = clean_string(i[0], "{}")                    
                    params[s_key] = i[0] # lo guardo en el diccionario global                  
                
                
                
        if isinstance(value, dict): # si es un diccionario, itero y resuelvo todas sus claves
            for k,v in value.items():
                clave = k
                # common._print(f"Clave a trabajar - [{clave}]", common.fg.RED+common.style.BRIGHT)

                # ojo, no permitimos diccionarios de más nivel en esta versión (eixigiría una función recursiva) --- hay que cambiarlo
                if not isinstance(v,dict):                    
                # si hay una lista de parámetros a resolver por magic, los obtengo y dejo marcada la cadena para luego hacer una sencilla sustitución
                    lista_parameters, cadena_cambiada, l_params = get_fstring_parameters(cadena = v, 
                                                                               param_delimiter = param_delimiter,          
                                                                               start_delimiter = "{", 
                                                                               end_delimiter = "}", 
                                                                               identificador = "@", 
                                                                             limpiar_delimiters = False)   
                    # 13/01/2021
                    if len(l_params): # si tenemos parámetros
                        params = update_list_of_params(l_params, params)                    

                    if len(lista_parameters)>0:
                        for i in lista_parameters: 
                            # if escupe:
                            #     common._print(f"lista_parameters = {lista_parameters}, cadena_cambiada = {cadena_cambiada}", common.Y)
                            magic_target = i[0]                                 
                            key = clave   
                            current_dictionary = m_current_dictionary                                
                            for dic in list_of_dictionaries:  

                                # if escupe:
                                #     if LOGICAL_NAME in dic:
                                #         common._print(f"del dicionario [{dic[LOGICAL_NAME]}]", common.R)
                                #     common._print(dic, common.fg.RED+common.style.BRIGHT)                                    
                                target_dictionary = dic
       
                                # busco en el diccionario en que me encuentro
                                res, valor, l = make_magic(current_dictionary = current_dictionary, target_dictionary = target_dictionary, key = key, magic = magic_target, param_delimiter = param_delimiter)
                                if len(l_params): # si tenemos parámetros
                                    params = update_list_of_params(l_params, params)                                
                                # si me devuelve algo con los identificadores quiere decir que no lo ha podido resolver en el diccionario actual (está apuntando a una clave que vuelve a devolver algo que está en otro diccionario superior)
                                # ahora cambio en la cadena_cambiada los valores obtenidos
                                # if escupe:
                                #     common._print(f"key = {key}, i[0] = {i[0]}, res = {res}, valor = {valor}", common.Y)

                                if res == 0: # encontrado
                                    cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                                    resultado_dict[k] = cadena_cambiada
                                    # 13/01/2021
                                    if i[0] in l_params: # estamos cambiando un parámetro?
                                        l_params[i[0]] = valor # guardamos su valor correspondiente
                                        # limpiamos la clave de params porque contendrá { y }
                                        s_key = clean_string(i[0], "{}")
                                        params[s_key] = valor # lo guardo en el diccionario global
                                    
                                    # if escupe:
                                    #     common._print(f"res = {res}, valor = {valor}", common.C)
                                    break
                                if res == 2: # encontrado pero tenemos un campo todavía a resolver {})
                                    #cadena_cambiada = cadena_cambiada.replace(i[1], valor)
                                    resultado_dict[k] = cadena_cambiada
                                    # if escupe:
                                    #     common._print(f"res = {res}, valor = {valor}", common.C)
                                    magic_target = valor
                                    i[0] = magic_target # añadido 23/10/2020 - por si hay parámetros que no se resuelven en la lista de diccionarios (el caso de {params}) - devolvemos lo que haya podido resolver
                        # por si nos quedan elementos que no hemos podido cambiar
                        for i in lista_parameters:
                            cadena_cambiada = cadena_cambiada.replace(i[1], i[0]) 
                            # 26/11/2020 antes de devolver el control, quitamos todos los identificadores de params                              
                            cadena_cambiada = cadena_cambiada.replace(param_delimiter, "")
                            resultado_dict[k] = cadena_cambiada
                            # 13/01/2021
                            if i[0] in l_params: # estamos cambiando un parámetro?
                                l_params[i[0]] = i[0] # guardamos su valor correspondiente
                                s_key = clean_string(i[0], "{}")                    
                                params[s_key] = i[0] # lo guardo en el diccionario global                            

                    else: # no hay nada que cambiar porque no tenemos lista_parameters
                        resultado_dict[k] = cadena_cambiada                             
            resultado = resultado_dict
        
    """ 
    29012021
    nuevo para intentar resolver a mayores profundidades, cuando llega aquí puede que se haya encontrado con un parámetro
    que se resolvería en otra pasada 
    """    
    if force_until_all_resolved: # si me piden que resuelva todo, es porque aún quedan parámetros por resolver
        if resultado == pending_resolution: 
            # esto quiere decir que no ha podido resolver nada más (puede que haya información que se resolverá después, cuando se carguen parámetros adicionales)
            # así que nos vamos
            return resultado, params
        else:
            # intentamos resolver nuevamente con una profundidad adicional y desde el principio
            # creo una clave temporal
            clave = str(timestamp())
            # copio lo que no hemos podido resolver
            valor = resultado
            # lo meto en la lista de diccionario para que intente resolver la clave con la información que ya tiene
            list_of_dictionaries.insert(0,{clave : valor})
            # y veo si se resuelve
            resultado, params = _resolve_dynamic_fstring(
                     clave = clave, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                     # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
                     params = params, # arrastro los parámetros para no perderlos
                     list_of_dictionaries = list_of_dictionaries, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                     current_dictionary = None, # diccionario donde quiero que empiece a buscar
                     # context_query = None, # lista de diccionarios guardada en context y que se recupera por el logical_name
                     param_delimiter = param_delimiter, # identifico, dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API
                     escupe = False, # escupo por pantalla info de rastreo?
                     force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                     pending_resolution = resultado, # si el parámetro force_until_all_resolved está a True, en la salida tiene que mirar si le sigue quedando lo mismo por resolver que cuando entró en la función, en ese caso cesa de intentar resolver
                     )  
    
    return resultado, params



def fix_dictionary_as_param(dictionary, swap = ("'",'"') ):
    """
    convierte un dictionary que está dentro de un string, pero esperando que las claves
    aparezcan entre dobles comillas (que es lo que espera json)

    Parameters
    ----------
    dictionary : TYPE
        DESCRIPTION.

    swap : TYPE tuple
        DESCRIPTION. will change first to second

    Returns
    -------
    None.

    """
    import re
    p = re.compile('(?<!\\\\)\'')
    d = p.sub('\"', dictionary)
    import json
    dic = json.loads(d)
    return dic
    
    
    

# =============================================================================
# Obtiene la información de una clave en una lista de diccionarios, resolviendo como fstring
# devuelve el resultado de la búsqueda, y todo lo que sean parámetros, a medida que ha ido buscando
# =============================================================================
def getFromDictionaries(
                 clave = None, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                 list_of_dictionaries = None, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                 current_dictionary = None, # diccionario donde quiero que empiece a buscar
                 params = {},
                 param_delimiter = "_PARAM_", # identifico, dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API
                 escupe = 0, # escupo por pantalla info de rastreo?
                 force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                 pending_resolution = None, # si el parámetro force_until_all_resolved está a True, en la salida tiene que mirar si le sigue quedando lo mismo por resolver que cuando entró en la función, en ese caso cesa de intentar resolver
                 # first_time = True,
        
        ):
    
    """
    objetivo, devolver contenido de una clave, buscando en una serie de diccionarios (query contexts) incluyendo la búsqueda en el área access (diccionario global)
    y resolver fstrings dinámicas (que pueden estar escritas en el propio diccionario - mediante la función magic)

    Parameters
    ----------
    clave : TYPE, optional
        DESCRIPTION. The default is None. clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)                
    list_of_dictionaries : TYPE, optional
        DESCRIPTION. The default is None. orden de diccionarios que trataremos para resolver la clave
    current_dictionary : TYPE, optional
        DESCRIPTION. The default is None. se usa para controlar qué diccionario se está tratando cuando se hace recursividad en la función, diccionario donde quiero que empiece a buscar
     params : TYPE, optional
        DESCRIPTION. The default is {}. construye la lista de parámetros que va encontrando (todo lo que no comience por "AR_")
    param_delimiter : TYPE, optional
        DESCRIPTION. The default is "_PARAM_". delimitador usado para parámetros, identifico dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API                 escupe : TYPE, optional
    escupe : TYPE, optional 
        DESCRIPTION. The default is 0. escupo por pantalla info de rastreo?
    force_until_all_resolved : TYPE, optional
        DESCRIPTION. The default is False. por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
    pending_resolution : TYPE, optional
        DESCRIPTION. The default is None. si el parámetro force_until_all_resolved está a True : TYPE

    Returns
    -------
    TYPE
        DESCRIPTION.

    """    
    
    if not isinstance(list_of_dictionaries, list):
        list_of_dictionaries = [list_of_dictionaries] # siempre se envía una lista
    
    # hacemos un wrapper porque realmente quiero que funcione con esta signature de función
    # _resolve_dynamic_fstring se queda como signature interna
    return  _resolve_dynamic_fstring(
                 clave = clave, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                 list_of_dictionaries = list_of_dictionaries, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                 current_dictionary = current_dictionary, # diccionario donde quiero que empiece a buscar
                 params = params,
                 param_delimiter = param_delimiter, # identifico, dentro de la estructura de definición de API (API_ROBOT_Providers_Microsoft, por ejemplo) que algo es un parámetro del API
                 escupe = escupe, # escupo por pantalla info de rastreo?
                 force_until_all_resolved = force_until_all_resolved, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                 pending_resolution = pending_resolution, # si el parámetro force_until_all_resolved está a True, en la salida tiene que mirar si le sigue quedando lo mismo por resolver que cuando entró en la función, en ese caso cesa de intentar resolver
                 # first_time = first_time,
                 )

def find_parameters(fstring: "cadena a analizar" = "", 
                    start_delimiter: "primer delimitador" = "{", 
                    end_delimiter: "delimitador final" = "}"):
    """
    encuentra, en una cadena, todos los elementos que se encuentran entre start_delimiter y end_delimiter
    si busca "en la madriguera había un {animal} que era muy {adjetivo}"
    la función devolverá [ {animal}, {adjetivo}]

    Parameters
    ----------
    fstring : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    import re
    regex_patron = r"{start_delimiter}[\w\d+-:]+{end_delimiter}".format(
        start_delimiter = start_delimiter,
        end_delimiter = end_delimiter) # buscamos secuencias de palabras dígitos, signos + y menos y : entre @
    cadena = fstring
    list_of_parameters = re.findall(regex_patron, cadena)    
    
    return list_of_parameters


# mem_variable = 10000000
# look_into_memory_variables = True
# look_into_environment_variables = True
# fstring = "{API_ROBOT_MAQUINA_DESARROLLO} - {mem_variable} - {noresolv} - {param1}---algo---{param2}"
# list_of_dictionaries = [{"pa1" : 1000},{"param" : {"param1" : "{param2}"}},{"param2" : 200}]
# start_delimiter = "{"
# end_delimiter = "}"
# force_resolve = True

import inspect

def compute_fstring(fstring: "string conteniendo información del tipo {param1}---algo---{param2}" = "{param1}---algo---{param2}",
                    list_of_dictionaries: "list of dictionaries to search information" = [],
                    look_into_memory_variables: "if True it will resolve against memory variables - with eval()" = False,
                    look_into_environment_variables: "if True it will look keys in environment" = False,
                    start_delimiter: "primer delimitador" = "{", 
                    end_delimiter: "delimitador final" = "}",
                    force_resolve: "si True entra en modo recursivo hasta que resuelve todos los parámetros" = False,
                    v_locals: "para procesar info de variables locales de la calling function, hay que pasarle locals()" = {},
                    v_globals: "para procesar info de variables locales de la calling function, hay que pasarle globals()" = {}):
    """
    resuelve una fstring buscando información en una lista de diccionarios, environment variables, locals y globals

    Parameters
    ----------
    fstring : "string conteniendo información del tipo {param1}---algo---{param2}", optional
        DESCRIPTION. The default is "{param1}---algo---{param2}".
    list_of_dictionaries : "list of dictionaries to search information", optional
        DESCRIPTION. The default is [].
    look_into_memory_variables : "if True it will resolve against memory variables - with eval()", optional
        DESCRIPTION. The default is False.
    look_into_environment_variables : "if True it will look keys in environment", optional
        DESCRIPTION. The default is False.
    start_delimiter : "primer delimitador", optional
        DESCRIPTION. The default is "{".
    end_delimiter : "delimitador final", optional
        DESCRIPTION. The default is "}".
    force_resolve : "si True entra en modo recursivo hasta que resuelve todos los parámetros", optional
        DESCRIPTION. The default is False.
    v_locals : "para procesar info de variables locales de la calling function, hay que pasarle locals()", optional
        DESCRIPTION. The default is {}.
    v_globals : "para procesar info de variables locales de la calling function, hay que pasarle globals()", optional
        DESCRIPTION. The default is {}.

    Returns
    -------
    fstring : TYPE
        DESCRIPTION.
    list_of_results : TYPE
        DESCRIPTION.

    """

    

    # try:
    #     func_name = inspect.currentframe().f_code.co_name        
    #     module = types.ModuleType(func_name)
    #     module.__dict__.update(sys._getframe(1).f_locals)
    # except:
    #     pass

    
    # 1) obtenemos todos los parámetros que se encuentren entre {}
    """ aquí deberíamos usar _resolve_dynamic_fstring pero con la capacidad de hacer búsquedas profundas en diccionarios """
    list_of_parameters = find_parameters(fstring)
    
    
    list_of_clean_parameters = []
    # limpiamos la lista para obtener los parámetros sin {}
    for parametro in list_of_parameters:
        clean_parametro = parametro.replace(start_delimiter, "")
        clean_parametro = clean_parametro.replace(end_delimiter, "")
        list_of_clean_parameters.append((parametro, clean_parametro))
    
    # 2) iteramos por cada parámetro intentando encontrarlo en la lista de diccionarios, luego en memoria, luego en environment
    # intento en lista de parámetros
    list_of_results = []
    list_of_lors = []
    for parametro, clean_parametro in list_of_clean_parameters:
        # resultado, params = _resolve_dynamic_fstring(parametro, list_of_dictionaries, force_until_all_resolved=True)
        clean_parametro, valor, d = find_value(clean_parametro, list_of_dictionaries)  
        # si encuentro {} en el valor, obligo a la resolución como si fuese una fstring nueva
        if force_resolve:
            if isinstance(valor, str):
                n_list_of_parameters = find_parameters(valor) 
                if len(n_list_of_parameters)>0:
                    valor, lor = compute_fstring(fstring = valor,
                                    list_of_dictionaries = list_of_dictionaries,
                                    look_into_memory_variables = look_into_memory_variables,
                                    look_into_environment_variables = look_into_environment_variables,
                                    force_resolve = force_resolve)                
        # value, _ = find_key_in_list_of_dictionaries(clave = parametro, list_of_dictionaries = list_of_dictionaries)        
        list_of_results.append([parametro, clean_parametro, valor])

    # resolvemos en variables de memoria?
    if look_into_memory_variables:
        for t_parametro in list_of_results:
            # si tiene como valor None es que no lo ha resuelto
            if t_parametro[2] == None: # no se ha podido resolver en la primera pasada
                try:
                    t_parametro[2] = eval(f"{t_parametro[1]}")
                except:
                    # está entre las variables locales de la función que llama?
                    for k,v in v_locals.items():
                        if t_parametro[1] == k:
                            t_parametro[2] = v
                            continue
                    # está entre las variables globales de la función que llama?
                    for k,v in v_globals.items():
                        if t_parametro[1] == k:
                            t_parametro[2] = v
                            continue
                    continue

    # resolvemos en environment variables?
    if look_into_environment_variables:
        for t_parametro in list_of_results:
            # si tiene como valor None es que no lo ha resuelto
            if t_parametro[2] == None: # no se ha podido resolver en la primera pasada
                try:
                    res = get_user_env(t_parametro[1])
                    if not res == "":
                        t_parametro[2] = res
                except:
                    continue            
                
    """ si el valor contiene {} significa que no ha sido resuelto, con lo que habría que dejarlo como está """
    # 3) resolvemos en la fstring enviada
    for el in list_of_results: 
        if not el[2] == None: # si ha habido cambio
            if isinstance(el[2], str): # si me llega un string tengo que ver si todavía tengo cosas por resolver
                if el[2].find("{") == -1: # si tiene un valor válido
                    fstring = fstring.replace(el[0], str(el[2])) # cambiado
            else:
                fstring = fstring.replace(el[0], str(el[2])) # cambiado
    
    
    # 4) devolvemos la fstring y la lista de parámetros con sus valores encontrados
    return fstring, list_of_results





# ---- .
# ---- * Aplicación recursiva de función para resolver parámetros --------------------------------------


def look_for_environment_variable(cadena: "string en la que buscamos para operar el cambio", 
                                  dictionary: "diccionario o JSON a cambiar" = {}, 
                                  exceptions: "lista de nombres de variable que no se cambian" = [],
                                  dictionary_for_search: "diccionario en que buscar, normalmente access" = {},
                                  list_of_changes: "guarda en un diccionario las claves que ha encontrado y el valor resuelto, si lo hay" = {},
                                  ):
    """
    
    Recibe un string y mira a ver si hay algo entre {} que considera un parámetro a resolver 
        chequea si aparece en un diccionario de búsqueda
        chequea si hay una variable de entorno con ese nombre y sustituye
    Si el diccionario no está vacío, intenta encontrar la clave en el diccionario, si no se va a environment variables.
    Si encuentra algo que cambiar, lo incluye en el diccionario 

    se le puede enviar una lista de excepciones para que no las resuelva en la cadena

    Parameters
    ----------
    cadena : "string en la que buscamos para operar el cambio"
        DESCRIPTION.
    dictionary : "diccionario o JSON a cambiar", optional
        DESCRIPTION. The default is {}.
    exceptions : "lista de nombres de variable que no se cambian", optional
        DESCRIPTION. The default is [].
    dictionary_for_search : "diccionario o lista de diccionarios en que buscar", optional
        DESCRIPTION. The default is {}.

    Returns
    -------
    cadena : TYPE
        DESCRIPTION.

    """
    
    import re

    global access

    if not isinstance(cadena, str):
        return cadena

    lista_de_elementos_entre_llaves = []
    
    if dictionary_for_search == {}:
        dictionary_for_search = dictionary.copy()
        
    
    """ localizar todo lo que esté entre {} """
    # detect delimiters of date commands
    start_delimiter = "{"
    end_delimiter = "}"

    # is it a date language specific command?
    # it needs to start with @D:
    patron_comando = r"{start_delimiter}[\w\d+-:]+{end_delimiter}".format(
        start_delimiter = start_delimiter,
        end_delimiter = end_delimiter) # buscamos secuencias de palabras dígitos, signos + y menos y : entre @

    regex_patron = patron_comando
    comandos = re.findall(regex_patron, cadena)
    
    if len(comandos)==0: # no hay nada que cambiar...
        return cadena    
    
    """ una vez obtenidos los comandos los busco
    1) en access
    2) en variables de entorno
    """
    lista_cambios = {}
    
    # si hemos encontrado comandos, intentamos encontrarlos en environment variables y en el diccionario de búsqueda (o diccionarios de búsqueda)
    # si no encontramos coincidencias, dejamos el comando en la cadena, tal y como estaba
    for comando in comandos:
        mem_comando = comando
        # le quitamos las llaves
        comando = comando.replace("{", "")
        comando = comando.replace("}", "")
        
        if comando in exceptions: # está en la lista de valores que queremos saltarnos?
            continue
        
        valor, params = _resolve_dynamic_fstring(
                      clave = comando, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                      list_of_dictionaries = dictionary_for_search, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                      force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                      )
        
        if valor == None: # no lo ha encontrado, buscamos en las variables de entorno
            valor = get_user_env(comando)
    
        if valor == None: # no lo ha encontrado, dejamos el valor original
            valor = mem_comando

        # OJO -> puede ser algo mucho más complejo que un diccionario, así que hay que hacer un cambio en todos los sitios en que apareza
        # tengo que buscar en toda la estructura (diccionarios o listas o lo que sea, y dónde se encuentre esta información, cambiarla con compute_fstring)

        # # 01/09/2021 nuevo (si una clave no se encuentra, se deja tal y como estaba
        if not dictionary == {}:
            # no puedo crear claves nuevas o me cargaría el diccionario original
            path = deep_search(dictionary, mem_comando) # se ha encontrado!
            
            # podría hacer una macro-sustitución en toda la profundidad del diccionario con la función
            # change_values_in_nested_structure() - pero de momento lo voy a dejar así

            if valor == None or valor == mem_comando: # o no ha encontrado nada o se ha encontrado a sí mismo, sin resolver
                valor = "{" + f"{comando}" + "}"
                # tc._print(f"{mem_comando} - {valor}") 
                # a = 1
    
        # cargamos los cambios como pares clave, valor en el diccionario que nos han enviado
        cleaned_mem_comando = mem_comando
        cleaned_mem_comando = cleaned_mem_comando.replace("{", "")
        cleaned_mem_comando = cleaned_mem_comando.replace("}", "")
        list_of_changes[cleaned_mem_comando] = valor
        
        lista_cambios[mem_comando] = valor
        
        # 01/09/2021 elimino esta parte porque si encontraba {kk} como creía que había encontrado algo, añadía una clave nueva en el diccionario, y estaba cambiando el diccionario original mientras se rastreaba, dando error
        # if not dictionary == {}:
        #     dictionary[e] = valor
            
    # ahora cambiamos los valores y devolvemos el resultado
    for k,v in lista_cambios.items():
        cadena = cadena.replace(k,str(v))
    
    return cadena

# =============================================================================
# Recibe un string y mira a ver si hay algo entre {} -> chequea si hay una variable de entorno con ese nombre y sustituye
# Recibe tb un diccionario. 
# Si el diccionario no está vacío, intenta encontrar la clave en el diccionario, si no se va a environment variables.
# Si encuentra algo que cambiar, lo incluye en el diccionario (que puede ser access)
# =============================================================================
def look_for_environment_variable_NEW(cadena: "string en la que buscamos para operar el cambio", 
                                  dictionary: "diccionario o JSON a cambiar" = {}, 
                                  exceptions: "lista de nombres de variable que no se cambian" = [],
                                  dictionary_for_search: "diccionario en que buscar, normalmente access" = {},
                                  ):
    """
    
    Recibe un string y mira a ver si hay algo entre {} -> chequea si hay una variable de entorno con ese nombre y sustituye
    Recibe tb un diccionario. 
    Si el diccionario no está vacío, intenta encontrar la clave en el diccionario, si no se va a environment variables.
    Si encuentra algo que cambiar, lo incluye en el diccionario (que puede ser access)

    Parameters
    ----------
    cadena : "string en la que buscamos para operar el cambio"
        DESCRIPTION.
    dictionary : "diccionario o JSON a cambiar", optional
        DESCRIPTION. The default is {}.
    exceptions : "lista de nombres de variable que no se cambian", optional
        DESCRIPTION. The default is [].
    dictionary_for_search : "diccionario o lista de diccionarios en que buscar", optional
        DESCRIPTION. The default is {}.

    Returns
    -------
    cadena : TYPE
        DESCRIPTION.

    """
    
    import re

    global access

    if not isinstance(cadena, str):
        return cadena

    lista_de_elementos_entre_llaves = []
    
    if dictionary_for_search == {}:
        dictionary_for_search = dictionary.copy()
        
    
    """ localizar todo lo que esté entre {} """
    # detect delimiters of date commands
    start_delimiter = "{"
    end_delimiter = "}"

    # is it a date language specific command?
    # it needs to start with @D:
    patron_comando = r"{start_delimiter}[\w\d+-:]+{end_delimiter}".format(
        start_delimiter = start_delimiter,
        end_delimiter = end_delimiter) # buscamos secuencias de palabras dígitos, signos + y menos y : entre @

    regex_patron = patron_comando
    comandos = re.findall(regex_patron, cadena)
    
    if len(comandos)==0: # no hay nada que cambiar...
        return cadena    
    
    """ una vez obtenidos los comandos los busco
    1) en access
    2) en variables de entorno
    """
    lista_cambios = {}
    
    for e in comandos:
        mem_e = e
        # le quitamos las llaves
        e = e.replace("{", "")
        e = e.replace("}", "")
        
        if e in exceptions: # está en la lista de valores que queremos saltarnos?
            continue
        
        valor, params = _resolve_dynamic_fstring(
                      clave = e, # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                      # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
                      list_of_dictionaries = dictionary_for_search, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                      force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                      )

        # valor, params = _resolve_dynamic_fstring(
        #               clave = "CM_work_folder", # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
        #               # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
        #               list_of_dictionaries = dictionary_for_search, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
        #               force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
        #               )

        
        if valor == None: # no lo ha encontrado, buscamos en las variables de entorno
            valor = get_user_env(e)
    
        if valor == None: # no lo ha encontrado, dejamos el valor original
            valor = mem_e

        # OJO -> puede ser algo mucho más complejo que un diccionario, así que hay que hacer un cambio en todos los sitios en que apareza
        # tengo que buscar en toda la estructura (diccionarios o listas o lo que sea, y dónde se encuentre esta información, cambiarla con compute_fstring)

        

    
    return cadena

# =============================================================================
# Aplica una función, recursivamente, a cada valor de un diccionario (de manera recursiva) 
# ejemplo:
#   apply_function_to_dict_recursive(execution_dictionary, look_for_environment_variable, dictionary = access, dictionary_for_search = access.copy())    
# =============================================================================
def apply_function_to_dict_recursive(d  = {},f  = None, *args, **kargs): 
    """
    Aplica una función, recursivamente, a cada valor de un diccionario (de manera recursiva) 
    ejemplo:
      apply_function_to_dict_recursive(execution_dictionary, look_for_environment_variable, dictionary = access, dictionary_for_search = access.copy())    
    

    Parameters
    ----------
    d : TYPE
        DESCRIPTION. diccionario
    f : TYPE
        DESCRIPTION. función a aplicar a cada valor
    *args : TYPE
        DESCRIPTION.
    **kargs : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION. True (si ha habido cambios) y el diccionario original con los cambios aplicados, y la lista de claves a cambiar y los valores obtenidos

    """
    retorno = False
 
    if d == None:
        raise Exception(f"get_key_in_dictionary: [{d}] está a None")
        return None
        
    if not isinstance(d, (list, dict, str)):
        raise Exception(f"get_key_in_dictionary: [{d}] no es un diccionario ni una lista ni un string")
        return None

    if isinstance(d, dict):
        for lk,lv in d.items():
            if isinstance(lv,list):
                for i in range(len(lv)): # cada i es un diccionario o un string
                    if isinstance(lv[i], dict): # sólo lo mando a resolver si es un diccionario
                        retorno = apply_function_to_dict_recursive(lv[i], f, *args, **kargs)
                    if isinstance(lv[i], str): # ahora voy a ejecutar la función
                        lstr = f(lv[i], *args, **kargs)           
                        d[lk][i] = lstr
                        
            if isinstance(lv,dict): # si tengo un diccionario como valor, también busco
                retorno = apply_function_to_dict_recursive(lv, f, *args, **kargs)
       
            if isinstance(lv, str): # ahora voy a ejecutar la función
                d[lk] = f(lv, *args, **kargs)        
                
    if isinstance(d, list):
        for i in range(len(d)): # cada i es un diccionario o un string
            if isinstance(d[i], dict): # sólo lo mando a resolver si es un diccionario
                retorno = apply_function_to_dict_recursive(d[i], f, *args, **kargs)

    return retorno, kargs.get("dictionary", {})


def resolve_dictionary_patterns_ORIGINAL(d: "dictionary to resolve" = {}, dictionary_to_search_on: "dictionary to search on, will prevail to environment variables" = {}):
    """
    sustituye patterns en diccionarios (por ejemplo access) buscando en dictionary_to_search_on y en environment variables

    Parameters
    ----------
    d : "dictionary to resolve", optional
        DESCRIPTION. The default is {}. Puede ser un diccionario o una lista de diccionarios...
    dictionary_to_search_on : "dictionary to search on, will prevail to environment variables", optional
        DESCRIPTION. The default is {}.

    Returns
    -------
    None.

    """
 
    return apply_function_to_dict_recursive(d, look_for_environment_variable, dictionary = d, dictionary_for_search = dictionary_to_search_on)

import pickle
def is_picklable(obj):
    """
    Check if an object is picklable.

    Args:
        obj: The object to check for picklability.

    Returns:
        bool: True if the object can be pickled, False otherwise.
    """
    try:
        pickle.dumps(obj)
        return True
    except (pickle.PicklingError, TypeError):
        return False

import copy
import collections
def try_deepcopy(obj, path="root"):
    """
    Tries to deepcopy the object recursively and logs the path if it fails.
    
    Args:
        obj: The object to deepcopy.
        path (str): The path to the current object being deepcopied.

    Returns:
        None
    """
    # try:
    #     print(path)        
    #     copy.deepcopy(obj)
    # except TypeError as e:
    #     print(f"Deepcopy failed at {path}. Object: {obj}. Error: {e}")
    #     return
    if path != "root":
        # print(path)
        res = is_picklable(obj)
        if res != True:
            print(f"Deepcopy failed at {path}. Object: {obj}. Error: {res}")
            input("Pulsa una tecla para continuar")
    if isinstance(obj, collections.abc.Mapping):  # For dictionaries
        for key, value in obj.items():
            next_path = f"{path}[{repr(key)}]"
            # print(next_path)
            try_deepcopy(value, path=next_path)
    elif isinstance(obj, (list, tuple)):  # For lists and tuples
        for index, item in enumerate(obj):
            next_path = f"{path}[{index}]"
            # print(next_path)            
            try_deepcopy(item, path=next_path)
    elif hasattr(obj, '__dict__'):  # For custom objects with attributes
        for key, value in obj.__dict__.items():
            next_path = f"{path}.{key}"
            # print(next_path)            
            try_deepcopy(value, path=next_path)

def resolve_dictionary_patterns(d: "dictionary to resolve" = {}, 
                                dictionary_to_search_on: "dictionary to search on, will prevail to environment variables" = {},
                                list_of_changes: "queremos el diccionario con las claves a cambiar y los valores resueltos?" = {},
                                preserve_dictionaries: "deepcopy interno de diccionarios" = True):
    """
    Description
    -----------
    
    sustituye patterns en diccionarios (por ejemplo access) buscando en dictionary_to_search_on y en environment variables

    Parameters
    ----------
    d : "dictionary to resolve", puede ser un diccionario o una lista de diccionarios
        DESCRIPTION. The default is {}. Puede ser un diccionario o una lista de diccionarios...
    dictionary_to_search_on : "dictionary to search on, will prevail to environment variables", optional
        DESCRIPTION. The default is {}.


    Returns
    -------
    None.

    """
    import copy
    if preserve_dictionaries:
        # !!! ojo - estas copias pueden dar problemas importantes de performance
        try:
            ldictionary_to_search_on = copy.deepcopy(dictionary_to_search_on) # preservamos el diccionario original
        except Exception as e:
            try_deepcopy(dictionary_to_search_on)
            a = 999
        ld = copy.deepcopy(d)
    else:
        ldictionary_to_search_on = dictionary_to_search_on
        ld = d
        

    # _, diccionario_resuelto = apply_function_to_dict_recursive(ld, look_for_environment_variable, dictionary = ld, dictionary_for_search = ldictionary_to_search_on)


    # # si es una lista de diccionarios, envío elemento a elemento
    if isinstance(dictionary_to_search_on, list):
        for dictionary in dictionary_to_search_on:
            _, diccionario_resuelto = apply_function_to_dict_recursive(ld, look_for_environment_variable, dictionary = ld, dictionary_for_search = dictionary, list_of_changes = list_of_changes)
            ld = diccionario_resuelto
    else:
        _, diccionario_resuelto = apply_function_to_dict_recursive(ld, look_for_environment_variable, dictionary = ld, dictionary_for_search = ldictionary_to_search_on, list_of_changes = list_of_changes)
        
    # debería devolver las claves y sus valores resueltos, por si queremos usarlos después
    
    return diccionario_resuelto

# ---- .
# ---- work with nested_structures and searchs

# operating strings
def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

# source: https://stackoverflow.com/questions/22162321/search-for-a-value-in-a-nested-dictionary-python
def deep_search_original(d: "dictionary to search on", search_pattern: "what to search", prev_datapoint_path: "first call need to include name of dictionary in code" ='d2'):
    """
    opera en estructuras complejas y anidadas de listas y diccionarios (JSON)
    devuelve una lista con el camino de cada clave que contiene, como valor, el search_pattern

    Parameters
    ----------
    d : "dictionary to search on"
        DESCRIPTION.
    search_pattern : "what to search"
        DESCRIPTION.
    prev_datapoint_path : "first call need to include name of dictionary in code", optional
        DESCRIPTION. The default is ''.

    Returns
    -------
    TYPE list
        DESCRIPTION. devuelve una lista con el camino de cada clave que contiene, como valor, el search_pattern


    Example
    -------
    
    >>>     d1 = {'dict1':
    >>>              {'part1':
    >>>                   {'.wbxml': 'application/vnd.wap.wbxml',
    >>>                    '.rl': 'application/resource-lists+xml'},
    >>>               'part2':
    >>>                   {'.wsdl': 'application/wsdl+xml',
    >>>                    '.rs': 'application/rls-services+xml',
    >>>                    '.xop': 'application/xop+xml',
    >>>                    '.svg': 'image/svg+xml'}},
    >>>          'dict2':
    >>>              {'part1':
    >>>                   {'.dotx': 'application/vnd.openxmlformats-..',
    >>>                    '.zaz': 'application/vnd.zzazz.deck+xml',
    >>>                    '.xer': 'application/patch-ops-error+xml'}}}
    >>> 
    >>>     d2 = {
    >>>         "items":
    >>>             {
    >>>                 "item":
    >>>                     [
    >>>                         {
    >>>                             "id": "0001",
    >>>                             "type": "donut",
    >>>                             "name": "Cake",
    >>>                             "ppu": 0.55,
    >>>                             "batters":
    >>>                                 {
    >>>                                     "batter":
    >>>                                         [
    >>>                                             {"id": "1001", "type": "Regular"},
    >>>                                             {"id": "1002", "type": "Chocolate"},
    >>>                                             {"id": "1003", "type": "Blueberry"},
    >>>                                             {"id": "1004", "type": "Devil's Food"}
    >>>                                         ]
    >>>                                 },
    >>>                             "topping":
    >>>                                 [
    >>>                                     {"id": "5001", "type": "None"},
    >>>                                     {"id": "5002", "type": "Glazed"},
    >>>                                     {"id": "5005", "type": "Sugar"},
    >>>                                     {"id": "5007", "type": "Powdered Sugar"},
    >>>                                     {"id": "5006", "type": "Chocolate with Sprinkles"},
    >>>                                     {"id": "5003", "type": "Chocolate"},
    >>>                                     {"id": "5004", "type": "Maple"}
    >>>                                 ]
    >>>                         },
    >>> 
    >>> 
    >>> 
    >>>                     ]
    >>>             }
    >>>     }
    
    >>> import pprint
    >>> pprint.pprint(deep_search(d1,'svg+xml','d1'))   
    
    >>> ["d1['dict1']['part2']['.svg']"]
    
    >>> pprint.pprint(deep_search(d2,'500','d2')) 
    
    >>> ["d2['items']['item'][0]['topping'][0]['id']",
    >>> "d2['items']['item'][0]['topping'][1]['id']",
    >>> "d2['items']['item'][0]['topping'][2]['id']",
    >>> "d2['items']['item'][0]['topping'][3]['id']",
    >>> "d2['items']['item'][0]['topping'][4]['id']",
    >>> "d2['items']['item'][0]['topping'][5]['id']",
    >>> "d2['items']['item'][0]['topping'][6]['id']"]   
    
    >>> pprint.pprint(deep_search(d2,'XYZ','d2')) 

    >>> []    

    Additional help
    ---------------
    
    You can obtain info directly from the results applying "eval()"

    >>> path = deep_search(d2,'500','d2')
    >>> for p in path:
    >>>     tc._print(eval(p)) 
    
    >>> 5001
    >>> 5002
    >>> 5005
    >>> 5007
    >>> 5006
    >>> 5003
    >>> 5004
     

    """
    search_pattern = str(search_pattern)
    
    output = []
    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    if type(current_datapoint) is dict:
        for dkey in current_datapoint:
            if search_pattern in str(dkey):
                c = current_datapoint_path
                c+="['"+dkey+"']"
                output.append(c)
            c = current_datapoint_path
            c+="['"+dkey+"']"
            for i in deep_search(current_datapoint[dkey], search_pattern, c):
                output.append(i)
    elif type(current_datapoint) is list:
        for i in range(0, len(current_datapoint)):
            if search_pattern in str(i):
                c = current_datapoint_path
                c += "[" + str(i) + "]"
                output.append(i)
            c = current_datapoint_path
            c+="["+ str(i) +"]"
            for i in deep_search(current_datapoint[i], search_pattern, c):
                output.append(i)
    elif search_pattern in str(current_datapoint):
        c = current_datapoint_path
        output.append(c)
    output = filter(None, output)
    return list(output)

# =============================================================================
# Encuentra paths de valores contenidos en listas (es decir, no son diccionarios)
# =============================================================================
def deep_search_lists_with_values(d: "dictionary to search on", search_pattern: "what to search" = None, prev_datapoint_path: "first call need to include name of dictionary in code" ='d2', exact_match: "True exact match, False if it's contained only" = False, output: "lista de paths a devolver que cumplan con la condicion" = list()):
    
    # puedo estar buscando algún valor...
    if not search_pattern == None:
        search_pattern = str(search_pattern)

    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    
    # tc._print(type(current_datapoint))    
    
    if type(current_datapoint) is dict:
        for dkey in current_datapoint:
            c = current_datapoint_path
            c+="['"+dkey+"']"
            for i in deep_search_lists_with_values(current_datapoint[dkey], search_pattern, c, output):
                pass
                
    if type(current_datapoint) is list:
        for i in range(0, len(current_datapoint)):
            if not isinstance(current_datapoint[i], dict): # es un valor no diccionario?
                c = current_datapoint_path
                c += "[" + str(i) + "]"
                output.append(c)
            c = current_datapoint_path
            c+="["+ str(i) +"]"
            for i in deep_search_lists_with_values(current_datapoint[i], search_pattern, c, output):
                if not i in output:
                    output.append(i)                
  
        
    # output = filter(None, output)
    return output    
    
    
    pass

def get_lists_with_values(d: "dictionary to search on", search_pattern: "what to search" = None, prev_datapoint_path: "first call need to include name of dictionary in code" ='d2', exact_match: "True exact match, False if it's contained only" = False):
    
    # puedo estar buscando algún valor...
    if not search_pattern == None:
        search_pattern = str(search_pattern)

    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    
    output = []
    # tc._print(type(current_datapoint))    
    
    if type(current_datapoint) is dict:
        for dkey in current_datapoint:
            c = current_datapoint_path
            c+="['"+dkey+"']"
            for i in get_lists_with_values(current_datapoint[dkey], search_pattern, c):
                if not i in output:
                    output.append(i)                   
                pass
                
    if type(current_datapoint) is list:
        for i in range(0, len(current_datapoint)):
            if not isinstance(current_datapoint[i], dict): # es un valor no diccionario?

                c = current_datapoint_path
                c += "[" + str(i) + "]"
                tc.__trace(f"... found {c}")                
                output.append(c)
            c = current_datapoint_path
            c+="["+ str(i) +"]"
            for i in get_lists_with_values(current_datapoint[i], search_pattern, c):
                if not i in output:
                    output.append(i)                
  
        
    output = filter(None, output)
    return list(output)    
    
    
    pass


def deep_search(d: "dictionary to search on", search_pattern: "what to search" = None, prev_datapoint_path: "first call need to include name of dictionary in code" ='d2', exact_match: "True exact match, False if it's contained only" = False):
    """
    recupera todos los path que contienen un valor concreto
    opera en estructuras complejas y anidadas de listas y diccionarios (JSON)
    puede recibir una lista o un diccionario como entrada prev_datapoint_path
    el diccionario que contiene los paths si llamará con el valor enviado en 
        devuelve una lista con el camino de cada clave que contiene, como valor, el search_pattern
        si search_pattern está a None, genera los path de todos los elementos finales del nested_structure

    Parameters
    ----------
    d : "dictionary to search on"
        DESCRIPTION.
    search_pattern : "what to search"
        DESCRIPTION.
    prev_datapoint_path : "first call need to include name of dictionary in code", optional
        DESCRIPTION. The default is 'd2'.
    exact_match : "True exact match, False if it's contained only", optional
        DESCRIPTION. The default is 'd2'.
    Returns
    -------
    TYPE list
        DESCRIPTION. devuelve una lista con el camino de cada clave que contiene, como valor, el search_pattern


    Example
    -------
    
    >>>     d1 = {'dict1':
    >>>              {'part1':
    >>>                   {'.wbxml': 'application/vnd.wap.wbxml',
    >>>                    '.rl': 'application/resource-lists+xml'},
    >>>               'part2':
    >>>                   {'.wsdl': 'application/wsdl+xml',
    >>>                    '.rs': 'application/rls-services+xml',
    >>>                    '.xop': 'application/xop+xml',
    >>>                    '.svg': 'image/svg+xml'}},
    >>>          'dict2':
    >>>              {'part1':
    >>>                   {'.dotx': 'application/vnd.openxmlformats-..',
    >>>                    '.zaz': 'application/vnd.zzazz.deck+xml',
    >>>                    '.xer': 'application/patch-ops-error+xml'}}}
    >>> 
    >>>     d2 = {
    >>>         "items":
    >>>             {
    >>>                 "item":
    >>>                     [
    >>>                         {
    >>>                             "id": "0001",
    >>>                             "type": "donut",
    >>>                             "name": "Cake",
    >>>                             "ppu": 0.55,
    >>>                             "batters":
    >>>                                 {
    >>>                                     "batter":
    >>>                                         [
    >>>                                             {"id": "1001", "type": "Regular"},
    >>>                                             {"id": "1002", "type": "Chocolate"},
    >>>                                             {"id": "1003", "type": "Blueberry"},
    >>>                                             {"id": "1004", "type": "Devil's Food"}
    >>>                                         ]
    >>>                                 },
    >>>                             "topping":
    >>>                                 [
    >>>                                     {"id": "5001", "type": "None"},
    >>>                                     {"id": "5002", "type": "Glazed"},
    >>>                                     {"id": "5005", "type": "Sugar"},
    >>>                                     {"id": "5007", "type": "Powdered Sugar"},
    >>>                                     {"id": "5006", "type": "Chocolate with Sprinkles"},
    >>>                                     {"id": "5003", "type": "Chocolate"},
    >>>                                     {"id": "5004", "type": "Maple"}
    >>>                                 ]
    >>>                         },
    >>> 
    >>> 
    >>> 
    >>>                     ]
    >>>             }
    >>>     }
    
    >>> import pprint
    >>> pprint.pprint(deep_search(d1,'svg+xml','d1'))   
    
    >>> ["d1['dict1']['part2']['.svg']"]
    
    >>> pprint.pprint(deep_search(d2,'500','d2')) 
    
    >>> ["d2['items']['item'][0]['topping'][0]['id']",
    >>> "d2['items']['item'][0]['topping'][1]['id']",
    >>> "d2['items']['item'][0]['topping'][2]['id']",
    >>> "d2['items']['item'][0]['topping'][3]['id']",
    >>> "d2['items']['item'][0]['topping'][4]['id']",
    >>> "d2['items']['item'][0]['topping'][5]['id']",
    >>> "d2['items']['item'][0]['topping'][6]['id']"]   
    
    >>> pprint.pprint(deep_search(d2,'XYZ','d2')) 

    >>> []    

    Additional help
    ---------------
    
    You can obtain info directly from the results applying "eval()"

    >>> path = deep_search(d2,'500','d2')
    >>> for p in path:
    >>>     tc._print(eval(p)) 
    
    >>> 5001
    >>> 5002
    >>> 5005
    >>> 5007
    >>> 5006
    >>> 5003
    >>> 5004
     

    """

    if not search_pattern == None:
        search_pattern = str(search_pattern)
    
    output = []
    current_datapoint = d
    current_datapoint_path = prev_datapoint_path
    if type(current_datapoint) is dict: # hago las búsquedas en el diccionario
        for dkey in current_datapoint:
            if not search_pattern == None:
                if search_pattern in str(dkey):
                    c = current_datapoint_path
                    c+="['"+dkey+"']"
                    output.append(c)

            elif isinstance(current_datapoint[dkey], (str,int,float)): # es un valor final?
                c = current_datapoint_path
                c+="['"+dkey+"']"
                output.append(c)
            c = current_datapoint_path
            c+="['"+dkey+"']"
            for i in deep_search(current_datapoint[dkey], search_pattern, c):
                if not i in output:
                    output.append(i)
                
    elif type(current_datapoint) is list: # hago las búsquedas en un elemento lista
        for i in range(0, len(current_datapoint)):
            if not search_pattern == None:            
                if search_pattern in str(i):
                    c = current_datapoint_path
                    c += "[" + str(i) + "]"
                    output.append(i)

            elif isinstance(current_datapoint[i], (str,int,float)): # es un valor final?
                c = current_datapoint_path
                c += "[" + str(i) + "]"
                output.append(i)
            c = current_datapoint_path
            c+="["+ str(i) +"]"
            for i in deep_search(current_datapoint[i], search_pattern, c):
                if not i in output:
                    output.append(i)                
    elif search_pattern == None: # no estoy buscando nada, sólo quiero los elementos terminales (leaves)
        if isinstance(current_datapoint, (str,int,float)): # es un valor final?               
            c = current_datapoint_path
            if not c in output:
                output.append(c)    
    elif search_pattern in str(current_datapoint):
        c = current_datapoint_path
        output.append(c)        
        
    output = filter(None, output)
    return list(output)



def change_values_in_nested_estructure(nested_structure: "structure (dict or list) where we want to operate changes" = [], 
                                       path: "path coming from deep_search" = [], 
                                       value_from: "original value" = "Sugar", 
                                       value_to: "new value" = "Extra-Sugar-HighPowered-But_Toxic!!!", 
                                       exact_match: "exact match or contained word only" = False):
    """
    change values in a nested structure (dict or list) from value_from to value_to
    using exact match or value_from contained only    
    original nested_structure is preserved, not changed
    

    Parameters
    ----------
    nested_structure : "structure (dict or list) where we want to operate changes", optional
        DESCRIPTION. The default is [].
    path : "path coming from deep_search", optional
        DESCRIPTION. The default is [].
    value_from : "original value", optional
        DESCRIPTION. The default is "Sugar".
    value_to : "new value", optional
        DESCRIPTION. The default is "Extra-Sugar-HighPowered".
    exact_match : "exact match or contained word only", optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None. new nested structure changed
    
    Example
    -------
    
    >>> path2 = deep_search(d2,'Sugar','d2')
    >>> dic_changed = change_values_in_nested_estructure(nested_structure = d2, 
    >>>                                   path = path2, 
    >>>                                   value_from = "Sugar", 
    >>>                                   value_to = "Extra-Sugar-HighPowered", 
    >>>                                   exact_match = False)
    
    
    

    """

    import re
    import copy
    dic = nested_structure # operate in local nexted_structure
    
    # dic = d2.copy()
    # value_from = "Sugar"
    # value_to = "Extra-Sugar-HighPowered-But_Toxic!!!"
    # path = path2
    # exact_match = False
    
    # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"
    if len(path)>0:
        first_path = path[0]
        position = first_path.find("[")
        dic_name = left(first_path, position)
        # ahora cambiamos todo dic_name por "dic" para poder operar correctamente en eval
        for idx in range(0, len(path)):
            # nos quedamos con todo a la derecha
            p = path[idx]
            rest_of_path = right(p, len(p) - position)
            path[idx] = f"dic{rest_of_path}" 
            
    # con esto encuentro los valores    
    for p in path:
        # tc._print(f"operando sobre el path ::{p}::")
        change = True
        resultado = eval(p)
        
        if isinstance(resultado,str):
            if exact_match:
                # comando = f"{p} = {p}.replace('{value_from}', '{value_to}')"
                regex_patron = f"\\b{value_from}+\\b" # busco cualquier aparición de una única palabra, exactamente               
                comando = f"{p} = re.sub(r'{regex_patron}', '{value_to}', {p})"
                # tc._print(comando, tc.G)
            else:
                comando = f"{p} = {p}.replace('{value_from}','{value_to}')"
                # tc._print(comando)                
        else:
            comando = f"{p} = {value_to}"
            # tc._print(comando, tc.B)            
            
 
        exec(comando) # aquí ya lo tengo, ahora sólo habría que cambiarlo    

    
    return dic    
    
    
def change_nested_structure(nested_structure: "dict or list to change" = [],
                            value_from: "original value" = "Sugar", 
                            value_to: "new value" = "Extra-Sugar-HighPowered-But_Toxic!!!", 
                            exact_match: "exact match or contained word only" = False):
    """
    change values in a nested_structure
    it's a wrapper that combines deep_search and change_values_in_nested_structure
        obtains paths from deep_search
        and calls change_values_in_nested_structure with paths obtained
    prevents original nested_structure from changes


    Parameters
    ----------
    nested_structure : "dict or list to change", optional
        DESCRIPTION. The default is [].
    value_from : "original value", optional
        DESCRIPTION. The default is "Sugar".
    value_to : "new value", optional
        DESCRIPTION. The default is "Extra-Sugar-HighPowered-But_Toxic!!!".
    exact_match : "exact match or contained word only", optional
        DESCRIPTION. The default is False.

    Returns
    -------
    new nested_structure changed

    """
    

    # get paths to change    
    path2 = deep_search(nested_structure, value_from)

    # changes values
    dic_changed = change_values_in_nested_estructure(nested_structure = nested_structure, 
                                       path = path2, 
                                       value_from = value_from, 
                                       value_to = value_to, 
                                       exact_match = exact_match)
    
  
    return dic_changed 

def all_values(d: "nested structure" = None, 
               path: "path of any key in the form d[0]['organizationId']" = None, 
               name_dict: "nombre local del dicionario" = None,
               ):
    """
    retrieves paths and values of all elements with the specified key

    Parameters
    ----------
    d : "nested structure", optional
        DESCRIPTION. The default is None.
    path : "path of any key in the form d2[0]['organizationId']", optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None. list of tuples containing path and value matching path expression

    """
    list_k_v = []
    
   
    # dic = d2.copy()
    # value_from = "Sugar"
    # value_to = "Extra-Sugar-HighPowered-But_Toxic!!!"
    # path = path2
    # exact_match = False
    
    # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"

    # path = "nestedStructure[0]['organizationId']"

    """ change original name of diccionationary to local dictionary for eval() """ 
    if name_dict == None:
        position = path.find("[")
        dic_name = left(path, position)
    else:
        dic_name = name_dict
    path = path.replace(f"{dic_name}[", "d[") # aunque me manden otro nombre de diccionario lo referencio siempre al nombre interno para poder llamar a eval

    """ get all paths """    
    paths = deep_search(d, prev_datapoint_path="d") # resolverá los paths con un nombre de diccionario interno "d" que conozco y que servirá para eval   
    
    # ejemplo de clave a buscar
    # path = "d[0]['organizationId']"

    """ detect patterns to obtain paths and values working with regex """    
    # de todos los paths del nestedStructure recupero los que se contengan números entre [] que significará que está en una lista
    import re

    """ find [digits] """
    regex_patron = r"\[[0-9]+\]" 
    comandos = re.findall(regex_patron, path)
    
    # consigo las "partes"
    path_patron = path

    """ build a pattern that substitutes [digits] by "\[[0-9]+\]" """
    # patron a buscar
    lp = path
    lp = lp.replace("[", "\[")
    lp = lp.replace("]", "\]")
    path_patron = path
    for c in comandos:
        path_patron = path_patron.replace(c, "\[[0-9]+\]")
    path_patron = path_patron.replace("['", "\['")
    path_patron = path_patron.replace("'']", "'\]")

    """ find it path matches pattern and, in this case, add to list (changing to original dictionary name) """
    for p in paths:

        # path_patron = "d2\\[[0-9]+\\]\\['organizationId'\\]"
        coms = re.findall(path_patron, p)
        if len(coms)>0:
            lp = p
            lp = lp.replace("d[", f"{dic_name}[")        
            list_k_v.append((lp, eval(p)))
    
    return list_k_v

def pointer_to_dict(d, path, level = 0):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    pointer_to_dict
    
    devuelve el diccionario apuntado por el path, en el level (hacia arriba), que se le pide
    siempre se devuelve una copia, por si se manipula, proteger el diccionario original
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - path (_type_): _description_
        - level (int, optional): _description_. Defaults to 0.
    """    
    dic = d.copy()



    
def extract_hierarchy_from_path(path: "string con llamada a un path de nestedStructure", elements_to_skip: "elemento que hay que quitar, 1 quitaría el último elemento" = 1, strict = False):
    """
    reverse the path hierarchy in elements_to_skip elements
    for example: in "d2[0]['organizationId']" with elements_to_skip = 1 we will get "d2[0]" with elements_to_skip = 2: "d2"
    if elements_to_skip is bigger than elements or -1 we could obtain, we will obtain the root element

    Parameters
    ----------
    path : "string con llamada a un path de nestedStructure"
        DESCRIPTION.
    elements_to_skip : "elemento que hay que quitar, 1 quitaría el último elemento", optional
        DESCRIPTION. The default is 1.
    strict: si está a False, puede llegar a devolver el puntero al diccionario (d), si está a True y pensando que es un JSON, devolverá el elemento d[xx]

    Returns
    -------
    path : TYPE
        DESCRIPTION.

    """
    # cada elemento que se quita comenzará siempre por [, como vamos hacia atrás, iremos buscando [ e iremos eliminando

    if elements_to_skip == -1:
        elements_to_skip = 1000000
    # path = "d2[0]['organizationId']"
    
    brackets = path.count("[")
    if elements_to_skip > brackets:
        elements_to_skip = brackets
        if strict:
            if elements_to_skip > 0:
                elements_to_skip -= 1
    
    for n in range(elements_to_skip):
        position = path.rfind("[") # encontramos, desde el final, la primera aparición de [
        path = left(path, position)
    
    return path

def get_value_from_path_OLD(nested_structure: "structure (dict or list) where we want to operate changes" = [], path: "path got from deep_search" = None):
    """
    gets value from dictionary using a path (as a string)    

    Parameters
    ----------
    nested_structure : "structure (dict or list) where we want to operate changes", optional
        DESCRIPTION. The default is [].
    path : "path got from deep_search", optional
        DESCRIPTION. The default is None.

    Returns
    -------
    retorno : TYPE
        DESCRIPTION. Value if found, None if not

    """

    if not isinstance(nested_structure, list):
        nested_structure = list(nested_structure)

    resultado = None
    

    import copy
    dic = nested_structure # operate in local nexted_structure
    
    # dic = d2.copy()
    # value_from = "Sugar"
    # value_to = "Extra-Sugar-HighPowered-But_Toxic!!!"
    # path = path2
    # exact_match = False
    
    # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"
    if not path == None:
        first_path = path
        position = first_path.find("[")
        dic_name = left(first_path, position)
        # ahora cambiamos todo dic_name por "dic" para poder operar correctamente en eval
        # nos quedamos con todo a la derecha
        p = path
        rest_of_path = right(p, len(p) - position)
        path = f"dic{rest_of_path}" 
            
    # con esto encuentro los valores - ojo, no compruebo si el path es válido  
    p = path
    # tc._print(f"operando sobre el path ::{p}::")
    change = True
    resultado = eval(p)
 
    
    return resultado

# exec_list = []

def set_value_for_path_OLD(nested_structure: "structure (dict or list) where we want to operate changes" = [], 
                       path: "path got from deep_search" = None,
                       new_value : "new value to set" = None):
    """
    gets value from dictionary using a path (as a string)    

    Parameters
    ----------
    nested_structure : "structure (dict or list) where we want to operate changes", optional
        DESCRIPTION. The default is [].
    path : "path got from deep_search", optional
        DESCRIPTION. The default is None.

    Returns
    -------
    retorno : TYPE
        DESCRIPTION. Value if found, None if not

    """

    # global exec_list

    if not isinstance(nested_structure, list):
        nested_structure = list(nested_structure)

    resultado = None
    


    dic = nested_structure # operate in local nexted_structure
    
    # dic = d2.copy()
    # value_from = "Sugar"
    # value_to = "Extra-Sugar-HighPowered-But_Toxic!!!"
    # path = path2
    # exact_match = False
    
    # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"
    if not path == None:
        first_path = path
        position = first_path.find("[")
        dic_name = left(first_path, position)
        # ahora cambiamos todo dic_name por "dic" para poder operar correctamente en eval
        # nos quedamos con todo a la derecha
        p = path
        rest_of_path = right(p, len(p) - position)
        path = f"dic{rest_of_path}" 
            
    # con esto encuentro los valores - ojo, no compruebo si el path es válido  
    p = f"{path} = {new_value}"
    # tc._print(f"operando sobre el path ::{p}::")
    change = True
    exec(p)
    tc.__trace(f"... new value for {path} : {new_value}", tc.Y)
            
    
    # exec_list.append(p)

def get_value_from_path(nested_structure: "structure (dict or list) where we want to operate changes" = [], path: "path got from deep_search" = None):
    """
    gets value from dictionary using a path (as a string)    

    Parameters
    ----------
    nested_structure : "structure (dict or list) where we want to operate changes", optional
        DESCRIPTION. The default is {}.
    path : "path got from deep_search", optional
        DESCRIPTION. The default is None.

    Returns
    -------
    retorno : TYPE
        DESCRIPTION. Value if found, None if not

    """

    # change made
    # if not isinstance(nested_structure, list):
    #     nested_structure = list(nested_structure)

    resultado = None
    

    import copy
    dic = nested_structure # operate in local nexted_structure
    

    # change made
    if not isinstance(path, str):
        return None
        
    # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"
    try:
        if not path == None:
            first_path = path
            position = first_path.find("[")
            dic_name = left(first_path, position)
            # ahora cambiamos todo dic_name por "dic" para poder operar correctamente en eval
            # nos quedamos con todo a la derecha
            p = path
            rest_of_path = right(p, len(p) - position)
            path = f"dic{rest_of_path}" 
    except:
        a = 999
            
    # con esto encuentro los valores - ojo, no compruebo si el path es válido  
    p = path
    # tc._print(f"operando sobre el path ::{p}::")
    change = True
    resultado = eval(p)
 
    
    return resultado

def set_value_for_path(nested_structure: "structure (dict or list) where we want to operate changes" = [], 
                       path: "path got from deep_search" = None,
                       new_value : "new value to set" = None):
    """
    gets value from dictionary using a path (as a string)    

    Parameters
    ----------
    nested_structure : "structure (dict or list) where we want to operate changes", optional
        DESCRIPTION. The default is [].
    path : "path got from deep_search", optional
        DESCRIPTION. The default is None.

    Returns
    -------
    retorno : TYPE
        DESCRIPTION. Value if found, None if not

    """

    if not isinstance(nested_structure, list):
        nested_structure = list(nested_structure)

    resultado = None
    


    dic = nested_structure # operate in local nexted_structure
    
    # dic = d2.copy()
    # value_from = "Sugar"
    # value_to = "Extra-Sugar-HighPowered-But_Toxic!!!"
    # path = path2
    # exact_match = False
    
    # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"
    if not path == None:
        first_path = path
        position = first_path.find("[")
        dic_name = left(first_path, position)
        # ahora cambiamos todo dic_name por "dic" para poder operar correctamente en eval
        # nos quedamos con todo a la derecha
        p = path
        rest_of_path = right(p, len(p) - position)
        path = f"dic{rest_of_path}" 
            
    # con esto encuentro los valores - ojo, no compruebo si el path es válido  
    p = f"{path} = {new_value}"
    # tc._print(f"operando sobre el path ::{p}::")
    change = True
    resultado = exec(p)
    tc.__trace(f"... new value for {path} : {new_value}", tc.Y) 
    
    return resultado

    
# =============================================================================
# Tratamiento de las nested_structures
# Una nested structure es un JSON, por ejemplo. Trata con diccionarios
# =============================================================================
class nested_structure:
    def __init__(self, 
                 d: "diccionario, lista o lista de diccionarios a trabajar" = [], 
                 name_dict: "local name of dict to operate with eval()" = "d",
                 educate_json: "si un diccionario contiene listas con valores, no sería un JSON educado" = False):
        """
        trabaja con un diccionario o lista de diccionarios como si fuesen bases de datos

        Parameters
        ----------
        d : "diccionario, lista o lista de diccionarios a trabajar", optional
            DESCRIPTION. The default is [].

        Returns
        -------
        None.

        """
        self._d = d
        self._paths = None
        self._internal_name_dict = "_self.d" # para resolver por eval internamente en el objeto
        self._external_name_dict = name_dict # para devolver la información al que llama al objeto
        if educate_json:
            self.educate_JSON()
        
    def deep_search(self, 
                    search_pattern: "what to search" = None,
                    # name_dict: "first call need to include name of dictionary in code" = None, 
                    exact_match: "True exact match, False if it's contained only" = False):
        """

        search_pattern es la parte más importante de esta función, determina qué estamos buscando
            devuelve todos los path que contengan el search_pattern tanto en key como en value


        opera en estructuras complejas y anidadas de listas y diccionarios (JSON)
        puede recibir una lista o un diccionario como entrada prev_datapoint_path
        el diccionario que contiene los paths si llamará con el valor enviado en 
            devuelve una lista con el camino de cada clave que contiene, como valor, el search_pattern
            si search_pattern está a None, genera los path de todos los elementos finales del nested_structure
        

        Parameters
        ----------
        search_pattern : "what to search", optional. 
            - si tiene un valor devuelve todos los paths que contienen ese valor en key o en value
            - si no se envían nada, devuelve todos los nodos terminales
            DESCRIPTION. The default is None.

        exact_match : "True exact match, False if it's contained only", optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """

        

        prev_datapoint_path = self._external_name_dict
        
        self._search_pattern = search_pattern
        # self._prev_datapoint_path = prev_datapoint_path
        self._exact_match = exact_match
        self._paths = deep_search(self._d, search_pattern, prev_datapoint_path, exact_match)
        return self._paths
        
    def flatten(self):
        """
        (c) Seachad
        
        Description:
        ---------------------- 
        flatten
        
        Devuelve el contenido del diccionario en formato flatten (como un csv)
        
        Extended Description:
        ---------------------
        _extended_summary_
        
        """        
        all_paths = self.deep_search()

        # d = d3 # elegimos el diccionario de prueba
        # d = self._d

        # columns = _columns_from_paths(d, all_paths)
        # final_structure, structure = _final_structure_from_paths(d, all_paths )
        # empty_raw = _emtpy_raw_from_columns(columns)
        # registros = []
        # registros = _function_to_generate_flat_json(d, final_structure, columns, empty_raw, registros)

        columns = self._columns_from_paths(all_paths)

        final_structure, structure = self._final_structure_from_paths( all_paths )
        empty_raw = self._emtpy_raw_from_columns(columns)
        registros = []
        # añadimos las columnas
        column_names = [x for x in columns]
        registros.append(column_names)        
        registros = self._function_to_generate_flat_json( final_structure, columns, empty_raw, registros)



        return registros

    def _columns_from_paths(self, all_paths):
        return _columns_from_paths(self._d, all_paths)

    def _final_structure_from_paths(self, all_paths ):
        return _final_structure_from_paths(self._d, all_paths )
    
    def _emtpy_raw_from_columns(self, columns):
        return _emtpy_raw_from_columns(columns)

    def _function_to_generate_flat_json(self, final_structure, columns, empty_raw, registros):
        return _function_to_generate_flat_json(self._d, final_structure, columns, empty_raw, registros)

    def get_columns_structure(self):
        """
        (c) Seachad
        
        Description:
        ---------------------- 
        get_columns_structure
        
        Devuelve la estructura de columnas de este elemento

        
        Extended Description:
        ---------------------
        Rastreamos todos los path y nos quedamos con todas las columnas que nos van llegando
        Así obtenemos la estructura de columnas necesarias para hacer flatten a este diccionario
        
        """
        all_paths = self.deep_search()


        pass

    def change_values(self, 
                            value_from: "original value" = "Sugar", 
                            value_to: "new value" = "Extra-Sugar-HighPowered-But_Toxic!!!", 
                            exact_match: "exact match or contained word only" = False):
        """
        change values in a nested_structure
        it's a wrapper that combines deep_search and change_values_in_nested_structure
            obtains paths from deep_search
            and calls change_values_in_nested_structure with paths obtained
        prevents original nested_structure from changes        

        Parameters
        ----------

        value_from : "original value", optional
            DESCRIPTION. The default is "Sugar".
        value_to : "new value", optional
            DESCRIPTION. The default is "Extra-Sugar-HighPowered-But_Toxic!!!".
        exact_match : "exact match or contained word only", optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        
        # get paths to change    
        path2 = self.deep_search(value_from, self._external_name_dict)
    
        # changes values
        dic_changed = change_values_in_nested_estructure(self._d, 
                                           path = path2, 
                                           value_from = value_from, 
                                           value_to = value_to, 
                                           exact_match = exact_match)
            
        
        return dic_changed

    def all_values(self, 
                   path: "path siempre referenciado al primer diccionario, por ejemplo (si está trabajando sobre una lista) -> d2[0]['organizationId']" = None):
        """
        devuelve todos los paths y valores para una clave concreta 

        Parameters
        ----------
        path : "path siempre referenciado al primer diccionario (si está trabajando sobre una lista)", optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None. list containing a tuple: first element -> list of paths containing element, second element -> value of unique element

        """




        return all_values( self._d, path, self._external_name_dict )


    def extract_hierarchy_from_path(self, path: "string con llamada a un path de nestedStructure", elements_to_skip: "elemento que hay que quitar, 1 quitaría el último elemento" = 1):
        """
        (c) Seachad
        
        Description:
        ---------------------- 
        extract_hierarchy_from_path
        
        devuelve el diccionario al que apunta el path con el offset level que se le pide
        offset siempre corre hacia atrás
        - 0 es el nivel actual
        - 1 es el nivel anterior
        - así hasta que lleva al primer niveles
        - (NOTA) si se le envía un nivel que no existe, simplemente devuelve el primer nivel del dicccionario
        
        Extended Description:
        ---------------------
        _extended_summary_
        
        
        Args:
        -----
            - path (string con llamada a un path de nestedStructure): _description_
            - elements_to_skip (elemento que hay que quitar, 1 quitar, optional): _description_. Defaults to 1.
        
        Returns:
        --------
            dict: diccionario al que apunta el valor que enviamos
        """        


        contenido = None
        literal_path =  extract_hierarchy_from_path(path, level = 0)
        # obtenemos el contenido 
        contenido = self.get_value_from_path(literal_path)
        return contenido




# =============================================================================
# Devuelve todos los paths que ha encontrado en que hay una lista con valores y no con diccionarios
# esto sería un JSON maldeducado...    
# =============================================================================
    def get_paths_of_lists_with_values(self):
        """
        devuelve paths de listas que contengan sólo valores (es decir, que no sean diccionarios)

        Returns
        -------
        None.

        """
        self._paths = get_lists_with_values(self._d)
        return self._paths
        pass
    
# =============================================================================
# Si el JSON contiene cosas maleducadas (tipo listas con valores) lo arregla...
# =============================================================================
    def educate_JSON(self):

        import datetime
        import terminal_colors as tc
        tc._print(f"... looking for list with final elements (no dicts)")
        # buscamos listas que contengan valores finales, no dict...
        paths = self.get_paths_of_lists_with_values()
        tc._print(f"... number of elements in lists: {len(paths)}")    
  
        
        # vamos cambiar cada path por un diccionario conteniendo una clave y un valor
        for path in paths:
            value = self.get_value_from_path(path)
            value = self.set_value_for_path(path, new_value = {"list_value" : value})
        
        
        pass
        
    def get_value_from_path(self, path):
        """
        returns value for the path

        Parameters
        ----------
        path : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        return get_value_from_path(nested_structure = self._d, path = path)
        pass
    
    def set_value_for_path(self, path, new_value):
        """
        actualiza un valor en un path con el nuevo valor

        Parameters
        ----------
        path : TYPE
            DESCRIPTION.
        new_value : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        set_value_for_path(nested_structure = self._d, path = path, new_value = new_value)
        pass
    
    
    def unique_values(self, 
                      path: "path to work on in order to get all unique values" = None,
                      ):
        """
        
        obtain information from a dictionary operating using paths
        returns a list of tuples where the paths point to a unique value
            element1 -> list of paths that point to value
            element2 -> value
        
        Example
        -------
        >>> all_values(path="data[0]['organizationId']")
        >>>
        >>> (["data[209]['organizationId']", "data[210]['organizationId']"],
        >>> '7a3a365b-3842-422c-9852-5d0deb1acbbd')        


        Parameters
        ----------
        path : "path to work on in order to get all unique values", optional
            DESCRIPTION. The default is None.

        Returns
        -------
        list_of_paths : TYPE
            DESCRIPTION.

        """

        
        list_of_paths = []        
        av = self.all_values(path)    
        tc._print(f"found {len(av)} paths in element", tc.C)
        # creo una lista de valores únicos para luego iterar por ella
        unique_values = list(set([x[1] for x in av]))
        for value in unique_values:
            paths = self.deep_search(value)
            tc._print(f"added {len(paths)} paths for - {value}", tc.C)
            list_of_paths.append((paths, value))       
            
        return list_of_paths
    
    def split_json_by_path(self, path: "path to split by" = None):
        """
        return a list of tuples, splitted by the path provided
            element1: json
            element2: value

        Example
        -------
        >>> split_by_unique_values
        

        Parameters
        ----------
        path : "path to split by", optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        

        
        list_of_jsons = []
        
        list_of_paths = self.unique_values(path)
        
        tc._print(f"found {len(list_of_paths)} unique values", tc.C)
        
        if len(list_of_paths)>0:

            # como hay que resolver, vamos a cambiar el resultado de lo que nos envían por el nombre interno del diccionario
            # pongo el nombre del diccionario local, porque no sé cómo se llama en origen (y no lo puedo obtener) así que lo cambio a "dic"

            first_path = list_of_paths[0][0][0]
            position = first_path.find("[")
            dic_name = left(first_path, position)
            # ahora cambiamos todo dic_name por "dic" para poder operar correctamente en eval
            dic_name=f"{dic_name}["
            
            for l in list_of_paths:
                ljson = []
        
                paths = l[0]
                value = l[1]
                for path in paths:

                    # quito la última llamada dentro del path para quedarme con el elemento completo
                    lpath = extract_hierarchy_from_path(path, 1) # me quedo con todos los elementos menos el último
                    lpath = lpath.replace(dic_name, "self._d[") # eval tiene que referirse al diccionario interno del objeto               
                    ld = eval(lpath)
                    ljson.append(ld)
                    
                list_of_jsons.append((ljson, value))
            
            return list_of_jsons
        else:
            return []

# ---- .
# ---- tests

def test_apply_function_to_dict_recursive():
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    test_apply_function_to_dict_recursive
    
    _summary_
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    """
    
    import os, json
    filename = "miniconfig.json"
    try:
        with open(filename) as json_file:
            miniconfig = json.load(json_file)
    except Exception as e:
        tc._print( f"Error de apertura del fichero de configuración >>>> {filename} - error {e}")    
    else:
        json_file.close()    

    import pprint

    tc._print("before")
    access = miniconfig[0].copy()
    pprint.pprint(access)
    
    # pendiente de que resuelva la info en environment variables, si no la encuentra en el diccionario
    # pendiente de que el diccionario dónde buscar pueda ser una lista de diccionarios...
    # por qué el dictionary_to_search_on se convierte mágicamente en el diccionario que se devuelve?
    
    tc._print("after", tc.G)
    access = resolve_dictionary_patterns(d = access, dictionary_to_search_on = access)
    pprint.pprint(access)
        
def test_resolve_dynamic_fstring(clave, diccionario):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    test_resolve_dynamic_fstring
    
    _summary_
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - clave (_type_): _description_
        - diccionario (_type_): _description_
    """    
    params = {}
    valor, params = _resolve_dynamic_fstring(
                 clave = "CM_work_folder", # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
                 # context = None, # contexto de queries (contiene toda la información lógica y el acceso a access con la información ya descargada de ENV y de ENCRYPT data)
                 list_of_dictionaries = [access], # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
                 current_dictionary = None, # diccionario donde quiero que empiece a buscar
                 # context_query = None, # lista de diccionarios guardada en context y que se recupera por el logical_name
                 params = params,
                 force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
                 )
    

def get_dictionary():

    true = True
    false = False

    d = [
    {
"date_now" : "@N@",
"API_ROBOT_MAQUINA_DESARROLLO" : "D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/",
"API_ROBOT_MAQUINA_DESARROLLO_OUT" : "{API_ROBOT_MAQUINA_DESARROLLO}1000 - MAQUINA_DESARROLLO",
"CM_extensions_d_conf" : "D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/100 - API_ROBOT_EXTENSIONS/PruebaLGV/",
"CM_extensions_d_path_in" : "D:/OneDrive - Seachad/API_ROBOT/data/",
"CM_extensions_d_rep_ea":"D:/OneDrive - /Rep_EA/",
"CM_extensions_d_rep_out_ar":"D:/REP_OUT/Rep_AR/",
"LGV_Configuration":"D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/05.- Proyectos/MAQUINA_TEST/API_ROBOT_VM",
"LGV_extension":"D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/100 - API_ROBOT_EXTENSIONS",
"LGV_reports_folder":"D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/1000 - MAQUINA_DESARROLLO/API_ROBOT_Reports_NEW/",

        "NAME_PROCESS": "PROCESS PRODUCCION ",
        "PROCESS_DESCRIPTION_FILE": "PROCESS - PRODUCTION.json",
        
        "PROCESS_TRACE_FILE": "{API_ROBOT_MAQUINA_DESARROLLO_OUT}/API_ROBOT_TRACE_FILES/{customer_name}.txt",
        "PROCESS_TRACE": true,

        "CUSTOMER_BATCH_NUMBER" : 10,
        "CUSTOMER_BATCH_DELAY_SGS" : 600,  

        "EXECUTE": true,

        "FILTERS": [ {"NAME_FILTER": "filter clientes", "FILTER": { "FILTER_CUSTOMERS_LIST": [
                        "Codere"
                    ]}}
        ],


        "EXTENSIONS": [
            {
                "AR_MODULE": "myExtensions",
                "AR_FUNCTIONS": [
                    {
                        "AR_TASK_PRODUCES": "_traza",
                        "AR_MANAGER_TYPE": "json_file",
                        
                        "@meta" : {
                        
                            "@meta.pf" : [
                                {"tooltip" : "pending"}
                                ]                           
                            }
                    },
                    {
                        "AR_TASK_PRODUCES": "_mapper",
                        "AR_MANAGER_TYPE": "json_file",

                        "@meta" : {
                        
                            "@meta.pf" : [
                                {"tooltip" : "pending"}
                                ],                           
                                
                            "@meta.API_ROBOT" : [                
                                {"AR_INPUT_PARAMETERS" : [
                                    {"AR_VARIABLE" : "filename", 
                                        "AR_REQUIRED" : true
                                        },
                                    {"AR_VARIABLE" : "parser_in",  
                                        "AR_VALUES" : "{ar_managers.list_of_parser_managers}",                         
                                        "AR_REQUIRED" : true},
                                    
                                    {"AR_VARIABLE" : "parser_out", 
                                        "AR_REQUIRED" : true}
                                    ]
                                 }
                                ]
                            }
                    }                    
                    
                ]
            },
            {



                "AR_MODULE": "{LGV_extension}/extensions_parsers",
                "AR_MODULE_LIBRARIES": ["{LGV_extension}/libraries"],

                "AR_FUNCTIONS": [

                    {
                        "AR_TASK_PRODUCES": "_parser_Params",
                        "AR_PARAMETERS" : [
                                             
                            {"path_OUT": "{CM_extensions_d_rep_out_ar}"},
                            {"path_LOG": "{CM_extensions_d_rep_out_ar}LOG/"}
                            
                            ],
                		"@meta" : {	
                                    
                                "@meta.API_ROBOT" : [                
                                    {"AR_INPUT_PARAMETERS" : [
                                        {"AR_VARIABLE" : "filename", 
                                            "AR_REQUIRED" : true
                                            },
                                        {"AR_VARIABLE" : "parser_in",
                                            "AR_VALUES" : "{ar_managers.list_of_parser_managers}",                         
                                            "AR_REQUIRED" : true},
                                        
                                        {"AR_VARIABLE" : "parser_out",  
                                            "AR_REQUIRED" : true}
                                        ]
                                     }
                                    ]  
                                } 

                    },
                    {
                        "AR_TASK_PRODUCES": "_parser_Azure",
                        "AR_PARAMETERS" : [
                            {"path_OUT": "{CM_extensions_d_rep_out_ar}"},
                            {"path_LOG": "{CM_extensions_d_rep_out_ar}LOG/"},
                            {"F_FACT" : "{CM_extensions_d_path_in}FACT/AzureOnetimeBillingReport.csv"},
                            {"F_MARG" : "{CM_extensions_d_path_in}FACT/margenesCSP.xlsx"},
			    {"F_SAPINV" : "{CM_extensions_d_rep_ea}SAPInvoices.xlsx"},
                            {"path_CONF" : "{CM_extensions_d_conf}"},
                            {"path_IN" : "{CM_extensions_d_path_in}"}                            
                            
                            ]
                    },
                    {
                        "AR_TASK_PRODUCES": "_parser_M365",
                        "AR_PARAMETERS" : [
                            {"path_IN_EA" : "{CM_extensions_d_rep_ea}"},
                            {"path_OUT": "{CM_extensions_d_rep_out_ar}"},
                            {"path_LOG": "{CM_extensions_d_rep_out_ar}LOG/"},
                            {"path_CONF" : "{CM_extensions_d_conf}"},
			    {"F_SAPINV" : "{CM_extensions_d_rep_ea}SAPInvoices.xlsx"},
                            {"path_IN" : "{CM_extensions_d_path_in}"}
                            ]

                    }


                ]
            }            

        ]
    }
]
    return d

def test_resolve_dictionary_patterns():
    diccionario = get_dictionary()


    access = [{"CM_work_folder" : "resuelto 1!",
              "directorio_out" : "resuelto 2!"}]
              
    dictionary_for_search = [diccionario, access]
    list_of_dictionaries = dictionary_for_search
    
    # l = [x for x in list_of_dictionaries if not isinstance(x, dict)]    
    
    # if len(l)>0:
    #     raise Exception("sólo puede enviarse una lista conteniendo diccionarios")
    
    # # list_of_dictionaries = list()
    # # dicts = list()
    # # dicts = convert_deep_dictionary_in_list_of_dictionaries(dictionary_for_search)   
    

    # valor, params = _resolve_dynamic_fstring(
    #               clave = "prueba fer", # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
    #               list_of_dictionaries = dictionary_for_search, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
    #               force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
    #               )   
    
    
    # # 1) cambio un nested_estructure en todos sus componentes
    # # 2) intento cambiar cada componente (recordemos que _resolve_dynamic_string no puede cambiar un diccionario a una lista desplegada de diccionarios, con lo que no podría profundizar en las búsquedas)

    # paths = deep_search(d2, "500")
    # paths = deep_search(d2)

    # for k,v in diccionario.items():
    #     valor, params = _resolve_dynamic_fstring(
    #                   clave = "prueba fer", # clave que quiero resolver (si la clave es un diccionario, resolverá todos sus elementos y devolverá un diccionario)
    #                   list_of_dictionaries = dictionary_for_search, # orden de diccionarios que trataremos para resolver la clave, desde el primero al último (se pasa por clave y la función los resuelve)
    #                   force_until_all_resolved = True, # por defecto dejo que se devuelvan parámetros sin resolver (cuidado con este flag, si queda algo sin resolver contínuamente, puede dar un reventado)
    #                   )   
    #     tc._print(valor)
        
    
    list_of_changes = {}
    diccionario = resolve_dictionary_patterns(d = diccionario[0], dictionary_to_search_on = diccionario, list_of_changes = list_of_changes )
    
    
    a = 1
    pass    

def get_columns_from_path(d, path):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    get_columns_from_path
    
    recibe un diccionario y un path
    devuelve el path en formato columnas, el path original y el valor del elemento
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - d (dict): diccionario en el que operamos
        - path (str): path del diccionario
    
    Returns:
    --------
        (tuple): column_name, original_path, value, type_value
    """
    import re
    regex_numbers_between_brackets = "\[\d*?\]"
    lpath = path[1:] # quito la "d" por facilidad de trabajo
    lpath = re.sub(regex_numbers_between_brackets, "", lpath)
    lpath = lpath.replace("['","")
    lpath = lpath.replace("']",".")
    lpath = lpath[:-1] 
    try:
        value = eval(path)       
    except Exception as e:
        tc._print(f"Error en eval de {path}")
    type_value = type(value)
    return lpath, path, value, str(type_value)


def get_list_elements(path):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    get_list_elements
    
    _summary_
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - path (_type_): _description_
    
    Returns:
    --------
        list: devuelve la lista de elementos que tienen una lista en el diccionario
    """    
    # devuelve la lista de elementos que tienen lista
    # devuelve el elemento que contiene la lista
    list_elements = []
    import re
    regex_numbers_between_brackets = "\[\d*?\]"
    p = re.compile(regex_numbers_between_brackets)
    lpath = path[1:] # quito la "d" por facilidad de trabajo
    # comandos = re.findall(regex_numbers_between_brackets, path)
    comandos = p.search( path)

    count = 0
    apariciones = []
    paths = []
    match_groups = []
    for match in p.finditer(path):
        count += 1
        match_groups.append(match.group())
        apariciones.append((match.start(), match.end()))
        paths.append(path[:match.end()])
        # list_elements.append((count, match.group(), match.start(), match.end(), path[:match.end()]))
        # tc._print("match", count, match.group(), "start index", match.start(), "End index", match.end())
    list_elements.append((count, match_groups, apariciones, paths))
    # limpiamos la lista
    # for comando in comandos:
    #     list_elements.append(comando)

    return list_elements
    pass

def _columns_from_paths(d, all_paths):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    calculate_columns
    
    calcula una lista con los nombres decorados de las columnas de un diccionario, recibiendo todos los paths del diccionario
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - d (dict): diccionario original
        - all_paths (paths): todos los paths del diccionario
    """    
    columns = {}
    """ CONSTRUIMOS LAS COLUMNAS QUE TENDRA LA LISTA """
    for path in all_paths:
        # position = path.find("['")
        # lpath = path[position:]
        lpath = get_columns_from_path(d, path)
        columns[lpath[0]] = lpath # guardamos el nombre de la columna y toda la información relativa al path que hemos calculado

    return columns

def _final_structure_from_paths(d, all_paths):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    calculate_final_structure
    
    Genera la estructura final con información de profundidad de claves, elementos previos a repetir, etc...
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - d (dict): diccionario original
        - all_paths (paths): todos los paths calculados previamente
    
    Returns:
    --------
        tuple: estructura a procesar para generar registros con información de profundidad, estructura original procesada (sirve para chequear información)
    """        

    """ ESTRUCTURA DE REGISTROS Y PARTES A REPETIR DEL JSON """
    regs = {}
    cnt = 0
    structure = {}
    regs = {}
    for path in all_paths:
        # como es un JSON miramos los paths de primer nivel
        current_element = extract_hierarchy_from_path(path, -1, strict = True) # esto me devuelve el diccionario
        regs[current_element] = True
        # tenemos que ver si hay elementos lista en alguno de estos paths
        list_elements = get_list_elements(path)
        for element in list_elements:
            for p in element[3]:
                deep = element[0]-1 # lo convertimos a un offset
                structure[p] = structure.get(p, {})
                structure[p][str(deep)] = structure[p].get(str(deep), [])
                structure[p][str(deep)].append(path)

    """ Ahora resuelvo la estructura encontrada """
    """ 
    Importante para que un nivel de profundidad superior tenga acceso a los niveles de profundidad inferior y así
    sabe qué es lo que tiene que ir repitiendo para construir el registro
    """ 
    final_structure = {}
    for k, v in structure.items():
        level_cero = extract_hierarchy_from_path(k, -1, strict = True)
        # k es d[0]
        deep = list(v.keys())[0] # cojo la única key que tiene
        values = v[deep]
        # deep es 1,2,3, ...
        final_structure[level_cero] = final_structure.get(level_cero, {})
        final_structure[level_cero][str(deep)] = final_structure[level_cero].get(str(deep), {})
        final_structure[level_cero][str(deep)][k] = final_structure[level_cero][str(deep)].get(k, [])
        final_structure[level_cero][str(deep)][k].append(values)  

    return final_structure, structure
    # esta función recibe un elemento y procede a ir hacia atrás hasta el nivel 0

LEAF = True
NO_LEAF = False




from collections import OrderedDict
def detect_leaves(d, final_structure, structure, all_paths):
    """ De la estructura final, detectamos las hojas """
    leaves = {} # vamos apuntando las leaves y las no leaves
    registros_path = []
    

    """ Primero marco todo como leaf """
    for k, v in final_structure.items():
        for kk, vv in v.items(): # vv es una lista de listas
            for kkk,vvv in vv.items():
                path = vvv[0]
                leaves[kkk] = LEAF
                # leaves[path[0]] = LEAF


    """ Por cada entrada de primera profundidad ... """
    # for k, v in final_structure.items():
    #     """ 
    #     k -> contiene el primer nivel (d[0], d[1], d[2], ...) 
    #     v -> contiene el nivel de profundidad 1, 2, 3, como clave y una lista con todos los elementos a ese nivel de profundidad, sean hojas o no
    #     """
    #     structure_ordered = OrderedDict(reversed(list(final_structure[k].items())))    
    #     for nivel_de_profundidad, vv in structure_ordered.items():
    #         registro_path = {}
    #         if isinstance(vv, dict):
    #             """ 
    #             si es un diccionario, me están llegando paths 
    #             empiezo a rastrear hacia atrás y lo que voy encontrando lo marco como no_leaf
    #             el nivel máximo de profundidad es el número de loops anidados para evitar la recursividad en la función
    #             vamos a llegar máximo a 3 niveles de profundidad, de momento
    #             """
    #             for kkk, vvv in vv.items():
    #                 for path in vvv:
    #                     # n_de_profundidad = int(nivel_de_profundidad)
    #                     for i in range(10, 0, -1):
    #                         hierarchy = extract_hierarchy_from_path(path[0], elements_to_skip = i)
    #                         leaves[hierarchy] = NO_LEAF
    #             # path_info = get_columns_from_path(d, vv)
    #             continue
    #         else:
    #             leaves[k] = False
    #             break

    """ Por cada entrada de primera profundidad ... """
    for k, v in final_structure.items():
        """ 
        k -> contiene el primer nivel (d[0], d[1], d[2], ...) 
        v -> contiene el nivel de profundidad 1, 2, 3, como clave y una lista con todos los elementos a ese nivel de profundidad, sean hojas o no
        """
        structure_ordered = final_structure    
        """ si hay un camino "hacia arriba" este elemento NO puede ser LEAF """
        for nivel_de_profundidad, vv in structure_ordered.items():
            registro_path = {}
            if isinstance(vv, dict):
                """ 
                si es un diccionario, me están llegando paths 
                empiezo a rastrear hacia atrás y lo que voy encontrando lo marco como no_leaf
                el nivel máximo de profundidad es el número de loops anidados para evitar la recursividad en la función
                vamos a llegar máximo a 3 niveles de profundidad, de momento
                """
                for kkk, vvv in vv.items():
                    for path in vvv:
                        # n_de_profundidad = int(nivel_de_profundidad)
                        for i in range(10, 0, -1):
                            hierarchy = extract_hierarchy_from_path(path[0], elements_to_skip = i)
                            leaves[hierarchy] = NO_LEAF
                # path_info = get_columns_from_path(d, vv)
                continue
            else:
                leaves[k] = False
                break



    """ 
    ultima pasada para encontrar siblings que se puedan haber quedado marcados como LEAF y realmente no lo son
    debido a que no formaban parte de la jerarquía máxima cuando se ha ido rastreando hacia atrás
    """
    leaves_LEAF = [x for x in leaves.keys() if leaves[x] == LEAF]
    for k in leaves_LEAF:
        v = leaves[k]
        """ 
        cojo todos los elementos que no son hojas 
        con extract_hierarchy_from_path obtengo su nivel anterior y veo si tiene siblings
        los marco como no_leaf
        """
        father = extract_hierarchy_from_path(k, elements_to_skip = 1)
        tc._print(f"{k} -> {father}")
        """ miro si la jerarquía anterior está en algún camino """
        leaves_LEAF_whitout_this = [x for x in leaves_LEAF if x != k]
        # si ya está marcado como NO_LEAF continuo
        for leaf in leaves_LEAF_whitout_this:
            if father in leaf and leaves[k] == True:
                leaves[k] = NO_LEAF
                break



    leaves_LEAF = {key:value for (key,value) in leaves.items() if value == LEAF}
    return leaves_LEAF
    pass


def _emtpy_raw_from_columns(columns, template_columns = None):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    emtpy_raw
    
    devuelve una estructura vacía, con los tipos por campo devueltos por la función
    pone a vacío los elementos incluídos en columnas
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - columns (_type_): _description_
    
    Returns:
    --------
        _type_: _description_
    """
    """ Creación de registro vacío """
    if template_columns == None:
        template_columns = {}
    for column_info in columns.values():
        if column_info[3] == "<class 'str'>":
            value = ""
        if column_info[3] == "<class 'int'>":
            value = 0
        if column_info[3] == "<class 'float'>":
            value = 0.0
        template_columns[column_info[0]] = value        
    return template_columns
    pass

# processed_paths_list = []

def __recursive_processing_of_information(
                                d, # diccionario sobre el que trabajamos
                                current_level_0, # nivel sobre el que estamos trabajando
                                level, # nivel de profundidad en el que estamos operando (0 es el de menor profundidad)
                                final_structure, # listas de paths con todas las diferentes profudndidades del diccionario
                                columns, # información por cada columnas
                                registro, # registro corriente en el que estamos trabajando
                                registros, # acumulado de registros para el diccionario
                                columns_processed = {}, # columnas que se han procesado (para luego borrar)
                                columns_to_maintain = {}, # columnas a mantener entre llamadas (se guardan las de nivel 0)
                                owner_level = 0, # qué nivel es el que ha empezado a llamar (2,1,0...?)
                                internal_call = False # la función recursiva se llama desde fuera o está en recursión?
                                ):

    """
    Description: 
    ------------

    Mediante recursividad, esta función recibe un diccionario y cierta información de control, y devuelve un conjunto de registros
    atendiendo a sus profundidades (marcadas en final_structure)

    """

    # esta función recibe un elemento y procede a ir hacia atrás hasta el nivel 0
    from collections import OrderedDict

    if int(level)==0 and internal_call == False: # nos están llamando desde fuera
        """ LLAMADO DESDE FUERA - ITERADOR DE ESTRUCTURAS """
        """ procesamos siempre desde el puntero a la profundidad más alta (siempre que haya listas estas van aumentando la profundidad y
        tienen que ir repitiendo todos los elementos de profundidades más bajas, hasta llegar a profundidad 0) """

        """ construyo desde el nivel más alto hasta el nivel más bajo de profundidad, es decir, en orden inverso """


        structure_ordered = OrderedDict(reversed(list(final_structure[current_level_0].items()))) # ahora lo tendrímos ordenado por deep pero al revés
        owner_level = int(list(structure_ordered.keys())[0])
        columns_to_maintain = {}
        columns_processed = {}
    else:
        """ LLAMADA RECURSIVA """ 
        structure_ordered = OrderedDict(reversed(list(final_structure[current_level_0][level].items()))) # ahora lo tendrímos ordenado por deep pero al revés
    
    # columns_processed = {}
    """ si llaman desde fuera, dejo el registro totalmente vacío """ 
    if not internal_call:
        registro = _emtpy_raw_from_columns(columns, registro)

    for k,v in structure_ordered.items():
        if k.isdigit(): # significa que me está llegando un nivel directamente
            deep = int(k)
            if not owner_level == deep: # está intentando iterar sobre los elementos inferiores, pero no han de ser procesados como tales ya que hay listas de mayor profundidad
                registro = _emtpy_raw_from_columns(columns, registro)
                return registros
        else:
            deep = int(level) # como no es un dígito cojo el nivel que me llega a la función


        """ rellenamos el registro """   
        info = None
        processing_key = "-"

        """ estamos procesando un diccionario o una lista de elementos? la lista son los paths finales... """
        if isinstance(v, dict):
            processing_key = list(v.keys())[0]
            # conseguimos all_paths y proecsamos una a una
            keys = v[processing_key]
            for element in keys[0]:
                info = get_columns_from_path(d, element) # aquí tenemos toda la información para rellena el registro
                registro[info[0]] = info[2]
                columns_processed[info[0]] = columns[info[0]]

        if isinstance(v,list): # estamos procesado la lista de elementos directamente
            # conseguimos all_paths y proecsamos una a una
            keys = v
            for element in keys[0]:
                info = get_columns_from_path(d, element) # aquí tenemos toda la información para rellena el registro
                registro[info[0]] = info[2]
                columns_processed[info[0]] = columns[info[0]]

        """ estamos en recursividad? """
        if not internal_call:
            columns_to_maintain = columns_processed.copy() # cuando llaman desde fuera y por si tengo que procesar profundidades, me quedo con la primera tanda de columnas que me llegó
  
        tc._print(f"Procesando {current_level_0} - {deep} - {k} - {processing_key }", tc.B)

        """ como no hemos llegado al nivel 0, llamamos a la función recursiva """ 
        if deep > 0:
            ldeep = deep - 1
            registros = recursive_processing_of_information(d, current_level_0, str(ldeep), final_structure, columns, registro, registros, columns_processed, columns_to_maintain, owner_level, internal_call = True)
        if deep == 0 and owner_level == deep:
            # llamada desde fuera a algo que no tiene listas
            #     
            registros.append(list(registro.values()))
            registro = _emtpy_raw_from_columns(columns, registro)
        if deep == 0 and not owner_level == deep: # hemos llegado al nivel de profunidad 0 en iteraciones de elementos que contienen listas
            registros.append(list(registro.values()))
            # quitamos todas las tablas procesadas menos las que tenemos que mantener
            l_columns_processed = columns_processed.copy()
            for k,v in l_columns_processed.items():
                if k in list(columns_to_maintain.keys()):
                    del columns_processed[k]

            registro = _emtpy_raw_from_columns(columns_processed, registro)
    
    return registros

def recursive_processing_of_information(
                                d, # diccionario sobre el que trabajamos
                                current_level_0, # nivel sobre el que estamos trabajando
                                level, # nivel de profundidad en el que estamos operando (0 es el de menor profundidad)
                                final_structure, # listas de paths con todas las diferentes profudndidades del diccionario
                                columns, # información por cada columnas
                                registro, # registro corriente en el que estamos trabajando
                                registros, # acumulado de registros para el diccionario
                                columns_processed = {}, # columnas que se han procesado (para luego borrar)
                                columns_to_maintain = {}, # columnas a mantener entre llamadas (se guardan las de nivel 0)
                                owner_level = 0, # qué nivel es el que ha empezado a llamar (2,1,0...?)
                                internal_call = False, # la función recursiva se llama desde fuera o está en recursión?
                                keys_to_process = [], # nivel en el que estamos trabajando (para debug)
                                ):

    """
    Description: 
    ------------

    Mediante recursividad, esta función recibe un diccionario y cierta información de control, y devuelve un conjunto de registros
    atendiendo a sus profundidades (marcadas en final_structure)

    """

    # esta función recibe un elemento y procede a ir hacia atrás hasta el nivel 0
    from collections import OrderedDict

    """ MIRANDO HACIA ATRAS CONSTRUIMOS LOS CAMPOS QUE SE NECESITAN """

    if int(level)==0 and internal_call == False: # nos están llamando desde fuera
        """ LLAMADO DESDE FUERA - ITERADOR DE ESTRUCTURAS """
        """ procesamos siempre desde el puntero a la profundidad más alta (siempre que haya listas estas van aumentando la profundidad y
        tienen que ir repitiendo todos los elementos de profundidades más bajas, hasta llegar a profundidad 0) """

        """ construyo desde el nivel más alto hasta el nivel más bajo de profundidad, es decir, en orden inverso """


        structure_ordered = OrderedDict(reversed(list(final_structure[current_level_0].items()))) # ahora lo tendrímos ordenado por deep pero al revés
        owner_level = int(list(structure_ordered.keys())[0])
        columns_to_maintain = {}
        columns_processed = {}
    else:
        """ LLAMADA RECURSIVA """ 
        # level = int(level) + 1
        structure_ordered = OrderedDict(reversed(list(final_structure[current_level_0][str(level)].items()))) # ahora lo tendrímos ordenado por deep pero al revés
        # sólo me quedo con el que corresponde
        # structure_ordered = {}
        # for key_to_process in keys_to_process:
        #     structure_ordered[key_to_process] = final_structure[current_level_0][str(int(level)+1)][key_to_process]
        # level = int(level) - 1
        # level = str(level)

    
    # columns_processed = {}
    """ si llaman desde fuera, dejo el registro totalmente vacío """ 
    if not internal_call:
        registro = _emtpy_raw_from_columns(columns, registro)

    """ Recorro del nivel más alto hasta el nivel más bajo, las estructuras que hay en el diccionario """
    for k,v in structure_ordered.items():
        if k.isdigit(): # significa que me está llegando un nivel directamente
            deep = int(k)
            if not owner_level == deep: # está intentando iterar sobre los elementos inferiores, pero no han de ser procesados como tales ya que hay listas de mayor profundidad
                registro = _emtpy_raw_from_columns(columns, registro)
                return registros
        else:
            deep = int(level) # como no es un dígito cojo el nivel que me llega a la función


        """ rellenamos el registro """   
        info = None
        processing_key = "-"

        """ AHORA CONSTRUIMOS LOS REGISTROS """
        """ estamos procesando un diccionario o una lista de elementos? la lista son los paths finales... """
        if isinstance(v, dict):
            all_keys = list(v.keys())
            for processing_key in all_keys:
            # conseguimos all_paths y proecsamos una a una
                keys = v[processing_key]
                for element in keys[0]:
                    info = get_columns_from_path(d, element) # aquí tenemos toda la información para rellena el registro
                    registro[info[0]] = info[2]
                    columns_processed[info[0]] = columns[info[0]]

                    """ estamos en recursividad? """
                    if not internal_call:
                        columns_to_maintain = columns_processed.copy() # cuando llaman desde fuera y por si tengo que procesar profundidades, me quedo con la primera tanda de columnas que me llegó
            
                    tc._print(f"Procesando {current_level_0} - {deep} - {k} - {processing_key }", tc.B)

                    """ como no hemos llegado al nivel 0, llamamos a la función recursiva """ 
                    if deep > 0:
                        # ldeep = deep - 1
                        ldeep = deep - 1
                        keys_to_process = list(final_structure[current_level_0][str(deep)]) # estas son las UNICAS claves que debe procesar
                        registros = recursive_processing_of_information(d, current_level_0, str(ldeep), final_structure, columns, registro, registros, columns_processed, columns_to_maintain, owner_level, internal_call = True, keys_to_process = keys_to_process)

                    if deep == 0 and owner_level == deep:
                        # llamada desde fuera a algo que no tiene listas
                        #     
                        registros.append(list(registro.values()))
                        registro = _emtpy_raw_from_columns(columns, registro)

                    if deep == 0 and not owner_level == deep: # hemos llegado al nivel de profunidad 0 en iteraciones de elementos que contienen listas
                        registros.append(list(registro.values()))
                        # quitamos todas las tablas procesadas menos las que tenemos que mantener
                        l_columns_processed = columns_processed.copy()
                        for k,v in l_columns_processed.items():
                            if k in list(columns_to_maintain.keys()):
                                del columns_processed[k]

                        registro = _emtpy_raw_from_columns(columns_processed, registro)

            return registros

        """ CARGAMOS INFORMACION """
        if isinstance(v,list): # estamos procesado la lista de elementos directamente
            # conseguimos all_paths y proecsamos una a una
            keys = v
            for element in keys[0]:
                info = get_columns_from_path(d, element) # aquí tenemos toda la información para rellena el registro
                registro[info[0]] = info[2]
                columns_processed[info[0]] = columns[info[0]]

        """ estamos en recursividad? """
        if not internal_call:
            columns_to_maintain = columns_processed.copy() # cuando llaman desde fuera y por si tengo que procesar profundidades, me quedo con la primera tanda de columnas que me llegó

        tc._print(f"Procesando {current_level_0} - {deep} - {k} - {processing_key }", tc.B)

        """ como no hemos llegado al nivel 0, llamamos a la función recursiva """ 
        if deep > 0:
            ldeep = deep - 1
            registros = recursive_processing_of_information(d, current_level_0, str(ldeep), final_structure, columns, registro, registros, columns_processed, columns_to_maintain, owner_level, internal_call = True)

        if deep == 0 and owner_level == deep:
            # llamada desde fuera a algo que no tiene listas
            #     
            registros.append(list(registro.values()))
            registro = _emtpy_raw_from_columns(columns, registro)

        if deep == 0 and not owner_level == deep: # hemos llegado al nivel de profunidad 0 en iteraciones de elementos que contienen listas
            registros.append(list(registro.values()))
            # quitamos todas las tablas procesadas menos las que tenemos que mantener
            l_columns_processed = columns_processed.copy()
            for k,v in l_columns_processed.items():
                if k in list(columns_to_maintain.keys()):
                    del columns_processed[k]

            registro = _emtpy_raw_from_columns(columns_processed, registro)                

    
    return registros





def _function_to_generate_flat_json(d, final_structure, columns, empty_raw, registros):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    recursive_function_to_generate_flat_json
    
    Genera un formato flatten (csv) de un json
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - d (dict): diccionario con el que se operar
        - final_structure (dict): estructura final preprocesada con las diferentes profundidades por registro
        - columns (list): lista con los nombres de las columnas precalculadas
    """  



    """ CREAMOS LOS VALORES Y LOS ASIGNAMOS A LAS COLUMNAS """
    """ Versión preliminar porque se ha de construir con información previa de estructura de registros para repetir deeps inferiores, etc... """

    mem_empty_raw = empty_raw


    # creo la lista de valores con el diccionario
    lista_valores = []
    lista_valores.append(list(columns.keys()))
    present_element = -1 # indicador de salto de path en el primer elemento (significa registro nuevo)
    new_reg = False
    
    # registros = []
    # rastreamos, 1 a 1, los elementos de nivel 0
    for structure in final_structure:
        """ VAMOS LLENANDO DESDE EL SUELO - profundidad 0 - PASANDO POR LAS SIGUIENTES PROFUNDIDADES """
        # ordenamos las claves en orden inverso para construir los registros desde la mayor profundidad
        # si tengo varias claves, las reordeno al revés
        tc._print(f"proceso de {structure}")
        l_registros = recursive_processing_of_information(d, 
                        structure, # current level 0 a procesar
                        "0", # empezamos siempre por el level 0
                        final_structure, # estructura precocinada de datos para poder navegar
                        columns, # información de las columnas
                        empty_raw, # registro corriente vacío
                        registros, # lista de registros
                        )

    return registros

def flatten_VM2_dictionary(d):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    flatten_VM_dictionary
    
    Función especializada en hacer un flatten a la estructura concreta de VM2
    
    Extended Description:
    ---------------------
    Dado que conocemos la estructura es más sencillo hacer el flatten que un flatten genérico que explote cualquier nivel de anidación y profundidad 
    
    
    Args:
    -----
        - d (_type_): _description_
    """

    def isNaN(num):
        return num!= num

    import pandas as pd
    df = pd.json_normalize(
        d, 
        errors='ignore',
        record_path =['Providers'], # <- tengo que construir una lista de listas con los datos de cada proveedor
        # meta=[
        #     'contracts',
        # #     ['contract_name'], 
        # #     # ['contracts', 'contract_name']
        # ]
    )
    df = df.reset_index()  # make sure indexes pair with number of rows

    # cojo una fila de ejemplo para crear la estructura que necesito de columnas, así me vendrá toda la información de data.contracts
    fila = df.loc[0]

    df1 = pd.DataFrame()

    """ ESTRUCTURA DE COLUMNAS DEL NUEVO DATAFRAME """
    columns = {}
    for col in df.columns:
        # si la columna es data.contracts quiero coger todas las columnas que dependen de ella
        if col == 'data.contracts':
            for contract in fila['data.contracts']:
                for key in contract:
                    columns[f"data.contracts.{key}"] = key
        # for list_of_dicts_contract in fila["data.contracts"]:
        #     for elemento in list_of_dicts_contract:
        #         for key, value in elemento.items():
        #             tc._print(f"{key} : {value}")
        else:
            columns[col] = col
    # muestro las key de columns
    keys = list(columns.keys())
    tc._print(keys)
    # columna que contiene la información que queremos explotar
    sub_key = 'data.contracts' # nombre del campo que contiene una lista de diccionarios que queremos explotar

    original_columns = list(df.columns)
    # eliminamos sub_key de la lista original_columns porque la voy a sustituir por los nuevos valores
    original_columns.remove(sub_key)

    """ creo un DF NUEVO con toda la información EXPLOTANDO la columna data.contracts creando todos sus columnas y asignándole sus valores """
    list_of_rows = []
    for index, row in df.iterrows():
        # registro = {}        
        # for col in original_columns:
        #     registro[col] = row[col]
        registro = {x:row[x] for x in original_columns}
        cabecera = registro.copy() # esta cabecera contiene lo común para los registros que se puedan generar desde list_of_dicts_contract
        list_of_dicts_contract = row[sub_key]
        if isNaN(list_of_dicts_contract):
            list_of_dicts_contract = []
        if len(list_of_dicts_contract)>0:
            for elemento in list_of_dicts_contract:
                new_registro = dict(**cabecera) # copio la cabecera para generar un registro nuevo
                for key, value in elemento.items():
                    # tc._print(f"{key} : {value}")
                    new_registro[f"{sub_key}.{key}"] = value
                list_of_rows.append(new_registro.copy())
        if len(list_of_dicts_contract)==0:     
            list_of_rows.append(registro.copy()) # no hay contratos, meto el registro tal y como está                
        

    return pd.DataFrame(list_of_rows) # creo el df



# def ___function_to_generate_flat_json(d, final_structure, columns, empty_raw, registros):
#     """
#     (c) Seachad
    
#     Description:
#     ---------------------- 
#     recursive_function_to_generate_flat_json
    
#     Genera un formato flatten (csv) de un json
    
#     Extended Description:
#     ---------------------
#     _extended_summary_
    
    
#     Args:
#     -----
#         - d (dict): diccionario con el que se operar
#         - final_structure (dict): estructura final preprocesada con las diferentes profundidades por registro
#         - columns (list): lista con los nombres de las columnas precalculadas
#     """  



#     """ CREAMOS LOS VALORES Y LOS ASIGNAMOS A LAS COLUMNAS """
#     """ Versión preliminar porque se ha de construir con información previa de estructura de registros para repetir deeps inferiores, etc... """

#     mem_empty_raw = empty_raw

#     from collections import OrderedDict
#     # creo la lista de valores con el diccionario
#     lista_valores = []
#     lista_valores.append(list(columns.keys()))
#     present_element = -1 # indicador de salto de path en el primer elemento (significa registro nuevo)
#     new_reg = False
    

#     # rastreamos, 1 a 1, los elementos de nivel 0
#     for structure in final_structure:
#         # ordenamos las claves en orden inverso para construir los registros desde la mayor profundidad
#         # si tengo varias claves, las reordeno al revés
#         structure_ordered = OrderedDict(reversed(list(final_structure[structure].items()))) # ahora lo tendrímos ordenado por deep pero al revés

#         for deep, values in structure_ordered.items(): # rastreo por cada nivel de profundidad
#             key = list(values.keys())[0]
#             v = values[key][0] # cólo contiene una lista (siempre está almacenada en el primer index) y contiene todos los paths
#             all_paths = v
#             for path in all_paths:
#                 # obtengo columna y valor
#                 info = get_columns_from_path(d, path) # obtengo toda la información relvante de este path
#                 # hay que identificar los saltos de d[0], d[1], ...

#                 empty_raw[info[0]] = info[2] # info[0] contiene la coolumna e info[2] contiene sy valor
#             if not int(deep) == 0:
#                 l_final_structure = final_structure[structure][str(int(deep)-1)]
#                 for clave, valor in l_final_structure.items(): 
#                     recursive_function_to_generate_flat_json(d, {clave:valor}, columns, empty_raw, registros)
#             else:
#                 # hemos procesado el primer nivel
#                 # hay que poner el registro a empty
#                 # PENDIENTE
#                 pass
#                 registros.append(list(empty_raw.values()))
    
#     return registros



def test_deep_search1():

    import json

       




""" ------------------------------------------------------------------- """
""" CONVERT JSON TO CSV """
""" source: https://stackoverflow.com/questions/41180960/convert-nested-json-to-csv-file-in-python """
""" CHEQUEADO Y FUNCIONA CORRECTAMENTE el 12/09/2022 """
""" ------------------------------------------------------------------- """

def cross_join(left, right):
    from copy import deepcopy
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem

""" A MI NO ME ESTA FUNCIONANDO - DEVUELVE SIEMPRE None"""
def json_to_dataframe(data_in, as_df = True):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    json_to_dataframe
    
    Devuelve un JSON o como lista de registros o como df (si as_df está a True)
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - data_in (json): json a desenroscar
        - as_df (bool, optional): devuelve como dataframe de pandas si está a True. Defaults to True.
    """    
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        # elif isinstance(data, list):
        #     rows = []
        #     for item in data:
        #         [rows.append(elem) for elem in flatten_list(flatten_json(item, prev_heading))]
        # else:
        #     rows = [{prev_heading[1:]: data}]
        elif isinstance(data, list):
                rows = []
                if(len(data) != 0):
                    for i in range(len(data)):
                        [rows.append(elem) for elem in flatten_list(flatten_json(data[i], prev_heading))]
                else:
                    data.append(None)
                    [rows.append(elem) for elem in flatten_list(flatten_json(data[0], prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows
    rows = flatten_json(data_in, prev_heading='')    
    # convertir la lista de rows en un dataframe
    if as_df:
        import pandas
        return pandas.DataFrame(flatten_json(data_in))
    else:
        return rows



# if __name__ == '__main__':
#     json_data = {
#         "id": "0001",
#         "type": "donut",
#         "name": "Cake",
#         "ppu": 0.55,
#         "batters":
#             {
#                 "batter":
#                     [
#                         {"id": "1001", "type": "Regular"},
#                         {"id": "1002", "type": "Chocolate"},
#                         {"id": "1003", "type": "Blueberry"},
#                         {"id": "1004", "type": "Devil's Food"}
#                     ]
#             },
#         "topping":
#             [
#                 {"id": "5001", "type": "None"},
#                 {"id": "5002", "type": "Glazed"},
#                 {"id": "5005", "type": "Sugar"},
#                 {"id": "5007", "type": "Powdered Sugar"},
#                 {"id": "5006", "type": "Chocolate with Sprinkles"},
#                 {"id": "5003", "type": "Chocolate"},
#                 {"id": "5004", "type": "Maple"}
#             ],
#         "something": []
#     }
#     df = json_to_dataframe(json_data)
#     tc._print(df)


#     def test_with_dictionary_flatten(path):
#         with open(path, "r") as read_content:
#             dict_to_try = json.load(read_content)
#         d = dict_to_try
#         if True:
#             from datetime import datetime
#             # vamos a calcular la complejidad del diccionario contenido en nso

#             nso = nested_structure(d)
#             all_paths = nso.deep_search()
#             complexity = len(all_paths)        

#             _start = datetime.now()
#             resultado = flatten_VM2_dictionary(d)
#             _end = datetime.now()
#             tc._print(f"ha tardado {(_end - _start).total_seconds()} segundos para un diccionario de complejidad {complexity} obteniendo {len(resultado)} contratos")


#     """ PRUEBA CON VM1.decrypted.json en el directorio COMPARTIR """ 
#     path = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/Compartir/VM1.decrypted.json"
#     test_with_dictionary_flatten(path)

#     d1 = [{'dict1':
#              {'part1':
#                   {'.wbxml': 'application/vnd.wap.wbxml',
#                    '.rl': 'application/resource-lists+xml'},
#               'part2':
#                   {'.wsdl': 'application/wsdl+xml',
#                    '.rs': 'application/rls-services+xml',
#                    '.xop': 'application/xop+xml',
#                    '.svg': 'image/svg+xml'}},
#               'lista_con_valores' : ["valor1", "valor2"],
#          'dict2':
#              {'part1':
#                   {'.dotx': 'application/vnd.openxmlformats-..',
#                    '.zaz': 'application/vnd.zzazz.deck+xml',
#                    '.xer': 'application/patch-ops-error+xml',
#                    '.svg': 'image/svg+xml',
#                    'lista_con_valores' : ["valor101", "valor202"],
                   
                   
#                    }}}]

#     """ ------------------------------------------------------ """
#     """ Pruebas para flatten y luego DF """
#     """ ------------------------------------------------------ """

#     from datetime import datetime

#     """ CON NSO y dict3"""
#     if False:
#         nso = nested_structure(d3)
#         all_paths = nso.deep_search()
#         complexity = len(all_paths)
#         _s = datetime.now()
#         registros = nso.flatten()
#         _e = datetime.now()
#         tc._print(f"Tiempo de procesado de un diccionario de complejidad {complexity} - {_e-_s}")
#         """ END CON NSO """

#     import json

#     """ CON NSO """
#     """ 19KB """
#     if False:
#         filename = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/1000 - MAQUINA_DESARROLLO/API_ROBOT_OUT/API_ROBOT_Reports/data/SUBS/01dda5b3-8abb-40cc-bd5f-3cb3a774ee20_Csp_Subscriptions.json"
#         total_complexity = 0
#         with open(filename, "r") as f:
#             the_json = json.load(f)
#         _s = datetime.now()        
#         # procesamos todos los diccionarios del json
#         nso = nested_structure(the_json)
#         all_paths = nso.deep_search()
#         complexity = len(all_paths)
#         total_complexity += complexity
#         registros = nso.flatten()
#         _e = datetime.now()
#         tc._print(f"Tiempo de procesado de un diccionario de complejidad {total_complexity} - {_e-_s} - total registros {len(registros)}")
#         """ END CON NSO """


#     """ CON NSO """
#     """ 55KB """
#     if False:
#         filename = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/1000 - MAQUINA_DESARROLLO/API_ROBOT_OUT/API_ROBOT_Reports/data/SUBS/000e11e4-ff70-47a0-a056-69ba38089e30_Csp_Subscriptions.json"
#         total_complexity = 0
#         with open(filename, "r") as f:
#             the_json = json.load(f)
#         _s = datetime.now()        
#         # procesamos todos los diccionarios del json
#         nso = nested_structure(the_json)
#         all_paths = nso.deep_search()
#         complexity = len(all_paths)
#         total_complexity += complexity
#         registros = nso.flatten()
#         _e = datetime.now()
#         tc._print(f"Tiempo de procesado de un diccionario de complejidad {total_complexity} - {_e-_s} - total registros {len(registros)}")
#         """ END CON NSO """

#     if False:
#         """ CON NSO """
#         """ 1,2GB """
#         filename = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/1000 - MAQUINA_DESARROLLO/API_ROBOT_OUT/API_ROBOT_Reports/data/SUBS/Csp_Subscriptions_ALL.json"
#         total_complexity = 0
#         with open(filename, "r") as f:
#             the_json = json.load(f)
#         _s = datetime.now()        
#         # procesamos todos los diccionarios del json
#         nso = nested_structure(the_json)
#         all_paths = nso.deep_search()
#         complexity = len(all_paths)
#         total_complexity += complexity
#         registros = nso.flatten()
#         _e = datetime.now()
#         tc._print(f"Tiempo de procesado de un diccionario de complejidad {total_complexity} - {_e-_s} - total registros {len(registros)}")
#         """ END CON NSO """

#     if False:
#         """ CON NSO """
#         """ VM """
#         filename = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/Compartir/VM1.json"
#         total_complexity = 0
#         with open(filename, "r") as f:
#             the_json = json.load(f)
#         _s = datetime.now()        
#         # procesamos todos los diccionarios del json
#         nso = nested_structure(the_json)
#         all_paths = nso.deep_search()
#         complexity = len(all_paths)
#         total_complexity += complexity
#         registros = nso.flatten()
#         _e = datetime.now()
#         tc._print(f"Tiempo de procesado de un diccionario de complejidad {total_complexity} - {_e-_s} - total registros {len(registros)}")
#         """ END CON NSO """



#     """ ERRONEA """
#     if False:
#         """ FORMA DE HACERLO SIN CLASES """
#         nso = nested_structure(d4_simplificado)
#         all_paths = nso.deep_search()
#         d = d4_simplificado # elegimos el diccionario de prueba
#         columns = _columns_from_paths(d, all_paths)
#         final_structure, structure = _final_structure_from_paths(d, all_paths )
#         empty_raw = _emtpy_raw_from_columns(columns)
#         registros = []
#         registros = _function_to_generate_flat_json(d, final_structure, columns, empty_raw, registros)
#         tc._print(registros)
#         """ END FORMA DE HACERLO SIN CLASES """



#     # # """ ESTRUCTURA DE REGISTROS Y PARTES A REPETIR DEL JSON """
#     # # """ ESTA NO FUNCIONA """
#     # regs = {}
#     # cnt = 0
#     # structure = {}
#     # regs = {}
#     # for path in all_paths:
#     #     # como es un JSON miramos los paths de primer nivel
#     #     current_element = extract_hierarchy_from_path(path, -1, strict = True) # esto me devuelve el diccionario
#     #     regs[current_element] = True
#     #     # tenemos que ver si hay elementos lista en alguno de estos paths
#     #     list_elements = get_list_elements(path)
#     #     for element in list_elements:
#     #         for p in element[3]: # rastreo los paths
#     #             deep = element[0] # qué profundidad tiene este path?
#     #             if deep == 1:
#     #                 lp = p # la clave principal siempre es el primer nivel (se supone que viene todo ordenado)
#     #             """ d[0] """    
#     #             structure[lp] = structure.get(lp, {}) 
#     #             """d[0]['1']"""
#     #             structure[lp][str(deep)] = structure[lp].get(str(deep), {})  
#     #             """d[0]['1'][<path>]"""
#     #             structure[lp][str(deep)][p] = structure[lp][str(deep)].get(p, [])
#     #             """d[0]['1'][<path>][<paths_completos>]"""
#     #             structure[lp][str(deep)][p].append(path)
#     # obtengo columna y valor

#     # a = False
#     # if a:
#     #     # creamos un template de registro con valores vacíos

#     #     """ CREAMOS LOS VALORES Y LOS ASIGNAMOS A LAS COLUMNAS """
#     #     """ Versión preliminar porque se ha de construir con información previa de estructura de registros para repetir deeps inferiores, etc... """
#     #     # creo la lista de valores con el diccionario
#     #     lista_valores = []
#     #     lista_valores.append(list(columns.keys()))
#     #     present_element = -1 # indicador de salto de path en el primer elemento (significa registro nuevo)
#     #     new_reg = False
#     #     template_columns = {}
#     #     for path in all_paths:
#     #         # obtengo columna y valor
#     #         info = get_columns_from_path(d, path)
#     #         # hay que identificar los saltos de d[0], d[1], ...
#     #         current_element = extract_hierarchy_from_path(path, -1, strict = True) # esto me devuelve el diccionario
#     #         if not current_element == present_element:
#     #             # creo el registro vacío
#     #             if not present_element == -1: # no guardo el primer registro que estará vacio, lo detecta por los cambios en el primer nivel (d[0], d[1],...)   
#     #                 lista_valores.append(list(template_columns.values()))
#     #             """ Creación de registro vacío """
#     #             template_columns = {}
#     #             for column_info in columns.values():
#     #                 if column_info[3] == "<class 'str'>":
#     #                     value = ""
#     #                 if column_info[3] == "<class 'int'>":
#     #                     value = 0
#     #                 if column_info[3] == "<class 'float'>":
#     #                     value = 0.0
#     #                 template_columns[column_info[0]] = value        

#     #             present_element = current_element

#     #         template_columns[info[0]] = info[2]
#     #     lista_valores.append(list(template_columns.values())) # guardo el último registro    
    
#     # TODO: pendiente -> ver cuándo cambia una jerarquía del tipo [0] o [1] porque hay que repetir todo lo que está anterior y meter la información que corresponda, repitiendo los registros

#     # analizamos la estructura y conseguimos los punteros a registros y los que es necesario repetir



#             # debo conseguir todos los paths con esta estructura hasta el siguiente nivel            

#     """ Pruebas con deep_search """
#     if False:
#         paths = deep_search([d2, d1], "500")
#         paths = deep_search([d2, d1])
#         # pendiente - me da error 
#         value = get_value_from_path([d2, d1], paths[0])
#         # voy a crear un diccionario con la resolución de claves y todas los valores
#         tc._print(paths)
#         paths = deep_search_lists_with_values ([d2, d1])   
        
#     pass

def test_deep_search2():

    dic = {'AR_UNIQUE_NAME': 'Reseller_CspSubscriptions_splitting', 'AR_TASK': '_TR', 'AR_TASK_PRODUCES': '_split_json', 'AR_APPLIES_TO': [{'AR_EVENT_SUBSCRIPTION': 'ON_POST_EXECUTE', 'AR_APPLIES_TO': 'Reseller_CspSubscriptions'}], 'AR_PRIORITY': 100, 'path': "d[0]['organizationId']", 'AR_NOTES': '', 'AR_EXECUTE': True}

    path = "d['path']"
    d = dic
    
    nso = nested_structure(d , "d")
    
    value = nso.deep_search(path)       


def split_json_by_path(data: "dictionary to operate on" = None, path: "path for the unique values" = None):
    """
    returns a list o tuples containint
        element1: json with all the dictionaries for the value
        element2: unique value extrated from path

    Parameters
    ----------
    data : "dictionary to operate on", optional
        DESCRIPTION. The default is None.
    path : TYPE, optional
        DESCRIPTION. The default is "path for the unique values" = None.

    Returns
    -------
    list_of_jsons : TYPE
        DESCRIPTION.

    """
    list_of_paths = []
    
    # nso = nested_structure_operations(data, "data")
    
    av = all_values(d = data, path="data[0]['organizationId']", name_dict = "data")    
    # creo una lista de valores únicos para luego iterar por ella
    unique_values = list(set([x[1] for x in av]))
    for value in unique_values:
        paths = deep_search(d = data, search_pattern = value, prev_datapoint_path = 'data')
        # tc._print(f"\n{paths}")
        list_of_paths.append((paths, value))


    # ahora, por cada lista, extraigo los elementos y lleno un nuevo JSON (que contendrá diccionarios)
    # cada JSON irá a disco
    list_of_jsons = []
    for l in list_of_paths:
        ljson = []

        paths = l[0]
        value = l[1]
        for path in paths:
            # quito la última llamada dentro del path para quedarme con el elemento completo
            lpath = extract_hierarchy_from_path(path, 1) # me quedo con todos los elementos menos el último
            ld = eval(lpath)
            ljson.append(ld)
        list_of_jsons.append((ljson, value))

    return list_of_jsons
    


def test_unique_values():
    
    filename = "D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/O365_Reseller_CspSubscriptions_ResellerSubs.json"
    
    import json
    with open(filename) as json_file:
        data = json.load(json_file)    
    
    
    """ esto funciona """
    
    # list_of_jsons = split_json_by_path(data, path="data[0]['organizationId']")
    
    """ esto funciona """
    
    nso = nested_structure(d = data, name_dict = "data")    
    
    list_of_jsons = nso.split_json_by_path(path="data[0]['organizationId']")
    
    # genero un json por cada elemento, con el nombre del value
    for lt in list_of_jsons:
        ljson = lt[0]
        value = lt[1]
        # genero un json por cada elemento, con el nombre del value
        with open("D:/kk/"+value+".json", "w") as json_file:
            # data = json.load(json_file)               
            json.dump(ljson, json_file, indent = 6)   
            tc._print(ljson)
            tc._print("\n----------------\n") 
    
    # vamos a probar las diferentes funciones de nso
    
    # deep_search
    paths = nso.deep_search(search_pattern = "1719d86b-b270-4154-b48c-6aa62471fdc5")
    paths = nso.all_values("d[0]['organizationId']")
    u_values = nso.unique_values("d[0]['organizationId']")
    new_dic = nso.change_values(value_from = "05fa74de-9f9e-447b-8d7f-217ff7bfa4f5",
                      value_to = "*** - ***",
                      exact_match = True)
    
    
    
    """ sin nso """
    
    # list_of_paths = []
    
    # # nso = nested_structure_operations(data, "data")
    
    # av = all_values(d = data, path="data[0]['organizationId']", name_dict = "data")    
    # # creo una lista de valores únicos para luego iterar por ella
    # unique_values = list(set([x[1] for x in av]))
    # for value in unique_values:
    #     paths = deep_search(d = data, search_pattern = value, prev_datapoint_path = 'data')
    #     tc._print(f"\n{paths}")
    #     list_of_paths.append((paths, value))


    # # ahora, por cada lista, extraigo los elementos y lleno un nuevo JSON (que contendrá diccionarios)
    # # cada JSON irá a disco
    # list_of_jsons = []
    # for l in list_of_paths:
    #     ljson = []

    #     paths = l[0]
    #     value = l[1]
    #     for path in paths:
    #         # quito la última llamada dentro del path para quedarme con el elemento completo
    #         lpath = extract_hierarchy_from_path(path, 1) # me quedo con todos los elementos menos el último
    #         ld = eval(lpath)
    #         ljson.append(ld)
    #     list_of_jsons.append(ljson)
    #     len(list_of_jsons)
        
    #     # genero un json por cada elemento, con el nombre del value
    #     with open("D:/kk/"+value+".json", "w") as json_file:
    #         # data = json.load(json_file)               
    #         json.dump(ljson, json_file, indent = 6)   
    #         tc._print(ljson)
    #         tc._print("\n----------------\n")
    
    """ con nso """
    
    # d = data
    
    list_of_paths = []
    
    nso = nested_structure(data, "data")
    
    av = nso.all_values(path="data[0]['organizationId']")    
    # creo una lista de valores únicos para luego iterar por ella
    unique_values = list(set([x[1] for x in av]))
    for value in unique_values:
        paths = nso.deep_search(value)
        tc._print(f"\n{paths}")
        list_of_paths.append((paths, value))


    # ahora, por cada lista, extraigo los elementos y lleno un nuevo JSON (que contendrá diccionarios)
    # cada JSON irá a disco
    for l in list_of_paths:
        ljson = []

        paths = l[0]
        value = l[1]
        for path in paths:
            # quito la última llamada dentro del path para quedarme con el elemento completo
            lpath = extract_hierarchy_from_path(path, 1) # me quedo con todos los elementos menos el último
            ld = eval(lpath)
            ljson.append(ld)
            
        # genero un json por cada elemento, con el nombre del value
        with open("D:/kk/"+value+".json", "w") as json_file:
            # data = json.load(json_file)               
            json.dump(ljson, json_file, indent = 6)   
            tc._print(ljson)
            tc._print("\n----------------\n")


import pprint
# ---- .
# ---- main

true = True
false = False

d1 = {'dict1':
            {'part1':
                {'.wbxml': 'application/vnd.wap.wbxml',
                '.rl': 'application/resource-lists+xml'},
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}},
        'dict2':
            {'part1':
                {'.dotx': 'application/vnd.openxmlformats-..',
                '.zaz': 'application/vnd.zzazz.deck+xml',
                '.xer': '500'}}}

d2 = {
    "items":
        {
            "item":
                [
                    {
                        "id": "0001",
                        "type": "donut",
                        "name": "Cake",
                        "ppu": 0.55,

                        "batters":
                            {
                                "batter":
                                    [
                                        {"id": "1001", "type": "Regular"},
                                        {"id": "1002", "type": "Chocolate"},
                                        {"id": "1003", "type": "Blueberry"},
                                        {"id": "1004", "type": "Devil's Food"}
                                    ]
                            },
                        "topping":
                            [
                                {"id": "5001", "type": "None"},
                                {"id": "5002", "type": "Glazed"},
                                {"id": "5005", "type": "Sugar"},
                                {"id": "5007", "type": "Powdered Sugar Sugar1"},
                                {"id": "5006", "type": "Chocolate with Sprinkles"},
                                {"id": "5003", "type": "Chocolate"},
                                {"id": "5004", "type": "Maple"},
                                {"id": "5004", "type": 1500}
                            ]
                    },



                ]
        }
}    

d3 = [
    {'dict1':
            {'part1':
                {'.wbxml': 'application/vnd.wap.wbxml',
                '.rl': 'application/resource-lists+xml'},
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}},
        'dict2':
            {'part1':
                {'.dotx': 'application/vnd.openxmlformats-..',
                '.zaz': 'application/vnd.zzazz.deck+xml',
                '.xer': '500'}}},
    {'dict1':
            {'part1':
                {'.wbxml': 'application/vnd.wap.wbxml',
                '.rl': 'application/resource-lists+xml'},
            "lista1" : [
            {
            'lista1_part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'},                    
            
            'lista1_part3':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}
            }                
            ],
            "lista3" : [
            {
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml',
            "lista4" : [
            {
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'},                    
            
            'part3':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}
            }
            ],                     
                },                    
            
            'part3':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}
            }
            ],               
            "lista1" : [
            {
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'},                    
            
            'part3':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}
            }
            ],  
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}},
        'dict2':
            {'part1':
                {'.dotx': 'application/vnd.openxmlformats-..',
                '.zaz': 'application/vnd.zzazz.deck+xml',
                '.xer': '500'}}},
    {'dict1':
            {'part1':
                {'.wbxml': 'application/vnd.wap.wbxml',
                '.rl': 'application/resource-lists+xml'},
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}},
        'dict2':
            {'part1':
                {'.dotx': 'application/vnd.openxmlformats-..',
                '.zaz': 'application/vnd.zzazz.deck+xml',
                '.xer': '500'}}},
    {'dict1':
            {'part1':
                {'.wbxml': 'application/vnd.wap.wbxml',
                '.rl': 'application/resource-lists+xml'},
            'part2':
                {'.wsdl': 'application/wsdl+xml',
                '.rs': 'application/rls-services+xml',
                '.xop': 'application/xop+xml',
                '.svg': 'image/svg+xml'}},
        'dict2':
            {'part1':
                {'.dotx': 'application/vnd.openxmlformats-..',
                '.zaz': 'application/vnd.zzazz.deck+xml',
                '.xer': '500'}}}                                                                   

]


d4_simplificado = [
    {
        "Name": "BONPREU",
        "Providers": [
            {
                "Name": "Microsoft",
                "data": {
                    "tenant_id": "170c1e5f-0a9f-4a6f-8f20-YYYY",
                    "contracts": [
                        {
                            "contract_name": "CSP",
                            "expiration_date" : "2022-07-28",
                        },
                        {
                            "contract_name": "EA",
                        }
                    ]
                }
            },
            {
                "Name": "Cloudmore",
                "data": {
                    "organizationid": "-------- Cloudmore organization",
                }
            },
            {
                "Name": "Arrow",
                "data": {
                    "organizationid": "------- Arrow organization",
                }
            }
        ]
    },
    {
        "Name": "CODERE",
        "Providers": [
            {
                "Name": "Microsoft",
                "data": {
                    "organizationid": "170c1e5f-0a9f-4a6f-8f20-XXXX",
                    "contracts": [
                        {
                            "contract_name": "CSP",
                        },
                        {
                            "contract_name": "EA",
                        },
                        {
                            "contract_name": "New EA",
                        }
                    ]
                }
            },
            {
                "Name": "Cloudmore",
                "data": {
                    "organizationid": "-------- Cloudmore organization",
                    "contracts": [
                        {
                            "contract_name": "Cloudmore CSP",
                        },
                    ]                     
                }
            },
            {
                "Name": "Arrow",
                "data": {
                    "organizationid": "------- Arrow organization",
                    "contracts": [
                        {
                            "contract_name": "Arrow CSP",
                        },
                        {
                            "contract_name": "Arrow EA",
                        },
                        {
                            "contract_name": "Arrow New EA",
                        }
                    ]                    
                }
            }
        ]
    }    
    ]









def test_readJSON():
    filename = "D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/1000 - MAQUINA_DESARROLLO/API_ROBOT_EXECUTION/Process Production.json"
    list_of_changes = {}
    path_to_libraries = "D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/999 - API_ROBOT/libraries"
    sys.path.insert(0,path_to_libraries)     
    import common
    resultado = common.readJSON(filename, _resolve_patterns = True, 
                         _resolve_dates = True, 
                         _additional_dictionaries_to_look_in = [access], list_of_changes = list_of_changes)    
    
    pass


# if __name__ == "__main__":
#     test_resolve_dictionary_patterns()
    
    
    
#     pass
    
    
def resto_tests():
    test_unique_values()



    tc._print(test_deep_search1())
    
    # d1 = {'dict1':
    #          {'part1':
    #               {'.wbxml': 'application/vnd.wap.wbxml',
    #                '.rl': 'application/resource-lists+xml'},
    #           'part2':
    #               {'.wsdl': 'application/wsdl+xml',
    #                '.rs': 'application/rls-services+xml',
    #                '.xop': 'application/xop+xml',
    #                '.svg': 'image/svg+xml'}},
    #      'dict2':
    #          {'part1':
    #               {'.dotx': 'application/vnd.openxmlformats-..',
    #                '.zaz': 'application/vnd.zzazz.deck+xml',
    #                '.xer': 'application/patch-ops-error+xml'}}}

    d2 = {
        "items":
            {
                "item":
                    [
                        {
                            "id": "0001",
                            "type": "donut",
                            "name": "Cake",
                            "ppu": 0.55,
                            "batters":
                                {
                                    "batter":
                                        [
                                            {"id": "1001", "type": "Regular"},
                                            {"id": "1002", "type": "Chocolate"},
                                            {"id": "1003", "type": "Blueberry"},
                                            {"id": "1004", "type": "Devil's Food"}
                                        ]
                                },
                            "topping":
                                [
                                    {"id": "5001", "type": "None"},
                                    {"id": "5002", "type": "Glazed"},
                                    {"id": "5005", "type": "Sugar"},
                                    {"id": "5007", "type": "Powdered Sugar Sugar1"},
                                    {"id": "5006", "type": "Chocolate with Sprinkles"},
                                    {"id": "5003", "type": "Chocolate"},
                                    {"id": "5004", "type": "Maple"},
                                    {"id": "5004", "type": 1500}
                                ]
                        },



                    ]
            }
    }    
    
    # import pprint

    
    # path1 = deep_search(d1,'svg+xml','d1')
    # pprint.pprint(path1)     
      
    # # change string
    # # ----------------------------------------------
    
    # value_from = 'Sugar'
    # value_to = "Extra-Sugar-HighPowered" 
    
    # tc._print("\nd2 -----------------------", tc.R)
    # path2 = deep_search(d2,value_from,'d2')
    # pprint.pprint(path2)  

    # tc._print("\nAntes ---------------------------")
    # pprint.pprint(d2)
    # tc._print("\nOperación -----------------------", tc.R)
    
    # # ahora voy a cambiar "Sugar" por "Extra-Sugar-HighPowered"
    # dic_changed = change_values_in_nested_estructure(nested_structure = d2, 
    #                                    path = path2, 
    #                                    value_from = value_from, 
    #                                    value_to = value_to, 
    #                                    exact_match = True)
    
    # tc._print("\nDespues -------------------------", tc.G)    
    # pprint.pprint(dic_changed)     
        
    # # ----------------------------------------------
    
    # # change int    
    # # ----------------------------------------------
    
    # value_from = 1500
    # value_to = 2000
    
    # tc._print("\nd2 -----------------------", tc.R)
    # path2 = deep_search(d2,value_from,'d2')
    # pprint.pprint(path2)  

    # tc._print("\nAntes ---------------------------")
    # pprint.pprint(d2)
    # tc._print("\nOperación -----------------------", tc.R)
    
    # # ahora voy a cambiar "Sugar" por "Extra-Sugar-HighPowered"
    # dic_changed = change_values_in_nested_estructure(nested_structure = d2, 
    #                                    path = path2, 
    #                                    value_from = value_from, 
    #                                    value_to = value_to, 
    #                                    exact_match = True)
    
    # tc._print("\nDespues -------------------------", tc.G)    
    # pprint.pprint(dic_changed)     
        
    # # ----------------------------------------------     
    
    # # change combined
    # # ----------------------------------------------     
    # dic_changed = change_nested_structure(nested_structure = d2, 
    #                                    value_from = value_from, 
    #                                    value_to = value_to, 
    #                                    exact_match = True)
    
    # tc._print("\nDespues -------------------------", tc.G)    
    # pprint.pprint(dic_changed)      

    # # ----------------------------------------------     
    
    
    # pprint.pprint(deep_search(d2,'XYZ','d2'))    
    
    # test_apply_function_to_dict_recursive()
    
    # # encontrar subcadenas en python, y su índice de aparición
    # cadena = "Sugar Sugar Sugar1"
    
    # import re
    # value_from = "Sugar"
    # value_to = "Peligro Extremo!!"
    
    # patron = f"\\b{value_from}+\\b"

    # regex_patron = patron
    # cadena = "Sugar Sugar Sugar1"
    # list_of_parameters = re.findall(regex_patron, cadena) 
    
    # list_of_search = re.search(regex_patron, cadena)

    # cadena = "Sugar Sugar Sugar1"
    # offset = 0
    # cnt = 0
    # for m in re.finditer(regex_patron, cadena): # matchs originales
    #     tc._print(m)
    #     start_offset = m.span()[0] + (cnt * len(value_to))
    #     tc._print(m.span())
    #     tc._print((start_offset))
        
    #     position = start_offset
    #     lc = left(cadena, position)  
    #     tc._print(f"lc {lc}")
    #     position = m.span()[1] - (len(value_from) * cnt) + (len(value_to) * cnt)
    #     rc = right(cadena, position)
    #     tc._print(f"rc {rc}")
    #     tc._print(f"{lc}{value_to}{rc}")
    #     cadena = f"{lc}{value_to}{rc}"
    #     # offset += len(value_to)
    #     cnt += 1

def calculate_complexity(d):
    """ wrapper """
    return calculate_dict_complexity(d)


def calculate_dict_complexity(d):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    get_dict_complexity
    
    Devuelve un índice sobre la complejidad del diccionario, atendiendo a la complejidad de sus paths
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - d (_type_): _description_

    Returns:
    --------
    complexity_index (int): índice de la complejidad del diccionario
    inner_complexity (int): índice de la complejidad del diccionario, atendiendo a la cantidad de información que contiene

    """    

    # d = d4_simplificado # elegimos el diccionario de prueba
    nso = nested_structure(d)
    # saco todos los paths
    all_paths = nso.deep_search()
    complexity = len(all_paths)

    # inner_complexity = 0

    # for path in all_paths:
    #     value = get_value_from_path(d, path)
    #     inner_complexity += 1
        
    return complexity
    pass

def nested_json_structure():
    """ FORMA DE HACERLO SIN CLASES """
    path = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/Compartir/VM1.decrypted.json"

    import json
    with open(path, "r") as read_content:
        dict_to_try = json.load(read_content)
    d = dict_to_try


    # d = d4_simplificado # elegimos el diccionario de prueba
    nso = nested_structure(d)
    # saco todos los paths
    all_paths = nso.deep_search()
    complexity = len(all_paths)
    # obtengo todas las columnas
    columns = _columns_from_paths(d, all_paths)
    # obtengo TODAS las estructuras
    final_structure, structure = _final_structure_from_paths(d, all_paths )
    leaves = detect_leaves(d, final_structure, structure, all_paths)
    empty_row = _emtpy_raw_from_columns(columns)
    registros = []
    registros = _function_to_generate_flat_json(d, final_structure, columns, empty_row, registros)
    import datetime
    _start = datetime.datetime.now()
    resultado = flatten_VM2_dictionary(d)
    _end = datetime.datetime.now()
    tc._print(f"ha tardado {(_end - _start).total_seconds()} segundos para un diccionario de complejidad {complexity} obteniendo {len(resultado)} contratos")

    tc._print(registros)
    """ END FORMA DE HACERLO SIN CLASES """




def test_flatten_json():
    # source: https://stackoverflow.com/questions/41180960/convert-nested-json-to-csv-file-in-python
    from copy import deepcopy
    import pandas

    path = "C:/Users/ferna/OneDrive - Seachad (1)/07 - DESARROLLOS INTERNOS/Compartir/VM1.json"

    import json
    with open(path, "r") as read_content:
        dict_to_try = json.load(read_content)
    d = dict_to_try


    json_data = {
        "id": "0001",
        "type": "donut",
        "name": "Cake",
        "ppu": 0.55,
        "batters":
            {
                "batter":
                    [
                        {"id": "1001", "type": "Regular"},
                        {"id": "1002", "type": "Chocolate"},
                        {"id": "1003", "type": "Blueberry"},
                        {"id": "1004", "type": "Devil's Food"}
                    ]
            },
        "topping":
            [
                {"id": "5001", "type": "None"},
                {"id": "5002", "type": "Glazed"},
                {"id": "5005", "type": "Sugar"},
                {"id": "5007", "type": "Powdered Sugar"},
                {"id": "5006", "type": "Chocolate with Sprinkles"},
                {"id": "5003", "type": "Chocolate"},
                {"id": "5004", "type": "Maple"}
            ],
        "something": []
    }

    # d = json_data

    if True:
        import pandas
        try:
            rows = json_to_dataframe(d)
        except Exception as e:
            a = 999
        a = 999
        # return pandas.DataFrame(json_to_dataframe(d))   


if __name__ == "__main__":
    
    import datetime


    # test_deep_search1()    

    # nested_json_structure()


    # test_flatten_json()

    df = test_flatten_json()

    # import datetime        
    # _s = datetime.datetime.now()
    # paths = deep_search(d, search_pattern = "application", prev_datapoint_path = 'd')
    # _e = datetime.datetime.now()
    # tc._print(f"ha tardado {_e-_s} sgs")
    # pprint.pprint(paths)        
    
      


    """ BUSCO LISTA CON VALORES """    
    # import datetime
    # _s = datetime.datetime.now()
    # paths = get_lists_with_values(d, prev_datapoint_path = 'd')
    # _e = datetime.datetime.now()
    # tc._print(f"ha tardado {_e-_s} sgs")
    # tc._print(f"{len(paths)}")     
    # pprint.pprint(paths)

    # vamos cambiar cada path por un diccionario conteniendo una clave y un valor
    # for path in paths:
    #     value = get_value_from_path(d, path)
    #     tc._print(f"for {path} value {value}")
    #     value = set_value_for_path(d, path, {"item" : value})
        
    # voy a trabajar con un JSON externo        
    """ CUANTA TARDA EN PROCESAR UN DICCIONARIO MONSTRUOSO? """ 
    if False:
        filename = "D:/OneDrive - Seachad/07 - DESARROLLOS INTERNOS/Compartir/bb26d856-8d57-486d-9615-238e89c398b2/Fact_Users_Beta.json"
        import json
        with open(filename, 'r') as json_file:
            data = json.load(json_file)    
        
        # # buscamos listas que contengan valores finales, no dict...
        # _s = datetime.datetime.now()
        # paths = get_lists_with_values(data, prev_datapoint_path = 'data')
        # _e = datetime.datetime.now()
        # tc._print(f"ha tardado {_e-_s} sgs")    
        # tc._print(f"{len(paths)}")    
        # pprint.pprint(paths)    
        
        # # vamos cambiar cada path por un diccionario conteniendo una clave y un valor
        # _s = datetime.datetime.now()    
        # for path in paths:
        #     value = get_value_from_path(data, path)
        #     value = set_value_for_path(data, path, new_value = {"list_value" : value})
        # _e = datetime.datetime.now()
        # tc._print(f"ha tardado {_e-_s} sgs") 
        
        
        
        
        # con Nested Structure
        _s = datetime.datetime.now()
        ne = nested_structure(data, name_dict="data", educate_json=True)
        _e = datetime.datetime.now()
        tc._print(f"ha tardado {_e-_s} sgs")  