# ! CACHE CODE
import threading
import seachad.common_libraries.terminal_colors as tc
# class SingletonDict:
#     _instance = None
#     _lock = threading.Lock()

#     def __new__(cls):
#         if cls._instance is None:
#             with cls._lock:
#                 if cls._instance is None:
#                     cls._instance = super(SingletonDict, cls).__new__(cls)
#                     cls._instance._data = {}
#         return cls._instance

#     def __setattr__(self, name, value):
#         if name == "_data":
#             super(SingletonDict, self).__setattr__(name, value)
#         else:
#             self._data[name] = value

#     def __getattr__(self, name):
#         return self._data.get(name, None)

#     def __delattr__(self, name):
#         if name in self._data:
#             del self._data[name]
#         else:
#             raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

#     def __getitem__(self, key):
#         return self._data.get(key, None)

#     def __setitem__(self, key, value):
#         self._data[key] = value

#     def __delitem__(self, key):
#         if key in self._data:
#             del self._data[key]
#         else:
#             raise KeyError(f"'{key}'")

#     def __repr__(self):
#         return repr(self._data)

#     def items(self):
#         return self._data.items()

#     def delete_keys_starting_with(self, prefix):
#         """Elimina todas las claves que comiencen con el prefijo dado."""
#         keys_to_delete = [key for key in self._data if key.startswith(prefix)]
#         for key in keys_to_delete:
#             del self._data[key]

#     def clear(self):
#         """Elimina todas las claves del diccionario."""
#         self._data.clear()

#     def keys_starting_with(self, prefix):
#         """Devuelve todas las claves que comiencen con el prefijo dado."""
#         return [key for key in self._data if key.startswith(prefix)]

#     def values_starting_with(self, prefix):
#         """Devuelve todos los valores cuyas claves comiencen con el prefijo dado."""
#         return [value for key, value in self._data.items() if key.startswith(prefix)]

#     def dict_starting_with(self, prefix):
#         """Devuelve un diccionario de clave-valor para las claves que comiencen con el prefijo dado."""
#         return {key: value for key, value in self._data.items() if key.startswith(prefix)}
    
#     def to_dict(self):
#         """Devuelve todo el contenido del Singleton como un diccionario."""
#         return self._data.copy()

#     def from_dict(self, data):
#         """Llena el Singleton con los pares clave-valor de un diccionario dado."""
#         if isinstance(data, dict):
#             self._data.update(data)
#         else:
#             raise ValueError("El argumento debe ser un diccionario.")    

import threading

class SingletonDict:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(SingletonDict, cls).__new__(cls)
                    cls._instance._data = {}
        return cls._instance

    def __setattr__(self, name, value):
        if name == "_data":
            super(SingletonDict, self).__setattr__(name, value)
        else:
            with self._lock:
                self._data[name] = value

    def __getattr__(self, name):
        with self._lock:
            return self._data.get(name, None)

    def __delattr__(self, name):
        with self._lock:
            if name in self._data:
                del self._data[name]
            else:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __getitem__(self, key):
        with self._lock:
            return self._data.get(key, None)

    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value

    def __delitem__(self, key):
        with self._lock:
            if key in self._data:
                del self._data[key]
            else:
                raise KeyError(f"'{key}'")

    def __repr__(self):
        with self._lock:
            return repr(self._data)

    def items(self):
        with self._lock:
            return list(self._data.items())

    def delete_keys_starting_with(self, prefix):
        """Elimina todas las claves que comiencen con el prefijo dado."""
        with self._lock:
            keys_to_delete = [key for key in self._data if key.startswith(prefix)]
            for key in keys_to_delete:
                del self._data[key]

    def clear(self):
        """Elimina todas las claves del diccionario."""
        with self._lock:
            self._data.clear()

    def keys_starting_with(self, prefix):
        """Devuelve todas las claves que comiencen con el prefijo dado."""
        with self._lock:
            return [key for key in self._data if key.startswith(prefix)]

    def values_starting_with(self, prefix):
        """Devuelve todos los valores cuyas claves comiencen con el prefijo dado."""
        with self._lock:
            return [value for key, value in self._data.items() if key.startswith(prefix)]

    def dict_starting_with(self, prefix):
        """Devuelve un diccionario de clave-valor para las claves que comiencen con el prefijo dado."""
        with self._lock:
            return {key: value for key, value in self._data.items() if key.startswith(prefix)}

    def to_dict(self):
        """Devuelve todo el contenido del Singleton como un diccionario."""
        with self._lock:
            return self._data.copy()

    def from_dict(self, data):
        """Llena el Singleton con los pares clave-valor de un diccionario dado."""
        if isinstance(data, dict):
            with self._lock:
                self._data.update(data)
        else:
            raise ValueError("El argumento debe ser un diccionario.")

