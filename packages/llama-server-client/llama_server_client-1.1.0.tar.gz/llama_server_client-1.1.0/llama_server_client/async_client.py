from typing import Optional, Union, AsyncIterable, Type, List
from zmq import asyncio as zmq_asyncio
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


class AsyncLlamaClient(BaseLlamaClient):
    """
    AsyncLlamaClient is an asynchronous client class for communication with a server using ZeroMQ with asyncio.
    It handles socket creation, sending requests, and receiving responses with an option for timeouts.
    """

    def _create_context(self) -> zmq_asyncio.Context:
        """Create a new ZeroMQ async context."""
        return zmq_asyncio.Context()

    def _create_socket(self) -> zmq_asyncio.Socket:
        """Create a new ZeroMQ DEALER socket."""
        return self.context.socket(zmq.DEALER)

    async def _send_request(
        self, zmq_message_type: ZmqMessageType, request: Optional[T] = None
    ) -> AsyncIterable[Optional[Union[T, Base]]]:
        """
        Asynchronously sends a request to the server, and waits for a response, handling timeouts.

        :param zmq_message_type: The type of the ZeroMQ message to be sent.
        :param request: The request object to be sent, if applicable.
        :return: The unpacked response if successful, or raises a timeout exception.
        """
        message_header: ZmqMessageHeader = create_message_header(zmq_message_type)

        self.socket.setsockopt(zmq.IDENTITY, message_header.zmq_message_id.bytes)

        message_parts: List = [message_header.msgpack_pack()]
        if request:
            message_parts.append(request.msgpack_pack())

        await self.socket.send_multipart(message_parts)

        try:
            while True:
                resp_messages: List = await self.socket.recv_multipart()
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

    async def _handle_chat_completion_response(
        self, request: ChatCompletionRequest
    ) -> Optional[ChatCompletion]:
        """
        Handles ChatCompletion responses.
        """
        async for response in self._send_request(ZmqMessageType.CHAT_COMPLETION, request):
            return response

    async def _handle_chat_completion_chunk_response(
        self, request: ChatCompletionRequest
    ) -> AsyncIterable[Optional[ChatCompletionChunk]]:
        """
        Handles ChatCompletionChunk responses.
        """
        async for response in self._send_request(ZmqMessageType.CHAT_COMPLETION, request):
            yield response

    async def send_chat_completion_request(
        self, request: ChatCompletionRequest
    ) -> Union[AsyncIterable[Optional[ChatCompletionChunk]], Optional[ChatCompletion]]:
        """
        Asynchronously sends a ChatCompletionRequest to the server and waits for a ChatCompletion or ChatCompletionChunk response.

        :param request: The ChatCompletionRequest to send.
        :return: An AsyncIterable yielding ChatCompletionChunk responses if request.stream is True,
                 or a single ChatCompletion response if request.stream is False.
        """
        if request.stream:
            return self._handle_chat_completion_chunk_response(request)
        else:
            return await self._handle_chat_completion_response(request)

    async def send_session_state_request(
        self, request: SessionStateRequest
    ) -> Optional[SessionState]:
        """
        Asynchronously sends a SessionStateRequest to the server and waits for a SessionState response.

        :param request: The SessionStateRequest to send.
        :return: A SessionState response or None if timed out.
        """
        async for response in self._send_request(ZmqMessageType.SESSION_STATE, request):
            return response

    async def send_health_check_request(self) -> Optional[HealthCheck]:
        """
        Asynchronously sends a HealthCheck request to the server and waits for a HealthCheck response.

        :return: A HealthCheck response or None if timed out.
        """
        async for response in self._send_request(ZmqMessageType.HEALTH_CHECK):
            return response
