"""Operations that construct tables.

Each operation is the head of a log of one or more operations that when executed
produce a table.

To add a new operation type:

1. Add a protobuf message definition detailing the operations's arguments.

1. Add the operation to the TableComputeOp message as part of the oneof called "op"

1. Write a wrapper class that inherits from corvic.table.ops._Base (in this file).
   The wrapper should include properties for accessing the fields of the message.

1. Add the wrapper class to the "Op" union at the bottom of this file.

1. Note the mapping between the TableComputeOp field name for the new op and the
   wrapper class in corvic.table.ops._COMPUTE_OP_FIELD_NAME_TO_OP (in this file).

1. Add a case to the match statement in corvic.table.ops.from_proto.
"""

from __future__ import annotations

import dataclasses
import functools
import threading
from abc import abstractmethod
from collections import OrderedDict
from collections.abc import Iterable, Mapping, Sequence
from typing import Any, Final, Literal, overload

import cachetools
import polars as pl
import protovalidate
import pyarrow as pa
from google.protobuf import json_format
from more_itertools import flatten

import corvic.op_graph.feature_types as feature_type
from corvic import orm
from corvic.op_graph._schema import Field
from corvic.op_graph.errors import OpParseError
from corvic.op_graph.feature_types import FeatureType, ForeignKey
from corvic.op_graph.feature_types import from_proto as ftype_from_proto
from corvic.op_graph.proto_wrapper import ProtoOneofWrapper
from corvic.op_graph.row_filters import RowFilter
from corvic.op_graph.row_filters import from_proto as row_filters_from_proto
from corvic.result import BadArgumentError, Ok
from corvic_generated.algorithm.graph.v1 import graph_pb2
from corvic_generated.orm.v1 import table_pb2

ProtoOp = (
    table_pb2.SelectFromStagingOp
    | table_pb2.RenameColumnsOp
    | table_pb2.JoinOp
    | table_pb2.SelectColumnsOp
    | table_pb2.LimitRowsOp
    | table_pb2.OrderByOp
    | table_pb2.FilterRowsOp
    | table_pb2.DistinctRowsOp
    | table_pb2.UpdateMetadataOp
    | table_pb2.SetMetadataOp
    | table_pb2.RemoveFromMetadataOp
    | table_pb2.UpdateFeatureTypesOp
    | table_pb2.RollupByAggregationOp
    | table_pb2.EmptyOp
    | table_pb2.EmbedNode2vecFromEdgeListsOp
    | table_pb2.EmbeddingMetricsOp
    | table_pb2.EmbeddingCoordinatesOp
    | table_pb2.ReadFromParquetOp
    | table_pb2.SelectFromVectorStagingOp
    | table_pb2.ConcatOp
    | table_pb2.UnnestStructOp
    | table_pb2.AddLiteralColumnOp
)


@overload
def from_proto(
    proto: table_pb2.TableComputeOp, parent_ops: list[Op] | None = None
) -> Op: ...


@overload
def from_proto(
    proto: table_pb2.SelectFromStagingOp, parent_ops: list[Op] | None = None
) -> SelectFromStaging: ...


@overload
def from_proto(
    proto: table_pb2.RenameColumnsOp, parent_ops: list[Op] | None = None
) -> RenameColumns: ...


@overload
def from_proto(proto: table_pb2.JoinOp, parent_ops: list[Op] | None = None) -> Join: ...


@overload
def from_proto(
    proto: table_pb2.SelectColumnsOp, parent_ops: list[Op] | None = None
) -> SelectColumns: ...


@overload
def from_proto(
    proto: table_pb2.LimitRowsOp, parent_ops: list[Op] | None = None
) -> LimitRows: ...


@overload
def from_proto(
    proto: table_pb2.OrderByOp, parent_ops: list[Op] | None = None
) -> OrderBy: ...


@overload
def from_proto(
    proto: table_pb2.FilterRowsOp, parent_ops: list[Op] | None = None
) -> FilterRows: ...


@overload
def from_proto(
    proto: table_pb2.DistinctRowsOp, parent_ops: list[Op] | None = None
) -> DistinctRows: ...


@overload
def from_proto(
    proto: table_pb2.UpdateMetadataOp, parent_ops: list[Op] | None = None
) -> UpdateMetadata: ...


@overload
def from_proto(
    proto: table_pb2.SetMetadataOp, parent_ops: list[Op] | None = None
) -> SetMetadata: ...


@overload
def from_proto(
    proto: table_pb2.RemoveFromMetadataOp, parent_ops: list[Op] | None = None
) -> RemoveFromMetadata: ...


@overload
def from_proto(
    proto: table_pb2.UpdateFeatureTypesOp, parent_ops: list[Op] | None = None
) -> UpdateFeatureTypes: ...


@overload
def from_proto(
    proto: table_pb2.RollupByAggregationOp, parent_ops: list[Op] | None = None
) -> RollupByAggregation: ...


@overload
def from_proto(
    proto: table_pb2.EmptyOp, parent_ops: list[Op] | None = None
) -> Empty: ...


@overload
def from_proto(
    proto: table_pb2.EmbedNode2vecFromEdgeListsOp,
    parent_ops: list[Op] | None = None,
) -> EmbedNode2vecFromEdgeLists: ...


@overload
def from_proto(
    proto: table_pb2.EmbeddingMetricsOp,
    parent_ops: list[Op] | None = None,
) -> EmbeddingMetrics: ...


@overload
def from_proto(
    proto: table_pb2.EmbeddingCoordinatesOp,
    parent_ops: list[Op] | None = None,
) -> EmbeddingCoordinates: ...


@overload
def from_proto(
    proto: table_pb2.ReadFromParquetOp,
    parent_ops: list[Op] | None = None,
) -> ReadFromParquet: ...


@overload
def from_proto(
    proto: table_pb2.SelectFromVectorStagingOp,
    parent_ops: list[Op] | None = None,
) -> SelectFromVectorStaging: ...