_singleton = SingletonDict()

def get_singleton():
    return _singleton

import redis
import pickle


""" mapa de funciones a ejecutar cuando se mete en el CACHE un elemento concreto """
MAP_OF_FUNCTIONS_FOR_CACHE_set = [
    # ("impersonated_user_id", populate_session_with_impersonated_user)
]   

ACCEPTED_KEY_PREFIXES_FOR_SESSION_and_CACHE = [
    "IMP_", # for impersonations
    "BND_", # for metadatas (contiene información cacheada del metadata e inspect de SQLAlchemy -> cuando hay tablas o vistas nuevas, hay que borrar este caché)
    "LBL_", # for labels de Translations
    "MGM_", # for información interna (tipo panels)
    "AUD_", # for información de auditoría
    "GPC_", # global y session caches
    "PRU_", # para pruebas
    "DBG_", # para debug (por ejemplo, errores en la clave errores)
    "PGT_", # caché de páginas traducidas
    "TMP_", # claves temporales
    "HKS_", # claves de hooks para controlar recursividad en BEFORE FLUSH de SQLAlchemy
    "SEC_", # restricciones de acciones en base a security priorities - definido en setup.py
    "SCK_", # claves de sockets y de batchs (FLAGS),
    "PCD_", # claves de control de procesos (procesos que tienen que estar vivos -damons- y procesos que tienen que ejectuarse cada x tiempo)
    "CRG_", # claves de carga de información (datos de tablas)
    "ENC_", # claves e información de encriptación
]

MAP_OF_CACHE_KEYS_FOR_CLEANING = { # True -> esta clave puede ser borrada, False -> esta clave no puede ser borrada salvo en SETUP con force_clean
    "IMP_" : True,
    "BND_" : True,
    "LBL_" : False,
    "MGM_" : True,
    "AUD_" : True,
    "GPC_" : False,
    "PRU_" : True,
    "DBG_" : True,
    "PGT_" : False,
    "TMP_" : True,
    "HKS_" : True,
    "SEC_" : False,
    "SCK_" : False, # para que procesos BATCH puedan estar lanzados aunque rearranquemos flask_dashboards, sólo admitimos un borrado selectivo de las claves que estén a CLOSED (todas las claves terminan en CLOSED en algún momento, debido al window de vida que se le pone)
    "PCD_" : False, # control de procesos siempre sigue vivo
    "CRG_" : True, 
    "ENC_" : False
}

import datetime
MAP_OF_PYTHON_TYPES_TO_AVOID_PICKLE = (int,str,dict,list,float,datetime) # para estos tipos de datos no se hace pickle para acelerar

def check_prefixes(key):
    """ Devuelve si una clave no se está pidiendo con el prefijo adecuado """
    import common
    import os
    # si me llega el prefijo de deployment lo quito
    deploy_prefix = common.get_user_env("CM_DEPLOY_MODE")
    deploy_prefix = f"{deploy_prefix}_"
    
    if isinstance(key, bytes):
        key = key.decode('utf-8')
    key = key.replace(deploy_prefix, "")
    
    if key[:4] in ACCEPTED_KEY_PREFIXES_FOR_SESSION_and_CACHE:
        return True 
    return False


def qualify_cache_key(key):
    """ 
    Description:
    ------------

    Añade el prefijo de la aplicación al key
    """
    import common    
    return f"{common.get_user_env('CM_DEPLOY_MODE')}_{key}"

