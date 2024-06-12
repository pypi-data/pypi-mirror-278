def is_running_in_production(user, password, dbname, host, _logger=False, print_results=True):
    """
    Check if the Odoo environment is running in a production or testing environment.

    The function checks if the environment is production based on four conditions.

    Parameters:
    user (str): Username for authentication in the Odoo database.
    password (str): Password for the user for authentication.
    dbname (str): Name of the Odoo database.
    host (str): URL of the server hosting Odoo.

    Returns:
    bool: True if the environment is production, False if is not production.
    """

    import uuid
    import subprocess
    import xmlrpc
    import os.path

    try:
        # Connection to get parameters
        url = f'{host}/xmlrpc/'
        common_proxy = xmlrpc.client.ServerProxy(f"{url}2/common")
        uid = common_proxy.authenticate(dbname, user, password, {})
        object_proxy = xmlrpc.client.ServerProxy(f"{url}2/object")

        local_ip_parameter = object_proxy.execute_kw(dbname, uid, password, 'ir.config_parameter', 'search_read', [[('key', '=', 'local_ip')]], {"fields": ["value"], "limit": 1})
        local_mac_parameter = object_proxy.execute_kw(dbname, uid, password, 'ir.config_parameter', 'search_read', [[('key', '=', 'local_mac')]], {"fields": ["value"], "limit": 1})

        local_ip = local_ip_parameter[0].get('value', False)
        local_mac = local_mac_parameter[0].get('value', False)

        # Check if the URL is localhost
        # If the URL contains localhost or 127.0.0.1 is because is an local ambient, that means that isn't production
        is_localhost = ("localhost" in host or "127.0.0.1" in host)

        # Verify if the MAC from the parameter is the same as the MAC where Odoo is running
        is_server_mac = (local_mac == str(uuid.getnode())) if local_mac else False

        # Check if the IP from the parameter is the same as the IP running Odoo.
        is_the_ip = (local_ip in subprocess.getoutput("hostname -I").split()) if local_ip else False

        # Check if the file etc/produccion exists
        exist_etc_production = os.path.exists('/etc/produccion') and os.path.isfile('/etc/produccion')


        if print_results:
            print(f"Key 01 result: {is_localhost} \t Is localhost: {host}")
            print(f"Key 02 result: {is_server_mac} \t Parameter MAC = {local_mac}")
            print(f"Key 02 result: {is_the_ip} \t Parameter IP = {local_ip}")
            print(f"Key 03 result: {exist_etc_production} \t The file in /etc/: {'/etc/produccion'}")

        if _logger:
            _logger.info("\n\tLlave 01: %s \t Es local: %s", is_localhost, host)
            _logger.info("\n\tLlave 02: %s \t La MAC local: %s", is_server_mac, local_mac)
            _logger.info("\n\tLlave 02: %s \t La IP: %s", is_the_ip, local_ip)
            _logger.info("\n\tLlave 03: %s \t El archivo en /etc: %s", exist_etc_production, '/etc/produccion')

        return not is_localhost and (is_server_mac or is_the_ip) and exist_etc_production
    except Exception as e:
        if _logger:
            _logger.error(e)
        return False