@overload
def from_proto(
    proto: table_pb2.ConcatOp,
    parent_ops: list[Op] | None = None,
) -> Concat: ...


@overload
def from_proto(
    proto: table_pb2.UnnestStructOp,
    parent_ops: list[Op] | None = None,
) -> UnnestStruct: ...


@overload
def from_proto(
    proto: table_pb2.AddLiteralColumnOp,
    parent_ops: list[Op] | None = None,
) -> AddLiteralColumn: ...


def from_proto(  # noqa: C901, PLR0912
    proto: ProtoOp | table_pb2.TableComputeOp,
    parent_ops: list[Op] | None = None,
) -> Op:
    """Create an Op wrapper around an Op protobuf message."""
    protovalidate.validate(proto)
    match proto:
        case table_pb2.TableComputeOp():
            pass
        case table_pb2.EmptyOp():
            proto = table_pb2.TableComputeOp(empty=proto)
        case table_pb2.SelectFromStagingOp():
            proto = table_pb2.TableComputeOp(select_from_staging=proto)
        case table_pb2.RenameColumnsOp():
            proto = table_pb2.TableComputeOp(rename_columns=proto)
        case table_pb2.JoinOp():
            proto = table_pb2.TableComputeOp(join=proto)
        case table_pb2.SelectColumnsOp():
            proto = table_pb2.TableComputeOp(select_columns=proto)
        case table_pb2.LimitRowsOp():
            proto = table_pb2.TableComputeOp(limit_rows=proto)
        case table_pb2.OrderByOp():
            proto = table_pb2.TableComputeOp(order_by=proto)
        case table_pb2.FilterRowsOp():
            proto = table_pb2.TableComputeOp(filter_rows=proto)
        case table_pb2.DistinctRowsOp():
            proto = table_pb2.TableComputeOp(distinct_rows=proto)
        case table_pb2.UpdateMetadataOp():
            proto = table_pb2.TableComputeOp(update_metadata=proto)
        case table_pb2.SetMetadataOp():
            proto = table_pb2.TableComputeOp(set_metadata=proto)
        case table_pb2.RemoveFromMetadataOp():
            proto = table_pb2.TableComputeOp(remove_from_metadata=proto)
        case table_pb2.UpdateFeatureTypesOp():
            proto = table_pb2.TableComputeOp(update_feature_types=proto)
        case table_pb2.RollupByAggregationOp():
            proto = table_pb2.TableComputeOp(rollup_by_aggregation=proto)
        case table_pb2.EmbedNode2vecFromEdgeListsOp():
            proto = table_pb2.TableComputeOp(embed_node2vec_from_edge_lists=proto)
        case table_pb2.EmbeddingMetricsOp():
            proto = table_pb2.TableComputeOp(embedding_metrics=proto)
        case table_pb2.EmbeddingCoordinatesOp():
            proto = table_pb2.TableComputeOp(embedding_coordinates=proto)
        case table_pb2.ReadFromParquetOp():
            proto = table_pb2.TableComputeOp(read_from_parquet=proto)
        case table_pb2.SelectFromVectorStagingOp():
            proto = table_pb2.TableComputeOp(select_from_vector_staging=proto)
        case table_pb2.ConcatOp():
            proto = table_pb2.TableComputeOp(concat=proto)
        case table_pb2.UnnestStructOp():
            proto = table_pb2.TableComputeOp(unnest_struct=proto)
        case table_pb2.AddLiteralColumnOp():
            proto = table_pb2.TableComputeOp(add_literal_column=proto)

    return _from_compute_op(proto, parent_ops)


def empty() -> Op:
    return from_proto(table_pb2.EmptyOp())


def from_bytes(serialized_proto: bytes) -> Op:
    """Deserialize an Op protobuf message directly into a wrapper."""
    if not serialized_proto:
        return empty()

    proto = table_pb2.TableComputeOp()
    proto.ParseFromString(serialized_proto)
    return from_proto(proto)


def from_staging(
    blob_names: Sequence[str],
    arrow_schema: pa.Schema,
    feature_types: Sequence[FeatureType],
    expected_rows: int,
) -> SelectFromStaging:
    """Build a SelectFromStaging Op."""
    if len(arrow_schema) != len(feature_types):
        raise BadArgumentError(
            "length of arrow_schema must match length of feature_types"
        )
    if any(
        isinstance(feature, ForeignKey) and not feature.referenced_source_id
        for feature in feature_types
    ):
        raise BadArgumentError("referenced_source_id cannot be empty in foreign key")
    return from_proto(
        table_pb2.SelectFromStagingOp(
            blob_names=blob_names,
            arrow_schema=arrow_schema.serialize().to_pybytes(),
            feature_types=[feature_type.to_proto() for feature_type in feature_types],
            expected_rows=expected_rows,
        )
    )


def from_parquet(
    blob_names: Sequence[str],
    arrow_schema: pa.Schema,
    feature_types: Sequence[FeatureType],
    expected_rows: int,
):
    """Build a ReadFromParquet Op."""
    if len(arrow_schema) != len(feature_types):
        raise BadArgumentError(
            "length of arrow_schema must match length of feature_types"
        )
    if any(
        isinstance(feature, ForeignKey) and not feature.referenced_source_id
        for feature in feature_types
    ):
        raise BadArgumentError("referenced_source_id cannot be empty in foreign key")
    return from_proto(
        table_pb2.ReadFromParquetOp(
            blob_names=blob_names,
            arrow_schema=arrow_schema.serialize().to_pybytes(),
            feature_types=[feature_type.to_proto() for feature_type in feature_types],
            expected_rows=expected_rows,
        )
    )