def set_cache(key, dictionary, encrypt_info = False, encrypt = None, singleton = False):

    """ WRAPPER """
    return cache_set(key, dictionary, encrypt_info = encrypt_info, encrypt = encrypt, singleton = singleton)

_s = redis.StrictRedis(host='localhost', port=6379, db=0)

def get_cache_server():
    """ obtiene el servidor de redis """
    # s = None
    # try:
    #     s = redis.StrictRedis(host='localhost', port=6379, db=0)
    # except Exception as e:
    #     tc._print(f"El servidor de redis no parece estar instalado!!! - {e}", tc.R)
    return _s

import time
def acquire_lock(client, lock_name, acquire_timeout=10, lock_timeout=10):
    """
    Acquire a distributed lock using Redis.
    
    :param client: Redis client
    :param lock_name: The name of the lock
    :param acquire_timeout: Time to try acquiring the lock before giving up
    :param lock_timeout: Expiration time for the lock
    :return: The lock identifier if the lock is acquired, else None
    """
    lock_identifier = str(uuid.uuid4())
    end = time.time() + acquire_timeout
    
    while time.time() < end:
        if client.set(lock_name, lock_identifier, nx=True, px=lock_timeout*1000):
            return lock_identifier
        time.sleep(0.01)
    
    return None

def release_lock(client, lock_name, lock_identifier):
    """
    Release a distributed lock using Redis.
    
    :param client: Redis client
    :param lock_name: The name of the lock
    :param lock_identifier: The identifier of the lock
    :return: True if the lock is released, else False
    """
    pipeline = client.pipeline(True)
    
    while True:
        try:
            pipeline.watch(lock_name)
            if client.get(lock_name) == lock_identifier:
                pipeline.multi()
                pipeline.delete(lock_name)
                pipeline.execute()
                return True
            pipeline.unwatch()
            break
        except redis.WatchError:
            pass
        
    return False

