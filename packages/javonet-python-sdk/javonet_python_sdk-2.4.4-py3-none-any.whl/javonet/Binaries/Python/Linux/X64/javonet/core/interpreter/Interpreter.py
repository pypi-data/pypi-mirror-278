from javonet.core.handler.Handler import Handler
from javonet.core.protocol.CommandDeserializer import CommandDeserializer
from javonet.core.protocol.CommandSerializer import CommandSerializer
from javonet.utils.ConnectionType import ConnectionType
from javonet.utils.RuntimeName import RuntimeName
from javonet.utils.TcpConnectionData import TcpConnectionData


class Interpreter:
    response = None

    def execute(self, command, connection_type, tcp_connection_data: TcpConnectionData):
        command_serializer = CommandSerializer()
        serialized_command = command_serializer.serialize(command, connection_type, tcp_connection_data)
        if (command.runtime_name == RuntimeName.python) & (connection_type == ConnectionType.InMemory):
            from javonet.core.receiver.Receiver import Receiver
            response = Receiver().SendCommand(serialized_command, len(serialized_command))
        else:
            from javonet.core.transmitter.Transmitter import Transmitter
            response = Transmitter.send_command(serialized_command)
        command_deserializer = CommandDeserializer(response, len(response))

        return command_deserializer.deserialize()

    def process(self, byte_array, byte_array_len):
        command_deserializer = CommandDeserializer(byte_array, byte_array_len)
        received_command = command_deserializer.deserialize()
        python_handler = Handler()
        command_serializer = CommandSerializer()
        response_command = python_handler.handle_command(received_command)
        encoded_response = command_serializer.serialize(response_command, 0, "0.0.0.0:0")
        return encoded_response
