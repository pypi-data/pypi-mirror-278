"""Staging-agnostic in-memory executor."""

from __future__ import annotations

import dataclasses
import functools
from typing import TYPE_CHECKING, Final, cast

import polars as pl
import pyarrow as pa
import pyarrow.parquet as pq
import structlog

from corvic import embed, op_graph, sql
from corvic.lazy_import import lazy_import
from corvic.result import BadArgumentError, InternalError
from corvic.system.op_graph_executor import (
    ExecutionContext,
    ExecutionResult,
    TableComputeContext,
    TableComputeResult,
)
from corvic.system.staging import StagingDB
from corvic.system.storage import StorageManager
from corvic_generated.orm.v1 import table_pb2

_logger = structlog.get_logger()

if TYPE_CHECKING:
    from corvic import embedding_metric
else:
    embedding_metric = lazy_import("corvic.embedding_metric")


_MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY: Final = 3


def _as_df(
    batch_or_batch_container: pa.RecordBatchReader | pa.RecordBatch | _SchemaAndBatches,
):
    empty_dataframe = cast(
        pl.DataFrame, pl.from_arrow(batch_or_batch_container.schema.empty_table())
    )
    match batch_or_batch_container:
        case pa.RecordBatchReader():
            batches = list(batch_or_batch_container)
        case _SchemaAndBatches():
            batches = batch_or_batch_container.batches
        case pa.RecordBatch():
            batches = [batch_or_batch_container]

    if not batches:
        return empty_dataframe

    return cast(
        pl.DataFrame,
        pl.from_arrow(batches, rechunk=False, schema=empty_dataframe.schema),
    )


def _patch_batch_reader_schema(
    original_reader: pa.RecordBatchReader, new_schema: pa.Schema
) -> _SchemaAndBatches:
    def new_batches():
        for batch in original_reader:
            yield batch.select(new_schema.names).cast(new_schema)

    return _SchemaAndBatches(schema=new_schema, batches=list(new_batches()))


@dataclasses.dataclass
class _SchemaAndBatches:
    schema: pa.Schema
    batches: list[pa.RecordBatch]

    def to_batch_reader(self):
        return pa.RecordBatchReader.from_batches(
            schema=self.schema, batches=self.batches
        )

    @classmethod
    def from_dataframe(
        cls, dataframe: pl.DataFrame, metadata: dict[bytes, bytes] | None = None
    ):
        table = dataframe.to_arrow()
        schema = table.schema.with_metadata(metadata) if metadata else table.schema
        return cls(schema, table.to_batches())


@dataclasses.dataclass
class _InMemoryExecutionContext:
    exec_context: ExecutionContext

    # Using _SchemaAndBatches rather than a RecordBatchReader since the latter's
    # contract only guarantees one iteration and these might be accessed more than
    # once
    computed_batches_for_op_graph: dict[op_graph.Op, _SchemaAndBatches] = (
        dataclasses.field(default_factory=dict)
    )

    @classmethod
    def count_source_op_uses(cls, op: op_graph.Op, use_counts: dict[op_graph.Op, int]):
        for source in op.sources():
            use_counts[source] = use_counts.get(source, 0) + 1
            cls.count_source_op_uses(source, use_counts)

    @functools.cached_property
    def reused_tables(self) -> set[op_graph.Op]:
        use_counts = dict[op_graph.Op, int]()
        for op in self.output_tables:
            self.count_source_op_uses(op, use_counts)

        return {op for op, count in use_counts.items() if count > 1}

    @functools.cached_property
    def output_tables(self) -> set[op_graph.Op]:
        return {ctx.table_op_graph for ctx in self.exec_context.tables_to_compute}


class InMemoryTableComputeResult(TableComputeResult):
    """The in-memory result of computing a particular op graph."""

    def __init__(
        self,
        storage_manager: StorageManager,
        batches: _SchemaAndBatches,
        context: TableComputeContext,
    ):
        self._storage_manager = storage_manager
        self._batches = batches
        self._context = context

    def to_batch_reader(self) -> pa.RecordBatchReader:
        return self._batches.to_batch_reader()

    def to_urls(self) -> list[str]:
        # one file for now; we may produce more in the future
        file_idx = 0
        file_name = f"{self._context.output_url_prefix}.{file_idx:>06}"
        with (
            self._storage_manager.blob_from_url(file_name).open("wb") as stream,
            pq.ParquetWriter(stream, self._batches.schema) as writer,
        ):
            for batch in self._batches.batches:
                writer.write_batch(batch)

        return [file_name]

    @property
    def context(self) -> TableComputeContext:
        return self._context