def embed_node2vec_from_edge_lists(
    edge_list_tables: Sequence[EdgeListTable], params: graph_pb2.Node2VecParameters
):
    return from_proto(
        table_pb2.EmbedNode2vecFromEdgeListsOp(
            edge_list_tables=[edge_list.to_proto() for edge_list in edge_list_tables],
            node2vec_parameters=params,
        )
    )


def quality_metrics_from_embedding(
    table: Op,
) -> EmbeddingMetrics:
    return from_proto(table_pb2.EmbeddingMetricsOp(table=table.to_proto()))


def coordinates_from_embedding(
    table: Op, metric: Literal["cosine", "euclidean"] = "cosine"
) -> EmbeddingCoordinates:
    return from_proto(
        table_pb2.EmbeddingCoordinatesOp(
            table=table.to_proto(), n_components=3, metric=metric
        )
    )


def concat(tables: list[Op]) -> Ok[Concat | Empty] | BadArgumentError:
    if not tables:
        return Ok(from_proto(table_pb2.EmptyOp()))
    schema = tables[0].schema.to_arrow()
    for table in tables[1:]:
        if schema != table.schema.to_arrow():
            return BadArgumentError("table schemas do not match")
    return Ok(
        from_proto(table_pb2.ConcatOp(tables=[table.to_proto() for table in tables]))
    )


def _table_compute_op_cache_key(
    proto: table_pb2.TableComputeOp, parent_ops: list[Op] | None
):
    # N.B. parent_op is not part of the hash key on purpose. Since
    # ops in op-graphs are immutable it's safe to reuse parent
    # in arbitrary graphs.
    return proto.SerializeToString(deterministic=True)


@cachetools.cached(
    cache=cachetools.LRUCache(maxsize=128),
    key=_table_compute_op_cache_key,
    lock=threading.Lock(),
)
def _from_compute_op(
    proto: table_pb2.TableComputeOp, parent_ops: list[Op] | None
) -> Op:
    field_name = proto.WhichOneof(_Base.oneof_name())
    new_op_type = _COMPUTE_OP_FIELD_NAME_TO_OP.get(field_name)
    if new_op_type is None:
        raise BadArgumentError("unsupported operation type", operation_type=field_name)
    return new_op_type(proto, parent_ops if parent_ops else [])


