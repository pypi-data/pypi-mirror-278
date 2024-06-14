import json


class JsonFileResolver:
    def __init__(self, path):
        self.path = path
        try:
            with open(self.path, 'r') as f:
                self.json_object = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Configuration file {self.path} not found. Please check your configuration file.")

    def get_license_key(self):
        try:
            return self.json_object["licenseKey"]
        except KeyError:
            raise ValueError("License key not found in configuration file. Please check your configuration file.")

    def get_runtimes(self):
        return self.json_object["runtimes"]

    def get_runtime(self, runtime_name, config_name):
        runtimes = self.get_runtimes()
        if runtime_name in runtimes:
            runtime = runtimes[runtime_name]
            if isinstance(runtime, list):
                for item in runtime:
                    if item.get("name") == config_name:
                        return item
            elif runtime.get("name") == config_name:
                return runtime
        raise ValueError(
            f"Runtime config {config_name} not found in configuration file for runtime {runtime_name}. Please check "
            f"your configuration file.")

    def get_channel(self, runtime_name, config_name):
        runtime = self.get_runtime(runtime_name, config_name)
        if "channel" in runtime:
            return runtime["channel"]
        raise ValueError(
            f"Channel key not found in configuration file for config {config_name}. Please check your configuration "
            f"file.")

    def get_channel_type(self, runtime_name, config_name):
        channel = self.get_channel(runtime_name, config_name)
        if "type" in channel:
            return channel["type"]
        raise ValueError(
            f"Channel type not found in configuration file for config {config_name}. Please check your configuration "
            f"file.")

    def get_channel_host(self, runtime_name, config_name):
        channel = self.get_channel(runtime_name, config_name)
        if "host" in channel:
            return channel["host"]
        raise ValueError(
            f"Channel host not found in configuration file for config {config_name}. Please check your configuration "
            f"file.")

    def get_channel_port(self, runtime_name, config_name):
        channel = self.get_channel(runtime_name, config_name)
        if "port" in channel:
            return channel["port"]
        raise ValueError(
            f"Channel port not found in configuration file for config {config_name}. Please check your configuration "
            f"file.")
