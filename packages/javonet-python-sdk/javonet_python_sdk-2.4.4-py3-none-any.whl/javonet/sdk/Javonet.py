"""
The Javonet module is a singleton module that serves as the entry point for interacting with Javonet.
It provides functions to activate and initialize the Javonet SDK.
It supports both in-memory and TCP connections.
Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/javonet-static-class>`_ for more information.
"""
from javonet.core.transmitter.Transmitter import Transmitter
from javonet.utils.ConnectionType import ConnectionType
from javonet.sdk.RuntimeFactory import RuntimeFactory
from javonet.sdk.ConfigRuntimeFactory import ConfigRuntimeFactory
from javonet.utils.TcpConnectionData import TcpConnectionData

Transmitter.activate_with_license_file()


def in_memory():
    """
    Initializes Javonet using an in-memory channel on the same machine.
    
    Returns:
        RuntimeFactory: An instance configured for an in-memory connection.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/in-memory-channel>`_ for more information.
    """
    return RuntimeFactory(ConnectionType.InMemory, None)


def tcp(tcp_connection_data: TcpConnectionData):
    """
    Initializes Javonet with a TCP connection to a remote machine.
    
    Args:
        tcp_connection_data (str): The address of the remote machine.
        
    Returns:
        RuntimeFactory: An instance configured for a TCP connection.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/tcp-channel>`_ for more information.
    """
    return RuntimeFactory(ConnectionType.Tcp, tcp_connection_data)


def with_config(path):
    """
    Initializes Javonet with a configuration taken from external source.
    Currently supported: Configuration file in JSON format
    
    Args:
        path (str): Path to a configuration file.
        
    Returns:
        ConfigRuntimeFactory: An instance configured with configuration data.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/configure-channel>`_ for more information.
    """
    Transmitter.set_config_source(path)
    return ConfigRuntimeFactory(path)


def activate(license_key, proxy_host=None, proxy_user_name=None, proxy_user_password=None):
    """
    Activates Javonet with the provided license key and optional proxy settings.
    
    Args:
        license_key (str): The license key to activate Javonet.
        proxy_host (str, optional): The host for the proxy server. Defaults to None.
        proxy_user_name (str, optional): The username for the proxy server. Defaults to None.
        proxy_user_password (str, optional): The password for the proxy server. Defaults to None.
        
    Returns:
        int: The activation status code.
    Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/getting-started/activating-javonet>`_ for more information.
    """
    if proxy_host is None:
        return Transmitter.activate_with_credentials(license_key)
    else:
        if proxy_user_name is None:
            proxy_user_name = ""
        if proxy_user_password is None:
            proxy_user_password = ""

        return Transmitter.activate_with_credentials_and_proxy(license_key,
                                                               proxy_user_name, proxy_user_password)