def cache_set(key, value, encrypt_info = False, encrypt = None, z_operation = False, singleton = False):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    cache_set
    
    mete en el caché de REDIS la key y el valor (sea lo que sea)
    la key se cualifica con el prefijo de la aplicación
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - key (_type_): _description_
        - dictionary (_type_): _description_
    
    Returns:
    --------
        _type_: _description_
    """
    import common    
    if singleton:
        get_singleton()[key] = value
        return True
        
    # pongo un diccionario en redis con la key y el diccionario
    r = get_cache_server()

    key = qualify_cache_key(key)

    if encrypt == None:
        l_key = qualify_cache_key("CACHE_KEY")
        CACHE_KEY = r.get(l_key)
        encrypt = CACHE_KEY    
        
    METHOD_TO_ENCRYPT = common.encryption_get_method_to_encrypt()
    encrypt_key,_ = common.get_cached_key_for_encryption_method()

    l_key = qualify_cache_key("CACHED_ENCRYPTION_KEY")
    CACHED_ENCRYPTION_KEY = r.get(l_key)

    if encrypt_info:
        if value != None:
            # encrypt_key = encrypt
            # if not encrypt == CACHE_KEY: 
            #     encrypt =common.generateEncryptionKey(password = encrypt, encryption_method = METHOD_TO_ENCRYPT)
            # else:
            #     encrypt = CACHED_ENCRYPTION_KEY
            value = pickle.dumps(value)
            encrypted_value = common.encrypt(value, encrypt_key, is_in_bytes = True)

            value = encrypted_value
            if not z_operation:
                r.set(key, value)
            else:
                tc._print(f"zadd sólo admite diccionarios, no elementos encriptados o en otro formato cualquiera")
    else:
        try:
            if not z_operation:
                value = pickle.dumps(value)
        except Exception as e:
            for k,v in value.items():
                print(f"{k} - {type(v)}")
                try:
                    pickle.dumps(v)
                except Exception as e:
                    tc._print(f"ERROR: {e} en la clave {k} - mirar con detenimiento qué tiene porque hay un elemento, al menos, que no se puede hacer pickle...", tc.R)
            a = 999
        if not z_operation:
            r.set(key, value)
        else:
            r.zadd(key, value)
        # r.set(key, value)
    return True


    for k,v in value.items():
        print(k)

def cache_set_with_LOCK(key, value, encrypt_info=False, encrypt=None, z_operation=False, singleton = False):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    cache_set
    
    Stores the key and value (whatever it is) in the Redis cache.
    The key is qualified with the application's prefix.
    Usa locking para no permitir sobreescrituras en la misma clave de manera simultánea. Falta probarlo bien.
    
    Args:
    -----
        - key (_type_): The cache key
        - value (_type_): The value to be cached
        - encrypt_info (bool): Flag to indicate if encryption is needed
        - encrypt (_type_): Encryption key
        - z_operation (bool): Flag to indicate if ZADD operation is needed
    
    Returns:
    --------
        bool: True if the operation was successful
    """
    import common    
    if singleton:
        get_singleton()[key] = value
        return True    
    
    r = get_cache_server()
    key = qualify_cache_key(key)

    if encrypt == None:
        l_key = qualify_cache_key("CACHE_KEY")
        CACHE_KEY = r.get(l_key)
        encrypt = CACHE_KEY    

    METHOD_TO_ENCRYPT = common.encryption_get_method_to_encrypt()

    l_key = qualify_cache_key("CACHED_ENCRYPTION_KEY")
    CACHED_ENCRYPTION_KEY = r.get(l_key)

    lock_name = f"lock:{key}"
    lock_identifier = acquire_lock(r, lock_name)

    if not lock_identifier:
        return False  # Could not acquire lock

    try:
        if encrypt_info:
            if value is not None:
                if not encrypt == CACHE_KEY: 
                    encrypt = common.generateEncryptionKey(password=encrypt, encryption_method = METHOD_TO_ENCRYPT)
                else:
                    encrypt = CACHED_ENCRYPTION_KEY
                value = pickle.dumps(value)
                encrypted_value = common.encrypt(value, encrypt, is_in_bytes=True, encryption_method = METHOD_TO_ENCRYPT)
                value = encrypted_value
                if not z_operation:
                    r.set(key, value)
                else:
                    print("zadd only supports dictionaries, not encrypted or other formatted elements")
        else:
            try:
                if not z_operation:
                    value = pickle.dumps(value)
            except Exception as e:
                for k, v in value.items():
                    print(f"{k} - {type(v)}")
                    try:
                        pickle.dumps(v)
                    except Exception as e:
                        print(f"ERROR: {e} in the key {k} - check carefully what it has because there is at least one element that cannot be pickled")
            if not z_operation:
                r.set(key, value)
            else:
                r.zadd(key, value)
    finally:
        release_lock(r, lock_name, lock_identifier)
    
    return True

import threading

def test_cache_set_thread(key, value):
    result = cache_set(key, value)
    if result:
        print(f"Thread {threading.current_thread().name} successfully set the key {key}")
    else:
        print(f"Thread {threading.current_thread().name} failed to set the key {key}")

def test_cache_set():
    key = "test_key"
    value = "test_value"

    threads = []
    for i in range(10):
        thread = threading.Thread(target=test_cache_set_thread, args=(key, f"{value}_{i}"))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def clear_cache_prefixed_ns_fast(cache_prefix_to_clean = None, force_clean = False, singleton = False):
    """
    Clear el cache de modo rápido para una aplicación concreta, usando el prefijo de la aplicación deploy
    :param ns: str, namespace i.e your:prefix
    :return: 
    """
    import common    
    # source: https://stackoverflow.com/questions/21975228/redis-python-how-to-delete-all-keys-according-to-a-specific-pattern-in-python

    if singleton:
        get_singleton().delete_keys_starting_with(cache_prefix_to_clean)
        return True

    CHUNK_SIZE = 5000
    prefix = common.get_user_env("CM_DEPLOY_MODE")
    cache = get_cache_server()
    cursor = '0'
    if cache_prefix_to_clean == None:
        for k,v in MAP_OF_CACHE_KEYS_FOR_CLEANING.items(): # borramos sólo las claves que dejamos que se borren
            clean = False
            if v:
                clean = True
            if force_clean:
                clean = True
            if clean:    
                ns_keys = f"{prefix}_{k}*"
                cursor = '0'
                while cursor != 0:
                    cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
                    tc._print(f"keys to delete with prefix {ns_keys} - {len(keys)}", tc.Y)
                    if keys:
                        keys = [k for k in keys]
                        cache.delete(*keys)
                    cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)                        
                    tc._print(f"keys after deletion with prefix {ns_keys} - {len(keys)}", tc.G)
                        
    else:
        cursor = '0'
        ns_keys = f"{prefix}_{cache_prefix_to_clean}*"
        while cursor != 0:
            cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
            tc._print(f"keys to delete with prefix {ns_keys} - {len(keys)}", tc.Y)
            if keys:
                keys = [k for k in keys]
                cache.delete(*keys)
            tc._print(f"keys after deletion with prefix {ns_keys} - {len(keys)}", tc.G)                

    return True