class _Base(ProtoOneofWrapper[table_pb2.TableComputeOp]):
    """Base type for all log operations.

    Each operation is the head of a log, potentially referencing other operations
    to construct the table.

    These operations are convenience wrappers for reading and writing protobufs
    that describe table operations.
    """

    _parents: list[Op]

    def __init__(self, proto: table_pb2.TableComputeOp, parents: list[Op]):
        super().__init__(proto)
        self._parents = parents

    @functools.cached_property
    def schema(self) -> Schema:
        if isinstance(self, Op):
            return Schema.from_ops(self)
        raise BadArgumentError("unsupported schema on op")

    @classmethod
    def oneof_name(cls) -> str:
        return "op"

    @classmethod
    def expected_oneof_field(cls) -> str:
        """Returns the name of field for this type in the root proto op type."""
        if cls not in _OP_TO_COMPUTE_OP_FIELD_NAME:
            raise OpParseError(
                "operation field name must registered in _COMPUTE_OP_FIELD_NAME_TO_OP"
            )
        return _OP_TO_COMPUTE_OP_FIELD_NAME[cls]

    @abstractmethod
    def sources(self) -> list[Op]:
        """Returns the source tables that this operation depends on (empty if none)."""

    def _check_columns_valid(
        self, columns: Mapping[str, Any] | Sequence[str] | str
    ) -> Ok[None] | BadArgumentError:
        if isinstance(columns, str):
            columns = [columns]

        if not columns:
            return BadArgumentError("columns cannot be empty")

        for column in columns:
            if not self.schema.has_column(column):
                return BadArgumentError(
                    "op schema has no column with that name", name=column
                )
        if len(set(columns)) != len(columns):
            return BadArgumentError("columns must be unique")
        return Ok(None)

    def _check_join_columns(
        self,
        right: Op,
        left_join_columns: Sequence[str],
        right_join_columns: Sequence[str],
    ) -> Ok[None] | BadArgumentError:
        if len(left_join_columns) != len(right_join_columns):
            return BadArgumentError("number of matching columns must be the same")
        self._check_columns_valid(left_join_columns).unwrap_or_raise()
        right._check_columns_valid(right_join_columns).unwrap_or_raise()  # noqa: SLF001

        for left_field_name, right_field_name in zip(
            left_join_columns, right_join_columns, strict=False
        ):
            left_field = self.schema.get(left_field_name)
            right_field = right.schema.get(right_field_name)
            if not left_field or not right_field:
                return BadArgumentError("schema does not contain column")
            if left_field.dtype != right_field.dtype:
                return BadArgumentError(
                    "join on unequal datatypes",
                    left_column=left_field_name,
                    right_field=right_field_name,
                    left_type=str(left_field.dtype),
                    right_type=str(right_field.dtype),
                )
        return Ok(None)

    def join(
        self,
        right: Op,
        left_on: Sequence[str] | str,
        right_on: Sequence[str] | str,
        how: table_pb2.JoinType | Literal["inner", "left outer"],
    ) -> Join:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        if isinstance(how, str):
            match how:
                case "inner":
                    how = table_pb2.JOIN_TYPE_INNER
                case "left outer":
                    how = table_pb2.JOIN_TYPE_LEFT_OUTER
        if how == table_pb2.JOIN_TYPE_UNSPECIFIED:
            raise BadArgumentError("how must be specified")

        if isinstance(left_on, str):
            left_on = [left_on]
        if isinstance(right_on, str):
            right_on = [right_on]

        self._check_join_columns(
            right,
            left_join_columns=left_on,
            right_join_columns=right_on,
        ).unwrap_or_raise()

        return from_proto(
            table_pb2.JoinOp(
                left_source=self.to_proto(),
                right_source=right.to_proto(),
                left_join_columns=left_on,
                right_join_columns=right_on,
                how=how,
            ),
            [self, right],
        )

    def rename_columns(self, old_name_to_new: Mapping[str, str]):
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")
        self._check_columns_valid(old_name_to_new).unwrap_or_raise()

        new_names = set(old_name_to_new.values())
        if len(new_names) != len(old_name_to_new):
            raise BadArgumentError("table column names must be unique")

        for new_name in new_names:
            if self.schema.has_column(new_name) and new_name not in old_name_to_new:
                raise BadArgumentError(
                    "op schema already has a column with that name", name=new_name
                )

        return from_proto(
            table_pb2.RenameColumnsOp(
                source=self._proto, old_names_to_new=old_name_to_new
            ),
            [self],
        )

    def select_columns(self, columns: Sequence[str]) -> SelectColumns:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        if isinstance(columns, str):
            # N.B. if we dont explicitly handle the lone string type like this
            # we end up in the unfortuname situation where keys_to_remove
            # silently becomes a list of one character string.
            # I.e., a string is a valid sequence of strings
            columns = [columns]

        if len(columns) > 0:
            self._check_columns_valid(columns).unwrap_or_raise()

        return from_proto(
            table_pb2.SelectColumnsOp(source=self._proto, columns=columns), [self]
        )

    def limit_rows(self, num_rows: int) -> LimitRows:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        if num_rows <= 0:
            raise BadArgumentError("num_rows must be positive")
        if isinstance(self, LimitRows):
            proto = self.to_proto().limit_rows
            proto.num_rows = min(proto.num_rows, num_rows)
        else:
            proto = table_pb2.LimitRowsOp(source=self._proto, num_rows=num_rows)
        return from_proto(proto, [self])

    def order_by(self, columns: Sequence[str], *, desc: bool) -> OrderBy:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")
        self._check_columns_valid(columns).unwrap_or_raise()

        proto = table_pb2.OrderByOp(source=self._proto, columns=columns, desc=desc)
        return from_proto(proto, [self])

    def update_metadata(self, metadata_updates: Mapping[str, Any]) -> UpdateMetadata:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        proto = table_pb2.UpdateMetadataOp(source=self._proto)
        proto.metadata_updates.update(metadata_updates)
        return from_proto(proto, [self])

    def set_metadata(self, new_metadata: Mapping[str, Any]) -> SetMetadata:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        proto = table_pb2.SetMetadataOp(source=self._proto)
        proto.new_metadata.update(new_metadata)
        return from_proto(proto, [self])

    def remove_from_metadata(self, keys_to_remove: Sequence[str]) -> RemoveFromMetadata:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        if isinstance(keys_to_remove, str):
            # N.B. if we dont explicitly handle the lone string type like this
            # we end up in the unfortuname situation where keys_to_remove
            # silently becomes a list of one character string.
            # I.e., a string is a valid sequence of strings
            keys_to_remove = [keys_to_remove]
        proto = table_pb2.RemoveFromMetadataOp(
            source=self._proto, keys_to_remove=keys_to_remove
        )
        return from_proto(proto, [self])

    def update_feature_types(
        self, new_feature_types: Mapping[str, FeatureType]
    ) -> UpdateFeatureTypes:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")
        self._check_columns_valid(new_feature_types).unwrap_or_raise()

        if any(
            isinstance(feature, ForeignKey) and not feature.referenced_source_id
            for feature in new_feature_types.values()
        ):
            raise BadArgumentError(
                "referenced_source_id cannot be empty in foreign key"
            )

        new_feature_types_proto = {
            k: v.to_proto() for k, v in new_feature_types.items()
        }

        if isinstance(self, UpdateFeatureTypes):
            old_feature_types = dict(
                self.to_proto().update_feature_types.new_feature_types
            )
            old_feature_types.update(new_feature_types_proto)
            new_feature_types_proto = old_feature_types

        proto = table_pb2.UpdateFeatureTypesOp(
            source=self._proto, new_feature_types=new_feature_types_proto
        )
        return from_proto(proto, [self])

    def rollup_by_aggregation(  # noqa: C901
        self,
        group_by: Sequence[str] | str,
        target: str,
        aggregation: (
            table_pb2.AggregationType
            | Literal["count", "avg", "mode", "min", "max", "sum"]
        ),
    ) -> RollupByAggregation:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")
        self._check_columns_valid(group_by).unwrap_or_raise()
        self._check_columns_valid(target).unwrap_or_raise()

        if isinstance(aggregation, str):
            match aggregation:
                case "count":
                    aggregation = table_pb2.AGGREGATION_TYPE_COUNT
                case "avg":
                    aggregation = table_pb2.AGGREGATION_TYPE_AVG
                case "mode":
                    aggregation = table_pb2.AGGREGATION_TYPE_MODE
                case "min":
                    aggregation = table_pb2.AGGREGATION_TYPE_MIN
                case "max":
                    aggregation = table_pb2.AGGREGATION_TYPE_MAX
                case "sum":
                    aggregation = table_pb2.AGGREGATION_TYPE_SUM

        if aggregation == table_pb2.AGGREGATION_TYPE_UNSPECIFIED:
            raise BadArgumentError("aggregation must be specified")

        if isinstance(group_by, str):
            group_by = [group_by]

        return from_proto(
            table_pb2.RollupByAggregationOp(
                source=self.to_proto(),
                group_by_column_names=group_by,
                target_column_name=target,
                aggregation_type=aggregation,
            ),
            [self],
        )

    def filter_rows(self, row_filter: RowFilter) -> FilterRows:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        return from_proto(
            table_pb2.FilterRowsOp(
                source=self.to_proto(), row_filter=row_filter.to_proto()
            ),
            [self],
        )

    def unnest_struct(self, column_name: str) -> Ok[UnnestStruct] | BadArgumentError:
        struct_field = self.schema.get(column_name)
        if struct_field is None or not isinstance(struct_field.dtype, pa.StructType):
            return BadArgumentError(
                "no struct column with given name", column_name=column_name
            )

        for i in range(struct_field.dtype.num_fields):
            new_col_name = struct_field.dtype.field(i).name
            existing_field = self.schema.get(new_col_name)

            if existing_field is not None:
                return BadArgumentError(
                    "unnesting the struct would cause a column name conflict",
                    conflicting_column=new_col_name,
                )
        return Ok(
            from_proto(
                table_pb2.UnnestStructOp(
                    source=self.to_proto(), struct_column_name=column_name
                )
            )
        )

    def distinct_rows(self) -> DistinctRows:
        if not isinstance(self, Op):
            raise BadArgumentError("object is not an op")

        return from_proto(table_pb2.DistinctRowsOp(source=self.to_proto()), [self])

    def add_literal_column(
        self,
        column_name: str,
        literal: Any,
        dtype: pa.DataType | None = None,
        ftype: FeatureType | None = None,
    ) -> Ok[AddLiteralColumn] | BadArgumentError:
        if column_name in self.schema:
            return BadArgumentError(
                "a column already exists with that name",
                column_name=column_name,
            )
        if dtype is None:
            dtype = pl.DataFrame({column_name: [literal]}).to_arrow().schema[0].type
        if ftype is None:
            ftype = Field.decode_feature_type(dtype)

        proto_op = table_pb2.AddLiteralColumnOp(
            source=self._proto,
            column_arrow_schema=pa.schema([pa.field(column_name, dtype)])
            .serialize()
            .to_pybytes(),
            column_feature_type=ftype.to_proto(),
        )
        try:
            json_format.ParseDict({"literal": literal}, proto_op)
        except json_format.ParseError:
            return BadArgumentError("provided literal could not be serialized")

        return Ok(from_proto(proto_op))


