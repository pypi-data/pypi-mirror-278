from javonet.sdk.internal.abstract.AbstractConfigRuntimeFactory import AbstractConfigRuntimeFactory
from javonet.sdk.tools.JsonFileResolver import JsonFileResolver
from javonet.utils.ConnectionType import ConnectionType
from javonet.utils.RuntimeName import RuntimeName
from javonet.sdk.RuntimeContext import RuntimeContext
from javonet.core.transmitter.Transmitter import Transmitter
from javonet.utils.RuntimeNameHandler import RuntimeNameHandler
from javonet.utils.TcpConnectionData import TcpConnectionData


class ConfigRuntimeFactory(AbstractConfigRuntimeFactory):
    """
    The ConfigRuntimeFactory class implements the AbstractConfigRuntimeFactory interface and provides methods for creating runtime contexts.
    Each method corresponds to a specific runtime (CLR, JVM, .NET Core, Perl, Ruby, Node.js, Python) and returns a RuntimeContext instance for that runtime.
    """

    def __init__(self, path):
        self.path = path

    def clr(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with CLR runtime.

        Args:
			config_name (str): The name of the configuration to use.

        Returns:
            RuntimeContext instance for the CLR runtime

        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.clr, config_name)

    def jvm(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with JVM runtime.

        Args:
			config_name (str): The name of the configuration to use.

        Returns:
            RuntimeContext instance for the JVM runtime

        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.jvm, config_name)

    def netcore(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with .NET runtime.

        Args:
			config_name (str): The name of the configuration to use.

        Returns:
            RuntimeContext instance for the .NET runtime

        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.netcore, config_name)

    def perl(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with Perl runtime.

        Args:
			config_name (str): The name of the configuration to use.

        Returns:
            RuntimeContext instance for the Perl runtime

        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.perl, config_name)

    def ruby(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with Ruby runtime.

        Args:
			config_name (str): The name of the configuration to use.

        Returns:
            RuntimeContext instance for the Ruby runtime

        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.ruby, config_name)

    def nodejs(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with Node.js runtime.

        Args:
			config_name (str): The name of the configuration to use.

        Returns:
            RuntimeContext instance for the Node.js runtime

        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.nodejs, config_name)

    def python(self, config_name: str = "default"):
        """
        Creates RuntimeContext instance to interact with Python runtime.

        Args:
			config_name (str): The name of the configuration to use.
        
        Returns:
            a RuntimeContext instance for the Python runtime
        
        Refer to this `article on Javonet Guides <https://www.javonet.com/guides/v2/python/foundations/runtime-context>`_ for more information.
        """
        return ConfigRuntimeFactory._get_runtime_context(self, RuntimeName.python, config_name)

    def _get_runtime_context(self, runtime: RuntimeName, config_name: str = "default"):
        """
        Creates a RuntimeContext instance to interact with the specified runtime.

        Args:
            runtime (RuntimeName): The runtime name.
            config_name (str): The configuration name.

        Returns:
            RuntimeContext: A RuntimeContext instance for the specified runtime.
        """

        jfr = JsonFileResolver(self.path)

        try:
            license_key = jfr.get_license_key()
            Transmitter.activate_with_credentials(license_key)
        except Exception:
            # licenseKey not found - do nothing
            pass

        conn_type = jfr.get_channel_type(RuntimeNameHandler.get_name(runtime), config_name)
        if conn_type == "tcp":
            conn_data = TcpConnectionData(jfr.get_channel_host(RuntimeNameHandler.get_name(runtime), config_name),
                                          jfr.get_channel_port(RuntimeNameHandler.get_name(runtime), config_name))
            return RuntimeContext.get_instance(runtime, ConnectionType.Tcp, conn_data)
        elif conn_type == "inMemory":
            return RuntimeContext.get_instance(runtime, ConnectionType.InMemory)
        else:
            raise Exception("Invalid connection type")
