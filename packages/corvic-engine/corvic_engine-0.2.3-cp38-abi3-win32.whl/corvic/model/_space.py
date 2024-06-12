"""Spaces."""

from collections.abc import Iterable, Iterator
from typing import TypeAlias

import polars as pl

from corvic import embed, orm
from corvic.model._feature_view import FeatureView, FeatureViewEdgeTableMetadata
from corvic.model._wrapped_orm import WrappedOrmObject
from corvic.result import BadArgumentError

SpaceID: TypeAlias = orm.SpaceID


class Space(WrappedOrmObject[SpaceID, orm.Space]):
    """Spaces apply embedding methods to FeatureViews.

    Example:
    >>> space = Space.node2vec(feature_view, dim=10, walk_length=10, window=10)
    """

    def _sub_orm_objects(self, orm_object: orm.Space) -> Iterable[orm.Base]:
        return []

    @classmethod
    def node2vec(  # noqa: PLR0913
        cls,
        feature_view: FeatureView,
        *,
        dim: int,
        walk_length: int,
        window: int,
        p: float = 1.0,
        q: float = 1.0,
        batch_words: int | None = None,
        alpha: float = 0.025,
        seed: int | None = None,
        workers: int | None = None,
        min_alpha: float = 0.0001,
        negative: int = 5,
    ) -> embed.Node2Vec:
        """Run Node2Vec on the graph described by the feature view.

        Args:
            feature_view: The feature view to run Node2Vec on
            dim: The dimensionality of the embedding
            walk_length: Length of the random walk to be computed
            window: Size of the window. This is half of the context,
                as the context is all nodes before `window` and
                after `window`.
            p: The higher the value, the lower the probability to return to
                the previous node during a walk.
            q: The higher the value, the lower the probability to return to
                a node connected to a previous node during a walk.
            alpha: Initial learning rate
            min_alpha: Final learning rate
            negative: Number of negative samples
            seed: Random seed
            batch_words: Target size (in nodes) for batches of examples passed
                to worker threads
            workers: Number of threads to use. Default is to select number of threads
                as needed. Setting this to a non-default value incurs additional
                thread pool creation overhead.

        Returns:
            A Space
        """
        if not feature_view.relationships:
            raise BadArgumentError("Node2Vec requires some relationships")

        edge_tables = feature_view.output_edge_tables()
        if not edge_tables:
            raise BadArgumentError(
                "Node2Vec requires some with_sources to be output=True"
            )

        def edge_generator():
            for table in feature_view.output_edge_tables():
                edge_table_info = table.get_typed_metadata(FeatureViewEdgeTableMetadata)
                for batch in table.to_polars().unwrap_or_raise():
                    yield batch.with_columns(
                        pl.col(edge_table_info.start_source_column_name).alias(
                            "start_id"
                        ),
                        pl.lit(edge_table_info.start_source_name).alias("start_source"),
                        pl.col(edge_table_info.end_source_column_name).alias("end_id"),
                        pl.lit(edge_table_info.end_source_name).alias("end_source"),
                    ).select("start_id", "start_source", "end_id", "end_source")

        n2v_space = embed.Space(
            pl.concat((edge_list for edge_list in edge_generator()), rechunk=False),
            start_id_column_names=("start_id", "start_source"),
            end_id_column_names=("end_id", "end_source"),
            directed=True,
        )
        return embed.Node2Vec(
            space=n2v_space,
            dim=dim,
            walk_length=walk_length,
            window=window,
            p=p,
            q=q,
            alpha=alpha,
            min_alpha=min_alpha,
            negative=negative,
            seed=seed,
            batch_words=batch_words,
            workers=workers,
        )

    def to_polars(self) -> Iterator[pl.DataFrame]:
        raise NotImplementedError()