class SelectFromStaging(_Base):
    """Construct a table by selecting rows from the staging collection.

    These operations are leaf operations that describe data sources.
    """

    @property
    def blob_names(self) -> Sequence[str]:
        return self._proto.select_from_staging.blob_names

    @property
    def columns(self) -> Sequence[str]:
        return self._proto.select_from_staging.columns

    @functools.cached_property
    def arrow_schema(self) -> pa.Schema:
        return pa.ipc.read_schema(
            pa.py_buffer(self._proto.select_from_staging.arrow_schema)
        )

    @functools.cached_property
    def feature_types(self) -> Sequence[FeatureType]:
        return [
            ftype_from_proto(feature_type)
            for feature_type in self._proto.select_from_staging.feature_types
        ]

    @property
    def expected_rows(self) -> int:
        return self._proto.select_from_staging.expected_rows

    def sources(self):
        return list[Op]()


class RenameColumns(_Base):
    """Rename the columns in the result of another operation.

    Useful for resolving conflicts that would happen during joins,
    or just for adjusting poor source names.
    """

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.rename_columns.source)

    @property
    def old_name_to_new(self) -> Mapping[str, str]:
        return self._proto.rename_columns.old_names_to_new

    def sources(self):
        return [self.source]


class UpdateFeatureTypes(_Base):
    """Patch FeatureType of a table schema."""

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.update_feature_types.source)

    @functools.cached_property
    def new_feature_types(self) -> Mapping[str, FeatureType]:
        return {
            k: ftype_from_proto(v)
            for k, v in self._proto.update_feature_types.new_feature_types.items()
        }

    def sources(self):
        return [self.source]


class Join(_Base):
    """Join two tables together to produce a new table.

    All unique columns from the constituent tables appear in the
    results. Order matters, left columns will be preferred on conflict
    and the names for left columns will be preferred when names for
    the join columns differ.
    """

    @property
    def left_source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.join.left_source)

    @property
    def right_source(self) -> Op:
        if len(self._parents) > 1:
            return self._parents[1]
        return from_proto(self._proto.join.right_source)

    @property
    def left_join_columns(self) -> Sequence[str]:
        return self._proto.join.left_join_columns

    @property
    def right_join_columns(self) -> Sequence[str]:
        return self._proto.join.right_join_columns

    @property
    def how(self):
        return self._proto.join.how

    def sources(self):
        return [self.left_source, self.right_source]


class SelectColumns(_Base):
    """Enumerate the columns from a source table that should be kept."""

    @property
    def columns(self) -> Sequence[str]:
        return self._proto.select_columns.columns

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.select_columns.source)

    def sources(self):
        return [self.source]


class LimitRows(_Base):
    """Limit the number of rows in a table."""

    @property
    def num_rows(self) -> int:
        return self._proto.limit_rows.num_rows

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.limit_rows.source)

    def sources(self):
        return [self.source]


class OrderBy(_Base):
    """Order the rows in a table."""

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.order_by.source)

    @property
    def columns(self) -> Sequence[str]:
        return self._proto.order_by.columns

    @property
    def desc(self) -> bool:
        return self._proto.order_by.desc

    def sources(self):
        return [self.source]


class FilterRows(_Base):
    """Filter rows by applying a predicate."""

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.filter_rows.source)

    @property
    def row_filter(self) -> RowFilter:
        return row_filters_from_proto(self._proto.filter_rows.row_filter)

    def sources(self):
        return [self.source]


class DistinctRows(_Base):
    """Remove duplicate rows from the table."""

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.distinct_rows.source)

    def sources(self):
        return [self.source]


class UpdateMetadata(_Base):
    """Update table-wide metadata, overwriting old values."""

    @functools.cached_property
    def metadata_updates(self) -> Mapping[str, Any]:
        return json_format.MessageToDict(self._proto.update_metadata.metadata_updates)

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.update_metadata.source)

    def sources(self):
        return [self.source]


class SetMetadata(_Base):
    """Update table-wide metadata, overwriting old values."""

    @functools.cached_property
    def new_metadata(self) -> Mapping[str, Any]:
        return json_format.MessageToDict(self._proto.set_metadata.new_metadata)

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.set_metadata.source)

    def sources(self):
        return [self.source]


