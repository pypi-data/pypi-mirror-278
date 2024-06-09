from __future__ import annotations

from typing import Any
from typing import ClassVar
from typing import Type

from drakaina import rpc_registry
from drakaina.exceptions import InternalServerError
from drakaina.exceptions import RPCError
from drakaina.registries import RPC_SCHEMA
from drakaina.registries import RPCRegistry
from drakaina.serializers import BaseSerializer
from drakaina.serializers import JsonSerializer
from drakaina.types import OpenAPI
from drakaina.types import OpenRPC
from drakaina.utils import unwrap_func

__all__ = ("BaseRPCProtocol",)


class BaseRPCProtocol:
    """Base class for representing the remote procedure call (RPC) protocol.

    To implement your own RPC protocol, you must implement the `handle` method,
    which must accept two parameters - the incoming message of your protocol
    `rpc_request` and an environment object 'request' that contains information
    about the connection, the transport layer and other information not
    directly related to the rpc protocol.

    You must also specify a base error class and a default error class.
    If you implement your own error class hierarchy, you will need to map your
    implementation to drakaina error classes.

    :param registry:
        Registry of remote procedures.
        Default: `drakaina.registries.rpc_registry` (generic module instance)
    :param serializer:
        Serializer object.
    :param schema_serializer:
        The serializer object to serialize the schema.
        Default: `JsonSerializer` (stdlib.json)

    """

    __slots__ = (
        "registry",
        "serializer",
        "schema_serializer",
        "__schema",
    )

    base_error_class: ClassVar = RPCError
    """Base class for RPC protocol implementation."""

    default_error_class: ClassVar = InternalServerError
    """The default error class for representing internal exceptions."""

    # When you implement this class interface by implementing a child class,
    # you must map the user protocol exception classes to the generic
    # exception classes `drakaina.exceptions` in this class variable.
    _errors_map: ClassVar = {Exception: RPCError}

    def __init__(
        self,
        registry: RPCRegistry | None = None,
        serializer: BaseSerializer | None = None,
        schema_serializer: BaseSerializer | None = None,
    ):
        self.registry = registry if registry is not None else rpc_registry
        self.serializer = serializer
        self.schema_serializer = schema_serializer or JsonSerializer()

        self.__schema = None

    def handle_raw_request(
        self,
        raw_data: bytes,
        request: Any | None = None,
    ) -> bytes:
        """Accepts raw data, deserializes, processes the RPC request,
        and returns the serialized result.

        :param raw_data:
            Raw request data.
        :type raw_data:
        :param request:
            Request object or context data. Can be provided to
            a remote procedure.
        :type request: Any
        :return:
            Serialized RPC response data.

        """
        try:
            parsed_data = self.serializer.deserialize(raw_data)
        except Exception as exc:
            return self.get_raw_error(exc)

        response_data = self.handle(parsed_data, request=request)
        if response_data is None:
            return b""

        try:
            return self.serializer.serialize(response_data)
        except Exception as exc:
            return self.get_raw_error(exc)

    def get_raw_error(
        self,
        error: RPCError | Type[RPCError] | Exception | Type[Exception],
    ) -> bytes:
        """Returns the serialized error object.

        :param error:
            The instance or class of the error.
        :type error: RPCError | Type[RPCError] | Exception | Type[Exception]
        :return:
            Raw error data.

        """
        rpc_error = self.handle_error(error)
        return self.serializer.serialize(rpc_error.as_dict())

    def handle(self, rpc_request: Any, request: Any | None = None) -> Any:
        """Handles a procedure call.

        :param rpc_request:
            RPC request in protocol format.
        :param request:
            Optional parameter that can be passed as an
            argument to the procedure. By default, None will be passed.
        :return:
            Returns the result in protocol format.

        """
        raise NotImplementedError(
            "You must implement the `handle` method in the child class",
        )

    def handle_error(
        self,
        error: RPCError | Type[RPCError] | Exception | Type[Exception],
    ) -> RPCError:
        """Returns an exception object corresponding to the RPC protocol.

        :param error:
            The instance or class of the error.
        :type error: RPCError | Type[RPCError] | Exception | Type[Exception]
        :returns: Protocol specific error object.
        :rtype: RPCError

        """

        if isinstance(error, type) and issubclass(error, Exception):
            error = error()

        if isinstance(error, self.base_error_class):
            return error
        else:
            # Try to get mapped error class
            rpc_error_class = self._errors_map.get(type(error))
            # If nothing is retrieved, try to get the mapped error class
            #  from the base error classes
            if rpc_error_class is None and isinstance(error, RPCError):
                for base_error_class in type(error).__mro__:
                    if base_error_class in self._errors_map:
                        rpc_error_class = self._errors_map[base_error_class]
                        break
            if rpc_error_class is None:
                rpc_error_class = self.default_error_class

            try:
                error_message = error.message or ""
            except AttributeError:
                error_message = ""

            return rpc_error_class(error_message)

    @property
    def content_type(self) -> str:
        return self.serializer.content_type

    @property
    def schema_content_type(self) -> str:
        return self.schema_serializer.content_type

    def schema(self) -> dict:
        """Simple schema of service."""
        if self.__schema is None:
            self.__schema = {}
            for method_name, procedure_ in self.registry.items():
                procedure = unwrap_func(procedure_)
                if hasattr(procedure, RPC_SCHEMA):
                    self.__schema[method_name] = getattr(procedure, RPC_SCHEMA)
        return self.__schema

    def get_raw_schema(self) -> bytes:
        return self.schema_serializer.serialize(self.schema())

    def openrpc_schema(self) -> OpenRPC:
        """Implementation of OpenRPC specification.

        https://spec.open-rpc.org/

        """
        raise NotImplementedError()

    def get_raw_openrpc_schema(self) -> bytes:
        return self.schema_serializer.serialize(self.openrpc_schema())

    def openapi_schema(self) -> OpenAPI:
        """Implementation of OpenAPI specification.

        https://spec.openapis.org/oas/latest.html

        """
        raise NotImplementedError()

    def get_raw_openapi_schema(self) -> bytes:
        return self.schema_serializer.serialize(self.openapi_schema())
