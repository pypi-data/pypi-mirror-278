from typing import Optional, List, Union, Type, Generator
import zmq

from llama_server_client.base_client import BaseLlamaClient
from llama_server_client.schema import HealthCheck
from llama_server_client.schema.base import Base, T
from llama_server_client.schema.completion import ChatCompletionRequest, ChatCompletion, ChatCompletionChunk
from llama_server_client.schema.zmq_message_header import (
    ZmqMessageType, create_message_header, ZmqMessageHeader, ZmqMessageStatus
)
from llama_server_client.schema.session_state import SessionStateRequest, SessionState
from llama_server_client.error import LlamaClientError


class LlamaClient(BaseLlamaClient):
    """
    LlamaClient is a client class to communicate with a server using ZeroMQ and MessagePack, with a timeout feature.
    """

    def _create_context(self) -> zmq.Context:
        """Create a new ZeroMQ context."""
        return zmq.Context()

    def _create_socket(self) -> zmq.Socket:
        """Create a new ZeroMQ DEALER socket."""
        return self.context.socket(zmq.DEALER)

    def _send_request(
        self, zmq_message_type: ZmqMessageType, request: Optional[T] = None
    ) -> Generator[Optional[Union[T, Base]], None, None]:
        """
        Sends a request to the server, according to the specified message type, and waits for a response, handling timeouts.

        :param zmq_message_type: The type of the ZeroMQ message to be sent.
        :param request: The request object to be sent, if applicable.
        :return: The unpacked response if successful, or raises a timeout exception.
        """
        message_header: ZmqMessageHeader = create_message_header(zmq_message_type)

        self.socket.setsockopt(zmq.IDENTITY, message_header.zmq_message_id.bytes)

        message_parts: List = [message_header.msgpack_pack()]
        if request:
            message_parts.append(request.msgpack_pack())

        self.socket.send_multipart(message_parts)

        try:
            while True:
                resp_messages = self.socket.recv_multipart()
                if len(resp_messages) > 2:
                    raise ValueError("Invalid response length")

                response_header: ZmqMessageHeader = ZmqMessageHeader.msgpack_unpack(resp_messages[0])
                if response_header.status == ZmqMessageStatus.ERROR:
                    raise LlamaClientError(response_header)

                response_body_class: Type[Base] = zmq_message_type.get_associated_class
                if isinstance(request, ChatCompletionRequest) and request.stream:
                    yield ChatCompletionChunk.msgpack_unpack(resp_messages[1])
                else:
                    yield response_body_class.msgpack_unpack(resp_messages[1])

                if not response_header.has_more_message:
                    break

        except zmq.Again:
            self._initialize_context_and_socket()
            raise TimeoutError(f"Request timed out after {self.timeout} milliseconds")

    def send_chat_completion_request(
        self, request: ChatCompletionRequest
    ) -> Union[List[ChatCompletionChunk], Optional[ChatCompletion]]:
        """
        Sends a ChatCompletionRequest to the server and waits for a ChatCompletion or ChatCompletionChunk response.

        :param request: The ChatCompletionRequest to send.
        :return: A list of ChatCompletionChunk responses if request.stream is True,
                 or a single ChatCompletion response if request.stream is False.
        """
        if request.stream:
            responses = []
            for response in self._send_request(ZmqMessageType.CHAT_COMPLETION, request):
                responses.append(response)
            return responses
        else:
            return next(self._send_request(ZmqMessageType.CHAT_COMPLETION, request))

    def send_session_state_request(self, request: SessionStateRequest) -> Optional[SessionState]:
        """
        Sends a SessionStateRequest to the server and waits for a SessionState response.

        :param request: The SessionStateRequest to send.
        :return: A SessionState response or None if timed out.
        """
        return next(self._send_request(ZmqMessageType.SESSION_STATE, request))

    def send_health_check_request(self) -> Optional[HealthCheck]:
        """
        Sends a HealthCheck request to the server and waits for a HealthCheck response.

        :return: A HealthCheck response or None if timed out.
        """
        return next(self._send_request(ZmqMessageType.HEALTH_CHECK))