class RemoveFromMetadata(_Base):
    """Update table-wide metadata, overwriting old values."""

    @property
    def keys_to_remove(self) -> Sequence[str]:
        return self._proto.remove_from_metadata.keys_to_remove

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.remove_from_metadata.source)

    def sources(self):
        return [self.source]


class RollupByAggregation(_Base):
    """Compute an aggregation rollup and add it as a new column."""

    @property
    def source(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.rollup_by_aggregation.source)

    @property
    def group_by_column_names(self) -> Sequence[str]:
        return self._proto.rollup_by_aggregation.group_by_column_names

    @property
    def target_column_name(self) -> str:
        return self._proto.rollup_by_aggregation.target_column_name

    @property
    def aggregation_type(self):
        return self._proto.rollup_by_aggregation.aggregation_type

    def sources(self):
        return [self.source]


class Empty(_Base):
    """An operation the produces an empty table."""

    def sources(self):
        return list[Op]()


@dataclasses.dataclass(frozen=True)
class EdgeListTable:
    """A table bundled with edge metadata."""

    table: Op
    start_column_name: str
    end_column_name: str
    start_entity_name: str
    end_entity_name: str

    @classmethod
    def from_proto(cls, proto: table_pb2.EdgeListTable):
        return cls(
            from_proto(proto.table),
            start_column_name=proto.start_column_name,
            end_column_name=proto.end_column_name,
            start_entity_name=proto.start_entity_name,
            end_entity_name=proto.end_entity_name,
        )

    def to_proto(self):
        return table_pb2.EdgeListTable(
            table=self.table.to_proto(),
            start_column_name=self.start_column_name,
            end_column_name=self.end_column_name,
            start_entity_name=self.start_entity_name,
            end_entity_name=self.end_entity_name,
        )