class InMemoryExecutionResult(ExecutionResult):
    """A container for in-memory results.

    This container is optimized to avoid writes to disk, i.e., `to_batch_reader` will
    be fast `to_urls` will be slow.
    """

    def __init__(
        self,
        tables: list[InMemoryTableComputeResult],
        context: ExecutionContext,
    ):
        self._tables = tables
        self._context = context

    @classmethod
    def make(
        cls,
        storage_manager: StorageManager,
        in_memory_context: _InMemoryExecutionContext,
        context: ExecutionContext,
    ) -> InMemoryExecutionResult:
        tables = [
            InMemoryTableComputeResult(
                storage_manager,
                in_memory_context.computed_batches_for_op_graph[
                    table_context.table_op_graph
                ],
                table_context,
            )
            for table_context in context.tables_to_compute
        ]
        return InMemoryExecutionResult(
            tables,
            context,
        )

    @property
    def tables(self) -> list[InMemoryTableComputeResult]:
        return self._tables

    @property
    def context(self) -> ExecutionContext:
        return self._context


class InMemoryExecutor:
    """Executes op_graphs in memory (after staging queries)."""

    def __init__(self, staging_db: StagingDB, storage_manager: StorageManager):
        self._staging_db = staging_db
        self._storage_manager = storage_manager

    @classmethod
    def _is_sql_compatible(cls, op: op_graph.Op) -> bool:
        return isinstance(op, sql.SqlComputableOp) and all(
            cls._is_sql_compatible(sub_op) for sub_op in op.sources()
        )

    def _execute_read_from_parquet(
        self, op: op_graph.op.ReadFromParquet, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        batches: list[pa.RecordBatch] = []
        for blob_name in op.blob_names:
            with (
                self._storage_manager.blob_from_url(blob_name).open("rb") as stream,
            ):
                batches.extend(
                    # reading files with pyarrow, then converting them to polars
                    # can cause "ShapeError" bugs. That's why we're not reading this
                    # using pyarrow.
                    pl.read_parquet(
                        source=stream,
                        columns=op.arrow_schema.names,
                        use_pyarrow=False,
                    )
                    .to_arrow()
                    .to_batches()
                )
        return _SchemaAndBatches(op.arrow_schema, batches=batches)

    def _execute_rollup_by_aggregation(
        self, op: op_graph.op.RollupByAggregation, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        raise NotImplementedError(
            "rollup by aggregation outside of sql not implemented"
        )

    def _execute_rename_columns(
        self, op: op_graph.op.RenameColumns, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).rename(dict(op.old_name_to_new))
        )

    def _execute_select_columns(
        self, op: op_graph.op.SelectColumns, context: _InMemoryExecutionContext
    ):
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).select(op.columns)
        )

    def _execute_limit_rows(
        self, op: op_graph.op.LimitRows, context: _InMemoryExecutionContext
    ):
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).limit(op.num_rows)
        )

    def _execute_order_by(
        self, op: op_graph.op.OrderBy, context: _InMemoryExecutionContext
    ):
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).sort(
                op.columns, descending=op.desc
            )
        )

    def _row_filter_to_condition(  # noqa:  PLR0911, C901
        self, row_filter: op_graph.RowFilter
    ) -> pl.Expr:
        match row_filter:
            case op_graph.row_filter.CompareColumnToLiteral():
                match row_filter.comparison_type:
                    case table_pb2.COMPARISON_TYPE_EQ:
                        return pl.col(row_filter.column_name) == row_filter.literal
                    case table_pb2.COMPARISON_TYPE_NE:
                        return pl.col(row_filter.column_name) != row_filter.literal
                    case table_pb2.COMPARISON_TYPE_LT:
                        return pl.col(row_filter.column_name) < row_filter.literal
                    case table_pb2.COMPARISON_TYPE_GT:
                        return pl.col(row_filter.column_name) > row_filter.literal
                    case table_pb2.COMPARISON_TYPE_LE:
                        return pl.col(row_filter.column_name) <= row_filter.literal
                    case table_pb2.COMPARISON_TYPE_GE:
                        return pl.col(row_filter.column_name) >= row_filter.literal
                    case _:
                        raise op_graph.OpParseError(
                            "unknown comparison type value in row filter",
                            value=row_filter.comparison_type,
                        )
            case op_graph.row_filter.CombineFilters():
                sub_filters = (
                    self._row_filter_to_condition(sub_filter)
                    for sub_filter in row_filter.row_filters
                )
                match row_filter.combination_op:
                    case table_pb2.LOGICAL_COMBINATION_ANY:
                        return functools.reduce(
                            lambda left, right: left | right, sub_filters
                        )
                    case table_pb2.LOGICAL_COMBINATION_ALL:
                        return functools.reduce(
                            lambda left, right: left & right, sub_filters
                        )
                    case _:
                        raise op_graph.OpParseError(
                            "unknown logical combination op value in row filter",
                            value=row_filter.combination_op,
                        )

    def _execute_filter_rows(
        self, op: op_graph.op.FilterRows, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).filter(
                self._row_filter_to_condition(op.row_filter)
            )
        )

    def _execute_embedding_metrics(
        self, op: op_graph.op.EmbeddingMetrics, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        embedding_df = _as_df(self._execute(op.table, context))
        if len(embedding_df) < _MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY:
            # downstream consumers handle empty metadata by substituting their
            # own values
            return _SchemaAndBatches.from_dataframe(embedding_df)

        if "id" not in embedding_df.schema or "embedding" not in embedding_df.schema:
            raise BadArgumentError(
                "EmbeddingMetrics op needs to be computed on Embedding table"
            )
        embedding = embedding_df.select("embedding").to_series().to_numpy()

        metadata: dict[bytes, bytes] = {
            b"ne_sum": str(embedding_metric.ne_sum(embedding, normalize=True)).encode(),
            b"condition_number": str(
                embedding_metric.condition_number(embedding, normalize=True)
            ).encode(),
            b"rcondition_number": str(
                embedding_metric.rcondition_number(embedding, normalize=True)
            ).encode(),
            b"stable_rank": str(
                embedding_metric.stable_rank(embedding, normalize=True)
            ).encode(),
        }
        return _SchemaAndBatches.from_dataframe(embedding_df, metadata=metadata)

    def _execute_embedding_coordinates(
        self, op: op_graph.op.EmbeddingCoordinates, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        # TODO(Hunterlige): Preserve metadata for all execute ops
        record_batch = self._execute(op.table, context)
        embedding_df = _as_df(record_batch)

        # the neighbors of a point includes itself. That does mean, that an n_neighbors
        # value of less than 3 simply does not work
        if len(embedding_df) < _MIN_EMBEDDINGS_FOR_EMBEDDINGS_SUMMARY:
            coordinates_df = embedding_df.with_columns(
                pl.Series(
                    name="embedding",
                    values=[[0.0] * op.n_components] * len(embedding_df),
                    dtype=pl.Array(pl.Float32, op.n_components),
                )
            )
            return _SchemaAndBatches.from_dataframe(
                coordinates_df, record_batch.schema.metadata
            )

        if "id" not in embedding_df.schema or "embedding" not in embedding_df.schema:
            raise BadArgumentError(
                "EmbeddingCoordinates op needs to be computed on Embedding table"
            )
        embedding = embedding_df.select("embedding").to_series().to_numpy()

        n_neighbors = 15
        init = "spectral"
        # y spectral initialisation cannot be used when n_neighbors
        # is greater or equal to the number of samples
        if embedding.shape[0] <= n_neighbors:
            init = "random"
            # n_neighbors is larger than the dataset size; truncating to X.shape[0] - 1
            n_neighbors = embedding.shape[0] - 1

        # import umap locally to reduce loading time
        # TODO(Hunterlige): Replace with lazy_import
        from umap import umap_ as umap

        projector = umap.UMAP(
            n_neighbors=n_neighbors,
            n_components=op.n_components,
            metric=op.metric,
            init=init,
            low_memory=False,
            verbose=True,
        )

        _logger.info(
            "generating embedding coordinates",
            num_embeddings=embedding_df.shape[0],
            metric=op.metric,
            n_neighbors=n_neighbors,
            init=init,
            n_components=op.n_components,
        )
        coordinates = projector.fit_transform(embedding)
        coordinates_df = embedding_df.with_columns(
            pl.Series(
                name="embedding",
                values=coordinates,
                dtype=pl.Array(pl.Float32, coordinates.shape[1]),
            )
        )
        return _SchemaAndBatches.from_dataframe(
            coordinates_df, record_batch.schema.metadata
        )

    def _execute_distinct_rows(
        self, op: op_graph.op.DistinctRows, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).unique()
        )

    def _execute_join(
        self, op: op_graph.op.Join, context: _InMemoryExecutionContext
    ) -> _SchemaAndBatches:
        left_df = _as_df(self._execute(op.left_source, context))
        right_df = _as_df(self._execute(op.right_source, context))

        match op.how:
            case table_pb2.JOIN_TYPE_INNER:
                join_type = "inner"
            case table_pb2.JOIN_TYPE_LEFT_OUTER:
                join_type = "left"
            case _:
                join_type = "inner"

        # in our join semantics we drop columns from the right source on conflict
        right_df = right_df.select(
            [
                col
                for col in right_df.columns
                if col in op.right_join_columns or col not in left_df.columns
            ]
        )

        return _SchemaAndBatches.from_dataframe(
            left_df.join(
                right_df,
                left_on=op.left_join_columns,
                right_on=op.right_join_columns,
                how=join_type,
            )
        )

    def _execute_empty(self, op: op_graph.op.Empty, context: _InMemoryExecutionContext):
        empty_table = pa.schema([]).empty_table()
        return _SchemaAndBatches(empty_table.schema, empty_table.to_batches())

    def _execute_concat(
        self, op: op_graph.op.Concat, context: _InMemoryExecutionContext
    ):
        dataframes = [_as_df(self._execute(table, context)) for table in op.tables]
        return _SchemaAndBatches.from_dataframe(pl.concat(dataframes))

    def _execute_unnest_struct(
        self, op: op_graph.op.UnnestStruct, context: _InMemoryExecutionContext
    ):
        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).unnest(op.struct_column_name)
        )

    def _execute_add_literal_column(
        self, op: op_graph.op.AddLiteralColumn, context: _InMemoryExecutionContext
    ):
        pl_schema = cast(
            pl.DataFrame, pl.from_arrow(op.column_arrow_schema.empty_table())
        ).schema
        name, dtype = next(iter(pl_schema.items()))

        return _SchemaAndBatches.from_dataframe(
            _as_df(self._execute(op.source, context)).with_columns(
                pl.lit(op.literal, dtype).alias(name)
            )
        )

    def _execute_embed_node2vec_from_edge_lists(
        self,
        op: op_graph.op.EmbedNode2vecFromEdgeLists,
        context: _InMemoryExecutionContext,
    ):
        dtypes: set[pa.DataType] = set()
        entities_dtypes: dict[str, pa.DataType] = {}
        for edge_list in op.edge_list_tables:
            schema = edge_list.table.schema.to_arrow()
            start_dtype = schema.field(edge_list.start_column_name).type
            end_dtype = schema.field(edge_list.end_column_name).type
            dtypes.add(start_dtype)
            dtypes.add(end_dtype)
            entities_dtypes[edge_list.start_column_name] = start_dtype
            entities_dtypes[edge_list.end_column_name] = end_dtype

        start_fields = [pa.field(f"start_id_{dtype}", dtype) for dtype in dtypes]
        start_fields.append(pa.field("start_source", pa.large_string()))
        start_id_column_names = [field.name for field in start_fields]

        end_fields = [pa.field(f"end_id_{dtype}", dtype) for dtype in dtypes]
        end_fields.append(pa.field("end_source", pa.large_string()))
        end_id_column_names = [field.name for field in end_fields]

        fields = start_fields + end_fields
        empty_edges_table = pl.from_arrow(pa.schema(fields).empty_table())

        if isinstance(empty_edges_table, pl.Series):
            empty_edges_table = empty_edges_table.to_frame()

        def edge_generator():
            for edge_list in op.edge_list_tables:
                start_column_name = edge_list.start_column_name
                end_column_name = edge_list.end_column_name
                start_column_type_name = entities_dtypes[start_column_name]
                end_column_type_name = entities_dtypes[end_column_name]
                for batch in self._execute(edge_list.table, context).batches:
                    yield (
                        _as_df(batch)
                        .with_columns(
                            pl.col(edge_list.start_column_name).alias(
                                f"start_id_{start_column_type_name}"
                            ),
                            pl.lit(edge_list.start_entity_name).alias("start_source"),
                            pl.col(edge_list.end_column_name).alias(
                                f"end_id_{end_column_type_name}"
                            ),
                            pl.lit(edge_list.end_entity_name).alias("end_source"),
                        )
                        .select(
                            f"start_id_{start_column_type_name}",
                            "start_source",
                            f"end_id_{end_column_type_name}",
                            "end_source",
                        )
                    )

        edges = pl.concat(
            [
                empty_edges_table,
                *(edge_list for edge_list in edge_generator()),
            ],
            rechunk=False,
            how="diagonal",
        )

        n2v_space = embed.Space(
            edges=edges,
            start_id_column_names=start_id_column_names,
            end_id_column_names=end_id_column_names,
            directed=True,
        )
        n2v_runner = embed.Node2Vec(
            space=n2v_space,
            dim=op.ndim,
            walk_length=op.walk_length,
            window=op.window,
            p=op.p,
            q=op.q,
            alpha=op.alpha,
            min_alpha=op.min_alpha,
            negative=op.negative,
        )
        n2v_runner.train(epochs=op.epochs)
        return _SchemaAndBatches.from_dataframe(n2v_runner.wv.to_polars())

    def _do_execute(  # noqa: PLR0911, PLR0912, C901
        self,
        op: op_graph.Op,
        context: _InMemoryExecutionContext,
    ) -> _SchemaAndBatches:
        if self._is_sql_compatible(op) and self._staging_db:
            query = sql.parse_op_graph(
                op,
                self._staging_db.query_for_blobs,
                self._staging_db.query_for_vector_search,
            )
            expected_schema = op.schema
            return _patch_batch_reader_schema(
                self._staging_db.run_select_query(query),
                new_schema=expected_schema.to_arrow(),
            )

        match op:
            case op_graph.op.SelectFromStaging():
                raise InternalError("SelectFromStaging should always be lowered to sql")
            case op_graph.op.SelectFromVectorStaging():
                raise InternalError(
                    "SelectFromVectorStaging should always be lowered to sql"
                )
            case op_graph.op.ReadFromParquet():
                return self._execute_read_from_parquet(op, context)
            case op_graph.op.RenameColumns():
                return self._execute_rename_columns(op, context)
            case op_graph.op.Join():
                return self._execute_join(op, context)
            case op_graph.op.SelectColumns():
                return self._execute_select_columns(op, context)
            case op_graph.op.LimitRows():
                return self._execute_limit_rows(op, context)
            case op_graph.op.OrderBy():
                return self._execute_order_by(op, context)
            case op_graph.op.FilterRows():
                return self._execute_filter_rows(op, context)
            case op_graph.op.DistinctRows():
                return self._execute_distinct_rows(op, context)
            case (
                op_graph.op.SetMetadata()
                | op_graph.op.UpdateMetadata()
                | op_graph.op.RemoveFromMetadata()
                | op_graph.op.UpdateFeatureTypes()
            ):
                return self._execute(op.source, context)
            case op_graph.op.EmbeddingMetrics() as op:
                return self._execute_embedding_metrics(op, context)
            case op_graph.op.EmbeddingCoordinates():
                return self._execute_embedding_coordinates(op, context)
            case op_graph.op.RollupByAggregation() as op:
                return self._execute_rollup_by_aggregation(op, context)
            case op_graph.op.Empty():
                return self._execute_empty(op, context)
            case op_graph.op.EmbedNode2vecFromEdgeLists():
                return self._execute_embed_node2vec_from_edge_lists(op, context)
            case op_graph.op.Concat():
                return self._execute_concat(op, context)
            case op_graph.op.UnnestStruct():
                return self._execute_unnest_struct(op, context)
            case op_graph.op.AddLiteralColumn():
                return self._execute_add_literal_column(op, context)

    def _execute(
        self,
        op: op_graph.Op,
        context: _InMemoryExecutionContext,
    ) -> _SchemaAndBatches:
        with structlog.contextvars.bound_contextvars(
            executing_op=op.expected_oneof_field()
        ):
            if op in context.computed_batches_for_op_graph:
                _logger.info("using previously computed table for op")
                return context.computed_batches_for_op_graph[op]

            try:
                _logger.info("starting op execution")
                batches = self._do_execute(op=op, context=context)
            finally:
                _logger.info("op execution complete")

            if op in context.output_tables or op in context.reused_tables:
                context.computed_batches_for_op_graph[op] = batches
            return batches

    def execute(self, context: ExecutionContext) -> InMemoryExecutionResult:
        in_memory_context = _InMemoryExecutionContext(context)

        for op in in_memory_context.output_tables:
            if op not in in_memory_context.computed_batches_for_op_graph:
                self._execute(op, in_memory_context)

        return InMemoryExecutionResult.make(
            self._storage_manager, in_memory_context, context
        )