def show_cache_prefixed_ns_fast(cache_prefix_to_clean = None, singleton = False):
    """
    Clear el cache de modo rápido para una aplicación concreta, usando el prefijo de la aplicación deploy
    :param ns: str, namespace i.e your:prefix
    :return: int, cleared keys
    """
    # source: https://stackoverflow.com/questions/21975228/redis-python-how-to-delete-all-keys-according-to-a-specific-pattern-in-python
    import common
    if singleton:
        the_dict = get_singleton().dict_starting_with(cache_prefix_to_clean)
        for k,v in the_dict.items():
            tc._print(f"{k}", tc.B, prompt = False)
            tc._print(v, tc.Y, prompt = False)
        return True

    CHUNK_SIZE = 5000
    prefix = common.get_user_env("CM_DEPLOY_MODE")
    cache = get_cache_server()
    cursor = '0'
    if cache_prefix_to_clean == None:
        for k,v in MAP_OF_CACHE_KEYS_FOR_CLEANING.items(): # borramos sólo las claves que dejamos que se borren
            ns_keys = f"{prefix}_{k}*"
            cursor = '0'
            while cursor != 0:
                cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
                tc._print(f"keys with prefix {ns_keys} - {len(keys)}", tc.Y)
                if keys:
                    keys = [k for k in keys]
                    tc._print(keys, tc.Y)
                for the_key in keys:
                    # quitamos el prefijo de deployment
                    the_key = the_key.decode('utf-8')
                    the_key = the_key.replace(f"{prefix}_", "")
                    value = _CACHE_get(the_key)                    
                    tc._print(f"{the_key}", tc.B, prompt = False)
                    tc._print(value, tc.Y, prompt = False)
                        
    else:
        cursor = '0'
        ns_keys = f"{prefix}_{cache_prefix_to_clean}*"
        while cursor != 0:
            cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
            tc._print(f"keys with prefix {ns_keys} - {len(keys)}", tc.Y)
            if keys:
                keys = [k for k in keys]
                tc._print(keys, tc.Y)
                for the_key in keys:
                    # quitamos el prefijo de deployment
                    the_key = the_key.decode('utf-8')
                    the_key = the_key.replace(f"{prefix}_", "")
                    value = _CACHE_get(the_key)
                    tc._print(f"{the_key}", tc.B, prompt = False)
                    tc._print(value, tc.Y, prompt = False)

    return True

def get_cache_prefixed_ns_fast(cache_prefix_to_clean = None, as_dict = True, singleton = False):
    """ 
    Obtiene todas las claves que tienen un prefijo concreto 
    Devuelve un diccionario clave-valor
    
    Se debe meter únicamente el patrón a buscar, no es necesario incluir, por ejemplo, el último "*"
    
    EXAMPLE:
    --------
    
    >>> dict_of_keys = get_cache_prefixed_ns_fast("SCK_")
    
    """
    import common    
    if singleton:
        the_dict = get_singleton().dict_starting_with(cache_prefix_to_clean)
        return the_dict    
    
    CHUNK_SIZE = 5000
    prefix = common.get_user_env("CM_DEPLOY_MODE")
    cache = get_cache_server()
    cursor = '0'
    dict_keys = {}
    list_keys = []
    ns_keys = f"{prefix}_{cache_prefix_to_clean}*"
    while cursor != 0:
        cursor, keys = cache.scan(cursor=cursor, match=ns_keys, count=CHUNK_SIZE)
        if keys:
            for k in keys:
                # k está en binario, así que lo convertimos a string
                k = k.decode('utf-8')
                # ahora le quitamos el prefijo que le metemos a todas las claves de REDIS
                k = k.replace(f"{prefix}_", "")
                if as_dict:
                    dict_keys[k] = cache_get(k)
                else:
                    list_keys.append({k:v})
    return dict_keys    

