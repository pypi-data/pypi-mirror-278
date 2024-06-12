"""Corvic system op graph executeor protocol."""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence
from typing import Protocol

import pyarrow as pa

from corvic import op_graph


@dataclasses.dataclass
class TableComputeContext:
    """Parameters needed to compute one table."""

    table_op_graph: op_graph.Op
    output_url_prefix: str


@dataclasses.dataclass
class ExecutionContext:
    """Description of the computation to be completed."""

    tables_to_compute: list[TableComputeContext]
    """A list of tables that the caller wants in addition to table_to_compute.

    This has advantages over multimple invocations of OpGraphExecutor when those
    additional tables would be computed to compute tables_to_compute anyway; i.e.,
    they are nodes in the tables_to_compute op graph.
    """


class TableComputeResult(Protocol):
    """Opaque container for the results of computing an OpGraph."""

    def to_batch_reader(self) -> pa.RecordBatchReader:
        """Render the results as a stream of RecordBatches."""
        ...

    def to_urls(self) -> list[str]:
        """Render the results as a list of urls pointing to parquet files."""
        ...

    @property
    def context(self) -> TableComputeContext:
        """The context this table was computed for."""
        ...


class ExecutionResult(Protocol):
    """Opaque container for the results of an execution."""

    @property
    def tables(self) -> Sequence[TableComputeResult]:
        """Results for the executed op graphs.

        Ordered according to the how their TableComputContexts were ordered in the
        ExecutionContext.
        """
        ...

    @property
    def context(self) -> ExecutionContext:
        """The context this table was computed for."""
        ...


class OpGraphExecutor(Protocol):
    """Execute table op graphs."""

    def execute(self, context: ExecutionContext) -> ExecutionResult:
        """Execute all the OpGraphs described by the context."""
        ...
