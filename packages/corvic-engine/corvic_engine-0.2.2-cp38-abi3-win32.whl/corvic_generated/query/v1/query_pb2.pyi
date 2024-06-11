from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RagMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RAG_METHOD_UNSPECIFIED: _ClassVar[RagMethod]
    RAG_METHOD_NAIVE: _ClassVar[RagMethod]
    RAG_METHOD_CORVIC: _ClassVar[RagMethod]
RAG_METHOD_UNSPECIFIED: RagMethod
RAG_METHOD_NAIVE: RagMethod
RAG_METHOD_CORVIC: RagMethod

class TokenUsage(_message.Message):
    __slots__ = ("token_input", "token_output")
    TOKEN_INPUT_FIELD_NUMBER: _ClassVar[int]
    TOKEN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    token_input: float
    token_output: float
    def __init__(self, token_input: _Optional[float] = ..., token_output: _Optional[float] = ...) -> None: ...

class QueryRequest(_message.Message):
    __slots__ = ("query", "rag_method", "model_system_instruction")
    QUERY_FIELD_NUMBER: _ClassVar[int]
    RAG_METHOD_FIELD_NUMBER: _ClassVar[int]
    MODEL_SYSTEM_INSTRUCTION_FIELD_NUMBER: _ClassVar[int]
    query: str
    rag_method: RagMethod
    model_system_instruction: str
    def __init__(self, query: _Optional[str] = ..., rag_method: _Optional[_Union[RagMethod, str]] = ..., model_system_instruction: _Optional[str] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ("token_usage", "response", "sources")
    TOKEN_USAGE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    token_usage: TokenUsage
    response: str
    sources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, token_usage: _Optional[_Union[TokenUsage, _Mapping]] = ..., response: _Optional[str] = ..., sources: _Optional[_Iterable[str]] = ...) -> None: ...