def cache_delete(key, z_operation = False, singleton = False):
    """
    (c) Seachad
    
    Description:
    ---------------------- 
    cache_delete
    
    borra una clave del caché
    
    Extended Description:
    ---------------------
    _extended_summary_
    
    
    Args:
    -----
        - key (str): clave a borrar
    
    Returns:
    --------
        _type_: _description_
    """    
    # pongo un diccionario en redis con la key y el diccionario
    if singleton:
        del get_singleton()[key]
        return True
    
    r = get_cache_server()
    key = qualify_cache_key(key)
    r.delete(key)
    return True

def get_cache(key, default_value = None, encrypt_info = False, encrypt = None, z_operation = False, singleton = False):
    """ WRAPPER """
    return cache_get(key, default_value = default_value, encrypt_info = encrypt_info, encrypt = encrypt, z_operation = z_operation, singleton = singleton)

def cache_get(key, default_value = None, encrypt_info = False, encrypt = None, z_operation = False, singleton = False):
    """ obtengo un diccionario de redis con la key 
    la key siempre está calificada con el prefijo de la aplicación deploy"""
    import common    
    if singleton:
        return get_singleton()[key]
    
    r = get_cache_server()
    key = qualify_cache_key(key)
    result = r.get(key)
    
    if encrypt == None:
        l_key = qualify_cache_key("CACHE_KEY")
        CACHE_KEY = r.get(l_key)
        encrypt = CACHE_KEY    
  
    METHOD_TO_ENCRYPT = common.encryption_get_method_to_encrypt()  
    decrypt_key,_ = common.get_cached_key_for_encryption_method()
  
    l_key = qualify_cache_key("CACHED_ENCRYPTION_KEY")
    CACHED_ENCRYPTION_KEY = r.get(l_key)
  
    if result is None:
        return default_value
        # return None
    else:
        if encrypt_info:
            try:
                    
                retorno = common.decrypt(result, decrypt_key, encryption_method = METHOD_TO_ENCRYPT)

                retorno = pickle.loads(retorno)
                # retorno = pickle.loads(retorno)
                result = retorno
            except Exception as e:
                tc._print(f"Error al desencriptar la información de {key}: {e}", tc.R)
                return default_value
                # return None
        else:
            result = pickle.loads(result)
        return result

def cache_flush_all(singleton = False):
    """ Esto permite borrar todos los caches de la aplicación (REDIS) """
    # se borran todas las claves de la aplicación (pero sólo las que comiencen con el prefijo concreto)
    import common    
    if singleton:
        get_singleton().clear()
        return True
    common.execute_Windows_command("redis-cli FLUSHALL")

def cache_delete_key(key, z_operation = False, singleton = False):
    """ Esto permite borrar una key del cache de la aplicación (REDIS) """
    if singleton:
        del get_singleton()[key]
        return True
    
    r = get_cache_server()

    # miro si tiene que borrar en cascada


    r.delete(key)
    pass

def cache_delete_keys(key_pattern, z_operation = False, singleton = False):
    """ Esto permite borrar una serie de keys que cumplan con el patrón (REDIS) 
    recibe un pattern con todas las keys que se quieren borrar
    """
    if singleton:
        get_singleton().delete_keys_starting_with(key_pattern)
        return True
    
    import redis
    r = get_cache_server()    
    keys = r.keys(key_pattern)
    for key in keys:
        # delete the key
        # miro si tiene que borrar en cascada
        
        r.delete(key)    
        pass

