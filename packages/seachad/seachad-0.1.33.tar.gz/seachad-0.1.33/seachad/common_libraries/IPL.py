# ? wrapper para IPL
def get_access(dict_to_load = None, lazyload = False, miniconfig_file = None, dot_env_path = None):
    return {}

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