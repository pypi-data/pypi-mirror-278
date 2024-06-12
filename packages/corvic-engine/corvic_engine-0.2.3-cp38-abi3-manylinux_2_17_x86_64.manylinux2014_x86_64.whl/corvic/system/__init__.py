"""Protocols defining the way corvic interacts with the platform."""

from typing import Final

from corvic.system.client import Client
from corvic.system.in_memory_executor import InMemoryExecutionResult, InMemoryExecutor
from corvic.system.op_graph_executor import (
    ExecutionContext,
    ExecutionResult,
    OpGraphExecutor,
    TableComputeContext,
    TableComputeResult,
)
from corvic.system.staging import StagingDB, VectorSimilarityMetric
from corvic.system.storage import (
    Blob,
    BlobClient,
    Bucket,
    DataKindManager,
    DataMisplacedError,
    StorageManager,
)

DEFAULT_VECTOR_COLUMN_NAMES_TO_SIZES: Final = {
    "2_dim_vector": 2,
    "3_dim_vector": 3,
    "8_dim_vector": 8,
    "16_dim_vector": 16,
    "32_dim_vector": 32,
    "64_dim_vector": 64,
    "128_dim_vector": 128,
}

__all__ = [
    "Blob",
    "BlobClient",
    "Bucket",
    "Client",
    "DEFAULT_VECTOR_COLUMN_NAMES_TO_SIZES",
    "DataKindManager",
    "DataMisplacedError",
    "ExecutionContext",
    "ExecutionResult",
    "InMemoryExecutionResult",
    "InMemoryExecutor",
    "OpGraphExecutor",
    "StagingDB",
    "StorageManager",
    "TableComputeContext",
    "TableComputeResult",
    "VectorSimilarityMetric",
]
