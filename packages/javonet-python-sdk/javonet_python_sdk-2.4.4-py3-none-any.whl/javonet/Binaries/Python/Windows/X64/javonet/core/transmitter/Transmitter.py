from javonet.core.transmitter.TransmitterWrapper import TransmitterWrapper


class Transmitter:

    @staticmethod
    def send_command(message):
        return TransmitterWrapper.send_command(message)

    @staticmethod
    def __activate(license_key="", proxy_host="", proxy_user_name="", proxy_user_password=""):
        return TransmitterWrapper.activate(license_key, proxy_host, proxy_user_name, proxy_user_password)

    @staticmethod
    def activate_with_license_file():
        return Transmitter.__activate()

    @staticmethod
    def activate_with_credentials(license_key):
        return Transmitter.__activate(license_key)

    @staticmethod
    def activate_with_credentials_and_proxy(license_key, proxy_host, proxy_user_name, proxy_user_password):
        return Transmitter.__activate(license_key, proxy_host, proxy_user_name, proxy_user_password)

    @staticmethod
    def set_config_source(source_path):
        return TransmitterWrapper.set_config_source(source_path)