class EmbedNode2vecFromEdgeLists(_Base):
    """Consume several tables as edge lists, produce node2vec embedding."""

    @functools.cached_property
    def edge_list_tables(self):
        return [
            EdgeListTable.from_proto(edge_list)
            for edge_list in self._proto.embed_node2vec_from_edge_lists.edge_list_tables
        ]

    @property
    def ndim(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.ndim

    @property
    def walk_length(self):
        return (
            self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.walk_length
        )

    @property
    def window(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.window

    @property
    def p(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.p

    @property
    def q(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.q

    @property
    def alpha(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.alpha

    @property
    def min_alpha(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.min_alpha

    @property
    def negative(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.negative

    @property
    def epochs(self):
        return self._proto.embed_node2vec_from_edge_lists.node2vec_parameters.epochs

    def sources(self):
        return [edge_list.table for edge_list in self.edge_list_tables]


class EmbeddingMetrics(_Base):
    """Compute embedding metrics metadata."""

    @property
    def table(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.embedding_metrics.table)

    def sources(self):
        return [self.table]


class EmbeddingCoordinates(_Base):
    """Compute embedding coordinates."""

    @property
    def table(self) -> Op:
        if self._parents:
            return self._parents[0]
        return from_proto(self._proto.embedding_coordinates.table)

    @property
    def n_components(self) -> int:
        return self._proto.embedding_coordinates.n_components

    @property
    def metric(self) -> str:
        return self._proto.embedding_coordinates.metric

    def sources(self):
        return [self.table]


class ReadFromParquet(_Base):
    """Read table from parquet files."""

    @property
    def blob_names(self) -> Sequence[str]:
        return self._proto.read_from_parquet.blob_names

    @functools.cached_property
    def arrow_schema(self) -> pa.Schema:
        return pa.ipc.read_schema(
            pa.py_buffer(self._proto.read_from_parquet.arrow_schema)
        )

    @functools.cached_property
    def feature_types(self) -> Sequence[FeatureType]:
        return [
            ftype_from_proto(feature_type)
            for feature_type in self._proto.read_from_parquet.feature_types
        ]

    @property
    def expected_rows(self) -> int:
        return self._proto.read_from_parquet.expected_rows

    def sources(self):
        return list[Op]()


class SelectFromVectorStaging(_Base):
    """Read table from parquet files."""

    @property
    def input_vector(self) -> Sequence[float]:
        return self._proto.select_from_vector_staging.input_vector

    @property
    def blob_names(self) -> Sequence[str]:
        return self._proto.select_from_vector_staging.blob_names

    @property
    def similarity_metric(self) -> str:
        return self._proto.select_from_vector_staging.similarity_metric

    @property
    def vector_column_name(self) -> str:
        return self._proto.select_from_vector_staging.vector_column_name

    @property
    def num_results(self) -> int:
        return self._proto.select_from_vector_staging.num_results

    def sources(self):
        return list[Op]()

    @functools.cached_property
    def arrow_schema(self) -> pa.Schema:
        return pa.ipc.read_schema(
            pa.py_buffer(self._proto.select_from_vector_staging.arrow_schema)
        )

    @functools.cached_property
    def feature_types(self) -> Sequence[FeatureType]:
        return [
            ftype_from_proto(feature_type)
            for feature_type in self._proto.select_from_vector_staging.feature_types
        ]


class Concat(_Base):
    """Concatenate tables."""

    @functools.cached_property
    def tables(self) -> list[Op]:
        return [from_proto(table) for table in self._proto.concat.tables]

    def sources(self):
        return self.tables


class UnnestStruct(_Base):
    """Unnest a struct column."""

    @property
    def source(self) -> Op:
        return from_proto(self._proto.unnest_struct.source)

    @property
    def struct_column_name(self) -> str:
        return self._proto.unnest_struct.struct_column_name

    def sources(self):
        return [self.source]


class AddLiteralColumn(_Base):
    """Add a new column were all entries are a particular literal value."""

    @property
    def source(self) -> Op:
        return from_proto(self._proto.add_literal_column.source)

    @functools.cached_property
    def literal(self):
        return json_format.MessageToDict(self._proto.add_literal_column)["literal"]

    @functools.cached_property
    def column_arrow_schema(self) -> pa.Schema:
        return pa.ipc.read_schema(
            pa.py_buffer(self._proto.add_literal_column.column_arrow_schema)
        )

    @functools.cached_property
    def column_feature_type(self) -> FeatureType:
        return ftype_from_proto(self._proto.add_literal_column.column_feature_type)

    def sources(self):
        return [self.source]


Op = (
    SelectFromStaging
    | RenameColumns
    | Join
    | SelectColumns
    | LimitRows
    | OrderBy
    | FilterRows
    | DistinctRows
    | UpdateMetadata
    | SetMetadata
    | RemoveFromMetadata
    | UpdateFeatureTypes
    | RollupByAggregation
    | Empty
    | EmbedNode2vecFromEdgeLists
    | EmbeddingMetrics
    | EmbeddingCoordinates
    | ReadFromParquet
    | SelectFromVectorStaging
    | Concat
    | UnnestStruct
    | AddLiteralColumn
)

_COMPUTE_OP_FIELD_NAME_TO_OP: Final = {
    "select_from_staging": SelectFromStaging,
    "rename_columns": RenameColumns,
    "join": Join,
    "select_columns": SelectColumns,
    "limit_rows": LimitRows,
    "order_by": OrderBy,
    "filter_rows": FilterRows,
    "distinct_rows": DistinctRows,
    "update_metadata": UpdateMetadata,
    "set_metadata": SetMetadata,
    "remove_from_metadata": RemoveFromMetadata,
    "update_feature_types": UpdateFeatureTypes,
    "rollup_by_aggregation": RollupByAggregation,
    "empty": Empty,
    "embed_node2vec_from_edge_lists": EmbedNode2vecFromEdgeLists,
    "embedding_metrics": EmbeddingMetrics,
    "embedding_coordinates": EmbeddingCoordinates,
    "read_from_parquet": ReadFromParquet,
    "select_from_vector_staging": SelectFromVectorStaging,
    "concat": Concat,
    "unnest_struct": UnnestStruct,
    "add_literal_column": AddLiteralColumn,
}

_OP_TO_COMPUTE_OP_FIELD_NAME: Final[dict[type[Any], str]] = {
    op: name for name, op in _COMPUTE_OP_FIELD_NAME_TO_OP.items()
}


def _make_schema_from_node2vec_params(n2v_op: EmbedNode2vecFromEdgeLists):
    if not n2v_op.edge_list_tables:
        raise BadArgumentError("unable to infer schema: empty edge table list")

    dtypes: set[pa.DataType] = set()
    for edge_list in n2v_op.edge_list_tables:
        schema = edge_list.table.schema.to_arrow()
        dtypes.add(schema.field(edge_list.start_column_name).type)
        dtypes.add(schema.field(edge_list.end_column_name).type)

    fields = [pa.field(f"column_{i}", dtype) for i, dtype in enumerate(dtypes)]
    # An extra field is added to id fields for the source name
    fields.append(pa.field(f"column_{len(dtypes)}", pa.large_string()))

    return Schema(
        [
            Field(
                "id",
                pa.struct(fields),
                feature_type.identifier(),
            ),
            Field(
                "embedding",
                pa.list_(value_type=pa.float32(), list_size=n2v_op.ndim),
                feature_type.embedding(),
            ),
        ]
    )


def _make_schema_for_embedding_coordinates(op: EmbeddingCoordinates):
    schema = op.table.schema

    if "id" not in schema or "embedding" not in schema:
        raise BadArgumentError(
            "EmbeddingMetrics op needs to be computed on Embedding table"
        )

    return Schema(
        [
            schema["id"],
            Field(
                "embedding",
                pa.list_(value_type=pa.float32(), list_size=3),
                feature_type.embedding(),
            ),
        ]
    )


def _make_schema_for_unnest_struct(op: UnnestStruct):
    schema = op.source.schema

    def gen_fields() -> Iterable[Field]:
        for field in schema:
            if field.name == op.struct_column_name:
                if not isinstance(field.dtype, pa.StructType):
                    raise BadArgumentError(
                        "unnest cannot be done on a non-struct column"
                    )

                yield from (
                    Field.from_arrow(field.dtype.field(i))
                    for i in range(field.dtype.num_fields)
                )
            else:
                yield field

    return Schema(list(gen_fields()))


def _make_schema_for_add_literal_column(op: AddLiteralColumn):
    return Schema(
        [
            *op.source.schema,
            Field.from_arrow(op.column_arrow_schema[0], op.column_feature_type),
        ]
    )


class Schema(Sequence[Field]):
    """List of fields describing data types and feature types of a table."""

    _fields: list[Field]

    def __init__(self, fields: list[Field]) -> None:
        self._fields = fields

    def __eq__(self, other: object) -> bool:
        """Two schemas are equal if all of their fields match."""
        if isinstance(other, Schema):
            return self._fields == other._fields
        return False

    @overload
    def __getitem__(self, selection: str) -> Field: ...

    @overload
    def __getitem__(self, selection: int) -> Field: ...

    @overload
    def __getitem__(self, selection: slice) -> Sequence[Field]: ...

    def __getitem__(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, selection: int | str | slice
    ) -> Field | Sequence[Field]:
        """This operation is akin to pyarrow.Schema.field.

        The result is either the array addressed Field(s) or the first field with a
        matching name depending on the type of argument passed.
        """
        if isinstance(selection, str):
            for field in self._fields:
                if field.name == selection:
                    return field
            raise KeyError("no field with that name")
        return self._fields[selection]

    def __len__(self):
        """The number of fields in this schema."""
        return len(self._fields)

    def __str__(self) -> str:
        """Legible string representation of this schema."""
        return "\n".join(str(field) for field in self)

    @overload
    def get(self, column_name: str, default: Field) -> Field: ...

    @overload
    def get(self, column_name: str, default: None = ...) -> Field | None: ...

    def get(self, column_name: str, default: Field | None = None) -> Field | None:
        return next((f for f in self if f.name == column_name), default)

    def has_column(self, column_name: str) -> bool:
        return self.get(column_name) is not None

    @classmethod
    def from_arrow(
        cls,
        arrow_schema: pa.Schema,
        feature_types: Sequence[FeatureType | None] | None = None,
    ) -> Schema:
        if feature_types:
            if len(feature_types) != len(arrow_schema):
                raise BadArgumentError("length of feature_types must match schema")
        else:
            feature_types = [None] * len(arrow_schema)
        return cls(
            fields=[
                Field.from_arrow(field, ftype)
                for field, ftype in zip(arrow_schema, feature_types, strict=True)
            ]
        )

    def to_arrow(self) -> pa.Schema:
        return pa.schema(field.to_arrow() for field in self)

    def to_polars(self) -> OrderedDict[str, pl.DataType]:
        table = pl.from_arrow(
            pa.schema(field.to_arrow() for field in self).empty_table()
        )
        if isinstance(table, pl.Series):
            table = table.to_frame()

        return table.schema

    def get_primary_key(self) -> Field | None:
        for field in self:
            match field.ftype:
                case feature_type.PrimaryKey():
                    return field
                case _:
                    pass
        return None

    def get_foreign_keys(self, source_id: orm.SourceID) -> list[Field]:
        def generate_matching_fields():
            for field in self:
                match field.ftype:
                    case feature_type.ForeignKey(ref_id) if ref_id == source_id:
                        yield field
                    case _:
                        pass

        return list(generate_matching_fields())

    @classmethod
    def from_ops(cls, ops: Op) -> Schema:  # noqa: PLR0911, PLR0912, C901
        match ops:
            case SelectFromStaging() | ReadFromParquet() | SelectFromVectorStaging():
                return Schema(
                    [
                        Field.from_arrow(afield, ftype)
                        for afield, ftype in zip(
                            ops.arrow_schema, ops.feature_types, strict=True
                        )
                    ]
                )
            case SelectColumns():
                return Schema(
                    [field for field in ops.source.schema if field.name in ops.columns]
                )
            case RenameColumns():

                def rename_column(field: Field) -> Field:
                    if field.name in ops.old_name_to_new:
                        return field.rename(ops.old_name_to_new[field.name])
                    return field

                return Schema(list(map(rename_column, ops.source.schema)))

            case UpdateFeatureTypes():

                def update_feature_type(field: Field) -> Field:
                    if field.name in ops.new_feature_types:
                        return Field(
                            field.name, field.dtype, ops.new_feature_types[field.name]
                        )
                    return field

                return Schema(list(map(update_feature_type, ops.source.schema)))

            case Join():
                left_schema = ops.left_source.schema
                right_schema = ops.right_source.schema
                left_names = {field.name for field in left_schema}
                return Schema(
                    list(
                        flatten(
                            (
                                (field for field in left_schema),
                                (
                                    field
                                    for field in right_schema
                                    if field.name not in left_names
                                    and field.name not in ops.right_join_columns
                                ),
                            )
                        )
                    )
                )

            case (
                LimitRows()
                | OrderBy()
                | FilterRows()
                | DistinctRows()
                | UpdateMetadata()
                | SetMetadata()
                | RemoveFromMetadata()
            ):
                return ops.source.schema

            case EmbeddingMetrics():
                return ops.table.schema

            case RollupByAggregation():
                schema = ops.source.schema
                new_fields = _generate_schema_for_rollup(
                    schema,
                    ops.aggregation_type,
                    ops.group_by_column_names,
                    ops.target_column_name,
                )
                return Schema(list(new_fields.values()))

            case Empty():
                return Schema([])

            case EmbedNode2vecFromEdgeLists():
                return _make_schema_from_node2vec_params(ops)

            case EmbeddingCoordinates():
                return _make_schema_for_embedding_coordinates(ops)

            case Concat():
                return ops.tables[0].schema

            case UnnestStruct():
                return _make_schema_for_unnest_struct(ops)

            case AddLiteralColumn():
                return _make_schema_for_add_literal_column(ops)


agg_mapping = {
    table_pb2.AGGREGATION_TYPE_COUNT: "count",
    table_pb2.AGGREGATION_TYPE_AVG: "avg",
    table_pb2.AGGREGATION_TYPE_MODE: "mode",
    table_pb2.AGGREGATION_TYPE_MIN: "min",
    table_pb2.AGGREGATION_TYPE_MAX: "max",
    table_pb2.AGGREGATION_TYPE_SUM: "sum",
}


def _generate_schema_for_rollup(
    schema: Schema,
    agg: table_pb2.AggregationType,
    group_by_column_names: Sequence[str],
    target_column_name: str,
) -> dict[str, Field]:
    new_fields: dict[str, Field] = {}
    group_by_str = "_".join(group_by_column_names)
    for field in schema:
        new_fields.update(
            {key: field for key in group_by_column_names if field.name == key}
        )
        if field.name == target_column_name:
            new_fields.update(
                {
                    f"{agg_mapping[agg]}_{target_column_name}_{group_by_str}": Field(
                        f"{agg_mapping[agg]}_{target_column_name}_{group_by_str}",
                        (
                            pa.uint32()
                            if agg_mapping[agg] == "count"
                            else (
                                pa.float32()
                                if agg_mapping[agg] == "avg"
                                else field.dtype
                            )
                        ),
                        (
                            feature_type.categorical()
                            if agg_mapping[agg] == "mode"
                            else feature_type.numerical()
                        ),
                    )
                }
            )
    return new_fields