def cache_get_keys(key_pattern, encrypt_info = False, encrypt = None, z_operation = False, singleton = False):
    """ Esto permite obtener una serie de keys que cumplan con el patrón (REDIS) 
    recibe un pattern con todas las keys que se quieren obtener
    devuelve un diccionario con cada clave y su valor
    
    Ejemplo:
    --------
    
    """
    import common    
    if singleton:
        return get_singleton().dict_starting_with(key_pattern)
    
    import redis
    dict_to_return = {}
    r = get_cache_server()    
    key_pattern = qualify_cache_key(key_pattern)
    keys = r.keys(key_pattern)
    
    if encrypt == None:
        l_key = qualify_cache_key("CACHE_KEY")
        CACHE_KEY = r.get(l_key)
        encrypt = CACHE_KEY      
    
    METHOD_TO_ENCRYPT = common.encryption_get_method_to_encrypt()    
    
    l_key = qualify_cache_key("CACHED_ENCRYPTION_KEY")
    CACHED_ENCRYPTION_KEY = r.get(l_key)    
    
    for key in keys:
        result = r.get(key)
        if not result is None:
            if encrypt_info:
                try:
                    decrypt_key = encrypt
                    if decrypt_key == None:
                        decrypt_key,_ = common.get_cached_key_for_encryption_method(encryption_method = METHOD_TO_ENCRYPT)
                    else:
                        if not decrypt_key == CACHE_KEY: 
                            decrypt_key =common.generateEncryptionKey(password = decrypt_key, encryption_method = METHOD_TO_ENCRYPT)
                        else:
                            decrypt_key = CACHED_ENCRYPTION_KEY
                    retorno = common.decrypt(result, decrypt_key, encryption_method = METHOD_TO_ENCRYPT)

                    retorno = pickle.loads(retorno)
                    # retorno = pickle.loads(retorno)
                    result = retorno
                except Exception as e:
                    tc._print(f"Error al desencriptar la información: {e}")
                    result = "error_decrypting_information"
                    # return None
            else:
                try:
                    result = pickle.loads(result)
                except Exception as e:
                    tc._print(f"Error al desencriptar la información: {e}", tc.R)
                    result = "error_decrypting_information"
        dict_to_return[key] = result
    return dict_to_return

def _CACHE_set(key, value, encrypt_info = False, encrypt= None , z_operation = False, singleton = False):
    """ permite guardar valores en el caché distribuido """
    if not check_prefixes(key):
        tc._print(f"_CACHE_set: key {key} no tiene prefijo adecuado", tc.R)
    cache_set(key, value, encrypt_info = encrypt_info, encrypt = encrypt, z_operation=z_operation, singleton = singleton)
    """ Puede que, dependiendo de una clave concreta, queramos ejecutar una función """
    for mapa in MAP_OF_FUNCTIONS_FOR_CACHE_set:
        if key == mapa[0]:
            mapa[1](value, CACHE)    
    pass

def _CACHE_delete(key, z_operation = False, singleton = False):
    """ permite borrar valores en el caché distribuido """
    cache_delete(key, z_operation = z_operation, singleton = singleton)

def _CACHE_get(key, default_value = None, encrypt_info = False, encrypt = None, z_operation = False, singleton = False):
    """ permite recuperar valores del caché distribuido """
    """ ejemplo de uso en cualquier parte del código
    from app.cache_REDIS import _CACHE_get
    valor = _CACHE_get("clave", default_value = "valor por defecto")
    
    """
    
    if not check_prefixes(key):
        tc._print(f"_CACHE_get: key {key} no tiene prefijo adecuado", tc.R)    

    return cache_get(key, default_value = default_value, encrypt_info=encrypt_info, encrypt=encrypt, z_operation = z_operation, singleton = singleton)

def cache_monkey_patched():
    # probamos que se hahecho correctamente el monkey patch para que las funciones de common estén apuntando a cache_REDIS, siempre y cuando se haya hecho el monkey patch
    tc._print(f"esta función se ejecuta en REDIS!!")
    # si el monkey patch se ha hecho correctamente, esta función debería estar apuntando a cache_REDIS


# ! FIN CACHE CODE
